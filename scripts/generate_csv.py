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
                       metavar='output_path',
                       type=str,
                       help='the path to csv file')
#parser.add_argument('command_path',
#                       metavar='command_path',
#                       type=str,
#                       help='the path to csv file')
args = parser.parse_args()

input_path = args.input_path
output_path = args.output_path
#command_path = args.command_path

filename_no_ext = Path(input_path).stem

info_line_pattern = "^[A-Z]:"

re_info_line = re.compile(info_line_pattern)

#commands = ["abc2midi {filename}.abc -Q 150".format(filename=filename_no_ext)]
tunes = []
tune = None
with open(input_path, "r") as f:

    lines = f.readlines()

    for line in lines:

        if re_info_line.match(line):
            if line.startswith("X:"):
                if tune is not None:
                    tunes.append(tune)
                    #mid_to_wave = "timidity {filename}{X}.mid -Ow -o {filename}{X}.raw.wav".format(filename=filename_no_ext,X=tune["X"])
                    #remove_silence = "sox {filename}{X}.raw.wav {filename}{X}.wav silence 1 0.1 1% -1 0.1 1%".format(filename=filename_no_ext,X=tune["X"])
                    #wav_to_mp3 = "lame {filename}{X}.wav -b 64 {tune_title}.mp3".format(filename=filename_no_ext,X=tune["X"],tune_title=tune["T"].replace(" ","_").replace("'","").replace(",","").replace("(","").replace(")",""))
                    #remove_raw_wav = "rm {filename}{X}.raw.wav".format(filename=filename_no_ext,X=tune["X"])
                    #remove_wav = "rm {filename}{X}.wav".format(filename=filename_no_ext,X=tune["X"])
                    #remove_mid = "rm {filename}{X}.mid".format(filename=filename_no_ext,X=tune["X"])
                    #commands.extend([mid_to_wave,remove_silence,wav_to_mp3,remove_mid,remove_raw_wav,remove_wav])
                tune = {}

            arr = line.split(":")
            key = arr[0].strip()
            value = arr[1].strip()

            tune[key] = value

    #keys = tunes[0].keys()
    keys = ["X","R","T","G","K","M","L","Q","E","I","C","S","Z","F","O","B","N","P","D","H","W","A"]
    with open(output_path, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(tunes)

#    with open(command_path,'w') as command_file:
#        commands = map(lambda x: x + '\n', commands)
#        command_file.writelines(commands)
