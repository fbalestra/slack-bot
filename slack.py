import os
from slackclient import SlackClient

# TODO(julien) Ask DevOps to configure this environment variable in live environment.
SLACKBOT_TOKEN = os.environ.get('SLACK_TOKEN')
slack_client = SlackClient(SLACKBOT_TOKEN)


def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call.get('ok'):
        return channels_call['channels']
    return None


def send_message(channel_id, message, attachments=None):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='julien test',
        attachments=attachments,
        icon_emoji=':stitch:'
    )


def channel_info(channel_id):
    channel_info = slack_client.api_call("channels.info", channel=channel_id)
    if channel_info:
        return channel_info['channel']
    return None


def list_print_channels():
    channels = list_channels()
    if channels:
        print("Channels: ")
        for channel in channels:
            print(channel['name'] + " (" + channel['id'] + ")")
            detailed_info = channel_info(channel['id'])
            if detailed_info:
                print('Latest text from ' + channel['name'] + ":")
                print(detailed_info['purpose']['value'])
            if channel['name'] == 'julien_api_tests':
                send_message(channel['id'], "Hello " +
                             channel['name'] + "! It worked!")
        print('-----')
    else:
        print("Unable to authenticate.")


def main():
    pass

if __name__ == '__main__':
    main()
