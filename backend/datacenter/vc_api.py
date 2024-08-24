from environs import Env
from requests import get
from urllib.parse import urlparse


def is_shorten_url(url):
    return 'vk.cc' in url


def get_shortened_link(token, url):
    payload = {'v': '5.199', 'access_token': token, 'url': url}
    response = get('https://api.vk.ru/method/utils.getShortLink',
                            params=payload)
    response.raise_for_status()

    short_url = response.json()['response']['short_url']

    return short_url


def get_link_click_count(token, url):
    payload = {
    	'v': '5.199',
    	'access_token': token,
    	'key': url,
        'interval': 'week'
    }
    response = get('https://api.vk.ru/method/utils.getLinkStats',
                            params=payload)
    response.raise_for_status()

    if len(response.json()['response']['stats']) > 0:
        click_count = response.json()['response']['stats'][0]['views']
    else:
        click_count = 0
    
    return click_count


def get_short_link_and_click_count(url: str):
    env = Env()
    env.read_env()
    token = env.str('VK_TOKEN')
    
    if not is_shorten_url(url):
        url = get_shortened_link(token, url)
    
    parsed_url = urlparse(url).path.lstrip('/')
    click_count = get_link_click_count(token, parsed_url)
    
    return url, click_count


# https://metanit.com/python/django/5.14.php - https://vk.cc/czLk7z
# https://docs.djangoproject.com/en/5.0/ref/models/querysets/ - https://vk.cc/czLk8u
# https://docs-python.ru/packages/biblioteka-python-telegram-bot-python/menju-klaviatury/ - https://vk.cc/czJVIu
# https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#the-register-decorator - https://vk.cc/czLcvF