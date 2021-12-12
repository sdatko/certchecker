FROM ubuntu:20.04
COPY . /certchecker/
RUN apt-get update && \
    apt-get --assume-yes dist-upgrade && \
    DEBIAN_FRONTEND=noninteractive \
        apt-get --assume-yes install --no-install-recommends \
        git \
        locales \
        libnotify-bin \
        python3-minimal \
        python3-pip \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    locale-gen 'en_US.UTF-8' && \
    pip3 install --no-cache-dir /certchecker/
ENV LC_ALL='en_US.UTF-8' \
    LANG='en_US.UTF-8' \
    LANGUAGE='en_US.UTF-8'
CMD ["certchecker"]
