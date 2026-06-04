FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
ENV DB_URL=postgresql://aidas_user:aidas_password@localhost:5432/aidas_db
WORKDIR /app

#promtail 수집용 로그 디렉토리 생성
RUN mkdir -p /var/log/aidas

# 의존성 설치
COPY services/web/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 코드 복사
COPY services/web/ .

# 컨테이너 포트 노출
EXPOSE 8000

# uvicorn 대신 python -m uvicorn 사용 (안정적임)
ENV PYTHONPATH=/app
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
