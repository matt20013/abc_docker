# ABC Docker

Docker image including tools to work with ABC music notation

## Docker

Build Locally
`docker build . -t abc`

Run From Local Build
`docker run -it -v ${PWD}/abcs:/abcs/ -v ${PWD}/mp3s:/mp3s/ -v ${PWD}/pdfs:/pdfs/ abc bash`



Create PDF file

`ABC_FILENAME=tunes` where tunes.abc is an ABC file in the `abcs` folder
This will create a file name `tunes.pdf` in the `pdfs` folder

`docker run -it -v ${PWD}/abcs:/abcs/ -v ${PWD}/mp3s:/mp3s/ -v ${PWD}/pdfs:/pdfs/ -v ${PWD}/scripts:/scripts/ --env ABC_FILENAME=tunes abc ./create_pdf.sh`


