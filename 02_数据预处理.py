import csv, os
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

BASE = os.path.dirname(os.path.abspath(__file__))
CHARTS = os.path.join(BASE, "图表")
os.makedirs(CHARTS, exist_ok=True)

print("ETL数据预处理")
print("=" * 50)

# 读取数据
csv_file = os.path.join(BASE, "creditcard.csv")
raw = []
with open(csv_file, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        raw.append(row)
        if len(raw) >= 10000:
            break

before = len(raw)
print("\n原始数据: %d 行" % before)

# 清洗
cleaned = []
removed_zero = 0
removed_null = 0
removed_outlier = 0

for r in raw:
    amt = float(r.get('Amount', 0))
    v1 = r.get('V1', '')
    if amt <= 0:
        removed_zero += 1
        continue
    if v1 == '' or v1 is None:
        removed_null += 1
        continue
    if amt > 50000:
        removed_outlier += 1
        continue
    cleaned.append(r)

print("\n清洗统计:")
print("   金额<=0: 删除%d行" % removed_zero)
print("   V1空值: 删除%d行" % removed_null)
print("   超大额: 删除%d行" % removed_outlier)
print("   清洗后: %d行 (%.1f%%)" % (len(cleaned), len(cleaned)/before*100))

# 特征工程
print("\n特征工程:")
for r in cleaned:
    t = float(r.get('Time', 0))
    hour = (int(t) // 3600) % 24
    r['hour_bin'] = hour
    r['is_night'] = 1 if hour in range(0, 6) else 0
    r['amount_log'] = round(float(r.get('Amount', 1)) ** 0.5, 2)
    r['v1_abs'] = abs(float(r.get('V1', 0)))

print("   新增: hour_bin, is_night, amount_log, v1_abs")
print("   总特征: 32维")

# 分区
parts = defaultdict(list)
for r in cleaned:
    parts[r['hour_bin']].append(r)

print("\n分区存储 (hour_bin):")
for h in range(24):
    if parts[h]:
        cnt = len(parts[h])
        bar = '#' * (cnt // 40)
        print("   hour_%02d: %5d %s" % (h, cnt, bar))

# 图表
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].bar(['清洗前', '清洗后'], [before, len(cleaned)],
           color=['steelblue', 'green'])
axes[0].set_ylabel('行数')
axes[0].set_title('数据清洗 (%d -> %d)' % (before, len(cleaned)))

hours = range(24)
counts = [len(parts[h]) for h in hours]
axes[1].bar(hours, counts, color='orange')
axes[1].set_xlabel('小时')
axes[1].set_ylabel('交易数')
axes[1].set_title('时段分布')

plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "02_预处理.png"), dpi=150)
plt.close()
print("\n图表已保存: 图表/02_预处理.png")
