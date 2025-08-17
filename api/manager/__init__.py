import glob
import os
from typing import List, Literal

import frontmatter
import yaml

from api.models import (
    EventBase, StoryEvent, StoryData, StoryTime, ImageEvent, MDEventBase, CharacterSettingEvent, WorldSettingEvent,
    ALL_EVENT
)
from api.log import ApiLogger
from .attributes import _parse_markdown_blocks
from .properties import _parse_properties

logger = ApiLogger()


def _get_md_events(md_files, authors, filter_pre) -> List[MDEventBase]:
    """获取 Markdown 事件列表"""
    md_events = list()
    for fpath in md_files:
        post = frontmatter.load(fpath)
        fm = post.metadata
        event_id, properties = _parse_properties(fpath, authors, filter_pre)
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
            attributes = _parse_markdown_blocks(content, authors)
            if properties.type == 'setting/character':
                event = CharacterSettingEvent(
                    id=event_id,
                    properties=properties,
                    attributes=attributes
                )
            elif properties.type == 'setting/world':
                event = WorldSettingEvent(
                    id=event_id,
                    properties=properties,
                    attributes=attributes
                )
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
        event_id, properties = _parse_properties(ipath, authors, filter_pre, img_info)
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
