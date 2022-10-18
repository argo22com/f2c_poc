FROM ubuntu:20.04

RUN apt-get -y update
RUN apt-get install -y --no-install-recommends software-properties-common
RUN add-apt-repository -y ppa:ubuntugis/ppa
RUN apt-get -y update
RUN apt-get install -y --no-install-recommends build-essential ca-certificates cmake \
    doxygen g++ git libeigen3-dev libgdal-dev libpython3-dev python3 python3-pip \
    python3-matplotlib lcov libgtest-dev swig libtbb-dev

RUN ln -s /usr/bin/python3 /usr/bin/python && \
    python -m pip install gcovr

COPY . ./f2c

WORKDIR /f2c/Fields2Cover

RUN mkdir -p build && \
    cd build && \
    cmake -DBUILD_PYTHON=ON .. && \
    make -j$(nproc) && \
    make install

CMD ../test.py
