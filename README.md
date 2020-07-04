# ABC Docker

Docker image including tools to work with ABC music notation

## Docker

Build Locally
`docker build . -t abc`

Run From Local Build
`docker run -it -v ${PWD}/abcs:/abcs/ -v ${PWD}/mp3s:/mp3s/ -v ${PWD}/pdfs:/pdfs/ abc bash`



### Create PDF file

`ABC_FILENAME=tunes` where tunes.abc is an ABC file in the `abcs` folder
This will create a file name `tunes.pdf` in the `pdfs` folder

`docker run -it -v ${PWD}/abcs:/abcs/ -v ${PWD}/mp3s:/mp3s/ -v ${PWD}/pdfs:/pdfs/  --env ABC_FILENAME=tunes abc ./create_pdf.sh`


### Create MP3 file

Pass in abc path (relative to scripts folder) e.g. `../abc/tunes.abc and then mp3s will be created in the `mp3s` folder with one mp3 file for each tune in the abc file

`docker run -it -v ${PWD}/abcs:/abcs/ -v ${PWD}/mp3s:/mp3s/ -v ${PWD}/pdfs:/pdfs/ abc python generate_mp3.py ../abcs/tunes.abc ../mp3s`


### Create CSV file

Pass in abc path (relative to scripts folder) e.g. `../abc/tunes.abc` and then CSV will be created in csvs folder i.e. `../csvs/tunes.csv`

`docker run -it -v ${PWD}/abcs:/abcs/  -v ${PWD}/csvs:/csvs/  abc python generate_csv.py ../abcs/inventions.abc ../csvs/inventions.csv`

