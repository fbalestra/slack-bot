import os, requests, slack

ms_username = os.environ.get('MS_USERNAME')
ms_password = os.environ.get('MS_PASSWORD')


def api_call(url_end='',payload={}):
    url = 'https://cloud.memsource.com/web/' + url_end

    return requests.get(url, params=payload).json()


def check_remaining_active(token):
    response = api_call('api/v2/user/getLimits', {'token': token})

    pjm_remaining = response['userCounts']['PROJECT_MANAGER']['max'] - response['userCounts']['PROJECT_MANAGER']['used']
    users_remaining = response['userCounts']['LINGUIST']['max'] - response['userCounts']['LINGUIST']['used']

    if pjm_remaining <= 2:
        slack.send_message('#general', "Only %s PjM account(s) remaining" % pjm_remaining)


def main():

    token = api_call('api/v3/auth/login', {'userName': ms_username, 'password': ms_password})['token']

    check_remaining_active(token)

if __name__ == '__main__':
    main()