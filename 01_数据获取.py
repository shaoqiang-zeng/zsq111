import csv, os, time, random, json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

BASE = os.path.dirname(os.path.abspath(__file__))
CHARTS = os.path.join(BASE, "图表")
os.makedirs(CHARTS, exist_ok=True)

print("数据获取模块")
print("=" * 50)

# 数据源1: 本地CSV
print("\n1. CSV文件读取")
csv_file = os.path.join(BASE, "creditcard.csv")
csv_rows = []
fraud_count = 0
total_count = 0

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_count += 1
        if total_count > 20000:
            break
        csv_rows.append(row)
        if int(row.get('Class', '0')) == 1:
            fraud_count += 1

print("   文件: creditcard.csv")
print("   读取行数: %d" % len(csv_rows))
print("   正常: %d, 欺诈: %d" % (len(csv_rows) - fraud_count, fraud_count))
print("   欺诈率: %.3f%%" % (fraud_count / len(csv_rows) * 100))

# 数据源2: 模拟API
print("\n2. API接口获取")
api_rows = []
for i in range(500):
    api_rows.append({
        'txn_id': 'TXN%d' % (int(time.time() * 1000) + i),
        'amount': round(random.lognormvariate(4.0, 1.0), 2),
        'time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'merchant': random.choice(['餐饮', '零售', '电子', '旅行', '医疗']),
        'device': random.choice(['iOS', 'Android', 'Web']),
    })

print("   接口: GET /api/transactions")
print("   获取: %d 条" % len(api_rows))
print("   示例: %s" % json.dumps(api_rows[0], ensure_ascii=False))

# 汇总
print("\n" + "=" * 50)
print("数据源汇总")
print("   CSV本地文件: %d 行" % len(csv_rows))
print("   API接口:     %d 行" % len(api_rows))
print("   合计:         %d 行" % (len(csv_rows) + len(api_rows)))

# 图表
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].pie([len(csv_rows), len(api_rows)], labels=['CSV', 'API'],
            autopct='%1.1f%%', colors=['steelblue', 'orange'])
axes[0].set_title('数据来源')

normal = len(csv_rows) - fraud_count
axes[1].bar(['正常', '欺诈'], [normal, fraud_count], color=['green', 'red'])
axes[1].set_title('标签分布')
for i, v in enumerate([normal, fraud_count]):
    axes[1].text(i, v + 5, str(v), ha='center')

plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "01_数据获取.png"), dpi=150)
plt.close()
print("\n图表已保存: 图表/01_数据获取.png")
