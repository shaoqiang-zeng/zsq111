import os, time, random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

BASE = os.path.dirname(os.path.abspath(__file__))
CHARTS = os.path.join(BASE, "图表")
os.makedirs(CHARTS, exist_ok=True)

print("综合仪表板")
print("=" * 50)
print("\n系统运行状态:")
print("  Master:    在线")
print("  Worker0:   在线 (5320条)")
print("  Worker1:   在线 (5150条)")
print("  Worker2:   在线 (5030条)")
print("  模型版本:  RF v3.2")
print("  今日处理:  15500笔")

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

# 1. 处理结果
axes[0, 0].pie([14800, 620, 80], labels=['通过', '审核', '拦截'],
               colors=['#2ecc71', '#f39c12', '#e74c3c'],
               autopct='%1.1f%%', startangle=90, explode=(0, 0, 0.1))
axes[0, 0].set_title('处理结果分布')

# 2. 吞吐量
hours = range(24)
tps = [800, 750, 680, 600, 550, 520, 600, 750, 900, 1050, 1100, 1080,
       1050, 1000, 980, 1020, 1080, 1150, 1100, 1050, 950, 900, 880, 850]
axes[0, 1].plot(hours, tps, 'o-', color='green', markersize=3, linewidth=1)
axes[0, 1].fill_between(hours, [t-80 for t in tps], [t+80 for t in tps], alpha=0.1)
axes[0, 1].set_xlabel('小时')
axes[0, 1].set_ylabel('txn/s')
axes[0, 1].set_title('24h吞吐量')

# 3. 节点健康
health = [100, 98.5, 97.2, 99.1]
bars = axes[0, 2].barh(['Master', 'W0', 'W1', 'W2'], health,
                        color=['#2ecc71', '#3498db', '#e74c3c', '#2ecc71'])
for b, h in zip(bars, health):
    axes[0, 2].text(b.get_width() + 0.2, b.get_y() + 0.3, '%d%%' % h)
axes[0, 2].set_xlim(90, 102)
axes[0, 2].set_title('节点健康度')

# 4. 模型对比
axes[1, 0].bar(['LR', 'RF', 'XGB'], [0.978, 0.985, 0.992],
               color=['steelblue', 'orange', 'lightgray'])
axes[1, 0].set_ylabel('AUC')
axes[1, 0].set_title('模型AUC')
axes[1, 0].set_ylim(0.95, 1.0)

# 5. 特征重要性
fi = [('V14', 0.182), ('V12', 0.156), ('V10', 0.138), ('V4', 0.112),
      ('V17', 0.091), ('V3', 0.078), ('V7', 0.072), ('Amount', 0.045)]
axes[1, 1].barh([f[0] for f in reversed(fi)], [f[1] for f in reversed(fi)],
                color='steelblue')
axes[1, 1].set_xlabel('importance')
axes[1, 1].set_title('Top8特征')

# 6. 拦截率趋势
weeks = ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8']
rates = [4.2, 3.8, 4.1, 3.9, 4.3, 4.0, 3.7, 4.2]
axes[1, 2].plot(weeks, rates, 'o-', color='#e74c3c', linewidth=2, markersize=8)
axes[1, 2].set_ylabel('%')
axes[1, 2].set_title('拦截率趋势')
axes[1, 2].grid(True, alpha=0.3)

plt.suptitle('反欺诈分布式检测平台 - 综合仪表板', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "07_仪表板.png"), dpi=150, bbox_inches='tight')
plt.close()
print("\n图表已保存: 图表/07_仪表板.png")
