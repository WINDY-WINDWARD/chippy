import logging
import pathlib as Path

# load log level from logger.json
import json
log_lvl=""
with open('logger.json') as json_file:
    data = json.load(json_file)
    log_lvl = data['logLevel']
    if log_lvl == "info":
        log_lvl = logging.INFO
    elif log_lvl == "debug":
        log_lvl = logging.DEBUG
    elif log_lvl == "warning":
        log_lvl = logging.WARNING
    elif log_lvl == "error":
        log_lvl = logging.ERROR
    elif log_lvl == "critical":
        log_lvl = logging.CRITICAL
    else:
        log_lvl = logging.CRITICAL

# set log path to parent directory
log_path = str(Path.Path(__file__).resolve().parent) + "/EmotionEngine.log"
print(log_path)
logging.basicConfig(filename=log_path, level=log_lvl, format='%(asctime)s %(levelname)s %(threadName)-10s %(module)s %(message)s')

import threading
from displayEngine import get_device
import Emotions.blinking.blink as blink
import Emotions.starEyes.starEyes as starEyes
from Emotions.lookLeft.lookLeft import lookLeft_hold
from Emotions.lookRight.lookRight import lookRight_hold
from Emotions.shy.shy import shy_hold
from Emotions.anger.anger import anger_hold
import Emotions.utilFunctions.displayFunctions as displayFunctions
from random import randint
import time
import pickle


class BlinkThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(BlinkThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self._lock = threading.Lock()

    def stop(self):
        logging.debug("BlinkThread stop %s", self._lock.locked())
        while self._lock.locked():
            logging.debug("wait for lock to be released")
            time.sleep(0.001)  # Wait a bit for the lock to be released
        self._stop_event.set()

    def stopped(self):
        logging.debug("BlinkThread check stopped %s", self._stop_event.is_set())
        return self._stop_event.is_set()
    
    def lock(self):
        logging.debug("BlinkThread lock")
        self._lock.acquire()

    def unlock(self):
        logging.debug("BlinkThread unlock")
        if self._lock.locked():
            self._lock.release()

    def run(self):
        while not self.stopped():
            try:
                blink.eyeOpen(display,randint(4,7))
                if self.stopped():
                    return
                self.lock()
                blink.triggerBlink(display)
            finally:
                self.unlock()



def EmotionEngine(display):
    global shared_data
    emotion = shared_data["emotion"]
    if emotion == "happy":
        starEyes.main(display,2)
    elif emotion == "sad":
        lookLeft_hold(display,2)
    elif emotion == "love":
        lookRight_hold(display,2)
    elif emotion == "anger":
        anger_hold(display,6)
    elif emotion == "fear":
        shy_hold(display,2)
    else:
        logging.error("emotion not found")
        display.Text_display("emotion not found")
        return
    shared_data["emotion"] = None

class EmotionPredictor:
    def __init__(self):
        self.svm_model = pickle.load(open("./ML_model/svm_model.sav", 'rb'))
        self.vectorizer = pickle.load(open("./ML_model/vectorizer.sav", 'rb'))
        self.emotions = ["neutral","happy", "sad", "love", "anger","fear"]

    def predict(self, text):
        logging.debug("EmotionPredictor predict"+ str(text))
        text = self.vectorizer.transform([str(text)])
        prediction = self.svm_model.predict(text)
        logging.debug("EmotionPredictor prediction: %s", prediction)
        return self.emotions[prediction[0]]
    
if __name__ == "__main__":
    # start blinking thread
    device = get_device()
    display = displayFunctions.DisplayFunctions(device)
    emotionPredictor = EmotionPredictor()
    blinkThread = BlinkThread(name="blinkThread")
    blinkThread.start()
    shared_data = {"emotion": None}
    # start emotion engine
    while True:
        text = input("Enter text: ")
        if text == "stop":
            blinkThread.stop()
            blinkThread.join()
            break
        emotion = emotionPredictor.predict(text)
        logging.debug("emotion: %s", emotion)
        # stop blinking thread
        blinkThread.stop()
        blinkThread.join()
        shared_data["emotion"] = emotion
        EmotionEngine(display)
        blinkThread = BlinkThread(name="blinkThread")
        blinkThread.start()