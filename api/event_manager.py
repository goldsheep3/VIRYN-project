import glob
import os
from typing import List, Literal, Union, Optional, Tuple, Any

import frontmatter
import yaml

from api.models import (
    EventBase, StoryEvent, Author, StoryData, AuthorGroup, Properties, EventRelated, StoryTime, ImageEvent,
    MDEventBase, ALL_EVENT
)
from api.log import ApiLogger

logger = ApiLogger()


def _get_author_info(qq: Union[str, int], authors: dict) -> Author:
    """辅助函数 | 根据 qq 号，从 authors 数据中获取作者信息"""
    author_data = authors.get(int(qq))
    if author_data is None:
        author_data = {}
    name = author_data.get('name', f'Creator {qq}')
    email = author_data.get('email')
    return Author(qq=str(qq), name=name, email=email)


def _get_properties(
        filepath,
        authors,
        filter_pre,
        img_yaml_info=None
) -> Optional[Tuple[str, Properties]]:
    """获取事件内部属性"""
    if not os.path.exists(filepath):
        # log: "File not found: {filepath}"
        return None

    logger.trace('')
    logger.trace(f"Processing file: {filepath}")

    # 文件类型判断，优先处理图片文件，只有 markdown 文件才用 frontmatter 解析
    file_ext = os.path.splitext(filepath)[1].lower()
    is_markdown = file_ext == ".md"
    is_image = file_ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"]

    if img_yaml_info or is_image:
        # Image
        metadata: dict[str, Any] = img_yaml_info if img_yaml_info else {}
    elif is_markdown:
        # Markdown
        try:
            post = frontmatter.load(filepath)
            metadata = post.metadata
        except Exception as e:
            logger.error(f"Failed to load frontmatter from {filepath}: {e}")
            return None
    else:
        # 非支持类型直接返回 None
        logger.error(f"Unsupported file type for event: {filepath}")
        return None

    def _metadata_get(key: str, type_: type, default=None):
        """辅助函数 | 从 frontmatter metadata 中获取指定类型的值"""
        value = metadata.get(key, default)
        logger.trace(f"{key}: {value}")
        if isinstance(value, type_):
            return value
        elif value is None:
            return default
        # 自动兼容 date/datetime 类型转字符串
        elif type_ is str and type(value).__name__ in ['date', 'datetime', 'time']:
            return str(value)
        else:
            raise ValueError(f"Expected {key} to be of type {type_.__name__}, got {type(value).__name__} instead.")

    # Id，统一为正斜杠
    event_id = os.path.relpath(filepath, os.path.join(os.path.dirname(__file__), '../')).replace('\\', '/')

    # State
    event_state = _metadata_get('state', str, 'unknown')
    # filter_pre 筛选过滤
    if filter_pre == 'not' and event_state == 'pre':
        return None
    elif filter_pre == 'only' and event_state != 'pre':
        return None
    elif event_state not in ['pre', 'release', 'original']:
        # log: "Unknown event state in file: {fpath}"
        return None

    # Author
    author_info = _metadata_get('author', dict)
    if not author_info:
        raise ValueError(f"Author information in {filepath} is not a dictionary.")
    create_author = _get_author_info(str(author_info.get('create', '')), authors)
    last_author = _get_author_info(str(author_info.get('last', '')), authors)
    contributors = author_info.get('contributors', [])
    logger.trace(f"Contributors: {contributors}, type: {type(contributors)}")
    if not isinstance(contributors, list):
        contributors = [str(contributors)]
    for c in contributors:
        logger.trace(f"Contributor: {c}, type: {type(c)}")
    contributors = [_get_author_info(c, authors) for c in contributors if c]
    author_group = AuthorGroup(create=create_author, last=last_author, contributors=contributors)

    # Related
    related_info = _metadata_get('related', dict, dict())
    for e_tags in ['story', 'character', 'world']:
        if isinstance(related_info.get(e_tags), str):
            related_info[e_tags] = [related_info[e_tags]]
        elif related_info.get(e_tags) is None:
            related_info[e_tags] = []
    related = EventRelated(
        story=related_info.get('story'),
        character=related_info.get('character'),
        world=related_info.get('world'),
    )

    # type 字段补全
    event_type = _metadata_get('type', str, '')
    if not event_type and is_image:
        event_type = 'image'

    # All Internal Properties
    properties = Properties(
        title=_metadata_get('title', str, os.path.basename(filepath)[:-3]),
        type=event_type,
        author=author_group,
        create_datetime=_metadata_get('date', str, ''),
        last_datetime=_metadata_get('last_date', str, ''),
        state=event_state,
        related=related
    )

    return event_id, properties


