import os
import requests
import json
from slackclient import SlackClient

# TODO(julien) Ask DOps to configure this environment variable in live environment.
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

slack_client = SlackClient(SLACK_BOT_TOKEN)


def get_slack_token(code):
    if code:
        payload = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code
        }

        response = requests.post('https://slack.com/api/oauth.access', data=payload)

        result = response.json()

        # if result['error'] == 'invalid_client_id':
        #    print('client_id: '+CLIENT_ID)

        return result

    return "Something wrong with get_slack_token"


def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call.get('ok'):
        return channels_call['channels']
    return None


def send_message(channel_id, message, attachments=None):
    return slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='julien test',
        attachments=attachments,
        icon_emoji=':sleuth_or_spy:'
    )


def get_private_channel(user_id):
    private_channel = slack_client.api_call("im.open", user=user_id)
    if private_channel.get('ok'):
        return private_channel['channel']['id']
    else:
        return None


def notify_pending_cweekly(stale_lps):

    buttons = [
        {
            "name": 'notifysts',
            "text": 'notify STs',
            "type": "button",
            "value": "ende"
         }
    ]

    # buttons = []

    # for k, v in stale_lps.items():
    #     button = {
    #         "name": k,
    #         "text": k+': '+v,
    #         "type": "button",
    #         "value": "ende"
    #     }
    #
    #     buttons.append(button)

    attachments = [
            {
                "text": "",
                "fallback": "Unable to notify STs",
                "callback_id": "cweekly",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": buttons
            }
        ]

    attachments = json.dumps(attachments)

    print(send_message("#general", stale_lps, attachments))


def main():
    pass

if __name__ == '__main__':
    main()
