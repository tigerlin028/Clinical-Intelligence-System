// API 配置
const API_ENDPOINTS = {
  development: "http://localhost:8000",
  production: "https://ingestion-service-523658399118.us-central1.run.app", // 你的实际服务URL
  ngrok: "https://your-ngrok-url.ngrok.io" // 如果需要本地测试
};

export const getApiUrl = () => {
  // 在开发环境中，可以通过环境变量切换
  if (process.env.NODE_ENV === 'development') {
    return process.env.NEXT_PUBLIC_API_URL || API_ENDPOINTS.development;
  }
  
  return API_ENDPOINTS.production;
};

export const API_URL = getApiUrl();