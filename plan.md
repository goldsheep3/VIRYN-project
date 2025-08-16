项目的主要组成包括一个存储目录及API、一个Nonebot2机器人、一个内容网站、一个管理网站。

Nonebot2机器人负责通讯群聊和API，从API获取数据返回，从群聊获取数据提交到API；
内容网站负责获取存储目录的数据根据一定规则反映到网页上，而管理网站可以通过API修改数据。

存储目录中以`事件`作为单位，每个事件通常都是一个`markdown(.md)`文件（或图像资产事件`jpg``png``gif``mp4`等文件）。
事件共有两种`story`和`setting`，其中`setting`又分为`setting/character`和`setting/world`。
每个事件都具有各自的若干内部属性和外部属性。
内部属性存储在yaml的front-matter中，内部属性则是markdown的文件内容，通过特定格式获取。
此外，图像资产也可以是事件，其存储在`/image`目录，同时存在`data/image_author.yaml`文件存储对应的author QQ号和pre状态。
事件都有着固定id，即根目录相对路径（如`/setting/world/country/gjq.md`）。
事件不能主动命名为`xxx_pre.md`，因为若存在该名字的故事事件则证明该事件整体为PRE状态。

对于任何事件，其内部属性一定包括：
```yaml
title: f95c0d  # 此处为事件名，默认为文件名
type: story  # 此处为事件类型(story, setting/world, setting/character)
author:
  create: 2940119626  # 事件创建者，qq号
  last: 2940119626  # 事件最后编辑者，qq号
  contributors: 2940119626  # 事件全部贡献者，qq号（可为数组）
date: 2025.08.13 22:57:10  # 事件创建时间，UTC+8
last_date: 2025.08.13 22:27:11  # 事件最后修改时间，UTF+8
state: original  # 事件状态（原生`original`/正常`release`/文件中包含PRE状态外部属性，或该文件本身处在PRE状态`pre`）
related:
  story: null  # 相关故事事件（可为数组）
  character: null  # 相关角色设定事件（可为数组）
  world: null  # 相关世界设定事件（可为数组）
```
内部属性中的qq号可以通过存储目录的`data/authors.yaml`文件获取。
对于故事事件，其特有内部属性为：
```yaml
story:  # 故事事件特有数据
  upstream: null  # 上游故事事件
  time:
    start: Nsj.17.01.01:14  # 事件开始时间，采用世界观特有纪元计算方法，精确到小时
    end: Nsj.17.01.01:17  # 事件结束时间，采用世界观特有纪元计算方法，精确到小时
```
对于`time`中的时间计法`{era_id}.{year}.{month}.{day}:{hour}`，与`data/calendar.yaml`有关。
故事事件没有特殊的外部属性。
对于设定事件，其没有更多内部属性，但外部属性有着特殊规则：
```markdown
### 外貌

他没有形体，是一团黑色的气团。![f085a1](/image/f085a1.png)[#粒子](/setting/world/px.md)

`last:2940119626;create:2940119626;date:2025.08.13 22:57:10;`

> *PRE*
> 
> 他没有形体，是一团黑色的气团。![f085a1](/image/f085a1.png)<br/>[#粒子](/setting/world/px.md)
> 
> `author:111;date:2025.08.13 22:57:14;delete:false;`
```
每一个非一级标题都进行检查。
如上示例的属性名为`外貌`，
内容为`他没有形体，是一团黑色的气团。![f085a1](/image/f085a1.png)[#粒子](/setting/world/px.md)`，
最后更新作者和属性创建者都是`2940119626`，最后修改日期是`2025.08.13 22:57:10`。
可能存在`>`的引用部分，若存在则匹配该属性存在PRE版本，作者为`111`，PRE提交时间为`2025.08.13 22:57:14`，
`他没有形体，是一团黑色的气团。![f085a1](/image/f085a1.png)<br/>[#粒子](/setting/world/px.md)`为PRE版本属性内容。
若整个属性均为新增，那可能没有内容和元数据，只有PRE引用部分。
若属性将要删除，则pre元数据的`delete`为`true`，此时忽略可能存在的pre内容行。

API处理数据时，对所有群聊提交的数据都处理为PRE，
但是`data/ops.yaml`中读取出数组的QQ号（字符串）作为作者时，直接替换/新增/删除而不处理为PRE状态，
同时调用PRE通过/驳回时也仅有这些QQ号的请求才能通过，否则返回错误提示且不更改。

API也可通过复制`template/setting/world/xxx.md`等文件的方式通过模板创建。
API每次的操作都会留下日志记录（无论是否成功）。这些日志存储在`log/2025-08-13.log`。