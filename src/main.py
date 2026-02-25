import os
import sys

# 保证能正确 import 同级的模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fetcher import fetch_feeds
from analyzer import process_and_score
from generator import generate_html

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    feeds_config_path = os.path.join(project_root, 'feeds.json')
    output_html_path = os.path.join(project_root, 'index.html')
    
    print(">>> 启动 Clean-News 极简新闻聚合器 <<<")
    
    # 1. 网络抓取层
    print("\n[1/3] 正在从 feeds.json 抓取并解析数据...")
    raw_data = fetch_feeds(feeds_config_path)
    
    if not raw_data:
        print("[Error] 未抓取到任何数据，程序退出。")
        return
        
    # 2. 核心打分层
    print("\n[2/3] 正在执行跨源词频共振打分算法...")
    processed_data, top_20 = process_and_score(raw_data)
    
    # 3. 极简展示层
    print("\n[3/3] 正在生成静态 HTML...")
    generate_html(processed_data, top_20, output_html_path)
    
    print("\n>>> Clean-News 更新完毕！ <<<")

if __name__ == '__main__':
    main()
