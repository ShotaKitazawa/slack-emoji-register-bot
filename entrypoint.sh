#!/usr/bin/env sh

if [ ${SLACK_TOKEN-undef} != 'undef' ]; then
    cat << _EOF_ > rtmbot.conf
DEBUG: True
SLACK_TOKEN: "$SLACK_TOKEN"
ACTIVE_PLUGINS:
    - src.plugins.FileUploadPlugin
    - src.plugins.URLUploadPlugin
    - src.plugins.SearchPlugin
    - src.plugins.HelpDisplayPlugin
_EOF_
    if [ $EXIST_HTTPS_SERVER ]; then
      echo "    - src.plugins.SearchAndChoosePlugin" >> rtmbot.conf
    fi
    rtmbot
else
    echo "env SLACK_TOKEN is not set. Exit."
    exit 64
fi
