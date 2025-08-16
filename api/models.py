from typing import List, Optional, Union
from pydantic import BaseModel


class Author(BaseModel):
    """创作者信息基类"""
    qq: str
    name: str
    email: Optional[str] = None


class AuthorGroup(BaseModel):
    """创作者信息基类"""
    create: Author
    last: Author
    contributors: List[Author]


class EventRelated(BaseModel):
    """事件相关基类"""
    story: Optional[List[str]] = None
    character: Optional[List[str]] = None
    world: Optional[List[str]] = None


class Properties(BaseModel):
    """事件内部属性基类"""
    title: str  # 事件名
    type: str  # story, setting/world, setting/character
    author: AuthorGroup
    create_datetime: str  # 创建时间
    last_datetime: str  # 最后修改时间
    state: str  # original, release, pre
    related: EventRelated


class AttributePre(BaseModel):
    """事件外部属性PRE状态"""
    key: str
    value: str
    last: Author
    last_datetime: str
    delete: bool = False


class Attribute(BaseModel):
    """事件外部属性基类"""
    key: List[str]  # 属性名
    value: str  # 属性值
    create: Author
    last: Author
    create_datetime: str
    last_datetime: str
    pre: Optional[AttributePre] = None  # PRE状态属性


class EventBase(BaseModel):
    """事件基类
    id: 事件文件的相对路径，唯一标识"""
    id: str
    properties: Properties


class ImageEvent(EventBase):
    """图片事件基类"""
    type: str = "image"


class MDEventBase(EventBase):
    """Markdown 事件基类"""


class StoryTime(BaseModel):
    """故事时间基类"""
    # todo: 之后修改为纪元时间类进行验证
    start: str  # 世界观纪元时间
    end: str


class StoryData(BaseModel):
    """故事内部属性基类"""
    upstream: Optional[str] = None
    time: StoryTime


class StoryEvent(MDEventBase):
    """故事事件基类"""
    story: StoryData
    content: str
    type: str = "story"


class SettingEvent(MDEventBase):
    """设定事件基类"""
    attributes: List[Attribute]
    type: str = "setting"


class CharacterSettingEvent(SettingEvent):
    """角色设定事件基类"""
    type: str = "setting/character"


class WorldSettingEvent(SettingEvent):
    """世界设定事件基类"""
    type: str = "setting/world"


# 定义特殊事件类型标记
ALL_EVENT = Union[StoryEvent, CharacterSettingEvent, WorldSettingEvent, ImageEvent]
