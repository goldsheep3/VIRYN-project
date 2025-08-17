import re
from typing import List, Dict, Optional, Any, Tuple

from api.log import ApiLogger
from api.models import AuthorGroup, Attribute, AttributePre, Author

logger = ApiLogger()

# 路径及元数据正则提前定义
HEADER_PATTERN = re.compile(r'^(#{1,6})\s+(.*)')
META_PATTERN = re.compile(r'<!--last:(.*?);contributors:(.*?);createDate:(.*?);lastDate:(.*?);-->')
PRE_START_PATTERN = re.compile(r'^>\s*\*PRE\*')
PRE_AUTHOR_PATTERN = re.compile(r'<!--author:(.*?);date:(.*?);delete:(.*?);-->')


def _parse_pre_block(
        content: List[str],
        authors_db: Dict[str, Dict[str, Any]]
) -> Tuple[Optional[AttributePre], List[str]]:
    """
    从内容中提取第一个 PRE 块并解析为 AttributePre 实例。PRE内容及元数据会从 content 中移除。
    若无 PRE 块则返回 (None, 原内容)。
    """
    pre_block = None
    i = 0
    while i < len(content):
        if PRE_START_PATTERN.match(content[i].strip()):
            pre_content_lines = []
            j = i + 1
            while j < len(content):
                line = content[j].strip()
                if line.startswith('>') and not PRE_START_PATTERN.match(line):
                    # 处理PRE内容，包括PRE元数据
                    line_content = line.lstrip('> ').rstrip()
                    if line_content.startswith('<!--author:'):
                        # 这是PRE元数据注释
                        meta_match = PRE_AUTHOR_PATTERN.match(line_content)
                        if meta_match:
                            author_qq = meta_match.group(1).strip()
                            author = Author.get(author_qq, authors_db)
                            pre_block = AttributePre(
                                key="PRE",
                                value='\n'.join(pre_content_lines).strip(),
                                last=author,
                                last_datetime=meta_match.group(2).strip(),
                                delete=str(meta_match.group(3)).lower() == "true"
                            )
                        # 删除PRE块内容和元数据
                        content = content[:i] + content[j+1:]
                        return pre_block, content
                    else:
                        pre_content_lines.append(line_content)
                    j += 1
                else:
                    break
            break
        i += 1
    return pre_block, content


def _parse_block_meta(
        content: List[str],
        authors: Dict[str, Dict[str, Any]]
) -> Tuple[Optional[Dict[str, Any]], List[str]]:
    """
    提取并解析块内容末尾的元数据（如有），返回 meta 字典和去除元数据后的内容。
    """
    META_PATTERN = re.compile(r'<!--last:(.*?);contributors:(.*?);createDate:(.*?);lastDate:(.*?);-->')
    if not content:
        return None, content
    last_line = content[-1].strip()
    meta_match = META_PATTERN.match(last_line)
    if not meta_match:
        return None, content
    last_qq = meta_match.group(1).strip()
    contributors_raw = meta_match.group(2).strip()
    if contributors_raw:
        contributors_qq = [c.strip() for c in contributors_raw.split(',') if c.strip()]
    else:
        contributors_qq = []
    create_qq = contributors_qq[0] if contributors_qq else None
    author_group = AuthorGroup.get_all(
        create=create_qq,
        last=last_qq,
        contributors=contributors_qq,
        authors=authors
    )
    meta = {
        'author_group': author_group,
        'createDate': meta_match.group(3).strip(),
        'lastDate': meta_match.group(4).strip()
    }
    # 去除元数据行
    return meta, content[:-1]


def _parse_markdown_blocks(
        markdown: str,
        authors: Dict[str, Dict[str, Any]]
) -> List[Attribute]:
    lines = markdown.splitlines()
    stack: List[Dict[str, Any]] = []
    blocks: List[Dict[str, Any]] = []

    def _parse_block_end():
        """辅助函数 | 块的结束处理"""
        block = stack.pop()
        pre, block['content'] = _parse_pre_block(block['content'], authors)
        block['pre'] = pre
        meta, block['content'] = _parse_block_meta(block['content'], authors)
        block['meta'] = meta
        block['parents'] = [item['title'] for item in stack]
        return block

    for line in lines:
        header_match = HEADER_PATTERN.match(line)
        if header_match:
            level = len(header_match.group(1))
            title = header_match.group(2).strip()
            while stack and stack[-1]['level'] >= level:
                blocks.append(_parse_block_end())
            stack.append({
                'level': level,
                'title': title,
                'content': [],
            })
        else:
            if stack:
                stack[-1]['content'].append(line)
    while stack:
        blocks.append(_parse_block_end())

    blocks.reverse()

    attributes: List[Attribute] = []
    for block in blocks:
        meta = block.get('meta', {})
        if not meta:
            continue
        attribute = Attribute(
            key=block['parents'] + [block['title']],
            value='\n'.join(block['content']).strip(),
            authors=meta['author_group'],
            create_datetime=meta['createDate'],
            last_datetime=meta['lastDate'],
            pre=block.get('pre')
        )
        attributes.append(attribute)
    return attributes
