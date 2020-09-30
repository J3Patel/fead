from google.cloud import firestore
import signal
import schedule as s
import time
import pyttsx3
import random
import RPi.GPIO as GPIO

interrupted = False

def turnMonitorOff():
	engine = pyttsx3.init()
	engine.setProperty('rate', 180)
	engine.say("please complete the task to turn on display")
	engine.runAndWait()
	GPIO.output(14, GPIO.HIGH)
	engine.stop()
	print("Monitor turn off")

def turnMonitorOn():
	GPIO.output(14, GPIO.LOW)
	engine = pyttsx3.init()
	engine.setProperty('rate', 180)
	engine.say("Task completed, Turning on the display")
	engine.runAndWait()
	engine.stop()
	print("Monitor turn on")

def callback(collectionSnap , documentChange, readTime):
	print("callback")
	for doc in documentChange:
		if not doc.document.to_dict()['isDone']:
			print("Taks uncompleete")
			turnMonitorOff()
		else:
			print("Task Completed")
			turnMonitorOn()

def listenToFirebase():
    db = firestore.Client()
    db.collection(u'tasks').document('me').on_snapshot(callback)

def signal_handler(signal, frame):
    # example.stop()
    print("interrupted")
    global interrupted
    interrupted = True
    stopHourly();

def addNewTask():
	db = firestore.Client()
	r = random.randint(0,10)
	data = {
	'count': 10,
	'id': str(r),
	'isDone': False
	}
	doc_ref = db.collection(u'tasks').document(u'me')
	doc_ref.set(data)

def job():
    addNewTask()
    print("hello working ")

def startHourly():
    print("hourly started")
    s.every(1).hours.tag("hourly").do(job)

def stopHourly():
	s.clear("hourly")

startHourly();
listenToFirebase();
signal.signal(signal.SIGINT, signal_handler)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
GPIO.output(14, GPIO.HIGH)

while not interrupted:
	# sensorDataRead()
	s.run_pending()
	time.sleep(10)


# export GOOGLE_APPLICATION_CREDENTIALS="/j/Work/Teenenggr/Projects/26 - fitness moti - 1 Sept/key.json"
# export GOOGLE_APPLICATION_CREDENTIALS="/home/pi/exer_dev/fead/key.json"
