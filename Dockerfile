FROM python:3.12-slim

# 设置环境变量，确保 Python 输出直接打印到控制台，且不生成 pyc 文件
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 创建非 root 用户并设置家目录
RUN addgroup --system appgroup && adduser --system --group appuser

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 预先创建 instance 目录并设置所有权为非 root 用户
RUN mkdir -p /app/instance && chown -R appuser:appgroup /app

# 切换到非 root 用户
USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "dzweb:create_app()"]
