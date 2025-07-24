from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from datetime import datetime
import pytz
import os


def send_mattermost_message(webhook_url, message):
    payload = {'text': message}
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        print('Message sent successfully to Mattermost!')
    else:
        print('Failed to send message to Mattermost.')


def schedule_multiple_notifications(webhook_url, messages, times):
    scheduler = BlockingScheduler(timezone=pytz.timezone("Asia/Seoul"))  # pytz 타임존 명시

    for i, message in enumerate(messages):
        time = times[i]
        scheduler.add_job(
            send_mattermost_message,
            'cron',
            day_of_week='mon-fri',
            hour=time.hour,
            minute=time.minute,
            args=[webhook_url, message]
        )

    scheduler.start()


webhook_url = os.environ.get('MATTERMOST_WEBHOOK_URL')
if not webhook_url:
    raise ValueError("MATTERMOST_WEBHOOK_URL environment variable is not set.")
messages = ['@all 입실 체크 하세요!', '@all 퇴실 체크 하세요!']
times = [datetime.strptime(time, '%H:%M') for time in ['08:30', '22:11']]

schedule_multiple_notifications(webhook_url, messages, times)