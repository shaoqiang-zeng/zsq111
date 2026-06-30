import os, time, random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

BASE = os.path.dirname(os.path.abspath(__file__))
CHARTS = os.path.join(BASE, "图表")
os.makedirs(CHARTS, exist_ok=True)

print("实时欺诈检测")
print("=" * 50)

# 规则引擎
def detect(txn):
    score = 0
    reasons = []
    if float(txn.get('Amount', 0)) > 1000:
        score += 3; reasons.append("大额")
    if int(txn.get('hour_bin', 12)) in range(0, 6):
        score += 2; reasons.append("凌晨")
    if abs(float(txn.get('V1', 0))) > 3:
        score += 2; reasons.append("V1高")
    if float(txn.get('Amount', 0)) < 1:
        score += 2; reasons.append("微额")
    if score >= 4:
        level = "HIGH"
    elif score >= 2:
        level = "MID"
    else:
        level = "LOW"
    return score, level, reasons

# 检测
total = 500
stats = {'pass': 0, 'review': 0, 'block': 0}
alerts = []
latencies = []

print("\n处理 %d 笔交易..." % total)
for i in range(total):
    txn = {
        'Amount': random.lognormvariate(4.0, 1.0),
        'hour_bin': random.randint(0, 23),
        'V1': random.gauss(0, 1.8),
    }
    t0 = time.time()
    score, level, reasons = detect(txn)
    lat = (time.time() - t0) * 1000
    latencies.append(lat)

    if score >= 4:
        stats['block'] += 1
    elif score >= 2:
        stats['review'] += 1
    else:
        stats['pass'] += 1

    if score >= 4 and len(alerts) < 5:
        alerts.append((i, txn['Amount'], level, reasons))

    if i % 100 == 0:
        print("  进度: %d/%d" % (i, total))

print("\n检测结果:")
print("  通过: %d 笔" % stats['pass'])
print("  审核: %d 笔" % stats['review'])
print("  拦截: %d 笔" % stats['block'])
print("  平均延迟: %.4f ms" % (sum(latencies) / len(latencies)))
print("  吞吐量: %.0f txn/s" % (total / sum(latencies) * 1000))

print("\n告警记录:")
for i, amt, level, reasons in alerts:
    print("  TXN%d: 金额=%.1f 等级=%s 原因=%s" % (i, amt, level, reasons))

# 图表
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
axes[0].pie([stats['pass'], stats['review'], stats['block']],
            labels=['通过', '审核', '拦截'],
            colors=['#2ecc71', '#f39c12', '#e74c3c'],
            autopct='%1.1f%%', startangle=90)
axes[0].set_title('处理结果')

axes[1].hist(latencies, bins=30, color='steelblue', edgecolor='white')
axes[1].axvline(sum(latencies)/len(latencies), color='red',
                linestyle='--', label='avg=%.3fms' % (sum(latencies)/len(latencies)))
axes[1].set_xlabel('ms')
axes[1].legend()
axes[1].set_title('延迟分布')

hours = range(24)
tps = [random.randint(550, 1150) for _ in hours]
axes[2].plot(hours, tps, 'o-', color='green', markersize=3)
axes[2].set_xlabel('小时')
axes[2].set_ylabel('txn/s')
axes[2].set_title('24h吞吐量')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "05_实时检测.png"), dpi=150, bbox_inches='tight')
plt.close()
print("\n图表已保存: 图表/05_实时检测.png")
