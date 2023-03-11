import threading, time, pyttsx3
import speech_recognition as sr
import datetime, webbrowser, wikipedia, os, requests, operator, tkinter, smtplib
from bs4 import BeautifulSoup
from PIL import Image, ImageTk

class EmailSender(object):
    def _init_(self):
        self.server = smtplib.SMTP_SSL("smtp.gmail.com")
        self.server.login("sender email", "Name")

    def sendEmail(self,receiver,content):
        self.server.sendmail('receiver email',receiver,content)


class Backend(threading.Thread):
    contacts = {
        "name": ['enter name'],
        "email": ['enter email']
    }

    def _init_(self, rate=115, event=None):
        super()._init_()

        if event:
            setattr(self, event, threading.Event())

        self._cancel = threading.Event()
        self.rate = rate
        self.engine = None

        self._say = threading.Event()
        self._text_lock = threading.Lock()
        self._text = []

        self._is_alive = threading.Event()
        self._is_alive.set()
        self.start()

    def _init_engine(self, rate):
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)  # setting up new voice rate
        engine.connect('finished-utterance', self._on_completed)
        engine.connect('started-word', self._on_cancel)
        return engine

    def say(self, text, stop=None):
        if self._is_alive.is_set():
            self._cancel.clear()

            if isinstance(text, str):
                text = [(text, stop)]

            if isinstance(text, (list, tuple)):
                for t in text:
                    if isinstance(t, str):
                        t = t, None

                    with self._text_lock:
                        self._text.append(t)

                    self._say.set()

    def cancel(self):
        self._cancel.set()

    def _on_cancel(self, name, location, length):
        if self._cancel.is_set():
            self.stop()

    def stop(self):
        self.engine.stop()
        time.sleep(0.5)
        self.engine.endLoop()

    def _on_completed(self, name, completed):
        if completed:
            self.engine.endLoop()
            self.on_finished_utterance(name, completed)

    def on_finished_utterance(self, name, completed):
        pass

    def terminate(self):
        self._is_alive.clear()
        self._cancel.set()
        self.join()

    def run(self):
        self.engine = engine = self._init_engine(self.rate)
        while self._is_alive.is_set():
            while self._say.wait(0.1):
                self._say.clear()

                while not self._cancel.is_set() and len(self._text):
                    with self._text_lock:
                        engine.say(*self._text.pop(0))
                    engine.startLoop()

    def userCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening.....")
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Recognizing....")
            query = r.recognize_google(audio)
            print(f"User said: {query}\n")
        except Exception as e:
            self.say("Could you please say that again...")
            return "None"
        return query

    def greeting(self):
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            self.say("Good Morning!Hope you have a wonderful day")
        elif hour >= 12 and hour < 16:
            self.say("Good Afternoon!")
        elif hour >= 16 and hour < 19.30:
            self.say("Good Evening!")
        else:
            self.say("Good Night!")
        self.say("Hi Tom here at your service.  How may I help you?")

    def mainFunctionality(self):
        self.greeting()
        while True:
            query = self.userCommand().lower()
            if 'wikipedia' in query:
                self.say("Searching wikipedia...,")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                self.say("According to Wikipedia")
                self.say(results)

            elif 'open youtube' in query:
                webbrowser.open("youtube.com")

            elif 'open google' in query:
                webbrowser.open("google.com")

            elif 'time' in query:
                strTime = datetime.datetime.now().strftime("%H %M %S")
                self.say(f"The Current Time is{strTime}")

            elif 'spotify' in query:
                spotifyPath = "Spotify path"
                os.startfile(spotifyPath)

            elif 'chrome' in query:
                chromePath = "chrome path"
                os.startfile(chromePath)

            elif 'code' in query:
                os.system("code")

            elif 'whatsapp' in query:
                whatsappPath = "Whatsapp path"
                os.startfile(whatsappPath)

            elif 'meet' in query:
                webbrowser.open('https://meet.google.com/new')

            elif 'send email' in query:
                try:
                    em = EmailSender()
                    print('Whom you want to send mail')
                    self.say('Whom you want to send mail')
                    reciver = self.takeCommand().lower()
                    for pos, name in enumerate(self.contacts['name']):
                        if name == reciver:
                            reciver = self.contacts["email"][pos]
                    print(reciver)
                    print('Enter your message:-')
                    self.say('Enter your message')
                    msg = self.takeCommand().lower()
                    em.sendEmail(reciver, msg)
                    print('mail send succesfully')
                    self.say('mail send succesfully')

                except:
                    print('please re-enter your mail')

            elif 'camera' in query:
                os.system("start microsoft.windows.camera:")

            elif 'temperature' in query:
                search = "temperature in Mumbai"
                url = f"https://www.google.com/search?q={search}"
                r = requests.get(url)
                data = BeautifulSoup(r.text, "html.parser")
                temp = data.find("div", class_="BNeawe").text
                self.say(f"current {search} is {temp}")
                print(f"The current temperature in mumbai is {temp}")

            elif 'calculations' in query:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    try:
                        self.say("I can do simple Arithmetic calculations   what would you like to calculate?")
                        print("Listening.....")
                        r.adjust_for_ambient_noise(source)
                        r.pause_threshold = 1
                        audio = r.listen(source)
                    except Exception as e:
                        self.say("Could you please say that again...")
                rec = r.recognize_google(audio)
                print(rec)

                def get_operator(op):
                    return {
                        '+': operator.add,
                        '-': operator.sub,
                        'x': operator.mul,
                        '/': operator.truediv,
                    }[op]

                def cal(op1, oper, op2):
                    op1, op2 = int(op1), int(op2)
                    return get_operator(oper)(op1, op2)

                self.say("The result is")
                self.say(cal(*(rec.split())))


def frontend():
        self = tkinter.Tk()
        self.title("Tom")
        self.geometry('800x449')

        IMAGE_PATH = 'main_img.jpeg'
        WIDTH, HEIGTH = 800, 449

        canvas = tkinter.Canvas(self, width=WIDTH, height=HEIGTH)
        canvas.pack()

        img = ImageTk.PhotoImage(Image.open(IMAGE_PATH).resize((WIDTH, HEIGTH)))
        canvas.background = img  # Keep a reference in case this code is put in a function.
        bg = canvas.create_image(0, 0, anchor=tkinter.NW, image=img)

        # Put a tkinter widget on the canvas.

        self.mainloop()

if __name__ == '_main_':
        t2 = threading.Thread(target=frontend,name='t1')
        t2.start()
        t1 = Backend()
        t1.mainFunctionality()