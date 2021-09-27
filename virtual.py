from math import fabs
from posixpath import pathsep
import pyttsx3
import speech_recognition as sr
import datetime as dt
import os
import cv2 #pip install opencv-python
import random
from requests import get 
import wikipedia
import webbrowser
import pywhatkit
import smtplib
import sys
import time
import requests 
from bs4 import BeautifulSoup #pip install bs4
import winsound #pip install Playsound
from tkinter import * #inbuilt
import psutil #pip install psutil 
import speedtest #pip install speedtest-cli
import pyautogui #pip install pyautogui
import winreg #inbuilt
import shlex #inbuilt
from googletrans import Translator  #pip install googletrans #if any error pip install googletrans==4.0.0-rc1
from pytube import YouTube #pip install pytube3  #if any error python -m pip install --upgrade pytube
import pywikihow #pip install pywikihow
from pywikihow import search_wikihow
from pywikihow import WikiHow

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1].id)heel
engine.setProperty('voice',voices[1].id)
engine.setProperty('rate',175)

def try_finding_chrome_path():
    result = None
    if winreg:
        for subkey in ['ChromeHTML\\shell\\open\\command','Applications\\crhome.exe\\shell\\open\\command']:
            try: result = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, subkey)
            except WindowsError: pass
            if result is not None:
                result_split = shlex.split(result, False, True)
                result = result_split[0] if result_split else None
                if os.path.isfile(result):
                    break
                result = None

    else:
        expected = "google-chrome" + (".exe" if os.time=="nt" else "")
        for parent in os.environ.get('PATH','').split(os.pathsep):
            path = os.path.join(parent,expected)
            if os.path.isfile(path):
                result = path
                break
    return result

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 3
        audio = r.listen(source, timeout=5, phrase_time_limit=7)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User Said: {query}")
    
    except Exception as e:
        speak("say that again please...")
        return take_command()
    return query

def selectGender():
    gender = take_command()
    #print(gender)
    if gender=="arva" or gender=="arwa" or gender=="Arwa" or gender=="Arva" or gender=="are vah" or gender=="are wah" or gender=="Are vah" or gender=="Are wah":
        engine.setProperty('voice',voices[0].id)
        speak("I am Arva, how may I assist you?")
    elif gender=="vishti" or gender=="Vishti" or gender=="misty" or gender=="Misty" or gender=="srishti" or gender=="drishti":
        engine.setProperty('voice',voices[1].id)
        speak("I am Vishti, how may I assist you?")
    else:
        speak("Can you please repeat")
        return selectGender()

def checkBattery():
    battery = psutil.sensors_battery()
    percentage = battery.percent
    return percentage

def wish():
    hour = int(dt.datetime.now().hour)

    battery = checkBattery()
    if battery>15 and battery<35:
        speak("REMINDER... Battery low, connect the charger")

    elif battery<=15 and battery>2:
        speak("Less than 15 percent battery remaining, connect the charger or the system will shut down")
        
    elif battery<=2:
        speak("Sleep mode on, less than 2 percent battery remaining")
        sys.exit()

    if hour>=0 and hour<=12:
        speak("Good Morning")
    elif hour>=12 and hour<=16:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    #speak("I am Arva, please tell me how can I help you?")
    #speak("Do you want to talk to Arva or Vishti?") 
    speak("Would you like to talk to Arva or Vishti?")
    selectGender()

