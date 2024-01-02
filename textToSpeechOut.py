import speech_recognition as sr 


def transcribeComputerAudio(duration = 3):
    recognizer = sr.Recognizer()

    for index, name in enumerate(sr.Microphone.list_working_microphones()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
    #set line 1 as default speaker, then speaker will be transfered to non default mic (index 2). mic is default actual one, cause mic can be manually set by other
    #i guess cable is default
    with sr.Microphone(device_index=2) as source:
        print("Adjusting noise ")
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

        print("Decoded Text : {}".format(text))
        return text

    except Exception as ex:

        print(ex)
        return None


print(transcribeComputerAudio())