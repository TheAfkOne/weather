import requests
import time
import pygame
import tkinter as tk
from tkinter import messagebox
from gtts import gTTS

def get_weather(api_key, city, state):
    location_query = f"{city},{state}"
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location_query}"
    response = requests.get(url)
    data = response.json()
    return data

def show_weather():
    city = city_entry.get()
    state = state_entry.get()

    try:
        # get data
        weather_data = get_weather(api_key, city, state)
        temperature = weather_data['current']['temp_f']
        condition = weather_data['current']['condition']['text']

        # print 
        result_label.config(text=f"Weather in {city}: {temperature}°F, {condition}")

        # text to speech
        weatherTTS = f"The weather in {city}, {state} is {condition} and the temperature is {temperature} degrees farenheit"
        language = 'en'
        tts = gTTS(text=weatherTTS, lang=language, slow=False)
        tts.save("weather.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load('weather.mp3')
        pygame.mixer.music.play()

        # log everything in file
        f = open("log.txt", "a")
        timestamp = time.strftime('%a %Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] [{time.tzname[0]}] >> {city}, {state} >> {condition} {temperature} F\n")
        f.close()

    except Exception as e:
        print("Error fetching weather:", e)
        messagebox.showerror("Error", str(e))

        
api_key = ":)"

root = tk.Tk()
root.title("Weather App")

window_width = 400
window_height = 150

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

position_right = int((screen_width / 2) - (window_width / 2))
position_down = int((screen_height / 2) - (window_height / 2))

root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

tk.Label(root, text="City:").grid(row=0, column=0)
city_entry = tk.Entry(root)
city_entry.grid(row=0, column=1)

tk.Label(root, text="State:").grid(row=1, column=0)
state_entry = tk.Entry(root)
state_entry.grid(row=1, column=1)

submit_btn = tk.Button(root, text="Get Weather", command=show_weather)
submit_btn.grid(row=2, column=0, columnspan=2)

result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=2)

root.mainloop()
