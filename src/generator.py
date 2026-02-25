import os
from datetime import datetime, timezone

def generate_html(processed_data, top_20_words, output_path):
    """
    极简展示层：将核心打分后的数据渲染为原生 HTML
    强制仅依赖 Pico.css 且不写任何自定义 CSS
    """
    
    # 获取当前渲染时间 (UTC -> 转换展示或直接展示 UTC)
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # 拼装头部与 Pico.css 引入
    html_parts = [
        "<!DOCTYPE html>",
        '<html lang="zh-CN">',
        "<head>",
        '    <meta charset="UTF-8">',
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '    <title>Clean-News</title>',
        '    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">',
        "</head>",
        "<body>",
        '    <main class="container">',
        "        <header>",
        "            <hgroup>",
        "                <h1>Clean-News</h1>",
        f"                <p>极简 · 稳定 · 全局视野 | 最后更新: {now_str}</p>",
        "            </hgroup>",
        "        </header>"
    ]
    
    # 拼装全局热词区域
    html_parts.append('        <section id="trending">')
    html_parts.append('            <h2>今日全网热词 Top 20</h2>')
    html_parts.append('            <div class="grid">')
    
    words_html = []
    for word, count in top_20_words:
        words_html.append(f"<kbd>{word}</kbd> <small>({count})</small>")
    html_parts.append("                <p>" + " &nbsp; ".join(words_html) + "</p>")
    
    html_parts.append('            </div>')
    html_parts.append('        </section>')
    html_parts.append('        <hr>')
    
    # 拼装各源新闻列表
    html_parts.append('        <section id="news">')
    
    for source, entries in processed_data.items():
        html_parts.append(f'            <article>')
        html_parts.append(f'                <header><strong>{source}</strong></header>')
        
        if not entries:
            html_parts.append('                <p>暂无数据或抓取失败。</p>')
        else:
            html_parts.append('                <ul>')
            for entry in entries:
                title = entry.get('title', '无标题')
                link = entry.get('link', '#')
                score = entry.get('score', 0)
                html_parts.append(f'                    <li><a href="{link}" target="_blank" rel="noopener noreferrer">{title}</a> <mark><small>分值: {score}</small></mark></li>')
            html_parts.append('                </ul>')
            
        html_parts.append('            </article>')
        
    html_parts.append('        </section>')
    
    # 拼装底部
    html_parts.extend([
        "        <footer>",
        '            <p><small>Powered by Python & Pico.css | <a href="https://github.com" target="_blank">GitHub Open Source</a></small></p>',
        "        </footer>",
        "    </main>",
        "</body>",
        "</html>"
    ])
    
    final_html = "\n".join(html_parts)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print(f"网页成功生成并保存至: {output_path}")
    return output_path
