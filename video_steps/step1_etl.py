"""
视频步骤1 — 数据获取与预处理 (30秒)
学生: 曾绍强  学号: 23110941038
"""
import csv, json, os, time, random
from collections import defaultdict

STU = "曾绍强 23110941038"
BASE = r"c:\Users\曾绍强\Desktop\云计算作业"
OUT = os.path.join(BASE, "processed_data")
os.makedirs(OUT, exist_ok=True)

# ===== 数据源1: CSV =====
print("=== 步骤1: 数据获取与预处理 ===\n")
csv_path = os.path.join(BASE, "creditcard.csv")
csv_data = []
with open(csv_path, 'r') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i >= 5000: break
        csv_data.append(row)
print(f"[数据源1] CSV文件: 284,807行(Kaggle信用卡欺诈数据集)")
print(f"  已读取: {len(csv_data)} 行 (演示用5000行)")
print(f"  特征: Time, V1~V28(PCA脱敏), Amount, Class")
print(f"  合规: 公开数据集, 已脱敏, 无PII\n")

# ===== 数据源2: API =====
print(f"[数据源2] Web API模拟 (RESTful)")
api_data = []
for i in range(200):
    api_data.append({
        'Time': str(random.randint(0, 172800)),
        'V1': str(round(random.gauss(0, 1.5), 4)),
        'Amount': str(round(random.lognormvariate(4, 1), 2)),
        'is_fraud': '1' if random.random() < 0.005 else '0',
    })
print(f"  接口: GET /api/transactions")
print(f"  响应: JSON格式")
print(f"  已获取: {len(api_data)} 行\n")

# ===== 清洗 =====
all_data = csv_data + api_data
before = len(all_data)
cleaned = [r for r in all_data if float(r.get('Amount', 0)) > 0]
removed = before - len(cleaned)
print(f"[数据清洗]")
print(f"  清洗前: {before}行 → 清洗后: {len(cleaned)}行")
print(f"  删除: {removed}行 (金额<=0)")
print(f"  保留率: {len(cleaned)/before*100:.1f}%\n")

# ===== 分区存储 =====
print(f"[分区存储] 按hour_bin分24区")
parts = defaultdict(list)
for row in cleaned:
    hour = (int(float(row['Time'])) // 3600) % 24
    parts[hour].append(row)

for h in sorted(parts.keys()):
    if parts[h]:
        bar = '#' * (len(parts[h]) // 30)
        print(f"  hour_{h:02d}: {len(parts[h]):5d}行 {bar}")

# 保存示例
meta = {'total': len(cleaned), 'partitions': len(parts), 'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')}
with open(os.path.join(OUT, '_meta.json'), 'w') as f:
    json.dump(meta, f)
print(f"\n  输出目录: {OUT}")
print(f"  分区数: {len(parts)}")
print(f"  完成! {STU}")

time.sleep(3)
