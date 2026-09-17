import weatherdata
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image

import os
import sys

drachten = weatherdata.WeatherLocation(53.1037,6.0877, "Drachten")
ulm_baden_württemberg = weatherdata.WeatherLocation(48.400002,9.983333, "Ulm, Baden\n-Württemberg")
athens = weatherdata.WeatherLocation(37.97945, 23.71622, "Athens")

# only a max of three for now!!
locations = (drachten, ulm_baden_württemberg, athens)
   
class MainGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WeatherApp")
        self.root.geometry("950x705") # Window size
        
       
        self.root.resizable(False,False)
    
        appicon = tk.PhotoImage(file=get_asset_path('images\\appicon.png'))
        self.root.iconphoto(True, appicon)
        
        canvas = tk.Canvas(self.root, width=950, height=705, highlightthickness=0)
        canvas.pack()

        # background image
        bg_img = tk.PhotoImage(file=get_asset_path("images\\bg.png"))
        bg = canvas.create_image(475, 353, image=bg_img)
        # title img
        title_img = tk.PhotoImage(file=get_asset_path('images\\title.png'))
        title = canvas.create_image(300,75, image=title_img)
        # funny copyright
        canvas.create_text(890, 700, text='Nick Brander 2025©',fill='White')
        
        
        
        wwb = tk.PhotoImage(file=get_asset_path("images\\wwb.png"))
        location_1_wwb = canvas.create_image(150,400, image=wwb)
        location_2_wwb = canvas.create_image(450,400, image=wwb)
        location_3_wwb = canvas.create_image(750,400, image=wwb)
        self.create_widgets(150,400, canvas, locations[0]) #location 1
        self.create_widgets(450,400, canvas, locations[1]) #location 2
        self.create_widgets(750,400, canvas, locations[2]) #location 3
        
        
        # increment by 300 for new locations btw
        
        
        self.root.mainloop()
        
    def create_widgets(self,x,y, canvas, location):
        canvas.create_text(x,y - 240, text=location.name, font=('Eras Demi ITC',20),fill='White') # e.g Drachten
        canvas.create_text(x - 55, y - 140, text=location.current_time, font=('Arial',25),fill='White') # e.g 10:09
        canvas.create_text(x - 40,y - 190, text=f'{location.current_temperature}°', font=('Arial',40),fill='White') # e.g 15c
        canvas.create_text(x - 35,y - 100, text=f'H:{location.daily_temperature_max}° L:{location.daily_temperature_min}°',font=('Eras Demi ITC',19),fill='White') # e.g H:15 L:9
        canvas.create_text(x + 20, y - 30, text=location.current_weather, font=('Eras Demi ITC',19),fill='White') # e.g Sunny
        canvas.create_text(x, y + 50, text=f'🌧Chance of rain:{location.rain_chance}%',font=('Eras Demi ITC',15),fill='White') # e.g Chance of rain: 75%
        
            
    
            
        
        
    
def get_asset_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Running as an EXE (look in the temporary unzip folder)
        base_path = sys._MEIPASS
    else:
        # Running normally as code (look where app.py is located)
        base_path = os.path.dirname(os.path.abspath(__file__))
        
    return os.path.join(base_path, relative_path)   

    
MainGUI()