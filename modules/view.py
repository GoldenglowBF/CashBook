import json
import os

# 定义数据文件的名称
DATA_FILE = 'data/records.json'

def load_1_json():
    global DATA_FILE
    DATA_FILE = 'data/records.json'

def load_2_json():
    global DATA_FILE
    DATA_FILE = 'data/records_1.json'

def load_records():
    """加载已有记录."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def get_recent_records(limit=5):
    """获取最近的几笔记录."""
    records = load_records()
    return records[-limit:]  # 返回最近的记录