#turn on "Less secure app access" from the settings of gmail
def sendEmail(id,pwd,to,content):
    smtpserver = smtplib.SMTP('smtp.gmail.com',587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(id,pwd)
    smtpserver.sendmail(id,to,content)
    smtpserver.close()

def add(a,b):
    return a+b

def sub(a,b):
    return a-b

def mul(a,b):
    return a*b

def remove(str):
    return str.replace(" ", "")

def translateSentence():
    isAvailable = False
    speak("In which language do you want to translate?")
    lang = take_command().lower()
    speak("What do you want to translate?")
    text = take_command().lower()
    text = text.replace('translate','')
    translator = Translator()
    if "french" in lang:
        l = "fr"
        isAvailable = True
    elif "german" in lang:
        l = "de"
        isAvailable = True
    elif "spanish" in lang:
        l = "es"
        isAvailable = True
    elif "hindi" in lang:
        l = "hi"
        isAvailable = True
    if isAvailable==True:
        translated = translator.translate(text,src='en',dest=l)
        return speak(f"The translation for {text} is: {translated.text}")
    else:
        return speak("Sorry, This language translation is currently not available!")

def alarm(timeforalarm):
    time = str(dt.datetime.now().strptime(timeforalarm,'%I:%M %p'))
    #print(time)
    time = time[11:-3]
    hour = time[:2]
    hour = int(hour)
    minute = time[3:5]
    minute = int(minute)
    speak(f"Done, alarm is set for {timeforalarm}")

    while True:
        if hour == dt.datetime.now().hour:
            if minute == dt.datetime.now().minute:
                #print("Alarm is Running")
                #speak("GET UP!!!!")
                winsound.PlaySound('abc',winsound.SND_ALIAS)

            elif minute < dt.datetime.now().minute:
                sys.exit()
                break

def startGame():


    boardWidth = 30
    boardHeight = 30
    tilesize = 10

    class Snake():

        def __init__(self):

            self.snakeX = [20, 20, 20]
            self.snakeY = [20, 21, 22]
            self.snakeLength = 3
            self.key = "w"
            self.points = 0

        def move(self): # move and change direction with wasd

            for i in range(self.snakeLength - 1, 0, -1):
                    self.snakeX[i] = self.snakeX[i-1]
                    self.snakeY[i] = self.snakeY[i-1]

            if self.key == "w":
                self.snakeY[0] = self.snakeY[0] - 1

            elif self.key == "s":
                self.snakeY[0] = self.snakeY[0] + 1

            elif self.key == "a":
                self.snakeX[0] = self.snakeX[0] - 1

            elif self.key == "d":
                self.snakeX[0] = self.snakeX[0] + 1

            self.eatApple()

        def eatApple(self):

            if self.snakeX[0] == apple.getAppleX() and self.snakeY[0] == apple.getAppleY():

                self.snakeLength = self.snakeLength + 1

                x = self.snakeX[len(self.snakeX)-1] # Snake grows
                y = self.snakeY[len(self.snakeY) - 1]
                self.snakeX.append(x+1)
                self.snakeY.append(y)

                self.points = self.points + 1
                apple.createNewApple()

        def checkGameOver(self):

            for i in range(1, self.snakeLength, 1):

                if self.snakeY[0] == self.snakeY[i] and self.snakeX[0] == self.snakeX[i]:
                    return True # Snake eat itself

            if self.snakeX[0] < 1 or self.snakeX[0] >= boardWidth-1 or self.snakeY[0] < 1 or self.snakeY[0] >= boardHeight-1:
                return True # Snake out of Boundary

            return False

        def getKey(self, event):

            if event.char == "w" or event.char == "d" or event.char == "s" or event.char == "a" or event.char == " ":
                self.key = event.char

        def getSnakeX(self, index):
            return self.snakeX[index]

        def getSnakeY(self, index):
            return self.snakeY[index]

        def getSnakeLength(self):
            return self.snakeLength

        def getPoints(self):
            return self.points


    class Apple:

        def __init__(self):
            self.appleX = random.randint(1, boardWidth - 2)
            self.appleY = random.randint(1, boardHeight - 2)

        def getAppleX(self):
            return self.appleX

        def getAppleY(self):
            return self.appleY

        def createNewApple(self):
            self.appleX = random.randint(1, boardWidth - 2)
            self.appleY = random.randint(1, boardHeight - 2)

    class GameLoop:

        def repaint(self):

            canvas.after(200, self.repaint)
            canvas.delete(ALL)

            if snake.checkGameOver() == False:

                snake.move()
                snake.checkGameOver()

                canvas.create_rectangle(snake.getSnakeX(0) * tilesize, snake.getSnakeY(0) * tilesize,
                                        snake.getSnakeX(0) * tilesize + tilesize,
                                        snake.getSnakeY(0) * tilesize + tilesize, fill="red")  # Head

                for i in range(1, snake.getSnakeLength(), 1):
                    canvas.create_rectangle(snake.getSnakeX(i) * tilesize, snake.getSnakeY(i) * tilesize,
                                            snake.getSnakeX(i) * tilesize + tilesize,
                                            snake.getSnakeY(i) * tilesize + tilesize, fill="blue")  # Body

                canvas.create_rectangle(apple.getAppleX() * tilesize, apple.getAppleY() * tilesize,
                                        apple.getAppleX() * tilesize + tilesize,
                                        apple.getAppleY() * tilesize + tilesize, fill="green")  # Apple

            else:   # GameOver Message
                canvas.delete(ALL)
                canvas.create_text(150, 100, fill="darkblue", font="Times 20 italic bold", text="GameOver!")
                canvas.create_text(150, 150, fill="darkblue", font="Times 20 italic bold", text="Points:" + str(snake.getPoints()))

    snake = Snake()
    apple = Apple()
    root = Tk()

    canvas = Canvas(root, width=300, height=300)
    canvas.configure(background="yellow")
    canvas.pack()

    gameLoop = GameLoop()
    gameLoop.repaint()

    root.title("Snake")
    root.bind('<KeyPress>', snake.getKey)
    root.mainloop()


wish()

if __name__ == "__main__":

    while True:
        
        query = take_command().lower()

        if "open notepad" in query:
            # npath = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Accessories\\notepad"
            # os.startfile(npath)
            notepad = 'notepad'
            os.system(notepad)

        elif "open command prompt" in query:
            os.system("start cmd")

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
            query = take_command()
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query,sentences=5)
            speak("According to wikipedia,")
            speak(results)
            #print(results)

        elif "open youtube" in query:
            #webbrowser.open("www.youtube.com")
            speak("what shall I play on youtube?")
            song = take_command()
            speak(f'playing {song} for you')
            pywhatkit.playonyt(song)
            sys.exit()

        elif "open facebook" in query:
            path = try_finding_chrome_path()
            path = path.replace(os.sep,'/')
            path = f'{path} %s'
            webbrowser.get(path).open("www.facebook.com")

        elif "open google" in query:
            speak("What should I search on google for you?")
            cm = take_command().lower()
            path = try_finding_chrome_path()
            path = path.replace(os.sep,'/')
            path = f'{path} %s'
            webbrowser.get(path).open(f"https://www.google.com/search?q={cm}")

        elif "send message" in query:
            speak("Tell me the number of the receiver")
            cnt_code = "+91"
            num = cnt_code + take_command()
            speak(f"Please confirm the number: {num}")
            userResponse = take_command().lower()
            if userResponse == "yes" or userResponse == "yeah" or userResponse == "ya":
                speak("what message has to be sent?")
                msg = input("Enter message here...")
                now = dt.datetime.now()
                h = now.hour
                m = now.minute + 1
                pywhatkit.sendwhatmsg(num,msg,h,m,2)
                speak("Message sent successfully.")
            else:
                speak("Okay! I'll not send the message")

        elif "send email" in query:
            try:
                def_email = "vishwapandya1999@gmail.com"
                def_pwd = "@vishwaPandya1999@"
                speak(f"Do you want to send message through {def_email} ?")
                response = take_command().lower()
                if "yes" in response:
                    speak("Provide me with the receiver's email address:")
                    to = input("Enter the receiver's email address:")
                    speak(f"What do you want to send to {to} ?")
                    content = take_command().lower()
                    sendEmail(def_email,def_pwd,to,content)
                elif "no" in response:
                    speak("Can you please guide me to login your email...")
                    speak("Provide me with the sender's email address:")
                    sender_id = input("Enter the sender's email address:")
                    speak("Provide me with the sender's password for login:")
                    sender_pwd = input("Enter the sender's password:")
                    speak(f"What do you want to send to {to} ?")
                    content = take_command().lower()
                    speak("Provide me with the receiver's email address:")
                    to = input("Enter the receiver's email address:")
                    speak(f"What do you want to send to {to} ?")
                    content = take_command().lower()
                    sendEmail(sender_id,sender_pwd,to,content)
                else:
                    speak("Okay, i'll not send any email")
                    break
            except Exception as e:
                print(e)

        elif "open camera" in query:
            cam = cv2.VideoCapture(0)
            cv2.namedWindow("camera")
            img_counter = 0
            while True:
                ret, frame = cam.read()
                if not ret:
                    print("failed to grab frame")
                    break
                cv2.imshow("test", frame)

                k = cv2.waitKey(1)
                if k%256 == 27:
                    # ESC pressed
                    print("Escape hit, closing...")
                    break
                elif k%256 == 32:
                    # SPACE pressed
                    img_name = "opencv_frame_{}.png".format(img_counter)
                    cv2.imwrite(img_name, frame)
                    print("{} written!".format(img_name))
                    img_counter += 1
            cam.release()
            cam.destroyAllWindows()

        elif "temperature" in query:
            speak("which place's temperature would you like to know?")
            place = take_command().lower()
            search = "Temperature in " + place
            url = f'https://www.google.com/search?q={search}'
            r = requests.get(url)
            data = BeautifulSoup(r.text,"html.parser")
            temp = data.find("div",class_="BNeawe").text
            speak(f"Current {search} is {temp}")

        elif "activate search mode" in query:
            speak("Plase tell me what do you want to search")
            how = take_command()
            max_results=1
            how_to = search_wikihow(how,max_results)
            assert len(how_to) == 1
            how_to[0].print()
            speak(how_to[0].summary)

        elif "alarm" in query:
            speak('Please tell me the time to set the alarm. Example: 10:10 am')
            userResponse = take_command()
            userResponse = userResponse.replace('set alarm to ','')
            userResponse = userResponse.replace('.','')
            userResponse = userResponse.upper()
            alarm(userResponse)

        elif "game" in query:
            speak('Okay.. I have the best game for you! The snake game! Would you like me to give you instructions?')
            userResponse = take_command().lower()
            if userResponse == 'yes':
                speak('Alright! You need to use w key to go up , a key to go left, d key to go right and s key to come down. Eat the apples you grow, if not you die! All the best')
                startGame()
                sys.exit()
            else :
                speak("Sorry couldn't understand you!")

        elif "do some calculations" in query or "can you calculate" in query:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                speak("What do you want to calculate? for example 5 plus 6 ")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                my_string = r.recognize_google(audio)
                print(my_string)
                def getOperator(opr):
                    return{
                        "+": add,
                        "-": sub,
                        "x": mul,
                        #"divided": operator.__truediv__,
                    }[opr]
                def EvaluateExpression(op1,opr,op2):
                    op1,op2 = int(op1), int(op2)
                    return getOperator(opr)(op1,op2)
                speak("The answer is: ")
                speak(EvaluateExpression(*(my_string.split())))

        elif "battery" in query or "how much power left" in query:
            battery = checkBattery()
            speak(f"Our system has {battery} percent battery")

        elif "check internet speed" in query or "speed test" in query or "internet speed" in query:
            st = speedtest.Speedtest()
            dl = round(st.download() / 1048576)
            up = round(st.upload() / 1048576)
            speak(f"The download speed is {dl} mbp s and upload speed is {up} mbp s")

        elif "increase volume" in query or "volume up" in query or "volume high" in query:
            pyautogui.press("volumeup")

        elif "decrease volume" in query or "volume down" in query or "volume low" in query:
            pyautogui.press("volumedown")

        elif "volume off" in query or "mute" in query:
            pyautogui.press("volumemute")

        elif "translate" in query:
            translateSentence()
            res = "yes"
            while res == "yes":
                speak("Do you want to translate something else?")
                res = take_command().lower()
                if "yes" in res:
                    translateSentence()
                else:
                    res = "no"
                    break

        elif "download video" in query:
            speak("Provide me the youtube link...")
            url = input("Enter link here:")
            speak("Downloading, please wait, this might take a few minutes")
            YouTube(url).streams.get_highest_resolution().download()
            speak("Download completed.")

        elif "search a file" in query or "open a file" in query:
            isFound = False
            listing1 = os.walk("C:/")
            listing2 = os.walk("G:/")
            listing3 = os.walk("H:/")
            listing4 = os.walk("I:/")
            search = input("Enter file name:")

            if isFound == False:
                speak(f"Searching {search} in G: drive")
                for root, dir, files in listing2:
                    if search in files:
                        print(os.path.join(root,search))
                        os.startfile(os.path.join(root,search)) #opening the file
                        isFound = True
                if isFound == False:
                    speak(f"{search} not found in G drive")

            if isFound == False:
                speak(f"Searching {search} in H: drive")
                for root, dir, files in listing3:
                    if search in files:
                        print(os.path.join(root,search))
                        os.startfile(os.path.join(root,search))
                        isFound = True
                if isFound == False:
                    speak(f"{search} not found in H drive")

            if isFound == False:
                speak(f"Searching {search} in I: drive")
                for root, dir, files in listing4:
                    if search in files:
                        print(os.path.join(root,search))
                        os.startfile(os.path.join(root,search))
                        isFound = True
                if isFound == False:
                    speak(f"{search} not found in I drive")

            if isFound == False:
                speak(f"Searching {search} in C: drive")
                for root, dir, files in listing1:
                    if search in files:
                        print(os.path.join(root,search))
                        os.startfile(os.path.join(root,search))
                        isFound = True
                if isFound == False:
                    speak(f"{search} not found in C drive")

        elif "no" in query:
            speak("Thank you for using me, have a great day ahead...")                
            sys.exit()

        speak("Do you have any other work?")
