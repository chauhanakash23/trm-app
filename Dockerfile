FROM python:3.9-slim

# 1) Set working directory
WORKDIR /app

# 2) Copy all your code in
COPY . /app

# 3) Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 4) Tell Docker which port to expose (App Engine Flex will set $PORT=8080)
EXPOSE 8080

# 5) Launch Streamlit on $PORT, 0.0.0.0 so it’s reachable
CMD ["bash", "-lc", "streamlit run app.py --server.port $PORT --server.address 0.0.0.0"]
