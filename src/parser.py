def parse_entries(entries):
    """
    防御性解析层
    接收原始的 feedparser 节点列表 (entries)，剥离不可靠的键并提取必要信息。
    """
    parsed_items = []
    for entry in entries:
        # 强制使用 .get()，严禁使用直接字典访问
        # 如果节点中连 title 和 summary 都没有，我们分别给予合理的默认空值
        title = entry.get('title', '无标题')
        link = entry.get('link', '')
        summary = entry.get('summary', '')
        # RSS中常见时间字段名为 published 或 updated
        published = entry.get('published', '')
        if not published:
            published = entry.get('updated', '')

        # 组装成标准字典
        parsed_items.append({
            'title': title,
            'link': link,
            'summary': summary,
            'published': published
        })
    return parsed_items
