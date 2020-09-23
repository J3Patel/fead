from google.cloud import firestore
import signal
import schedule as s
import time
import pyttsx3
import random

engine = pyttsx3.init()
interrupted = False
engine.say("Hello")
engine.runAndWait()

def turnMonitorOff():
	engine.say("please complete the task to start monitor")
	engine.runAndWait()
	print("Monitor turn off")

def turnMonitorOn():
	print("Monitor turn on")

def callback(collectionSnap , documentChange, readTime):
    for doc in documentChange:
        if doc.document.to_dict()['isDone'] == True:
            print("Task Completed")
            turnMonitorOn()
        else:
        	turnMonitorOff()

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
    # s.every().hours.tag("hourly").do(job)
    s.every(1).minutes.tag("minutoy").do(job)

def stopHourly():
	s.clear("hourly")

startHourly();
listenToFirebase();
signal.signal(signal.SIGINT, signal_handler)


while not interrupted:
	# sensorDataRead()
	s.run_pending()
	time.sleep(10)


# export GOOGLE_APPLICATION_CREDENTIALS="/j/Work/Teenenggr/Projects/26 - fitness moti - 1 Sept/key.json"
