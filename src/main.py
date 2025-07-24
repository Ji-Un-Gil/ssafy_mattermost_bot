from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from datetime import datetime


def send_mattermost_message(webhook_url, message):
    payload = {'text': message}
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        print('Message sent successfully to Mattermost!')
    else:
        print('Failed to send message to Mattermost.')


def schedule_multiple_notifications(webhook_url, messages, times):
    scheduler = BlockingScheduler()

    for i, message in enumerate(messages):
        time = times[i]
        scheduler.add_job(send_mattermost_message, 'cron', day_of_week='mon-fri', hour=time.hour, minute=time.minute, args=[webhook_url, message])

    scheduler.start()


webhook_url = 'https://meeting.ssafy.com/hooks/s9kdaz8mp3ghxx5a8qgzzrfhha'
messages = ['@all 입실 체크 하세요!', '@all 퇴실 체크 하세요!']
times = [datetime.strptime(time, '%H:%M') for time in ['08:30', '14:56']]

schedule_multiple_notifications(webhook_url, messages, times)