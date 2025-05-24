# 使用Python 3.12的官方镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（添加必要的构建工具）
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 先安装依赖以提高构建缓存效率
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 调试：验证文件已正确复制
RUN ls -la && \
    echo "Checking predict_web.py exists:" && \
    [ -f "predict_web.py" ] && echo "File exists" || echo "File missing"

# 创建必要目录
RUN mkdir -p static/uploads

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0 

# 暴露端口
EXPOSE 5000

## 关键修改点 ↓
CMD ["python", "app.py"]


# 使用生产级服务器启动（推荐）
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]

# 或者使用开发服务器（仅用于测试）
# CMD ["flask", "run", "--host=0.0.0.0"]