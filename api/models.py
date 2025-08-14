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
    story: Optional[Union[str, List[str]]] = None
    character: Optional[Union[str, List[str]]] = None
    world: Optional[Union[str, List[str]]] = None


class EventProperties(BaseModel):
    """事件内部属性基类"""
    title: str  # 事件名
    type: str  # story, setting/world, setting/character
    author: AuthorGroup
    date: str  # 创建时间
    last_date: str  # 最后修改时间
    state: str  # original, release, pre
    related: EventRelated


class ExternalProperty(BaseModel):
    """事件外部属性基类"""
    name: str  # 属性名
    value: str  # 属性值
    last_author: Author  # 最后编辑者
    create_author: Author  # 创建者
    last_modified: str  # 最后修改时间


class EventBase(BaseModel):
    """事件基类
    id: 事件文件的相对路径，唯一标识"""
    id: str
    properties: EventProperties


class StoryTime(BaseModel):
    """故事时间基类"""
    start: str  # 世界观纪元时间
    end: str


class StoryData(BaseModel):
    """故事内部属性基类"""
    upstream: Optional[str] = None
    time: StoryTime


class StoryEvent(EventBase):
    """故事事件基类"""
    story: StoryData
    content: str
    type: str = "story"


class SettingEvent(EventBase):
    """设定事件基类"""
    content: List[ExternalProperty]
    type: str = "setting"


class CharacterSettingEvent(SettingEvent):
    """角色设定事件基类"""
    type: str = "setting/character"


class WorldSettingEvent(SettingEvent):
    """世界设定事件基类"""
    type: str = "setting/world"
