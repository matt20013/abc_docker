FROM ubuntu:22.04
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONIOENCODING=UTF-8
RUN apt update
RUN apt-get install -y abcm2ps abcmidi timidity tclsh lame sox python3 nano ghostscript imagemagick
RUN cd "$(dirname $(which python3))" && ln -s idle3 idle \
    && ln -s pydoc3 pydoc \
    && ln -s python3 python \
    && ln -s python3-config python-config
COPY dependencies/*.sf2 /usr/share/sound/soundfonts/
COPY dependencies/*.otf /root/.fonts/
COPY scripts/ /scripts/
WORKDIR /scripts
ENV ABC_FONTS_PATH=/root/.fonts
