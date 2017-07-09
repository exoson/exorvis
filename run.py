import time
import os
import math
import webbrowser
from urllib.parse import urlparse

import pyautogui as pag
from tellcore.telldus import TelldusCore
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from wit_recognition import recognize_cmd

core = TelldusCore()
lights = core.devices()[1]

numbers = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
#    'eleven': 11,
} 
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

print(volume.GetMasterVolumeLevel())

def set_volume(level):
    '''Set volume level to level spesified by the level argument.'''
    global volume
    try:
        volume_level = numbers[level]
    except KeyError:
        print('Not valid volume level!')
        return
    converted_volume = 14.5 * math.log(volume_level)-33.546 if volume_level else - 65.25
    volume.SetMasterVolumeLevel(converted_volume, None)
def playpause_song():
    '''Pause currently played song.'''
    pag.press('playpause')
def next_song():
	'''Change to next soundtrack on list.'''
	pag.press('nexttrack')
def pause_movie():
    '''Simulate pressing space.'''
    pag.press('space')
def quit():
    '''Quit program.'''
    os._exit(0)
def pass_fnc():
    '''Don't do nothing.'''
    pass
def lights_on():
    '''Turn lights on.'''
    lights.turn_on()
def lights_off():
    '''Turn lights off'''
    lights.turn_off()
def google(query):
    '''Do google search of query and open it in new tab.'''
    url = 'http://google.com/search?q=' + urlparse(query).geturl()
    webbrowser.get('C:/Users/Lime/AppData/Local/Vivaldi/Application/vivaldi.exe %s').open(url, new=2)


commands = {
    '': pass_fnc,
    'stop': pause_movie,
    'turn off': quit,
    'lights on': lights_on,
    'lights off': lights_off,
	'next song': next_song,
    'play': playpause_song
}

while True:
    try:
        print ('Listening..')
        cmd = recognize_cmd()
        print ('Recognized: ' + cmd)
        if cmd.startswith('google '):
            google(cmd[7:])
        elif cmd.startswith('volume '):
            set_volume(cmd[7:])
        else:
            commands[cmd]()
    except KeyError as e:
        print (e)
