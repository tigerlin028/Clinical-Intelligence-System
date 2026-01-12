#!/bin/bash

echo "🚀 启动本地开发服务器..."

# 启动 FastAPI 服务
echo "📡 启动 API 服务在 http://localhost:8000"
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &

# 等待服务启动
sleep 3

echo "✅ 服务已启动！"
echo "📱 本地测试: http://localhost:8000/health"
echo "🌐 如需外网访问，请安装并运行: ngrok http 8000"
echo "🔄 代码修改会自动重载"

# 保持脚本运行
wait