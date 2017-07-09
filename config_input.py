import json

import pyaudio

p = pyaudio.PyAudio()

for index in range(p.get_device_count()):
    info = p.get_device_info_by_index(index)
    for key in info.keys():
        print ('Device ' + key + ': ' + str(info[key]))

device_idx = input('Which device index to use: ')

config_file = open('.config', 'r')

config_data = json.load(config_file)
config_file.close()
config_file = open('.config', 'w')

config_data['device_idx'] = int(device_idx)

json.dump(config_data, config_file)
