import os
from typing import Optional, Tuple, Any

import frontmatter

from api.log import ApiLogger
from api.models import AuthorGroup, Properties, EventRelated

logger = ApiLogger()


def _parse_properties(
        filepath,
        authors,
        filter_pre,
        img_yaml_info=None
) -> Optional[Tuple[str, Properties]]:
    """解析事件通用内部属性"""
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
    contributors = author_info.get('contributors', [])
    if not isinstance(contributors, list):
        contributors = [contributors]
    author_group = AuthorGroup.get_all(
        create=author_info.get('create', ''),
        last=author_info.get('last', ''),
        contributors=contributors,
        authors=authors
    )

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
