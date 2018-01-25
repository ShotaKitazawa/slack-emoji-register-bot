FROM python:3
WORKDIR /usr/src/app
ADD . .
RUN pip install --no-cache-dir -r requirements.txt
RUN cat << _EOF_ > rtmbot.conf
DEBUG: True
SLACK_TOKEN: $SLACK_TOKEN
ACTIVE_PLUGINS:
    - src.plugins.FileUploadPlugin
    - src.plugins.URLUploadPlugin
    - src.plugins.SearchPlugin
_EOF_
CMD [ "rtmbot" ]
