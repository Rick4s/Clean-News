import re
from collections import Counter
from datetime import datetime, timezone
import jieba

try:
    from email.utils import parsedate_to_datetime
except ImportError:
    pass

try:
    from .config import STOPWORDS, BOOSTER_WORDS
except ImportError:
    from config import STOPWORDS, BOOSTER_WORDS

def _parse_date(date_str):
    """
    尝试从字符串中解析出 timezone-aware 的 datetime 对象
    """
    if not date_str:
        return None
    try:
        return parsedate_to_datetime(date_str)
    except Exception:
        pass
    
    try:
        # 处理 ISO 8601 格式
        s = date_str.replace('Z', '+00:00')
        return datetime.fromisoformat(s)
    except Exception:
        pass
    
    return None

def extract_words(text):
    """
    从文本中提取有意义的词汇，过滤掉单字和停用词。
    英文正则提取，中文利用 jieba 提取。
    """
    if not text:
        return []
        
    text_lower = text.lower()
    # 提取英文词汇（连续2个字母以上）
    eng_words = re.findall(r'[a-z]{2,}', text_lower)
    
    # 提取中文词汇（剔除英文和数字，只留汉字）
    zh_text = re.sub(r'[^\u4e00-\u9fa5]', '', text)
    zh_words = list(jieba.cut(zh_text)) if zh_text else []
    
    words = eng_words + zh_words
    # 过滤：长度大于1且不在停用词表中
    final_words = [w for w in words if len(w) > 1 and w not in STOPWORDS]
    
    return final_words

def process_and_score(all_feeds_data):
    """
    三步走跨源词频共振打分引擎
    """
    # ====== Pass 1: 全局共识池 ======
    all_words = []
    for source, entries in all_feeds_data.items():
        for entry in entries:
            text = entry.get('title', '') + " " + entry.get('summary', '')
            all_words.extend(extract_words(text))
            
    # 统计出全网词频最高的 Top 20 个“热词”
    word_counts = Counter(all_words)
    top_20_list = word_counts.most_common(20)
    top_20_dict = dict(top_20_list)
    
    # ====== Pass 2: 回溯打分 & Pass 3: 截断输出 ======
    processed_data = {}
    
    # 缓存当前时间用于计分
    now_utc = datetime.now(timezone.utc)
    
    for source, entries in all_feeds_data.items():
        scored_entries = []
        for entry in entries:
            score = 0
            
            # --- 1. 共振分 ---
            text = entry.get('title', '') + " " + entry.get('summary', '')
            words = extract_words(text)
            for w in words:
                if w in top_20_dict:
                    score += top_20_dict[w]
                    
            # --- 2. 新鲜分 ---
            date_str = entry.get('published', '')
            dt = _parse_date(date_str)
            if dt:
                try:
                    # 确保是 UTC 以计算 timedelta
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    delta = now_utc - dt
                    if delta.days == 0:
                        score += 10
                    elif delta.days == 1:
                        score += 5
                except Exception:
                    pass
                    
            # --- 3. 提权分 ---
            title = entry.get('title', '')
            for booster in BOOSTER_WORDS:
                if booster in title:
                    score += 100
                    break
                    
            entry['score'] = score
            scored_entries.append(entry)
            
        # 降序排列并强制切片保留前10条
        scored_entries.sort(key=lambda x: x['score'], reverse=True)
        processed_data[source] = scored_entries[:10]
        
    return processed_data, top_20_list

if __name__ == '__main__':
    import os
    try:
        from .fetcher import fetch_feeds
    except ImportError:
        from fetcher import fetch_feeds
        
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    feeds_config_path = os.path.join(project_root, 'feeds.json')
    
    print("开始获取数据并执行核心共振打分...")
    raw_data = fetch_feeds(feeds_config_path)
    
    if not raw_data:
        print("未抓取到有效数据，测试结束。")
    else:
        processed_data, top_20 = process_and_score(raw_data)
        
        print("\n--- 当天的全网 Top 5 热词 ---")
        for i, (word, count) in enumerate(top_20[:5], 1):
            print(f"{i}. {word} ({count}次)")
            
        print("\n--- 得分最高的那 1 条新闻 ---")
        best_entry = None
        best_score = -1
        best_source = ""
        
        for source, entries in processed_data.items():
            if entries and entries[0]['score'] > best_score:
                best_entry = entries[0]
                best_score = entries[0]['score']
                best_source = source
                
        if best_entry:
            print(f"[{best_source}] {best_entry['title']}")
            print(f"总分: {best_score}")
