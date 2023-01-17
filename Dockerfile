FROM pypy:3

WORKDIR /usr/src/app

RUN apt-get update &&\
    apt install build-essential libuv1-dev libssl-dev -y &&\
    pip install --no-cache-dir socketify pydantic pydantic-factories ujson && \
    apt-get remove -y --purge build-essential && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000

CMD [ "pypy3", "./app.py" ]
