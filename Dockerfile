FROM ubuntu:22.04
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONIOENCODING=UTF-8
RUN apt update
RUN apt-get install -y abcm2ps timidity tclsh lame sox python3 nano ghostscript imagemagick build-essential unzip wget

# Download and install latest abcMIDI
RUN wget https://ifdo.ca/~seymour/runabc/abcMIDI-2026.02.18.zip && \
    unzip abcMIDI-2026.02.18.zip && \
    cd abcmidi && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf abcmidi abcMIDI-2026.02.18.zip

RUN cd "$(dirname $(which python3))" && ln -s idle3 idle \
    && ln -s pydoc3 pydoc \
    && ln -s python3 python \
    && ln -s python3-config python-config
COPY dependencies/*.sf2 /usr/share/sound/soundfonts/
COPY dependencies/*.otf /root/.fonts/
COPY scripts/ /scripts/
WORKDIR /scripts
ENV ABC_FONTS_PATH=/root/.fonts
