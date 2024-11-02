import json
import os

# 定义数据文件的名称
DATA_FILE = 'data/records.json'

def load_records():
    """加载已有记录."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_records(records):
    """保存记录到 JSON 文件."""
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(records, file, ensure_ascii=False, indent=4)

def add_record(date, amount, category, note):
    """添加一条新的记账记录."""
    records = load_records()
    
    # 创建新的记录
    new_record = {
        "date": date,
        "amount": amount,
        "category": category,
        "note": note
    }
    
    # 将新记录添加到列表
    records.append(new_record)
    
    # 保存所有记录
    save_records(records)

def delete_record(date=None, amount=None, category=None, note=None):
    """删除符合条件的记账记录，并返回删除操作是否成功."""
    records = load_records()
    
    # 定义删除前的记录数量
    initial_count = len(records)
    
    # 根据提供的参数过滤记录
    records = [record for record in records if not (
        (date is None or record['date'] == date) and
        (amount is None or record['amount'] == amount) and
        (category is None or record['category'] == category) and
        (note is None or record['note'] == note)
    )]
    
    # 如果记录被删除，保存修改后的记录列表
    if len(records) < initial_count:
        save_records(records)
        return True  # 返回删除成功
    else:
        return False  # 返回未找到记录

