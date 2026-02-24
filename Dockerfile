FROM ubuntu:22.04
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONIOENCODING=UTF-8
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt-get install -y abcm2ps timidity tclsh lame sox python3 nano ghostscript imagemagick build-essential git

# Download and install latest abcMIDI from GitHub
RUN git clone https://github.com/sshlien/abcmidi.git && \
    cd abcmidi && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf abcmidi

RUN cd "$(dirname $(which python3))" && ln -s idle3 idle \
    && ln -s pydoc3 pydoc \
    && ln -s python3 python \
    && ln -s python3-config python-config
COPY dependencies/*.sf2 /usr/share/sound/soundfonts/
COPY dependencies/*.otf /root/.fonts/
COPY scripts/ /scripts/
RUN chmod +x /scripts/*.sh && chmod +x /scripts/action_entrypoint.py
WORKDIR /scripts
ENV ABC_FONTS_PATH=/root/.fonts
ENTRYPOINT ["/scripts/action_entrypoint.py"]
