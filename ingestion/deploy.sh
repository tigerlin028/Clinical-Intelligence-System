#!/bin/bash

# 快速部署脚本 - 解决 ML 服务部署慢的问题
set -e

# 配置变量 - 你的实际项目配置
PROJECT_ID="clinical-intelligence-system"
SERVICE_NAME="ingestion-service"
REGION="us-central1"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 开始快速部署..."
echo "📋 项目: $PROJECT_ID"
echo "🏷️  镜像: $IMAGE_NAME"

# 确保已登录并设置项目
gcloud config set project $PROJECT_ID

# 启用必要的 API（如果还没启用）
echo "🔧 确保 API 已启用..."
gcloud services enable run.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com

# 方法1: 使用本地 Docker 构建 + 推送（比 Cloud Build 快）
echo "📦 构建 Docker 镜像（利用缓存）..."
docker build -f Dockerfile.optimized --platform linux/amd64 -t $IMAGE_NAME:latest .

echo "⬆️ 推送镜像到 Container Registry..."
docker push $IMAGE_NAME:latest

echo "🚀 部署到 Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10 \
  --set-env-vars="ENVIRONMENT=production"

echo "✅ 部署完成！"
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')
echo "🌐 服务 URL: $SERVICE_URL"
echo "🧪 测试健康检查: $SERVICE_URL/health"

# 测试服务是否正常
echo "🔍 测试服务..."
curl -f "$SERVICE_URL/health" && echo "✅ 服务正常运行！" || echo "❌ 服务可能有问题"