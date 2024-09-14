import pyttsx3
import speech_recognition as sr
import datetime
import os
import subprocess
import webbrowser
import wikipedia
import pyjokes
import time
import pyautogui
import psutil
import winshell
import camera
from camera import cam
import socket
import imdb
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

# Initialize the TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
# Asshly should be able to remember what she had just said

global memory
memory="nothing yet !"

def speak(audio):
    global memory
    memory=audio
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1.0
        r.phrase_threshold = 0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold = True
        r.dynamic_energy_threshold = 4000
        r.adjust_for_ambient_noise(source, duration=0.5)
        r.dynamic_energy_adjustment = 2

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=25)
            print("Recognizing...")
            order = r.recognize_google(audio, language='en-in')
            print(f"User said: {order}\n")
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return "None"
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return "None"
        except Exception as e:
            speak("Unable to recognize your voice.")
            print(f"Error: {e}")
            return "None"
    return order

def show_info():
    speak("Fetching system information...")
    info = {
        "Operating System": os.uname().sysname,
        "OS Version": os.uname().version,
        "Machine": os.uname().machine,
        "Processor": os.uname().processor,
        "System Name": os.uname().nodename
    }
    
    for key, value in info.items():
        speak(f"{key}: {value}")

def open_notepad():
    try:
        os.startfile('C:\\Windows\\system32\\notepad.exe')
        speak("Notepad opened successfully.")
    except Exception as e:
        speak(f"Unable to open Notepad. Error: {e}")

def close_notepad():
    try:
        subprocess.run(["task kill", "/IM", "notepad.exe", "/F"], check=True)
        speak("Notepad closed successfully.")
    except subprocess.CalledProcessError as e:
        speak(f"Failed to close Notepad. Error: {e}")

def open_vscode():
    try:
        os.startfile('C:\\Users\\otien\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe')
        speak("Visual Studio Code opened successfully.")
    except Exception as e:
        speak(f"Unable to open Visual Studio Code. Error: {e}")

def close_vscode():
    try:
        subprocess.run(["taskkill", "/IM", "Code.exe", "/F"], check=True)
        speak("Visual Studio Code closed successfully.")
    except subprocess.CalledProcessError as e:
        speak(f"Failed to close Visual Studio Code. Error: {e}")

def play_music():
    try:
        music_url = 'https://music.youtube.com/'
        webbrowser.open(music_url)
        speak("Playing music for you.")
    except Exception as e:
        speak(f"Unable to open music. Error: {e}")

def search_wikipedia(order):
    try:
        result = wikipedia.summary(order, sentences=2)
        speak("According to Wikipedia:")
        speak(result)
    except wikipedia.exceptions.DisambiguationError:
        speak(f"Multiple results found for {order}. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("No results found for that order.")
    except Exception as e:
        speak(f"Error occurred: {e}")

def username():
    speak("What should I call you, sir?")
    uname = takeCommand()
    if uname.lower() == "none":
        uname = "Guest"
    speak(f"Welcome, Mister {uname}. How can I assist you today?")

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning, Sir.")
    elif 12 <= hour < 18:
        speak("Good afternoon, Sir.")
    else:
        speak("Good evening, Sir.")

def cpu_status():
    usage = psutil.cpu_percent()
    speak(f"CPU usage is at {usage} percent.")
    battery = psutil.sensors_battery()
    if battery:
        speak(f"Battery level is at {battery.percent} percent.")
    else:
        speak("Battery information is not available.")


def get_public_ip():
    try:
        ip = requests.get('https://api.ipify.org').text
        speak(f"Your public IP address is {ip}.")
    except Exception as e:
        speak(f"An error occurred: {e}")        
def get_ip():
    ip = socket.gethostbyname(socket.gethostname())
    speak(f"Your IP address is {ip}.")

def open_notepad():
    try:
        os.startfile('C:\\Windows\\system32\\notepad.exe')
        speak("Notepad opened successfully.")
    except Exception as e:
        speak(f"Unable to open Notepad. Error: {e}")

def close_notepad():
    try:
        subprocess.run(["taskkill", "/IM", "notepad.exe", "/F"], check=True)
        speak("Notepad closed successfully.")
    except subprocess.CalledProcessError as e:
        speak(f"Failed to close Notepad. Error: {e}")

def movie():
    moviesdb = imdb.IMDb()
    speak("Please tell me the movie name")
    text = takeCommand()
    movies = moviesdb.search_movie(text)
    speak("Searching for " + text)

    if len(movies) == 0:
        speak("No results found for the movie, sir.")
    else:
        speak("I found these, sir: ")
        for movie in movies:
            title = movie.get("title")
            year = movie.get("year")
            info = movie.getID()
            movie_details = moviesdb.get_movie(info)
            rating = movie_details.get("rating", "N/A")  # Handle missing rating
            plot = movie_details.get('plot outline', "No plot summary available")  # Handle missing plot

            current_year = int(datetime.datetime.now().strftime('%Y'))

            if year and year < current_year:
                speak(f"{title} was released in {year} and has an IMDB rating of {rating}. The plot summary of the movie is: {plot}.")
            else:
                speak(f"{title} will be released in {year} and has an IMDB rating of {rating}. The plot summary of the movie is: {plot}.")
            
            break
                

def send_mail(to, subject, content):
    sender_email = 'esamba333@gmail.com'
    password = 'mlbdrkluhpzwkflu'
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to
    msg['Subject'] = subject
    
    msg.attach(MIMEText(content, 'plain'))
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, to, msg.as_string())
        speak("Email sent successfully.")
    except Exception as e:
        speak(f"An error occurred: {e}")


