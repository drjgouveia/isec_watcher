FROM python:3.7

ENV WDM_LOG = 0
ENV PYTHONUNBUFFERED=1
ENV SHELL=/bin/bash
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get update && apt-get -y install cron nano google-chrome-stable
WORKDIR /app

COPY crontab /etc/cron.d/crontab
COPY . /app/
RUN pip3 install -r requirements.txt
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

# run crond as main process of container
CMD ["cron", "-f"]