import csv
import re
import argparse
import shlex
import subprocess
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

def generate_commands(tune, input_path, midi_folder, mp3s_folder):
    abc_path = input_path
    midi_path = "{midi_folder}/{X}.mid".format(midi_folder=midi_folder,X=tune["X"])
    raw_wav_path = "{mp3s_folder}/{X}.raw.wav".format(mp3s_folder=mp3s_folder,X=tune["X"])
    wav_path = "{mp3s_folder}/{X}.wav".format(mp3s_folder=mp3s_folder,X=tune["X"])
    mp3_path = "{mp3s_folder}/{X}-{tune_title}.mp3".format(mp3s_folder=mp3s_folder,X=str(int(tune["X"])).zfill(3),tune_title=tune["T"].replace(" ","_").replace("'","").replace(",","").replace("(","").replace(")","") )

    abc_to_midi = ["abc2midi", abc_path, tune["X"], "-o", midi_path, "-Q", "150"]
    mid_to_wave = ["timidity", midi_path, "-Ow", "-o", raw_wav_path]
    remove_silence = ["sox", raw_wav_path, wav_path, "silence", "1", "0.1", "1%", "-1", "0.1", "1%"]
    wav_to_mp3 = ["lame", wav_path, "-b", "64", mp3_path]
    remove_raw_wav = ["rm", raw_wav_path]
    remove_wav = ["rm", wav_path]
    remove_mid = ["rm", midi_path]

    return [abc_to_midi, mid_to_wave,remove_silence,wav_to_mp3,remove_mid,remove_raw_wav,remove_wav]


filename_no_ext = Path(input_path).stem

info_line_pattern = "^[A-Z]:"

re_info_line = re.compile(info_line_pattern)

commands = []
tunes = []
tune = None

midi_folder = "/midi/" + filename_no_ext
mp3s_folder = "/mp3s/" + filename_no_ext

Path(midi_folder).mkdir(parents=True, exist_ok=True)
Path(mp3s_folder).mkdir(parents=True, exist_ok=True)

with open(input_path, "r", encoding="utf-8") as f:

    lines = f.readlines()

    for line in lines:

        if re_info_line.match(line):
            if line.startswith("X:"):
                if tune is not None:
                    if "K" in tune:
                        tunes.append(tune)
                        commands.extend(generate_commands(tune, input_path, midi_folder, mp3s_folder))
                tune = {}

            arr = line.split(":")
            key = arr[0].strip()
            value = arr[1].strip()

            tune[key] = value

if tune is not None:
    if "K" in tune:
        tunes.append(tune)
        commands.extend(generate_commands(tune, input_path, midi_folder, mp3s_folder))

for command in commands:

    print(' '.join(shlex.quote(arg) for arg in command))
    out = subprocess.Popen(command,
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)

    stdout,stderr = out.communicate()
    print(stdout)
    print(stderr)

#    with open(command_path,'w') as command_file:
#        commands = map(lambda x: x + '\n', commands)
#        command_file.writelines(commands)
