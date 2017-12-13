FROM python:3
WORKDIR /usr/src/app
ADD . .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./bot.py" ]
