from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
import site

import wave
import pyaudio

import time
from pygame import mixer
from pygame._sdl2 import get_num_audio_devices, get_audio_device_name#debug



location = site.getsitepackages()[0]

path = location+"\\Lib\\site-packages\\TTS\\.models.json"

model_manager = ModelManager(path)

model_path, config_path, model_item = model_manager.download_model("tts_models/en/ljspeech/tacotron2-DDC")

voc_path, voc_config_path, _ = model_manager.download_model(model_item["default_vocoder"])

synthesizer = Synthesizer(
    tts_checkpoint=model_path,
    tts_config_path=config_path,
    vocoder_checkpoint=voc_path,
    vocoder_config=voc_config_path
)

FILENAME = "speech.wav"

TESTTEXT = "See ya!"

isPlaying = False

def playAudio(file_path):
    chunk = 1024

    #open the WAV file
    wav_file = wave.open(file_path, 'rb')

    #initialize PyAudio
    audio = pyaudio.PyAudio()

    #open the audio stream
    stream = audio.open(format=audio.get_format_from_width(wav_file.getsampwidth()),
                        channels=wav_file.getnchannels(),
                        rate=wav_file.getframerate(),
                        output=True)

    #read the audio data and play it in chunks
    data = wav_file.readframes(chunk)
    while data:
        stream.write(data)
        data = wav_file.readframes(chunk)

    #cleanup
    stream.stop_stream()
    stream.close()
    audio.terminate()
    wav_file.close()

def createAudio(text):

	outputs = synthesizer.tts(text)
	synthesizer.save_wav(outputs, FILENAME)
	playThroughMicrophone(FILENAME)


def playThroughMicrophone(file_path):
    mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')
    mixer.music.load(file_path)
    mixer.music.play() #play it
    while mixer.music.get_busy():  #wait for music to finish playing
        time.sleep(1)

    mixer.quit()

def playRecordingLoop():
    global isPlaying
    
    if isPlaying:
        isPlaying = False
        playThroughMicrophone("stop.wav")


    else:
        isPlaying = True
        playThroughMicrophone("start.wav")




def debug():
	mixer.init()
	print("Intput: ", [get_audio_device_name(x, 0).decode() for x in range(get_num_audio_devices(0))])
	print("Output:", [get_audio_device_name(x, 1).decode() for x in range(get_num_audio_devices(1))])
	mixer.quit()

#playThroughMicrophone(FILENAME)
#debug()

#createAudio("Say debug to exit debug mode. Say name to change the assistants name. Say personality to change the assistants personality. Say voice to toggle the two speaking modes. Say options to hear the personality options.")