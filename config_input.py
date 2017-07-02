import json

import pyaudio

p = pyaudio.PyAudio()

for index in range(p.get_device_count()):
    print 'Device index: ' + str(index)
    print 'Device name: ' + p.get_device_info_by_index(index)['name']

device_idx = input('Which device index to use: ')

config_file = open('.config', 'r')

config_data = json.load(config_file)
config_file.close()
config_file = open('.config', 'w')

config_data['device_idx'] = device_idx

json.dump(config_data, config_file)
