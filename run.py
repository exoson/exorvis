import time
import os
import webbrowser
import urllib

import pyautogui as pag
from tellcore.telldus import TelldusCore

from wit_recognition import recognize_cmd

core = TelldusCore()
lights = core.devices()[1]


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
    url = 'http://google.com/search?q=' + urllib.quote(query)
    webbrowser.get('/usr/bin/vivaldi  %s').open(url, new=2)


commands = {
    '': pass_fnc,
    'stop': pause_movie,
    'turn off': quit,
    'lights on': lights_on,
    'lights off': lights_off,
}

while True:
    try:
        cmd = recognize_cmd()
        print 'Recognized: ' + cmd
        if cmd.startswith('google '):
            google(cmd[7:])
        else:
            commands[cmd]()
    except Exception as e:
        print e
