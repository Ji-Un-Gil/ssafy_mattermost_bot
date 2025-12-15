from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from datetime import datetime, date
import pytz
import os

# 제외할 날짜 리스트 (공휴일 등)
HOLIDAYS = [
    date(2025, 10, 3),  # 개천절
    date(2025, 10, 6),  # 추석 연휴
    date(2025, 10, 7),  # 추석
    date(2025, 10, 8),  # 추석 연휴
    date(2025, 10, 9),  # 한글날
    date(2025, 12, 16),  # 잡페어
    date(2025, 12, 17),  # 잡페어
    date(2025, 12, 25),  # 크리스마스
    date(2025, 12, 29),  # 방학
    date(2025, 12, 30),  # 방학
    date(2025, 12, 31),  # 방학
    date(2026, 1, 1),  # 방학
    date(2026, 1, 2),  # 방학
]

# 서울 시간대 객체
KST = pytz.timezone("Asia/Seoul")

def send_mattermost_message(webhook_url, message):
    """실제로 Mattermost에 메시지를 전송하는 함수"""
    payload = {'text': message}
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()  # 2xx 응답 코드가 아니면 예외 발생
        print(f"[{datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S')}] Message sent successfully to Mattermost!")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message to Mattermost: {e}")

def scheduled_job(webhook_url, message, holidays):
    """스케줄러에 의해 실행될 함수. 공휴일인지 확인 후 메시지를 보냅니다."""
    today = datetime.now(KST).date()
    if today not in holidays:
        send_mattermost_message(webhook_url, message)
    else:
        print(f"[{datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S')}] Skipping notification on {today} as it is a designated holiday.")

def schedule_multiple_notifications(webhook_url, messages, times, holidays):
    """여러 개의 알림을 스케줄링하는 함수"""
    scheduler = BlockingScheduler(timezone=KST)

    for i, message in enumerate(messages):
        time = times[i]
        scheduler.add_job(
            scheduled_job,
            'cron',
            day_of_week='mon-fri',
            hour=time.hour,
            minute=time.minute,
            args=[webhook_url, message, holidays]
        )
        print(f"Scheduled: '{message}' at {time.strftime('%H:%M')} on weekdays, excluding holidays.")

    print("Scheduler started... Press Ctrl+C to exit.")
    scheduler.start()


# --- 메인 실행 부분 ---
if __name__ == "__main__":
    webhook_url = os.environ.get('MATTERMOST_WEBHOOK_URL')
    if not webhook_url:
        raise ValueError("MATTERMOST_WEBHOOK_URL environment variable is not set.")
    
    messages = [
        '''@all 
# :check_0859_pyn: 입실 체크 하세요!''', 
        '''@all 
# :out_check: 퇴실 체크 하세요!'''
        ]
    times = [datetime.strptime(time, '%H:%M').time() for time in ['08:30', '18:00']]

    schedule_multiple_notifications(webhook_url, messages, times, HOLIDAYS)