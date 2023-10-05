#FROM python:3.9-slim-buster
FROM python:3.9-buster 
WORKDIR /app
RUN apt-get update && \
    apt-get install -y build-essential cmake && \
    apt-get clean

RUN pip install --upgrade pip pytest cmake scikit-build setuptools fastapi uvicorn sse-starlette pydantic-settings starlette-context
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
VOLUME ["/app/data"] 
EXPOSE 5000
#setup volume
CMD [ "python", "/app/startup.py" ]


#docker run -v /Users/4838599/github/langchain-trials/aidata:/app/data -p 5001:5000 your-image-name
