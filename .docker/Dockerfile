FROM ubuntu:20.04 AS build-deps

RUN apt-get -y update && \
    apt-get install -y --no-install-recommends software-properties-common && \
    add-apt-repository -y ppa:ubuntugis/ppa && \
    apt-get -y update && \
    apt-get install -y --no-install-recommends build-essential ca-certificates cmake \
        doxygen g++ git libeigen3-dev libgdal-dev libpython3-dev python3 python3-pip \
        python3-matplotlib lcov libgtest-dev swig libtbb-dev gdal-bin python3-gdal && \
\
    ln -s /usr/bin/python3 /usr/bin/python && \
    python -m pip install gcovr


FROM build-deps AS f2c

RUN mkdir -p /f2c

COPY ./Fields2Cover /f2c/Fields2Cover

WORKDIR /f2c/Fields2Cover

RUN mkdir -p build && \
    cd build && \
    cmake -DBUILD_PYTHON=ON .. && \
    make -j$(nproc) && \
    make install


FROM f2c AS app

COPY ./src /src
COPY --from=f2c /usr/local /usr/local

CMD /src/server.py
