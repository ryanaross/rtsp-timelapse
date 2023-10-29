FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN pip install opencv-python-headless

RUN apt-get update && apt-get -y install cron vim libx264-dev
RUN apt-get clean; rm -rf /var/lib/apt/lists/*

# COPY crontab /var/spool/cron/crontabs/root
# RUN chmod 0600 /var/spool/cron/crontabs/root

RUN apt-get install tzdata -y
RUN ln -sf /usr/share/zoneinfo/US/Pacific /etc/localtime
RUN echo "US/Pacific" | tee /etc/timezone && dpkg-reconfigure --frontend noninteractive tzdata

CMD ["python", "main.py"]