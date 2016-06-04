import os
from slackclient import SlackClient

# TODO(julien) Ask DevOps to configure this environment variable in live environment.
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
slack_client = SlackClient(SLACK_BOT_TOKEN)


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
        icon_emoji=':flag-jp:'
    )


def get_private_channel(user_id):
    private_channel = slack_client.api_call("im.open", user=user_id)
    if private_channel.get('ok'):
        return private_channel['channel']['id']
    else:
        return None


def main():
    pass
    #print(get_private_channel('U1E5R1QKA'))
    # print slack_client.api_call("users.list")['members'][0]
    #send_message("D1E5RD1RN","haha!")

if __name__ == '__main__':
    main()
