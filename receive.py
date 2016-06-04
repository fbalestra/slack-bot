from __future__ import print_function

import os
import re
import json

from flask import Flask, request, Response
import slack

app = Flask(__name__)

# TODO(julien) Ask DevOps to configure this environment variable in live environment.
SLACK_TOKEN = os.environ.get('SLACK_TOKEN')

@app.route('/', methods=['POST', 'GET'])
def inbound():
    print (request.path)

    if request.form.get('token') != SLACK_TOKEN:
        print("no :(\nrequest: " + request.form.get('token'))
        print("actual: " + SLACK_TOKEN)
        return Response(), 403

    channel_id = request.form.get('channel_id')
    username = request.form.get('user_name')
    user_id = request.form.get('user_id')
    text = request.form.get('text')

    # previous version with bot reactin to keyword
    # m = re.match(r'track (\d+)', text)
    m = re.match(r'(\d+)', text)
    if m:
        job_id = int(m.group(1))
        slack.send_message(channel_id,
                "wait a moment, %s. I'm checking *%d" % (username, job_id))
        #job = check_job(job_id)
        message = "Received message: " + str(job_id)
        slack.send_message(channel_id, message)
    else:
        slack.send_message(channel_id, "I don't know what to do :(")
        return Response('unrecognized command'), 400
    return Response(), 200


"""
@app.route('/', methods=['POST', 'GET'])
def status():
    print (request.form.get('token'))
    #print(request.form.get('text'))
    return Response('It works!')
"""

if __name__ == "__main__":
    app.run(debug=True)
