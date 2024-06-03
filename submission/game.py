#!/usr/bin/python3

import pygame
import numpy as np
from Utilities import *
import argparse
import os

from Application import Application
from Maze import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--music", type=str, help="Add path to music Files")
    parser.add_argument("--night", help="Start game in night mode", action="store_true")
    args = parser.parse_args()
    musicPath = ""
    supported_audio_formats = [".wav", ".mp3", ".ogg"]

    #error messages
    if(args.music == "" or args.music == None):
        print("No music file provided. Using default music file")
        musicPath =  "res/sound/music.mp3"
    elif(os.path.isfile(args.music)):
        file, ext = os.path.splitext(args.music)
        if(ext not in supported_audio_formats):
            print("Provided music file is not in supported format. Using default music file.")
            musicPath = "res/sound/music.mp3"
        else:
            musicPath = args.music
    else:
        print("Given Music file not found. Using default music file.")
        musicPath = "res/sound/music.mp3"

    print("Taking music from",musicPath )
    


    app = Application(musicPath, args.night)
    app.RunGSH()
    app.Exit()