from array import array
import struct
import pyaudio
import json
import requests
import math
import time

from constants import WIT_KEY

MAX_SILENT = 5
THRESHOLD = .03
CHUNK_SIZE = 512
FORMAT = pyaudio.paInt16
RATE = 8000
CHANNELS = 2
SHORT_NORMALIZE = (1.0/32768.0)

def is_silent(block):
    '''Returns if the RMS of block is less than the threshold.'''
    count = len(block)/2
    form = "%dh" % (count)
    shorts = struct.unpack(form, block)
    sum_squares = 0.0

    for sample in shorts:
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    rms_value = math.sqrt(sum_squares / count)
    return rms_value, rms_value <= THRESHOLD


def returnUpTo(iterator, values, returnNum):
    '''Returns as many (up to returnNum) blocks as it can.'''
    if iterator+returnNum < len(values):
        return (iterator + returnNum,
                "".join(values[iterator:iterator + returnNum]))
    else:
        temp = len(values) - iterator
        return (iterator + temp + 1, "".join(values[iterator:iterator + temp]))


global start_time
start_time = 0
def gen(p, stream):
    '''Python generator- yields roughly 512k to generator.'''
    num_silent = 0
    snd_started = False
    start_pack = 0
    counter = 0
    i = 0
    data = []
    while 1:
        rms_data = stream.read(CHUNK_SIZE)
        snd_data = array('i', rms_data)
        for d in snd_data:
            data.append(struct.pack('<i', d))

        rms, silent = is_silent(rms_data)

        if silent and snd_started:
            num_silent += 1

        elif not silent and not snd_started:
            i = len(data) - CHUNK_SIZE*1  # Set the counter back a few seconds
            if i < 0:                     # so we can hear the start of speech.
                i = 0
            speech_start = i
            snd_started = True
            #print "TRIGGER at " + str(rms) + " rms."

        elif not silent and snd_started and not i >= len(data):
            i, temp = returnUpTo(i, data, 1024)
            yield temp
            num_silent = 0

        if snd_started and num_silent > MAX_SILENT:
            #print "Stop Trigger"
            break

        if counter > 75:  # Slightly less than 10 seconds.
            #print "Timeout, Stop Trigger"
            break

        if snd_started:
            counter = counter + 1
    global start_time
    start_time = time.time()
    # Yield the rest of the data.
    #print "Pre-streamed " + str(i-speech_start) + " of " + str(len(data)-speech_start) + "."
    while (i < len(data)):
        i, temp = returnUpTo(i, data, 1024)
        yield temp
    print "Swapping to thinking."



def recognize_cmd():
    '''Record a command, recognise it with wit.ai and return it as text.'''
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
                    input=True, output=False,
                    frames_per_buffer=CHUNK_SIZE)

    headers = {'Authorization': 'Bearer ' + access_key,
               'Content-Type': 'audio/raw; encoding=signed-integer; bits=16;' +
               ' rate=8000; endian=little', 'Transfer-Encoding': 'chunked'}
    url = 'https://api.wit.ai/speech'

    resp = requests.post(url, headers=headers, data=gen(p, stream))
    delta_time = time.time() - start_time
    #print 'delta: ' + str(delta_time)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return json.loads(resp.content)['_text']
