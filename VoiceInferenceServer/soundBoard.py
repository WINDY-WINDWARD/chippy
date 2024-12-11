import os
from piper.voice import PiperVoice
import time
import wave
import pyaudio
from contextlib import contextmanager
from ctypes import CFUNCTYPE, c_char_p, c_int, cdll

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)

MODEL= "en_US-ryan-high.onnx"
PATH = "piper/models/"

def check_path():
    if not os.path.exists(PATH + MODEL):
        print("Critical Error: Could not find Voice model...")
        return RuntimeError("Critical Error: Could not find Voice model...")
    
class SoundBoard:

    def __init__(self):
        try:
            check_path()
        except Exception as e:
            print("Error: " + str(e))
            return
        self.piper = PiperVoice.load(PATH + MODEL)
        with noalsaerr():
            self.pyaud = pyaudio.PyAudio()


    def speak(self, text: str) -> bool:
        """
        Synthesizes and plays the given text using the PiperVoice model and PyAudio.
        
        Args:
            text (str): The text to synthesize and play.
        
        Returns:
            bool: True if successful, False if an error occurred.
        """
        try:
            # track time of execution
            start_time = time.time_ns()
            file = wave.open("tts_generated/temp.wav", "wb")
            self.piper.synthesize(text, file, length_scale=1.2)
            file.close()

            end_time = time.time_ns()
            print("Execution time ms: " + str((end_time - start_time)/1000000))
            # # play the bytes
            # f= wave.open("tts_generated/temp.wav", "rb")
            # stream = self.pyaud.open(format=self.pyaud.get_format_from_width(f.getsampwidth()),
            #                 channels=f.getnchannels(),
            #                 rate=f.getframerate(),
            #                 output=True)
            
            
            # while len(data := f.readframes(512)):
            #     stream.write(data)
            
            # stream.close()
            # self.pyaud.terminate()
            return True
        except Exception as e:
            print("Error: " + str(e))
            return False
        
    
        




if __name__ == "__main__":
    # check_path()
    # print("Voice Model: " + MODEL)


    # piper = PiperVoice.load(PATH + MODEL)

    # audio = piper.synthesize_stream_raw("Hi There, what the fuck is happening")

    # for audio_bytes in audio:
    #     piper.config.sample_rate
    #     print(audio_bytes)

    # # play the bytes
    # import pyaudio
    # p = pyaudio.PyAudio()

    # stream = p.open(format=pyaudio.paInt16,
    #                 channels=1,
    #                 rate=22050,
    #                 output=True)

    # stream.write(audio_bytes)

    # stream.stop_stream()
    # stream.close()

    # p.terminate()

    sb = SoundBoard()
    sb.speak("So, I was at the mall the other day, and I saw this really cool shirt. I was like, 'Oh man, I have to get that.' So, I went to the store, and I tried it on. And let me tell you, it was love at first sight. I mean, it was like the shirt was made for me. I was like, 'This is the one.' So, I bought it, and I've been wearing it ever since. It's just so comfortable, and it looks so good. I mean, I've gotten so many compliments on it. It's just one of those things that makes you feel good when you wear it. You know?")
