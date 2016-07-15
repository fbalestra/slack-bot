from __future__ import print_function
import os, re, slack
from queryjob import check_job, build_reply
from flask import Flask, request, Response

app = Flask(__name__)

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')


@app.route('/auth', methods=['POST', 'GET'])
def auth():

    if request.args.get('code'):
        code = request.args.get('code')
    else:
        return Response('No code.'), 401

    print("code: "+code)

    response = slack.get_slack_token(code)

    print("slack response: {0}".format(response))

    return Response(), 200


@app.route('/slack', methods=['POST', 'GET'])
def inbound():
    if request.form.get('token') != SLACK_TOKEN:
        return Response(), 403

    username = request.form.get('user_name')
    user_id = request.form.get('user_id')
    channel_id = slack.get_private_channel(user_id)
    text = str(request.form.get('text'))

    m = re.match(r'(\d+)', text)

    if m:
        job_id = int(m.group(1))

        print (slack.send_message(channel_id, "_Please wait a moment, %s. I am checking *%d_" % (username, job_id)))

        # TODO (julien) find a way to reply to Slack immediately and continue after
        # Response("Got it!"), 200

        job = check_job(job_id)
        message, attachments = build_reply(job)
        slack.send_message(channel_id, message, attachments)
        # TODO (julien) work on daemon + threads
        # checker.add(job)
    else:
        slack.send_message(channel_id, "It looks like you did not enter a valid id")
        return Response('unrecognized parameter'), 400
    return Response(), 200


@app.route('/cweekly', methods=['POST', 'GET'])
def cweekly():

    print('Cataweekly: {0}'.format(request.form.get('stale_lps')))

    slack.notify_pending_cweekly(request.form.get('stale_lps'))

    return Response('Cweekly request received.'), 200


@app.route('/button', methods=['POST', 'GET'])
def button():
    print ('Button pressed :D')

    return Response('Button pressed!!!'), 200

if __name__ == "__main__":
    app.run(debug=True)