# 部署指南

## 🚀 前端部署到Vercel

### 自动部署（推荐）
1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 点击 "New Project"
3. 选择你的GitHub仓库：`Clinical-Intelligence-System`
4. 设置项目配置：
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Install Command**: `npm install`

### 环境变量（可选）
如果需要，可以在Vercel中设置环境变量：
- `NEXT_PUBLIC_API_URL`: 后端API地址（已在代码中配置）

## 🔧 后端状态
- ✅ 已部署到Google Cloud Run
- ✅ URL: `https://ingestion-service-ghib4spk7q-uc.a.run.app`
- ✅ 健康检查通过
- ✅ RAG系统集成完成

## 🧪 测试系统
部署完成后，你可以：
1. 访问Vercel提供的前端URL
2. 上传包含患者信息的音频文件
3. 验证系统功能：
   - 音频转录
   - PII脱敏
   - 患者识别
   - 医疗记录检索
   - 新医疗信息提取

## 📋 功能清单
- ✅ 音频上传和转录 (Whisper)
- ✅ PII检测和脱敏 (spaCy)
- ✅ 说话人识别
- ✅ RAG系统集成
- ✅ 患者记录检索
- ✅ 医疗信息提取
- ✅ 前后端同步
- ✅ 错误处理和状态显示

## 🔗 相关链接
- 前端仓库: GitHub上的`frontend`目录
- 后端服务: Google Cloud Run
- 测试脚本: `test_rag_system.py`