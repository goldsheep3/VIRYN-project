from typing import List, Optional

from api.models import (
    EventBase, StoryEvent, SettingEvent, CharacterSettingEvent, WorldSettingEvent, Attribute, Author, StoryData,
    ImageEvent, ALL_EVENT
)
from api import manager
from api.log import ApiLogger

logger = ApiLogger()


# 1. 获取事件列表
def get_events(_operator_qq: Optional[str] = None) -> List[ALL_EVENT]:
    """获取所有事件列表"""
    logger.debug(f"get_events called, operator_qq={_operator_qq}")
    events = manager.get_events('all', 'all')
    logger.debug(f"get_events 返回 {len(events)} 个事件")
    return events


# 2. 获取setting事件列表
def get_setting_events(operator_qq: Optional[str] = None) -> List[SettingEvent]:
    """获取所有setting事件列表。"""
    # 1. 遍历`/event`目录，获取所有的事件文件
    # 2. 解析每个事件文件，生成对应的EventBase对象
    # 3. 过滤出type为`setting/world`或`setting/character`的事件
    # 4. 返回所有事件对象的列表
    ...


# 3. 获取setting/character事件列表
def get_character_setting_events(operator_qq: Optional[str] = None) -> List[CharacterSettingEvent]:
    """获取所有setting/character事件列表。"""
    ...


# 4. 获取setting/world事件列表
def get_world_setting_events(operator_qq: Optional[str] = None) -> List[WorldSettingEvent]:
    """获取所有setting/world事件列表。"""
    ...


# 5. 获取story事件列表
def get_story_events(operator_qq: Optional[str] = None) -> List[StoryEvent]:
    """获取所有story事件列表。"""
    ...


# 6. 获取image事件列表
def get_image_events(operator_qq: Optional[str] = None) -> List[ImageEvent]:
    """获取所有image事件列表。"""
    ...


# 7. 获取事件详情
def get_event_detail(event_id: str, operator_qq: Optional[str] = None) -> EventBase:
    """获取指定事件详情。"""
    ...


# 8. 获取设定事件外部属性
def get_event_property(event_id: str, property_name: str, operator_qq: Optional[str] = None) -> Attribute:
    """获取指定事件的外部属性。"""
    ...


# 9. 获取创作者列表
def get_authors(operator_qq: Optional[str] = None) -> List[Author]:
    """获取创作者列表。"""
    ...


# 10. 新建story事件
def create_story_event(event: StoryEvent, operator_qq: Optional[str] = None) -> dict:
    """新建story事件。"""
    ...


# 11. 新建setting/character事件
def create_character_setting_event(event: CharacterSettingEvent, operator_qq: Optional[str] = None) -> dict:
    """新建setting/character事件。"""
    ...


# 12. 新建setting/world事件
def create_world_setting_event(event: WorldSettingEvent, operator_qq: Optional[str] = None) -> dict:
    """新建setting/world事件。"""
    ...


# 13. 新建image事件
def create_image_event(event: EventBase, operator_qq: Optional[str] = None) -> dict:
    """新建image事件。"""
    ...


# 14. 新建设定事件外部属性
def create_event_property(event_id: str, external_property: Attribute, operator_qq: Optional[str] = None) -> dict:
    """新建设定事件外部属性。"""
    ...


# 15. 修改story事件特有内部属性
def update_story_event_internal(event_id: str, story_data: StoryData, operator_qq: Optional[str] = None) -> dict:
    """修改story事件特有内部属性。"""
    ...


# 16. 修改story事件content内容
def update_story_event_content(event_id: str, content: str, operator_qq: Optional[str] = None) -> dict:
    """修改story事件content内容。"""
    ...


# 17. 修改setting事件外部属性
def update_event_property(event_id: str, property_name: str, external_property: Attribute,
                          operator_qq: Optional[str] = None) -> dict:
    """修改setting事件外部属性。"""
    ...


# 18. 删除setting事件外部属性
def delete_event_property(event_id: str, property_name: str, operator_qq: Optional[str] = None) -> dict:
    """删除setting事件外部属性。"""
    ...


# 19. 删除story事件
def delete_story_event(event_id: str, operator_qq: Optional[str] = None) -> dict:
    """删除story事件。"""
    ...


# 20. 获取存在pre的事件列表
def get_pre_events(operator_qq: Optional[str] = None) -> List[EventBase]:
    """获取存在pre的事件列表。"""
    ...


# 21. 获取存在pre的story事件列表
def get_pre_story_events(operator_qq: Optional[str] = None) -> List[StoryEvent]:
    """获取存在pre的story事件列表。"""
    ...


# 22. 获取存在pre的setting事件列表
def get_pre_setting_events(operator_qq: Optional[str] = None) -> List[SettingEvent]:
    """获取存在pre的setting事件列表。"""
    ...


# 23. 获取存在pre且状态为新建的事件列表
def get_pre_new_events(operator_qq: Optional[str] = None) -> List[EventBase]:
    """获取存在pre且状态为新建的事件列表。"""
    ...


# 24. 获取setting事件中存在pre的属性列表
def get_pre_setting_properties(operator_qq: Optional[str] = None) -> List[Attribute]:
    """获取setting事件中存在pre的属性列表。"""
    ...


# 25. 批准通过pre的story新增/修改事件
def approve_pre_story_event(event_id: str, operator_qq: str) -> dict:
    """批准通过pre的story新增/修改事件。"""
    ...


# 26. 批准通过pre的setting新增事件
def approve_pre_setting_event(event_id: str, operator_qq: str) -> dict:
    """批准通过pre的setting新增事件。"""
    ...


# 27. 批准通过pre的setting外部属性新增/修改事件
def approve_pre_setting_property(event_id: str, property_name: str, operator_qq: str) -> dict:
    """批准通过pre的setting外部属性新增/修改事件。"""
    ...


# 28. 批准通过pre的story删除事件
def approve_pre_story_delete(event_id: str, operator_qq: str) -> dict:
    """批准通过pre的story删除事件。"""
    ...


# 29. 批准通过pre的setting外部属性删除事件
def approve_pre_setting_property_delete(event_id: str, property_name: str, operator_qq: str) -> dict:
    """批准通过pre的setting外部属性删除事件。"""
    ...


# 30. 批准通过pre的setting删除事件
def approve_pre_setting_delete(event_id: str, operator_qq: str) -> dict:
    """批准通过pre的setting删除事件。"""
    ...


# 31. 批准驳回pre的story新增/修改事件
def reject_pre_story_event(event_id: str, operator_qq: str) -> dict:
    """批准驳回pre的story新增/修改事件。"""
    ...


# 32. 批准驳回pre的setting新增事件
def reject_pre_setting_event(event_id: str, operator_qq: str) -> dict:
    """批准驳回pre的setting新增事件。"""
    ...


# 33. 批准驳回pre的setting外部属性新增/修改事件
def reject_pre_setting_property(event_id: str, property_name: str, operator_qq: str) -> dict:
    """批准驳回pre的setting外部属性新增/修改事件。"""
    ...


# 34. 批准驳回pre的story删除事件
def reject_pre_story_delete(event_id: str, operator_qq: str) -> dict:
    """批准驳回pre的story删除事件。"""
    ...


# 35. 批准驳回pre的setting外部属性删除事件
def reject_pre_setting_property_delete(event_id: str, property_name: str, operator_qq: str) -> dict:
    """批准驳回pre的setting外部属性删除事件。"""
    ...


# 36. 批准驳回pre的setting删除事件
def reject_pre_setting_delete(event_id: str, operator_qq: str) -> dict:
    """批准驳回pre的setting删除事件。"""
    ...
