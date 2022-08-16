from resemble import Resemble
import requests
import urllib.request
from playsound import playsound
import speech_recognition as sr
import re
import os
import sys
import time
import os
from dotenv import dotenv_values

config = dotenv_values(".env")
try:
    token = config["api_key"]
except KeyError:
    print("Make sure you have a .env file in the same directory as this script with a resmeble.ai api key!")

Resemble.api_key(token)

page = 1
page_size = 10

project_uuid = "b96e7ffc"

willow_id = "ce731770"
aiden_id = "aiden"

voice_names = {"aiden":"","willow":"ce731770"}


voice_uuid = willow_id


def create_voice_clip(text):
    callback_uri = 'https://example.com/callback/resemble-clip'
    
    # this is the clip we want to create
    response = Resemble.v2.clips.create_async(
      project_uuid,
      voice_uuid,
      callback_uri,
      text,
      title=None,
      sample_rate=None,
      output_format=None,
      precision=None,
      include_timestamps=None,
      is_public=None,
      is_archived=None
    )
    #this is in case I don't want to use clips.all
    clip = response['item']['uuid']


def play_voice_clip():
    response = Resemble.v2.clips.all(project_uuid, page, page_size)
    clips = response['items']
    
    print(clips)

    url = clips[0]['audio_src']

    file = urllib.request.urlretrieve(url, "response.wav")
    print(file)
    playsound('response.wav')



def text_to_speech(text):
    create_voice_clip(text)
    print("Created voice clip!")

    response = os.popen("py play_voice_clip.py")
    sys.exit()
    print(response)


def play_prerecorded_clip(voice_name,clip_name):
    try:
        playsound(voice_name+'_clips\\'+clip_name+'.wav')
    except Exception as e:
        pass
        playsound(voice_name+'_clips\\'+clip_name+'.mp3')


def play_non_voice_clip(clip_name):
    try:
        playsound('non_voice_clips\\'+clip_name+'.wav')
    except Exception as e:
        playsound('non_voice_clips\\'+clip_name+'.mp3')




def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio)
            print(query)
            keyword_found = re.search('[wW]illow say', query)
            print(keyword_found)
            if keyword_found: 
                keyword_location = keyword_found.span()[1]
                text = query[keyword_location:]
                text_to_speech(text)

            else:
                for name in voice_names.keys():
                    bee_movie_regex = ".*?["+name[0].upper() +name[0]+ "]" + name[1:] + "\s.*\s?([Bb]ee|b) [Mm]ovie"
                    bee_movie_match = re.match(bee_movie_regex, query)

                    introduction_regex = ".*?["+name[0].upper() +name[0]+ "]" + name[1:] + "\s.*\s?introduce[d]*"
                    introduction_match = re.match(introduction_regex, query)


                    

                    
                    if bee_movie_match:
                        play_prerecorded_clip(name,"bee_movie_script")
                        
                    elif introduction_match:
                        print("introduction")
                        play_prerecorded_clip(name,"introduction")
                
                seinfeld_regex = ".*?what[']*s the deal with.*?"
                seinfeld_match = re.match(seinfeld_regex, query)
                if seinfeld_match:
                    play_non_voice_clip("seinfeld")

                despacito_regex = ".*?sad.*?[Dd]espacito.*?"
                despacito_match = re.match(despacito_regex, query)
                if despacito_match:
                    play_non_voice_clip("despacito")

                law_and_order_regex = ".*?[Jj]ustice.*?"
                law_and_order_match = re.match(law_and_order_regex, query)
                if law_and_order_match:
                    play_non_voice_clip("law_and_order")

        except sr.UnknownValueError:
            print("Could not understand audio")


while True:
    speech_to_text()



