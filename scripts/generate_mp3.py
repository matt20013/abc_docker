import csv
import re
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='Generate CSV file of ABC notation metadata')
parser.add_argument('input_path',
                       metavar='input_path',
                       type=str,
                       help='the path to abc file')
parser.add_argument('output_path',
                       metavar='output_folder',
                       type=str,
                       help='the path to mp3 folder')

args = parser.parse_args()

input_path = args.input_path
output_path = args.output_path


filename_no_ext = Path(input_path).stem

info_line_pattern = "^[A-Z]:"

re_info_line = re.compile(info_line_pattern)

commands = []
tunes = []
tune = None

midi_folder = "midi/" + filename_no_ext
mp3s_folder = "mp3s/" + filename_no_ext

Path(midi_folder).mkdir(parents=True, exist_ok=True)
Path(mp3s_folder).mkdir(parents=True, exist_ok=True)

with open(input_path, "r") as f:

    lines = f.readlines()

    for line in lines:

        if re_info_line.match(line):
            if line.startswith("X:"):
                if tune is not None:
                    tunes.append(tune)
                    abc_path = input_path
                    midi_path = "{midi_folder}/{X}.mid".format(midi_folder=midi_folder,X=tune["X"]) 
                    raw_wav_path = "{mp3s_folder}/{X}.raw.wav".format(mp3s_folder=mp3s_folder,X=tune["X"])
                    wav_path = "{mp3s_folder}/{X}.wav".format(mp3s_folder=mp3s_folder,X=tune["X"])
                    mp3_path = "{mp3s_folder}/{X}-{tune_title}.mp3".format(mp3s_folder=mp3s_folder,X=str(int(tune["X"])).zfill(3),tune_title=tune["T"].replace(" ","_").replace("'","").replace(",","").replace("(","").replace(")","") )
                    abc_to_midi = "abc2midi {abc_path} {X} -o {midi_path} -Q 150".format(abc_path=abc_path, midi_path=midi_path,X=tune["X"])
                    mid_to_wave = "timidity {midi_path} -Ow -o {raw_wav_path}".format(midi_path=midi_path,raw_wav_path=raw_wav_path)
                    remove_silence = "sox {raw_wav_path} {wav_path} silence 1 0.1 1% -1 0.1 1%".format(raw_wav_path=raw_wav_path,wav_path=wav_path)
                    wav_to_mp3 = "lame {wav_path} -b 64 {mp3_path}".format(wav_path=wav_path,mp3_path=mp3_path)
                    remove_raw_wav = "rm {raw_wav_path}".format(raw_wav_path=raw_wav_path)
                    remove_wav = "rm {wav_path}".format(wav_path=wav_path)
                    remove_mid = "rm {midi_path}".format(midi_path=midi_path)
                    commands.extend([abc_to_midi, mid_to_wave,remove_silence,wav_to_mp3,remove_mid,remove_raw_wav,remove_wav])
                tune = {}

            arr = line.split(":")
            key = arr[0].strip()
            value = arr[1].strip()

            tune[key] = value

import subprocess

for command in commands:

    print(command)
    out = subprocess.Popen(command.split(" "), 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)

    stdout,stderr = out.communicate()
    print(stdout)
    print(stderr)

#    with open(command_path,'w') as command_file:
#        commands = map(lambda x: x + '\n', commands)
#        command_file.writelines(commands)
