# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from app.service.user_service import reset_monthly_points  # Adjust the import based on your project structure
from datetime import datetime

def reset_points():
    """
    This function resets the monthly points for all users.
    """
    try:
        # Call the service function to reset points (you need to implement this service)
        reset_monthly_points()
        print(f"Monthly points reset at {datetime.now()}")
    except Exception as e:
        print(f"Error resetting points: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Schedule the job to run at midnight on the first day of every month
    scheduler.add_job(reset_points, 'cron', day=1, hour=0, minute=0)
    scheduler.start()
