import requests


def fetch_yes_or_no_image():
    """Fetch image from wtf API"""

    return requests.get('https://yesno.wtf/api').json()['image']
