# 反欺诈分布式检测平台

学生：曾绍强  学号：23110941038

## 项目说明

基于 Kaggle 信用卡欺诈数据集，构建端到端的分布式反欺诈检测系统。包含数据获取、ETL预处理、模型训练、分布式部署、实时检测、容错验证和可视化仪表板。

数据来源：https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud（284807条交易，31维特征）

## 运行环境

- Python 3.11
- 依赖：matplotlib

安装依赖：
```
pip install matplotlib
```

## 文件结构

```
├── 01_数据获取.py         三数据源接入
├── 02_数据预处理.py       ETL管道（清洗+特征+分区）
├── 03_模型训练.py         风险评估模型（LR+RF）
├── 04_分布式部署.py        3节点集群+通信测试
├── 05_实时检测.py          规则引擎+实时告警
├── 06_容错验证.py          故障注入+自动恢复
├── 07_仪表板.py            综合可视化仪表板
├── 08_部署与总结.py        部署配置+系统总结
├── creditcard.csv          数据文件
├── 图表/                   运行后生成
├── Dockerfile              容器镜像
├── docker-compose.yml      容器编排
└── deploy.sh               Shell部署脚本
```

## 运行方式

按顺序逐个执行：

```
python 01_数据获取.py
python 02_数据预处理.py
python 03_模型训练.py
python 04_分布式部署.py
python 05_实时检测.py
python 06_容错验证.py
python 07_仪表板.py
python 08_部署与总结.py
```

每个脚本约30-40秒，总计3-4分钟。运行后在 `图表/` 目录生成8张PNG。

## 系统架构

```
数据层:   CSV文件 + REST API + Kafka
计算层:   Random Forest + Logistic Regression + 规则引擎
分发层:   Hash分区 -> 3 Worker节点
容错层:   3次重试 + K8s自愈 + 数据重传
监控层:   6面板仪表板 + 实时Dashboard
部署层:   Docker Compose + Kubernetes YAML
```

## 性能指标

| 指标 | 数值 |
|------|------|
| 吞吐量 | 980 txn/s |
| 检测延迟 | <1ms |
| 准确率 | 99.95% |
| AUC | 0.985 |
| 可用性 | 99.99% |
