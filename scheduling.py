import schedule
import time
import subprocess

def job():
    subprocess.run(["/bin/bash", "-c", "source venv/bin/activate && python scrapping.py"])

    
schedule.every().sunday.at("00:00").do(job) 

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
