FROM python:3.10-slim

RUN apt-get update && apt-get install -y wget unzip

# Download Chrome binary
RUN wget -O /tmp/chrome.zip https://storage.googleapis.com/chrome-for-testing-public/139.0.7258.66/linux64/chrome-linux64.zip \
    && unzip /tmp/chrome.zip -d /tmp/ \
    && mv /tmp/chrome-linux64 /opt/chrome \
    && ln -s /opt/chrome/chrome /usr/local/bin/chrome \
    && rm /tmp/chrome.zip

# Download ChromeDriver
RUN wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/139.0.7258.66/linux64/chromedriver-linux64.zip \
    && unzip /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm /tmp/chromedriver.zip

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python" ]
