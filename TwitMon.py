import time
import RPi.GPIO as GPIO
import sys
import Queue
import threading
from twython import TwythonStreamer

# Search Terms
TERMS = '#fml'

LED = 22

#Twitter app keys
CONSUMER_KEY = 'jnBo9oveigooTbIoISyGvgTQu'
CONSUMER_SECRET = 'hwFEiykTGIab7j4Wox1b1cW8NtdB9J4IJHnn69HbEKOOdSVorY'
ACCESS_TOKEN = '47125686-HjSO8eykmh0V7s7p6tz80ZhnBxTiqtsxQ76CvecEQ'
ACCESS_TOKEN_SECRET = 'BiQgWbLeiuAqSZryRyTKKlASmMxsfp4XOdL0yIyiohfPZ'

q = Queue.Queue()
counting = threading.Lock()
counter = 0

def blink(text):
	global counter
	print text.encode('utf-8')
	print
	counting.acquire(True)
	counter += 1
	counting.release()
	GPIO.output(LED, GPIO.HIGH)
	time.sleep(2.5)
	counting.acquire(True)
	counter -= 1
	counting.release()
	if counter == 0:
		GPIO.output(LED, GPIO.LOW)

def work():
	text = q.get()
	if(len(text)):
		blink(text)
		q.task_done()


# Callback for Twython Streamer
class TwitMonStreamer(TwythonStreamer):
	def on_success(self, data):
		if 'text' in data:
			q.put(data['text'])
			t = threading.Thread(target=work)
			t.daemon = True
			t.start()

# Setup GPIO as output
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)

#create streamer
try:
	stream = TwitMonStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	if len(sys.argv) > 1:
		stream.statuses.filter(track=sys.argv[1])
	else:
		stream.statuses.filter(track=TERMS)
except KeyboardInterrupt:
	GPIO.cleanup()

