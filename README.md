# zsq111
# zsq111 分布式金融风控欺诈检测平台
对应课程实验十四~实验十六期末大作业完整工程
作者：Zeng Shaoqiang
学号：23110941038

## 一、项目简介
基于Spark分布式计算搭建全流程风控平台：
1. 多渠道数据获取（接口爬虫+本地CSV数据源）
2. HDFS分区存储+分布式ETL数据清洗
3. 分布式机器学习（线性回归风险打分、K-Means客户分群）
4. 集群容错、节点故障自动重试机制
5. 实时可视化监控仪表板
6. 一键Docker Compose集群部署

## 二、环境依赖
### 基础环境
- Python 3.9
- Spark 3.3.0
- Hadoop 3.2
- Docker & Docker Compose
- Pandas、Matplotlib、Scikit-learn

### Python依赖一键安装
```bash
pip install -r fraud_platform/requirements.txt
