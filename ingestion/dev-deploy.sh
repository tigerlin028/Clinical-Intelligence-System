#!/bin/bash

# 开发环境快速部署 - 只更新代码，不重新安装依赖
set -e

SERVICE_NAME="ingestion-service"
REGION="us-central1"

echo "🔄 开发环境快速更新..."

# 只复制 Python 文件，使用现有的运行实例
echo "📝 更新应用代码..."

# 方法1: 使用 gcloud run services replace（如果只改了代码）
# 这会重用现有的容器镜像，只更新环境变量或配置

# 方法2: 使用 Cloud Code 或者本地开发
echo "💡 建议："
echo "1. 本地开发: uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo "2. 使用 ngrok 暴露本地服务: ngrok http 8000"
echo "3. 前端临时指向本地: http://localhost:8000 或 ngrok URL"

echo "🚀 或者运行完整部署: ./deploy.sh"