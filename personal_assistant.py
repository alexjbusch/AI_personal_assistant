from resemble import Resemble
import requests
import urllib.request
import json
from playsound import playsound
import speech_recognition as sr
import re
import os
import sys
import time
import os
from dotenv import dotenv_values
import logging


import get_wikipedia_text
#logging.basicConfig(level=logging.DEBUG)


current_voice_clip_number = 0



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
alextwo_id = "4d5e5d99"

voice_names = {"aiden":"aiden","willow":"ce731770", "alex to":"4d5e5d99"}


voice_uuid = alextwo_id

def text_to_speech(text, voice_uuid = voice_names["alex to"]):
    callback_uri = 'http://54.165.100.224:5000/'
    # this creates an audio clip
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

    r = requests.get(callback_uri)

    """
    try:
        r.raise_for_status()
    except HTTPException as e:
        print(e)
        raise e
    """ 
    
    c = r.content
    response = c.decode("utf-8")
    if response == "no data":
        while response == "no data":
            #print("pinging server")
            response = requests.get(callback_uri).content.decode("utf-8") 
    
    json_object = json.loads(response)
    print(json_object)
    url_of_audio_file = json_object["url"]
    print(url_of_audio_file)

    global current_voice_clip_number
    current_voice_clip_number += 1

    voice_clip = "response"+str(current_voice_clip_number)+".wav"
    file, headers = urllib.request.urlretrieve(url_of_audio_file, voice_clip)
    print(headers)
    playsound(voice_clip)
    


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



def delete_all_clips():
    response = Resemble.v2.clips.all(project_uuid, page, page_size)
    clips = response['items']
    for clip in clips:
        clip_uuid = clip["uuid"]
        response = Resemble.v2.clips.delete(project_uuid, clip_uuid)
        print(response)


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

            """
            keyword_found = re.search('[wW]illow say', query)
            if keyword_found: 
                keyword_location = keyword_found.span()[1]
                text = query[keyword_location:]
                text_to_speech(text)
            """
            if (match := re.search(r'(.+) say (.+)', query)):
                voice_name = match.group(1).lower()
                text = match.group(2)
                if voice_name in voice_names.keys():
                    #print("voice id number: "+voice_names[voice_name])
                    text_to_speech(text, voice_uuid = voice_names[voice_name])
                else:
                    print(voice_name+ " not in "+str(voice_names.keys()))


            else:
                for name in voice_names.keys():
                    bee_movie_regex = ".*?["+name[0].upper() +name[0]+ "]" + name[1:] + "\s.*\s?([Bb]ee|b) [Mm]ovie"
                    bee_movie_match = re.match(bee_movie_regex, query)


                    what_question_regex = ".*?["+name[0].upper() +name[0]+ "]" + name[1:] + " what is(.*)"
        

                    what_question_match = re.match(what_question_regex, query)
                    if what_question_match:
                        subject = what_question_match.group(1)
                        subject = re.sub('\A\s+(a|an)(\s+)', '', subject)
                        print(subject)
                        answer = get_wikipedia_text.Text(subject)
                        text_to_speech(answer, voice_uuid = voice_names[name])

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


delete_all_clips()


while True:
    speech_to_text()

"""
text_to_speech("test_1")
text_to_speech("test_2")
"""

#text_to_speech("testing one")
#text_to_speech("testing two")

def test(text):
    """
    callback_uri = 'http://54.165.100.224:5000/'
    # this creates an audio clip
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
    #print(response)


    # this gets all clips we've created
    #response = Resemble.v2.clips.all(project_uuid, page, page_size)
    #clips = response['items']
    #print(clips)

    
    response = requests.get(callback_uri).content.decode("utf-8") 
    if response == "no data":
        while response == "no data":
            print("pinging server")
            response = requests.get(callback_uri).content.decode("utf-8") 
    
    print(response)
    json_object = json.loads(response)
    url_of_audio_file = json_object["url"]
    """
    url_of_audio_file = "https://app.resemble.ai/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBCRDFtTndRPSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--4a1d350861cdb6c3017bd5e4237bd77ecdb1d54f/366ee89e-79bb41e1.wav"
    #url_of_audio_file = "https://app.resemble.ai/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBCUDFvTndRPSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--9c1d1ee163e300e66839d97cf64db81f79717743/e58161f2-cf47608f.wav"
    file = urllib.request.urlretrieve(url_of_audio_file, "response.wav")
    playsound("response.wav")

#test("")
