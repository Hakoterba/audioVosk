#!/usr/bin/env python3

# prerequisites: as described in https://alphacephei.com/vosk/install and also python module `sounddevice` (simply run command `pip install sounddevice`)
# Example usage using Dutch (nl) recognition model: `python test_microphone.py -m nl`
# For more help run: `python test_microphone.py -h`

import argparse
import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json
from myinterpreter import Myinterpreter
import eel
import threading
import sys

my = Myinterpreter()
q = queue.Queue()
html_file = 'index.html'
eel.init('web')

@eel.expose
def returnImg(data):
    image_paths = {
        1: "./img/gb-a.png",
        2: "./img/gb-b.png",
        3: "./img/gb-bas.png",
        4: "./img/gb-droite.png",
        5: "./img/gb-gauche.png",
        6: "./img/gb-haut.png",
        7: "./img/gb-l.png",
        8: "./img/gb-r.png",
        9: "./img/gb-select.png",
        10: "./img/gb-start.png"
    }
    
    link = "./img/gb.png"
    
    if data.find("oui") >= 0:
        link = image_paths[1]
    elif data.find("non") >= 0:
        link = image_paths[2]
    elif data.find("en bas") >= 0:
        link = image_paths[3]
    elif data.find("droite") >= 0:
        link = image_paths[4]
    elif data.find("gauche") >= 0:
        link = image_paths[5]
    elif data.find("haut") >= 0:
        link = image_paths[6]
    elif data.find("bouton elle") >= 0:
        link = image_paths[7]
    elif data.find("bouton air") >= 0:
        link = image_paths[8]
    elif data.find("select") >= 0:
        link = image_paths[9]
    elif data.find("menu") >= 0:
        link = image_paths[10]

    print("")
    return link

def run_eel():
    eel.start(html_file, size=(600, 500))

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))
    
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="audio file to store recording to")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="input device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="sampling rate")
parser.add_argument(
    "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
args = parser.parse_args(remaining)

try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info["default_samplerate"])
        
    if args.model is None:
        model = Model(lang="en-us")
    else:
        model = Model(lang=args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None
        
    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device,
            dtype="int16", channels=1, callback=callback):
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)
        eel_thread = threading.Thread(target=run_eel)
        eel_thread.daemon = True
        eel_thread.start()
    
        rec = KaldiRecognizer(model, args.samplerate)
        
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                parler = json.loads(rec.FinalResult())
                print(parler['text'])
                if parler['text'].find('stop') >= 0:
                    print('Bye!')
                    sys.exit()
                my.interpret(parler['text'])
                path = returnImg(parler['text'])
                eel.setImage(path)

            if dump_fn is not None:
                dump_fn.write(data)

except KeyboardInterrupt:
    print("\nDone")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))
    
