import json
import os
import requests
import feedparser

try:
    from .parser import parse_entries
except ImportError:
    # 兼容直接运行 this script 作为主程序的本地测试需求
    from parser import parse_entries

def fetch_feeds(config_path):
    """
    网络抓取层：读取 feeds.json 并拉取节点数据
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            feeds = json.load(f)
    except Exception as e:
        print(f"[Warning] 无法读取 feeds 配置: {e}")
        return {}

    all_data = {}

    for feed in feeds:
        name = feed.get('name', 'Unknown Source')
        url = feed.get('url', '')
        if not url:
            continue
            
        try:
            # 加入 timeout 强制处理网络超时，防止卡死
            # 加入 requests 应对更复杂的网络要求和 status 检查
            response = requests.get(url, timeout=15)
            # 捕获 403, 500 等 HTTP 错误
            response.raise_for_status()

            # 交给 feedparser 处理纯文本
            parsed_feed = feedparser.parse(response.content)
            
            # 检查 feedparser 层面的严重抓取异常（如内容根本不是合法结构）
            if parsed_feed.bozo and isinstance(parsed_feed.bozo_exception, Exception):
                # 如果完全没有解析出条目再去警告（有的源即便有 bozo 也能容错提取一定内容）
                if not parsed_feed.entries:
                    print(f"[Warning] 解析出错或非规范源，已跳过: {url}")
                    continue
            
            # 使用防御性解析器转换出干净的节点列表
            safe_entries = parse_entries(parsed_feed.entries)
            all_data[name] = safe_entries
            
        except requests.exceptions.Timeout:
            print(f"[Warning] 抓取失败 (超时)，已跳过: {url}")
            continue
        except requests.exceptions.HTTPError as e:
            print(f"[Warning] 抓取失败 (HTTP错误: {e.response.status_code})，已跳过: {url}")
            continue
        except Exception as e:
            print(f"[Warning] 抓取失败 (未知错误: {type(e).__name__})，已跳过: {url}")
            continue

    return all_data

if __name__ == '__main__':
    # 自动化验证测试桩：读取 feeds.json, 打印前 2 条新闻标题和链接
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    feeds_config_path = os.path.join(project_root, 'feeds.json')

    print("开始执行抓取测试...")
    test_results = fetch_feeds(feeds_config_path)
    
    count = 0
    print("\n--- 成功抓取到的前 2 条新闻 ---")
    for source_name, entries in test_results.items():
        for entry in entries:
            print(f"标题: {entry['title']}")
            print(f"链接: {entry['link']}")
            print("-" * 30)
            count += 1
            if count >= 2:
                break
        if count >= 2:
            break
    
    if count == 0:
        print("未抓取到任何新闻节点。")
