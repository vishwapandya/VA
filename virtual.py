import pyttsx3
import speech_recognition as sr
import datetime as dt
import os
import cv2
import random
from requests import get 
import wikipedia
import webbrowser
import pywhatkit
import smtplib
import sys
import time
############
import requests 
from bs4 import BeautifulSoup
#################
import pywikihow
from pywikihow import search_wikihow
from pywikihow import WikiHow

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1].id)
engine.setProperty('voice',voices[0].id)

#text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=1, phrase_time_limit=7)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User Said: {query}")
    
    except Exception as e:
        speak("say that again please...")
        return take_command()
    return query

#voice to text
def wish():
    hour = int(dt.datetime.now().hour)

    if hour>=0 and hour<=12:
        speak("Good Morning")
    elif hour>=12 and hour<=16:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    #speak("I am Arva, please tell me how can I help you?")
    #gender = speak("Do you want to talk to Arva or Vishti?") 
    

def sendEmail(to,content):
    smtpserver = smtplib.SMTP('smtp.gmail.com',587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login("your email id","password")
    smtpserver.sendmail('your email id',to,content)
    smtpserver.close()

def remove(str):
    return str.replace(" ", "")

def search_wikihow(query, max_results = 10, lang="en"):
    return list(WikiHow.search(query,max_results,lang))

if __name__ == "__main__":
        #speak("Hello I am Jarvis")
        #take_command()
        wish()

        while True:
            query = take_command().lower()

            if "yes" in query:
                engine.setProperty('voice',voices[1].id)

            if "open notepad" in query:
                npath = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Accessories\\notepad"
                os.startfile(npath)

            elif "open command prompt" in query:
                os.system("start cmd")

            elif "open camera" in query:
                number = random.randint(0,100)
                #initializing cv2
                videoCaptureObject = cv2.VideoCapture(0)
                result = True
                while(result):
                    #read the frames while the camera is on- it will return a boolean value 
                    ret,frame = videoCaptureObject.read()
                    #cv2.imwrite() method is used to save an image to any storage device
                    img_name = "img"+str(number)+".png"
                    cv2.imwrite(img_name, frame)
                    start_time = time.time
                    result = False
                print("Snapshot taken")
                # releases the camera
                videoCaptureObject.release()
                #closes all the window that might be opened while this process
                cv2.destroyAllWindows()
                
            elif "play music" in query:
                music_dir = "D:\\songs"
                songs = os.listdir(music_dir)
                #rd = random.choice(songs)
                for song in songs:
                    if song.endswith('.mp3'):
                        os.startfile(os.path.join(music_dir,song))

            elif "ip address" in query:
                ip = get('https://api.ipify.org').text
                speak(f"Your IP address is {ip}")

            elif "wikipedia" in query:
                speak("Searching Wikipedia...")
                query = query.replace("wikipedia","")
                results = wikipedia.summary(query,sentences=5)
                speak("According to wikipedia,")
                speak(results)
                #print(results)

            elif "open youtube" in query:
                webbrowser.open("www.youtube.com")

            elif "open facebook" in query:
                webbrowser.open("www.facebook.com")

            elif "open google" in query:
                speak("What should I search on google for you?")
                cm = take_command().lower()
                webbrowser.open(f"{cm}")
    ###################################################################################3
            elif "send message" in query:
                speak("ok, please tell me the mobile number")
                num = '+91'
                num = num + take_command()
                #audio = r.listen(source, timeout=1, phrase_time_limit=15)
                speak(f"Do you confirm the number is {num}")
                userResponse = take_command().lower()
                if userResponse == "yes":
                    now = dt.datetime.now()
                    hour = now.hour 
                    minute = now.minute + 3 
                    pywhatkit.sendwhatmsg(num,"hello how are you",hour,minute)
                    speak("Meassage Sent")
                    sys.exit()
                else:
                    speak("Ok, I will not send the message")
                    sys.exit()
################################################################################3
            elif "play a song on youtube" in query:
                speak("which song would you like me to play?")
                song = take_command()
                speak(f'playing {song} for you')
                pywhatkit.playonyt(song)
                sys.exit()
##############################################################################33
            elif "send email" in query:
                try:
                    speak("Whom should I send?")
                    id = take_command().lower() + '@gmail.com'
                    to = remove(id)
                    print(to)
                    speak("Do you want to send email to " + to)
                    userResponse = take_command().lower()
                    print(userResponse)
                    if userResponse == "yes":
                        speak("What should I send?")
                        content = take_command().lower()
                        sendEmail(to, content)
                        speak("Email has been sent to " + to)
                    else:
                        speak("Okay... So i'll not send any email")
                except Exception as e:
                    print(e)
            ################################################################

            elif "temperature" in query:
                search = "Temperature in Mumbai"
                url = f'https://www.google.com/search?q={search}'
                r = requests.get(url)
                data = BeautifulSoup(r.text,"html.parser")
                temp = data.find("div",class_="BNeawe").text
                speak(f"Current {search} is {temp}")

            ###################################################################

            elif "activate search mode" in query:
                speak("Plase tell me what do you want to search")
                how = take_command()
                max_results=1
                how_to = search_wikihow(how,max_results)
                assert len(how_to) == 1
                how_to[0].print()
                speak(how_to[0].summary)

            ######################################################################

            elif "no" in query:
                speak("Thank you for using me, have a great day ahead...")                
                sys.exit()

            speak("Do you have any other work?")