def handle_email_sending():
    speak("Who should I send the email to?")
    to = takeCommand()
    if to.lower() == "none":
        speak("No recipient provided.")
        return
    
    speak("What is the subject of the email?")
    subject = takeCommand()
    if subject.lower() == "none":
        speak("No subject provided.")
        return
    
    speak("What is the content of the email?")
    content = takeCommand()
    if content.lower() == "none":
        speak("No content provided.")
        return
    
    send_mail(to, subject, content)        

def open_browser(search_url):
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open_new_tab(search_url)

def click_link(image_path):
    # This function clicks on a link based on an image of the link
    try:
        location = pyautogui.locateCenterOnScreen(image_path)
        if location:
            pyautogui.click(location)
        else:
            speak("Link not found on the screen.")
    except Exception as e:
        speak(f"An error occurred: {e}")

def scroll_down(pixels=300):
    # This function scrolls down by a specified number of pixels
    pyautogui.scroll(-pixels)

def close_browser():
    # This function closes the browser
    pyautogui.hotkey('ctrl', 'w')


def take_screenshot():
    speak("Sir, please tell me the name of the file to save.")
    name = takeCommand().lower()
    speak("Please hold the screen for a moment.")
    time.sleep(3)
    img = pyautogui.screenshot()
    img.save(f'{name}.png')
    speak(f"Screenshot taken and saved as {name}.png.")
    
    speak("Would you like to view the screenshot?")
    show_screenshot = takeCommand()
    if 'yes' in show_screenshot or 'yeah' in show_screenshot:
        img.show()

def delete_screenshot():
    speak("What is the name of the file you want to delete?")
    name = takeCommand().lower()
    file_path = f'{name}.png'
    
    if os.path.exists(file_path):
        os.remove(file_path)
        speak(f"Screenshot {name}.png has been deleted.")
    else:
        speak(f"No screenshot found with the name {name}.")

