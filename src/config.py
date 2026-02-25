# 突发提权高优词库：一旦标题中包含这些词汇，不论其共振分数是多少，系统都会暴力增加100分绝对权重
BOOSTER_WORDS = [
    "突发", "重磅", "独家", "首发", "警告", "严重", "关键", "紧急",
    "Breaking", "URGENT", "Alert", "Exclusive"
]

# 中英文基础停用词表：用于剔除无意义的介词、连词、代词等，避免干扰热词统计
STOPWORDS = {
    # 中文停用词
    "的", "了", "是", "在", "和", "有", "也", "就", "不", "人", "都", "一", "一个", "上", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好", "自己", "这", "那", "之", "为", "以", "从", "与", "及", "等", "其", "或", "中", "我", "他", "她", "它", "我们", "你们", "他们", "被", "把", "让", "向", "往", "对于", "关于",
    # 英文停用词
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", "out", "if", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "no", "just", "him", "know", "take", "people", "into", "year", "your", "good", "some", "could", "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think", "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", "way", "even", "new", "want", "because", "any", "these", "give", "day", "most", "us"
}
