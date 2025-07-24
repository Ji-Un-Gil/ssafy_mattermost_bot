import sys
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from datetime import datetime
import pytz

# 스크립트가 시작될 때 즉시 이 메시지를 출력하여 실행 여부를 확인합니다.
print("main.py script started successfully!", file=sys.stderr)


def send_mattermost_message(webhook_url, message):
    print(f"Sending message to Mattermost: {message}", file=sys.stderr)
    payload = {'text': message}
    response = requests.post(webhook_url, json=payload)
    print(f"Response status code: {response.status_code}", file=sys.stderr)
    if response.status_code == 200:
        print('Message sent successfully to Mattermost!', file=sys.stderr)
    else:
        print('Failed to send message to Mattermost.', file=sys.stderr)


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
    print("Scheduler started. Waiting for scheduled times...", file=sys.stderr) # 이 메시지는 스케줄러 시작 직후 출력됩니다.


webhook_url = 'https://meeting.ssafy.com/hooks/s9kdaz8mp3ghxx5a8qgzzrfhha'
messages = ['@all 입실 체크 하세요!', '@all 퇴실 체크 하세요!']
times = [datetime.strptime(time, '%H:%M') for time in ['08:30', '17:31']]

schedule_multiple_notifications(webhook_url, messages, times)