if __name__ == '__main__':
    speak("I am your virtual assistant Ashly.")
    username()
    wishMe()
    
    while True:
        order = takeCommand().lower()

        if 'how are you' in order:
            speak("I am fine, thank you. How are you, Sir?")

        elif 'i am fine' in order or 'good' in order:
            speak("Good to hear that!")

        elif 'what is love' in order:
            speak("Love is a profound feeling that can bring great joy and meaning to our lives.")

        elif 'who are you' in order or "what's your name?" in order:
            speak("I am Ashly, your virtual assistant.how should i help you today sir ?")

        elif 'i love you' in order:
            speak("Thank you! As an AI, I can't love, but I'm here to assist you.how can i help you?")

        elif 'who created you' in order:
            speak("I was developed by Engineer Samba inorder to serve as his personall assistance to help in various progamming and computer issues as well as his private and confidential matters.")

        elif 'can you fall in love with anybody' in order or 'can you be my love' in order:
            speak("I don’t have feelings, but I'm here to help you.")

        elif 'play music' in order:
            play_music()
        elif'repeat what you have just said' in order or "what" in order or "repeat" in order or "come again" in order or "sorry" in order:
            engine.say("i said ....")
            speak(memory)

        elif 'show my public ip' in order:
            get_public_ip()

        elif 'tell me of a movie' in order:
            movie()    

        elif 'get ip' in order:
            get_ip()    

        elif 'give me sytem infomation' in order:
             show_info()    

        elif 'open amazon' in order: 
            speak("Opening Amazon. Happy shopping!")
            webbrowser.open("https://www.amazon.com")  

        elif 'open google' in order: 
            speak("Opening Google.")
            webbrowser.open("https://www.google.com")  

        elif 'open stack overflow' in order: 
            speak("Opening Stack Overflow. Happy coding!")
            webbrowser.open("https://stackoverflow.com")         

        elif 'open notepad' in order:
             open_notepad()
        elif 'close notepad' in order:
             close_notepad()
                
        elif 'open visual studio' in order:
            open_vscode()
        elif 'close visual studio' in order:
            close_vscode()

        elif 'open brave' in order or 'open browser' in order:
            try:
                os.startfile('C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe')
                speak("Brave Browser opened successfully.")
            except Exception as e:
                speak(f"Unable to open Brave Browser. Error: {e}")

        elif ' search in wikipedia' in order:
            speak("Searching Wikipedia...")
            order = order.replace("wikipedia", "").strip()
            search_wikipedia(order)

        elif 'send an email' in order or 'i want you send an email to ' in order:
            speak("to whom should i sent the email to ")
            to=takeCommand()
            speak("what is the sublect of the email sir?")
            subject=takeCommand()
            speak("Ok then,tell me the contents or the body of your email to write.")
            content=takeCommand()
            send_mail()   
            
        elif 'where is ' in order:
            location = order.replace("where is", "").strip()
            speak("Locating...")
            webbrowser.open(f"https://www.google.co.in/maps/place/{location}")

        elif 'write a note' in order:
            speak("What should I write, Sir?")
            note = takeCommand()
            with open('ashly.txt', "a") as file:
                speak("Should I include the date and time as well?")
                sn = takeCommand()
                if 'yes' in sn:
                    strTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    file.write(f"{strTime} - {note}\n")
                else:
                    file.write(f"{note}\n")
                speak("Note saved.")

        elif 'show note' in order:
            speak("Showing notes...")
            try:
                with open("ashly.txt", "r") as file:
                    notes = file.read()
                    print(notes)
                    speak(notes)
            except FileNotFoundError:
                speak("No notes found.")

        elif 'give me a joke' in order:
            speak(pyjokes.get_joke(language="en", category="neutral"))

        elif 'what is the time' in order:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}.")

        elif 'shutdown' in order:
            speak("Your system is about to shut down. Please save your work.")
            time.sleep(5)
            subprocess.call(['shutdown', '/s'])

        elif 'restart' in order:
            speak("Restarting the PC.")
            subprocess.call(['shutdown', '/r'])
            
        elif 'hibernate' in order:
            speak("Hibernating the system.")
            subprocess.call(['shutdown', '/h'])

        elif 'log off' in order:
            speak("Signing out. Please save your work.")
            time.sleep(5)
            subprocess.call(['shutdown', '/l'])

        elif 'switch window' in order:
            pyautogui.hotkey('alt', 'tab')
            time.sleep(1)

        elif 'take a screenshot' in order:
            take_screenshot()

        elif 'delete screenshot' in order:
            delete_screenshot()

        elif 'show me cpu status' in order:
            cpu_status()

        elif 'empty the recycle bin' in order:
            speak("Are sure about this, sir?")
            my_answer = takeCommand()
            if 'yes' in my_answer:
                winshell.recycle_bin().empty(confirm="False", show_progress="False", sound="True")
                speak("Recycle bin cleaned.")
            else:
                speak("The data in the recycle bin is still there.")

        elif 'open the camera' in order or 'camera' in order:
            speak("Should I turn the camera on, sir?")
            answer = takeCommand()
            if 'yes' in answer or 'go on' in answer or 'just do it' in answer or 'of course' in answer:
                cam()

        elif (("search" in order) or ("open" in order)) and (("internet" in order) or ("google" in order) or ("chrome" in order)):
            speak("What do you want to search for, sir?")
            answer = "None"
            while answer == "None":
                answer = takeCommand()
            
            search_url = "https://www.google.com/search?q=" + answer
            open_browser(search_url)

        elif (("search" in order) or ("open" in order)) and (("youtube" in order) or ("you" in order and "tube" in order)):
            speak("What do you want to search for, sir?")
            answer = "None"
            while answer == "None":
                answer = takeCommand()
            
            search_url = "https://www.youtube.com/search?q=" + answer
            open_browser(search_url)
            click_link()
        elif "play" in order and "song" in order and "youtube" in order:
            speak("What song do you want to play?")
            song_name = takeCommand()
            
            # Replace spaces with '+' for URL compatibility
            song_name = song_name.replace(" ", "+")
            search_url = "https://www.youtube.com/results?search_query=" + song_name
            open_browser(search_url)
            
            # Example to click on the first result
            # You'll need an image of the clickable link or button
            image_path = input("Enter the path to the image of the link: ").strip()
            click_link(image_path)
        elif "click" in order:
            # Handle click action here
            image_path = input("Enter the path to the image of the link: ").strip()
            click_link(image_path)
        elif "scroll" in order:
            pixels = int(input("Enter the number of pixels to scroll down: "))
            scroll_down(pixels)
        elif "close" in order:
            close_browser()    
        elif'show ip' in order or 'what is my ip address?' in order or 'ip' in order:
            host=socket.gethostname()
            ip=socket.gethostbyname(host)
            speak("Your ip address is"+ ip)

        elif 'send an email' in order or 'i want you send an email to ' in order:
            handle_email_sending()    
       

        elif 'exit' in order or 'quit' in order:
            speak("Thank you for using me, sir! Have a nice day.")
            break