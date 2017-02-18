from tkinter import *
import tkinter.font as tkfont
import tkinter.messagebox
from time import sleep
import os,sys,random
from PIL import ImageTk,Image

#Defines frame dimensions
height=250
width=422

'''
smallmap_corners = {topleft: [32.955651, -106.930123], topright: [32.955651, -106.892924],
                    botleft: [32.937436, -106.930123], botright: [32.937436, -106.892924]}
largemap_corners = {topleft: [32.979024, -106.967445], topright: [32.979024, -106.858726],
                    botleft: [32.925260, -106.930123], botright: [32.925260, -106.858726]}
'''

class Map:

    # Loads Small Map
    load_smallmap = Image.open("Map Image.png")
    load_smallmap.thumbnail(size=(width, height))

    # Loads Large Map
    load_largemap = Image.open("Large Map.png")
    load_largemap.thumbnail(size=(width, height))

    # Loads Crosshair
    load_crosshair = Image.open("Crosshair.png")
    crosshair_size = (20, 20)
    load_crosshair.thumbnail(size=(crosshair_size[0], crosshair_size[1]))

    # Coordinates of Small and Large Map sides
    smallmap_side = {'top': 32.955651, 'bot': 32.937436, 'left': -106.930123, 'right': -106.892924}
    largemap_side = {'top': 32.979024, 'bot': 32.925260, 'left': -106.967445, 'right': -106.858726}
    map_side = smallmap_side.copy()  # Map being displayed

    # ***************** Instantiate *****************
    def __init__(self, master):
        self.__master = master
        # Sets window parameters
        self.__master.resizable(width=False, height=False)
        self.__master.geometry('{}x{}'.format(width, height))
        self.__frame = Frame(self.__master)
        self.__frame.pack()

        # Runs Map functions
        self.__map_side = self.smallmap_side.copy()  # Small Map being displayed
        self.frame_dimensions()
        self.__random_coordinate = self.getRandomNumber()
        self.choose_map()
        self.convert_pixel()
        self.display_map()

    # Sets length, width, and border values of map frame in terms of latitude and longitude coordinates
    def frame_dimensions(self):
        self.__latitude_top = self.__map_side['top']
        self.__latitude_bot = self.__map_side['bot']
        self.__latitude_length = self.__latitude_top - self.__latitude_bot

        self.__longitude_right = self.__map_side['right']
        self.__longitude_left = self.__map_side['left']
        self.__longitude_length = (self.__longitude_left - self.__longitude_right)*(-1)

    # Random test coordinates
    def getRandomNumber(self):
        self.__rand_lat = round(random.uniform(self.__latitude_bot, self.__latitude_top), 6)
        self.__rand_long = round(random.uniform(self.__longitude_right, self.__longitude_left), 6)
        print(self.__rand_lat, self.__rand_long)
        return [self.__rand_lat, self.__rand_long]

    # Derives proportionality between latitude/longitude coordinates and x,y direction pixels
    # Converts latitude/longitude coordinates to x,y pixel parameters
    def convert_pixel(self):
        y_relation = height / self.__latitude_length
        x_relation = width / self.__longitude_length
        y = (self.__latitude_top - self.__rand_lat) * y_relation
        x = (self.__longitude_left - (self.__rand_long))*(-1) * x_relation
        # Seperates integers and decimals
        self.__pixel_integer = [int(y), int(x)]
        print(int(y), int(x))
        self.__pixel_decimals = (y % 1, x % 1)
        print(y % 1, x % 1)

    # Chooses Map and notifies user if Rocket leaves Small Map
    def choose_map(self):
        if self.__random_coordinate[0] > self.__latitude_top or self.__random_coordinate[0] < self.__latitude_bot:
            tkinter.messagebox.showwarning('Warning', 'Rocket has left the competition area!!!')
            print("Rocket has left competition area!!!")
            self.__map_side = self.largemap_side.copy()
            self.__load_map = self.load_largemap
        elif self.__random_coordinate[1] < self.__longitude_left or self.__random_coordinate[1] > self.__longitude_right:
            tkinter.messagebox.showwarning('Warning', 'Rocket has left the competition area!!!')
            print("Rocket has left competition area!!!")
            self.__map_side = self.largemap_side.copy()
            self.__load_map = self.load_largemap
        elif self.__random_coordinate[0] < self.smallmap_side['top'] or self.__random_coordinate[0] > self.smallmap_side['bot']:
            self.__map_side = self.smallmap_side.copy()
            self.__load_map = self.load_smallmap
        elif self.__random_coordinate[1] > self.smallmap_side['left'] or self.__random_coordinate[1] < self.smallmap_side['right']:
            self.__map_side = self.smallmap_side.copy()
            self.__load_map = self.load_smallmap

     # Displays Map and Crosshair
    def display_map(self):
        self.__load_map.paste(self.load_crosshair, (self.__pixel_integer[1] - int(self.crosshair_size[0] / 2), self.__pixel_integer[0] - int(self.crosshair_size[1] / 2)), self.load_crosshair)  # Positions and blends Crosshair with map
        map = ImageTk.PhotoImage(self.__load_map)
        crosshair = ImageTk.PhotoImage(self.load_crosshair)
        label_map = Label(self.__frame, image=map)
        label_map.pack()


#Displays path of Crosshair
'''
path_array = [[32.940321, -106.913103], [32.941321, -106.913103], [32.942321, -106.913103], [32.943321, -106.913103], [32.945321, -106.913103]]

def getCoordinates():
    for i in range(5):
        path_coordinate = path_array[i]
    root.after(500, getCoordinates)
    return path_coordinate

root.after(0, getCoordinates)
'''

root = Tk()
run_map = Map(root)
root.mainloop()

