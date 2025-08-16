from fastapi import FastAPI, Query
from typing import List, Optional, Union

from api.models import (
    EventBase, StoryEvent, SettingEvent, CharacterSettingEvent, WorldSettingEvent, ExternalProperty, Author, StoryData,
    ImageEvent, ALL_EVENT
)
from api import utils
from api.log import ApiLogger

logger = ApiLogger()
app = FastAPI()


# 1. 获取事件列表
@app.get('/events')
def get_events(
        operator_qq: Optional[str] = Query(None)
) -> List[ALL_EVENT]:
    """获取所有事件列表，返回完整字段（支持多态）"""
    logger.debug(f"收到 /events 请求，operator_qq={operator_qq}")
    logger.debug("调用 utils.get_events")
    events = utils.get_events(operator_qq)
    logger.debug(f"utils.get_events 返回 {len(events)} 个事件")
    return events


# 2. 获取setting事件列表
@app.get('/events/setting')
def get_setting_events(operator_qq: Optional[str] = Query(None)) -> List[SettingEvent]:
    """获取所有setting事件列表。"""
    return utils.get_setting_events(operator_qq)


# 3. 获取setting/character事件列表
@app.get('/events/setting/character')
def get_character_setting_events(operator_qq: Optional[str] = Query(None)) -> List[CharacterSettingEvent]:
    """获取所有setting/character事件列表。"""
    return utils.get_character_setting_events(operator_qq)


# 4. 获取setting/world事件列表
@app.get('/events/setting/world')
def get_world_setting_events(operator_qq: Optional[str] = Query(None)) -> List[WorldSettingEvent]:
    """获取所有setting/world事件列表。"""
    return utils.get_world_setting_events(operator_qq)


# 5. 获取story事件列表
@app.get('/events/story')
def get_story_events(operator_qq: Optional[str] = Query(None)) -> List[StoryEvent]:
    """获取所有story事件列表。"""
    return utils.get_story_events(operator_qq)


# 6. 获取image事件列表
@app.get('/events/image')
def get_image_events(operator_qq: Optional[str] = Query(None)) -> List[ImageEvent]:
    """获取所有image事件列表。"""
    return utils.get_image_events(operator_qq)


# 7. 获取事件详情
@app.get('/event/{event_id}')
def get_event_detail(event_id: str, operator_qq: Optional[str] = Query(None)) -> EventBase:
    """获取指定事件详情。"""
    return utils.get_event_detail(event_id, operator_qq)


# 8. 获取设定事件外部属性（根据事件id+属性名）
@app.get('/event/{event_id}/property/{property_name}')
def get_event_property(event_id: str, property_name: str, operator_qq: Optional[str] = Query(None)) -> ExternalProperty:
    """获取指定事件的外部属性。"""
    return utils.get_event_property(event_id, property_name, operator_qq)


# 9. 获取创作者列表
@app.get('/authors')
def get_authors(operator_qq: Optional[str] = Query(None)) -> List[Author]:
    """获取创作者列表。"""
    return utils.get_authors(operator_qq)


# 10. 新建story事件
@app.post('/event/story')
def create_story_event(event: StoryEvent, operator_qq: Optional[str] = Query(None)) -> dict:
    """新建story事件。"""
    return utils.create_story_event(event, operator_qq)


# 11. 新建setting/character事件
@app.post('/event/setting/character')
def create_character_setting_event(event: CharacterSettingEvent, operator_qq: Optional[str] = Query(None)) -> dict:
    """新建setting/character事件。"""
    return utils.create_character_setting_event(event, operator_qq)


# 12. 新建setting/world事件
@app.post('/event/setting/world')
def create_world_setting_event(event: WorldSettingEvent, operator_qq: Optional[str] = Query(None)) -> dict:
    """新建setting/world事件。"""
    return utils.create_world_setting_event(event, operator_qq)


# 13. 新建image事件
@app.post('/event/image')
def create_image_event(event: EventBase, operator_qq: Optional[str] = Query(None)) -> dict:
    """新建image事件。"""
    return utils.create_image_event(event, operator_qq)


# 14. 新建设定事件外部属性
@app.post('/event/{event_id}/property')
def create_event_property(
        event_id: str, external_property: ExternalProperty, operator_qq: Optional[str] = Query(None)) -> dict:
    """新建设定事件外部属性。"""
    return utils.create_event_property(event_id, external_property, operator_qq)


# 15. 修改story事件特有内部属性
@app.put('/event/story/{event_id}/internal')
def update_story_event_internal(event_id: str, story_data: StoryData, operator_qq: Optional[str] = Query(None)) -> dict:
    """修改story事件特有内部属性。"""
    return utils.update_story_event_internal(event_id, story_data, operator_qq)


# 16. 修改story事件content内容
@app.put('/event/story/{event_id}/content')
def update_story_event_content(event_id: str, content: str, operator_qq: Optional[str] = Query(None)) -> dict:
    """修改story事件content内容。"""
    return utils.update_story_event_content(event_id, content, operator_qq)


# 17. 修改setting事件外部属性
@app.put('/event/{event_id}/property/{property_name}')
def update_event_property(event_id: str, property_name: str, external_property: ExternalProperty,
                          operator_qq: Optional[str] = Query(None)) -> dict:
    """修改setting事件外部属性。"""
    return utils.update_event_property(event_id, property_name, external_property, operator_qq)


# 18. 删除setting事件外部属性
@app.delete('/event/{event_id}/property/{property_name}')
def delete_event_property(event_id: str, property_name: str, operator_qq: Optional[str] = Query(None)) -> dict:
    """删除setting事件外部属性。"""
    return utils.delete_event_property(event_id, property_name, operator_qq)


