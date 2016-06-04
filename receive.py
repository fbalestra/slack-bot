from __future__ import print_function

import os
import re
import json

from flask import Flask, request, Response
import slack

app = Flask(__name__)

# TODO(julien) Ask DevOps to configure this environment variable in live environment.
SLACK_SLASH_TOKEN = os.environ.get('SLACK_TOKEN')

@app.route('/', methods=['POST', 'GET'])
def inbound():
    if request.form.get('token') != SLACK_SLASH_TOKEN:
        return Response(), 403

    channel_id = request.form.get('channel_id')
    username = request.form.get('user_name')
    user_id = request.form.get('user_id')
    text = str(request.form.get('text'))

    print ("channel id: " + channel_id)

    # previous version with bot reacting to keyword
    # m = re.match(r'track (\d+)', text)
    m = re.match(r'(\d+)', text)

    if m:
        job_id = int(m.group(1))
        print (1)
        slack.send_message("#general",
                "wait a moment, %s. I'm checking *%d" % (username, job_id))
        print (2)

        #job = check_job(job_id)
        message = "Received message: " + str(job_id)
        slack.send_message(channel_id, message)
    else:
        slack.send_message(channel_id, "I don't know what to do :(")
        return Response('unrecognized command'), 400
    return Response(), 200
    

if __name__ == "__main__":
    app.run(debug=True)
