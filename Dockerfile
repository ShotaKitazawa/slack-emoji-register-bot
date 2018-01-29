FROM python:3
WORKDIR /usr/src/app
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir src
WORKDIR /usr/src/app/src
ADD src .
WORKDIR /usr/src/app
ADD build.sh .
RUN chmod 755 build.sh
CMD [ "./build.sh" ]
