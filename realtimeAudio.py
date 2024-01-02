import speech_recognition as sr
from textToSpeech2 import *
from botCommunication import *
import quickTTS.sapi

#cd C:\Users\ephra\Downloads\Source\PersonalAssistant | python realtimeAudio.py

startKeyword = "jolene"
stopKeyword = "goodbye" 

debugStart = "debug"
isNameChange = False
isPersonalityChange = False

listenForKeywordDuration = 2
listenForSentenceDuration = 20

playWaiting = True

voice = quickTTS.sapi.Sapi()
voice.set_voice("Microsoft Zira Desktop - English (United States)") #sets to female


#debug
printDecode = True
quickSpeech = True

def main():
    recognizer = sr.Recognizer()

    recording = False
    debugMode = False

    snippets_duration = listenForKeywordDuration

    while True:
        text = None
        #recognizer = sr.Recognizer()
        text = transcribeComputerAudio(snippets_duration)

        if debugMode:
            debugMode = handle_commands(text)
        else:
            if recording:
                print(text)
                if text:
                    responce = sendMessage(text)
                    print(responce)

                    if quickSpeech:
                        speek(responce)
                    else:
                        createAudio(responce)


                if text and stopKeyword in text.lower():
                    print("Stop keyword found!")
                    #playAudio("outro.wav")
                    recording = False
                    snippets_duration = listenForKeywordDuration  #reset snippets duration to 2 seconds



            else:
                if text and startKeyword in text.lower():
                    print("Start keyword found!")
                    message = initializeCoversation()
                    print(message)
                    if quickSpeech:
                        speek(message)

                    else:
                        createAudio(message)

                    recording = True
                    snippets_duration = listenForSentenceDuration  #change snippets duration to 10 seconds after start keyword

                elif text and debugStart in text.lower():
                    debugMode = True
                    speek("Debug mode started. Say help for more info.")


                

def construct_sentence(transcripts):
    cleaned_transcripts = [t for t in transcripts if t is not None]
    return ' '.join(cleaned_transcripts)


def recordAndListen(recognizer, duration):
    with sr.Microphone() as source:
        #print("Adjusting noise ")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print(f"Recording for {duration} seconds")
        recorded_audio = recognizer.listen(source, phrase_time_limit = duration)#, timeout=duration)
        print("Done recording")

    try:
        print("Recognizing the text")
        text = recognizer.recognize_google(
                recorded_audio, 
                language="en-US"
            )

        if printDecode: print("Decoded Text : {}".format(text))
        return text

    except Exception as ex:

        print(ex)
        return None


def transcribeComputerAudio(duration = 3):
    recognizer = sr.Recognizer()

    #for index, name in enumerate(sr.Microphone.list_working_microphones()):
        #print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
    #set line 1 as default speaker, then speaker will be transfered to non default mic (index 2). mic is default actual one, cause mic can be manually set by other
    #i guess cable is default. index changes.
    with sr.Microphone(device_index=3) as source:
        print("Adjusting noise ")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print(f"Recording for {duration} seconds")
        if playWaiting and duration == listenForSentenceDuration:
            playRecordingLoop()
        recorded_audio = recognizer.listen(source, phrase_time_limit = duration)#, timeout=duration)
        if playWaiting and duration == listenForSentenceDuration:
            playRecordingLoop()
        print("Done recording")

    try:
        print("Recognizing the text")
        text = recognizer.recognize_google(
                recorded_audio, 
                language="en-US"
            )

        print("Decoded Text : {}".format(text))
        return text

    except Exception as ex:

        print(ex)
        return None



def handle_commands(text):
    global name, personality, quickSpeech, isNameChange, isPersonalityChange, startKeyword

    if text:
        if isPersonalityChange:

            for title in personalitySettings.keys():
                if title in text.lower():
                    setPersonality(title)
                    speek(f"personality is now {title}")
                    perHasChanged = True
                    break

        if isNameChange:
            setName(text)
            startKeyword = text.lower()
            speek(f"Name has been set to {text}.")
            isNameChange = False

        if "help" in text:
            playThroughMicrophone("help.wav")

        if "debug" in text:
            speek("Ending debug.")
            return False

        elif "name" in text:
            speek("Initiating name change.")
            isNameChange = True

        elif "personality" in text:
            speek("Initiating persinality change.")
            isPersonalityChange = True

        elif "voice" in text:
            if quickSpeech:
                speek("Swaping voice to realizim mode.")
                quickSpeech = False
            else:
                speek("Swaping voice to quick mode.")
                quickSpeech = True

        elif "option" in text:
            for title in personalitySettings:
                speek(title)

        elif startKeyword in text:
            speek("End debug before starting")




    return True


def speek(message):
    voice.create_recording(FILENAME, message)
    playThroughMicrophone(FILENAME)

def printImportant():
    print(name, startKeyword, "debugMode: ", debugMode)


main()