def _get_md_events(md_files, authors, filter_pre) -> List[MDEventBase]:
    """获取 Markdown 事件列表"""
    md_events = list()
    for fpath in md_files:
        post = frontmatter.load(fpath)
        fm = post.metadata
        event_id, properties = _get_properties(fpath, authors, filter_pre)
        if not properties:
            # log: "Failed to get internal properties for file: {fpath}"
            continue
        if properties.type == 'story':
            story_data = fm.get('story', dict)
            if not isinstance(story_data, dict):
                # log
                continue
            story_obj = StoryData(
                upstream=story_data.get('upstream') if story_data else None,
                time=StoryTime(
                    start=story_data.get('time', {}).get('start', '') if story_data.get('time') else '',
                    end=story_data.get('time', {}).get('end', '') if story_data.get('time') else ''
                )
            )
            event = StoryEvent(
                id=event_id,
                properties=properties,
                story=story_obj,
                content=post.content
            )
        elif properties.type[:7] == 'setting':
            content = post.content
            if properties.type == 'setting/character':
                # event = CharacterSettingEvent()
                continue
            elif properties.type == 'setting/world':
                # event = WorldSettingEvent()
                continue
            else:
                # log: "Unknown setting event type in file: {fpath}"
                continue
        else:
            # log: "Unknown event type in file: {fpath}"
            continue
        md_events.append(event)
    return md_events


def _get_img_events(img_files, img_yaml_info: dict, authors, filter_pre) -> List[EventBase]:
    """获取图片事件列表"""
    img_events = list()
    for ipath in img_files:
        # 用图片文件名查找 images.yaml 中的属性
        img_info = img_yaml_info.get(os.path.basename(ipath), {})
        event_id, properties = _get_properties(ipath, authors, filter_pre, img_info)
        if not properties:
            # log: "Failed to get internal properties for file: {ipath}"
            continue
        event = ImageEvent(
            id=event_id,
            properties=properties
        )
        img_events.append(event)
    return img_events


def get_events(
    filter_type: Literal[
        'story', 'setting', 'setting/world', 'setting/character', 'image', 'not_image', 'all'
    ] = 'not_image',
    filter_pre: Literal['only', 'not', 'all'] = 'all'
) -> List[ALL_EVENT]:
    """根据条件，获取事件列表"""
    base_dir = os.path.join(os.path.dirname(__file__), '../event')
    events = list()
    md_scan_dirs = list()
    img_scan_dirs = list()
    # 1. 筛选扫描目录
    if filter_type == 'not_image':
        # 只处理 md 文件
        md_scan_dirs = ['story', 'setting/world', 'setting/character']
    elif filter_type == 'image':
        # 只处理 image 文件
        img_scan_dirs = ['image']
    elif filter_type == 'setting':
        # 处理 setting 下的文件
        md_scan_dirs = ['setting/world', 'setting/character']
    elif filter_type == 'all':
        # 处理所有文件
        md_scan_dirs = ['story', 'setting/world', 'setting/character']
        img_scan_dirs = ['image']
    else:
        md_scan_dirs = [filter_type]
    # 2. 获取 yaml 数据
    authors = dict()
    try:
        author_yaml = os.path.join(os.path.dirname(__file__), '../data/authors.yaml')
        with open(author_yaml, encoding='utf-8') as f:
            authors = yaml.safe_load(f)
        if not isinstance(authors, dict):
            # log: "Author data in author.yaml is not a dictionary."
            raise
    except FileNotFoundError:
        # log: "author.yaml file not found, using empty author data."
        pass
    images = dict()
    try:
        image_yaml = os.path.join(os.path.dirname(__file__), '../data/images.yaml')
        with open(image_yaml, encoding='utf-8') as f:
            images = yaml.safe_load(f)
        if not isinstance(images, dict):
            # log: "Image data in image.yaml is not a dictionary."
            raise
    except FileNotFoundError:
        # log: "image.yaml file not found, using empty image data."
        pass
    # 3. 对 md 进行扫描和处理
    if md_scan_dirs:
        md_files = list()
        for sub in md_scan_dirs:
            sub_dir = os.path.join(base_dir, sub)
            md_files.extend(glob.glob(os.path.join(sub_dir, '**', '*.md'), recursive=True))
        events.extend(_get_md_events(md_files, authors, filter_pre))
    # 4. 对 img 进行扫描和处理
    if img_scan_dirs:
        image_files = list()
        image_exts = ['png', 'jpg', 'jpeg', 'gif', 'webp']
        for sub in img_scan_dirs:
            sub_dir = os.path.join(base_dir, sub)
            for ext in image_exts:
                image_files.extend(glob.glob(os.path.join(sub_dir, '**', f'*.{ext}'), recursive=True))
        events.extend(_get_img_events(image_files, images, authors, filter_pre))
    # 5. 返回事件列表
    return events
