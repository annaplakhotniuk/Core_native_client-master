# Base image with Ubuntu and Python 3.10
#FROM ubuntu:latest

# Set environment variables
#ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
#RUN apt-get update \
#    && apt-get install -y python3.10 \
#                          python3-pip \
#                          chromium-browser \
#                          xvfb \
#                          x11vnc \
#                          openbox \
#                          xterm \
#                          tesseract-ocr \
#                          tesseract-ocr-eng \
#                          tesseract-ocr-all \
#                          libgl1-mesa-glx \
#                          remmina \
#                          remmina-plugin-rdp \
#                          xserver-xorg-video-dummy \
#                          x11-xserver-utils \
#                          menu \
#                          libx11-dev \
#                          libxtst-dev \
#                          libpng-dev

# Set up Xvfb and X11vnc
#RUN Xvfb :0 -screen 0 1920x1080x24 > /dev/null 2>&1 &
#RUN x11vnc -display :0 -nopw -listen localhost -xkb -ncache 10 -ncache_cr -forever > /dev/null 2>&1 &

# Set up Openbox
#RUN echo 'exec openbox-session' > ~/.xinitrc

# Set the working directory
#WORKDIR /home/user/PycharmProjects/Test_Native_Client

# Copy the test files
#COPY . /home/user/PycharmProjects/Test_Native_Client

# Install Python dependencies
#RUN pip3 install --no-cache-dir -r requirements.txt

# Expose VNC and X11 ports
#XPOSE 5900
#EXPOSE 6000

# Start Xvfb and openbox when the container starts
#CMD Xvfb :0 -screen 0 1920x1080x24 > /dev/null 2>&1 & openbox --replace

# Base image with Ubuntu Mate
FROM ubuntu:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
RUN apt-get update && apt-get install -y ubuntu-mate-desktop \
                                                    x11vnc \
                                                    xvfb \
                                                    python3.10 \
                                                    python3-pip \ 
                                                    chromium-browser \
                                                    remmina \ 
                                                    remmina-plugin-rdp \ 
                                                    caja

# Set the working directory
WORKDIR /home/user/PycharmProjects/Test_Native_Client

# Copy the test files
COPY . /home/user/PycharmProjects/Test_Native_Client


# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Set up Xvfb and X11vnc
RUN Xvfb :0 -screen 0 1920x1080x24 > /dev/null 2>&1 &
RUN x11vnc -display :0 -nopw -listen localhost -xkb -ncache 10 -ncache_cr -forever > /dev/null 2>&1 &

# Expose VNC port
EXPOSE 5900

# Start Xvfb and Mate desktop when the container starts
CMD Xvfb :0 -screen 0 1920x1080x24 > /dev/null 2>&1 & mate-session