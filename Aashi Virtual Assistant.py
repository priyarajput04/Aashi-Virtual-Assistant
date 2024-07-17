# pip install pyaudio
import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install SpeechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser
import os
import smtplib
import time
import random
import threading
import requests # pip install requests
from twilio.rest import Client # pip install twilio


# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Replace 'your_api_key' with your actual OpenWeatherMap API key
API_KEY = 'your_api_key'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

# Replace 'your_api_key' with your actual News API key
NEWS_API_KEY = 'your_api_key'
NEWS_BASE_URL = "http://newsapi.org/v2/top-headlines?"

# Replace 'your_api_key' with your actual Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = 'your_api_key'
STOCK_BASE_URL = "https://www.alphavantage.co/query?"

# Replace these placeholders with your actual Twilio account SID, Auth Token, and Twilio phone number
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'

# Replace these placeholders with your actual Twilio account SID, Auth Token, and Twilio phone number
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am Aashi. Please tell me how may I help you.")

def takeCommand():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query.lower()

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()

def setReminder(reminder_time, message):
    def reminder():
        while True:
            current_time = datetime.datetime.now().strftime("%H:%M")
            if current_time == reminder_time:
                speak(message)
                break
            time.sleep(30)  # Check every 30 seconds to avoid high CPU usage

    reminder_thread = threading.Thread(target=reminder)
    reminder_thread.start()

def getWeather(location):
    complete_url = f"{BASE_URL}q={location}&appid={API_KEY}&units=metric"
    response = requests.get(complete_url)
    
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather = data['weather'][0]
        temp = main['temp']
        pressure = main['pressure']
        humidity = main['humidity']
        description = weather['description']

        weather_report = (f"Temperature: {temp}°C\n"
                          f"Pressure: {pressure} hPa\n"
                          f"Humidity: {humidity}%\n"
                          f"Description: {description}")
        speak(weather_report)
    else:
        speak("Sorry, I couldn't retrieve the weather information. Please try again.")

def getNews(country='us'):
    complete_url = f"{NEWS_BASE_URL}country={country}&apiKey={NEWS_API_KEY}"
    response = requests.get(complete_url)
    
    if response.status_code == 200:
        data = response.json()
        articles = data['articles']
        if len(articles) == 0:
            speak("Sorry, I couldn't find any news articles.")
        else:
            speak("Here are the top news headlines:")
            for i, article in enumerate(articles[:5], 1):  # Get top 5 headlines
                speak(f"{i}. {article['title']}")
    else:
        speak("Sorry, I couldn't retrieve the news information. Please try again.")

def getStockPrice(symbol):
    complete_url = f"{STOCK_BASE_URL}function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(complete_url)
    
    if response.status_code == 200:
        data = response.json()
        try:
            last_refreshed = data['Meta Data']['3. Last Refreshed']
            last_close = data['Time Series (1min)'][last_refreshed]['4. close']
            speak(f"The latest price for {symbol} is {last_close} dollars.")
        except KeyError:
            speak("Sorry, I couldn't retrieve the stock price information. Please check the stock symbol and try again.")
    else:
        speak("Sorry, I couldn't retrieve the stock price information. Please try again.")

def makePhoneCall(number):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    try:
        call = client.calls.create(
            to=number,
            from_=TWILIO_PHONE_NUMBER,
            url='http://demo.twilio.com/docs/voice.xml'
        )
        speak(f"Calling {number}...")
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't make the call. Please try again.")

def sendText(number, message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    try:
        message = client.messages.create(
            to=number,
            from_=TWILIO_PHONE_NUMBER,
            body=message
        )
        speak(f"Text message sent to {number}.")
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't send the text message. Please try again.")

def getDefinition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            definition = data[0]['meanings'][0]['definitions'][0]['definition']
            speak(f"The definition of {word} is: {definition}")
        else:
            speak("Sorry, I couldn't find the definition.")
    else:
        speak("Sorry, I couldn't retrieve the definition information. Please try again.")

def getJoke():
    jokes = [
        "Why did the chicken go to the seance? To talk to the other side!",
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why did the hipster burn his tongue? Because he drank his coffee before it was cool!",
        "Why did the bicycle fall over? Because it was two-tired!",
        "Why did the tomato turn red? Because it saw the salad dressing!",
        "Why don't skeletons fight each other? They don't have the guts!",
        "Why did the coffee file a police report? It got mugged!",
        "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
        "Why did the ditch digger become a gardener? He found his calling!",
        "Why did the bicycle fall in love? Because it was two-tired to resist!",
        "Why did the table go to therapy? It had trouble standing on its own four legs!",
        "Why did the computer go to the doctor? It had a virus!",
        "Why did the coffee file a police report? It got mugged!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why did the hipster burn his tongue? Because he drank his coffee before it was cool!",
    ]
    joke = random.choice(jokes)
    speak(joke)

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()

        if 'set reminder' in query:
            try:
                speak("What time should I set the reminder for? Please say the time in HH:MM format.")
                reminder_time = takeCommand()
                speak("What is the reminder message?")
                reminder_message = takeCommand()
                setReminder(reminder_time, reminder_message)
                speak(f"Reminder set for {reminder_time}")
            except Exception as e:
                print(e)
                speak("I am not able to set the reminder")

        elif 'weather in' in query:
            location = query.replace('weather in', '').strip()
            getWeather(location)

        elif 'news' in query:
            getNews()

        elif 'stock price' in query:
            symbol = query.replace('stock price', '').strip().upper()
            getStockPrice(symbol)

        elif 'make phone call' in query:
            speak("Please provide the phone number.")
            number = takeCommand().replace(' ', '')  # Remove spaces from the phone number
            makePhoneCall(number)

        elif 'send text' in query:
            try:
                speak("Please provide the phone number.")
                number = takeCommand().replace(' ', '')  # Remove spaces from the phone number
                speak("What is the message?")
                message = takeCommand()
                sendText(number, message)
            except Exception as e:
                print(e)
                speak("I am not able to send the text message")

        elif 'definition of' in query:
            word = query.replace('definition of', '').strip()
            getDefinition(word)

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query:
            music_dir = 'C:\\Users\\YourName\\Music'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'send an email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "receiveremail@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("I am not able to send this email")

        elif 'tell me a joke' in query:
            getJoke()
        
        # Add more commands as needed
