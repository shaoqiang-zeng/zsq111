#!/bin/bash
# ============================================================
# 反欺诈检测平台 — 一键部署脚本
# 学生: 曾绍强  学号: 23110941038
# 用法: bash deploy.sh [start|stop|restart|status]
# ============================================================

set -e
MODE=${1:-start}

case $MODE in
  start)
    echo "=== 反欺诈检测平台 启动 ==="
    echo "[1/3] 检查环境..."
    python --version || { echo "需要Python3.11+"; exit 1; }
    echo "[2/3] 安装依赖..."
    pip install matplotlib -q
    echo "[3/3] 启动系统..."
    python fraud_platform/main.py
    ;;

  stop)
    echo "停止所有服务..."
    docker compose -f fraud_platform/docker-compose.yml down 2>/dev/null || true
    ;;

  restart)
    bash $0 stop
    bash $0 start
    ;;

  status)
    echo "=== 平台状态 ==="
    echo "Python: $(python --version 2>&1)"
    echo "数据文件: $(ls -lh creditcard.csv 2>/dev/null || echo '未找到')"
    echo "输出目录: $(ls processed_data/ 2>/dev/null || echo '未生成')"
    echo "仪表板图表: $(ls dashboard_charts.png 2>/dev/null || echo '未生成')"
    ;;

  *)
    echo "用法: bash deploy.sh [start|stop|restart|status]"
    ;;
esac
