
import signal
import schedule as s
import time
import pyttsx3
import random
import RPi.GPIO as GPIO

interrupted = False

def signal_handler(signal, frame):
    # example.stop()
    print("interrupted")
    global interrupted
    interrupted = True
    stopHourly();

def job():
    print("hello working ")

def startHourly():
    print("hourly started")
    s.every(1).hours.tag("hourly").do(job)
    # s.every(10).minutes.tag("minutoy").do(job)

def stopHourly():
	s.clear("hourly")

startHourly();
signal.signal(signal.SIGINT, signal_handler)
time.sleep(20)
job()

while not interrupted:
	# sensorDataRead()
	s.run_pending()
	time.sleep(10)


# export GOOGLE_APPLICATION_CREDENTIALS="/j/Work/Teenenggr/Projects/26 - fitness moti - 1 Sept/key.json"
# export GOOGLE_APPLICATION_CREDENTIALS="/home/pi/exer_dev/fead/key.json"