# 19. 删除story事件
@app.delete('/event/story/{event_id}')
def delete_story_event(event_id: str, operator_qq: Optional[str] = Query(None)) -> dict:
    """删除story事件。"""
    return utils.delete_story_event(event_id, operator_qq)


# 20. 获取存在pre的事件列表
@app.get('/events/pre')
def get_pre_events(operator_qq: Optional[str] = Query(None)) -> List[EventBase]:
    """获取存在pre的事件列表。"""
    return utils.get_pre_events(operator_qq)


# 21. 获取存在pre的story事件列表
@app.get('/events/story/pre')
def get_pre_story_events(operator_qq: Optional[str] = Query(None)) -> List[StoryEvent]:
    """获取存在pre的story事件列表。"""
    return utils.get_pre_story_events(operator_qq)


# 22. 获取存在pre的setting事件列表
@app.get('/events/setting/pre')
def get_pre_setting_events(operator_qq: Optional[str] = Query(None)) -> List[SettingEvent]:
    """获取存在pre的setting事件列表。"""
    return utils.get_pre_setting_events(operator_qq)


# 23. 获取存在pre且状态为新建的事件列表
@app.get('/events/pre/new')
def get_pre_new_events(operator_qq: Optional[str] = Query(None)) -> List[EventBase]:
    """获取存在pre且状态为新建的事件列表。"""
    return utils.get_pre_new_events(operator_qq)


# 24. 获取setting事件中存在pre的属性列表
@app.get('/events/setting/property/pre')
def get_pre_setting_properties(operator_qq: Optional[str] = Query(None)) -> List[ExternalProperty]:
    """获取setting事件中存在pre的属性列表。"""
    return utils.get_pre_setting_properties(operator_qq)


# 25. 批准通过pre的story新增/修改事件
@app.post('/event/story/{event_id}/approve')
def approve_pre_story_event(event_id: str, operator_qq: str = Query(...)) -> dict:
    """批准通过pre的story新增/修改事件。"""
    return utils.approve_pre_story_event(event_id, operator_qq)


# 26. 批准通过pre的setting新增事件
@app.post('/event/setting/{event_id}/approve')
def approve_pre_setting_event(event_id: str, operator_qq: str = Query(...)) -> dict:
    """批准通过pre的setting新增事件。"""
    return utils.approve_pre_setting_event(event_id, operator_qq)


# 27. 批准通过pre的setting外部属性新增/修改事件
@app.post('/event/setting/{event_id}/property/{property_name}/approve')
def approve_pre_setting_property(event_id: str, property_name: str, operator_qq: str = Query(...)) -> dict:
    """批准通过pre的setting外部属性新增/修改事件。"""
    return utils.approve_pre_setting_property(event_id, property_name, operator_qq)


# 28. 批准通过pre的story删除事件
@app.post('/event/story/{event_id}/approve_delete')
def approve_pre_story_delete(event_id: str, operator_qq: str = Query(...)) -> dict:
    """批准通过pre的story删除事件。"""
    return utils.approve_pre_story_delete(event_id, operator_qq)


# 29. 批准通过pre的setting外部属性删除事件
@app.post('/event/setting/{event_id}/property/{property_name}/approve_delete')
def approve_pre_setting_property_delete(event_id: str, property_name: str, operator_qq: str = Query(...)) -> dict:
    """批准通过pre的setting外部属性删除事件。"""
    return utils.approve_pre_setting_property_delete(event_id, property_name, operator_qq)


# 30. 批准通过pre的setting删除事件
@app.post('/event/setting/{event_id}/approve_delete')
def approve_pre_setting_delete(event_id: str, operator_qq: str = Query(...)) -> dict:
    """批准通过pre的setting删除事件。"""
    return utils.approve_pre_setting_delete(event_id, operator_qq)


# 31. 批准驳回pre的story新增/修改事件
@app.post('/event/story/{event_id}/reject')
def reject_pre_story_event(event_id: str, operator_qq: str = Query(...)) -> dict:
    """批准驳回pre的story新增/修改事件。"""
    return utils.reject_pre_story_event(event_id, operator_qq)


# 32. 批准驳回pre的setting新增事件
@app.post('/event/setting/{event_id}/reject')
def reject_pre_setting_event(event_id: str, operator_qq: str = Query(...)) -> dict:
    """批准驳回pre的setting新增事件。"""
    return utils.reject_pre_setting_event(event_id, operator_qq)


# 33. 批准驳回pre的setting外部属性新增/修改事件
@app.post('/event/setting/{event_id}/property/{property_name}/reject')
def reject_pre_setting_property(event_id: str, property_name: str, operator_qq: str = Query(...)) -> dict:
    """批准驳回pre的setting外部属性新增/修改事件。"""
    return utils.reject_pre_setting_property(event_id, property_name, operator_qq)


# 34. 批准驳回pre的story删除事件
@app.post('/event/story/{event_id}/reject_delete')
def reject_pre_story_delete(event_id: str, operator_qq: str = Query(...)) -> dict:
    """批准驳回pre的story删除事件。"""
    return utils.reject_pre_story_delete(event_id, operator_qq)


# 35. 批准驳回pre的setting外部属性删除事件
@app.post('/event/setting/{event_id}/property/{property_name}/reject_delete')
def reject_pre_setting_property_delete(event_id: str, property_name: str, operator_qq: str = Query(...)) -> dict:
    """批准驳回pre的setting外部属性删除事件。"""
    return utils.reject_pre_setting_property_delete(event_id, property_name, operator_qq)


# 36. 批准驳回pre的setting删除事件
@app.post('/event/setting/{event_id}/reject_delete')
def reject_pre_setting_delete(event_id: str, operator_qq: str = Query(...)) -> dict:
    """批准驳回pre的setting删除事件。"""
    return utils.reject_pre_setting_delete(event_id, operator_qq)
