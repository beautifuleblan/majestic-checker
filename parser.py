from json import loads
from user_agents import random as random_useragent
import requests
from bs4 import BeautifulSoup

def get_site_content(proxy, proxy_type, domain):
    proxy_formatted = {}

    if len(proxy) == 4:
        proxy_formatted['http'] = proxy_formatted['https'] = \
            f'{proxy_type.lower()}://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}'
    else:
        proxy_formatted['http'] = proxy_formatted['https'] = f'{proxy_type.lower()}://{proxy[0]}:{proxy[1]}'

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
                  ',application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'user-agent': random_useragent(),
        'upgrade-insecure-requests': '1',
        'referer': 'https://majestic.com/'
        }

    formatted_domain = domain.split('//')[-1].split('/')[0]
    params = {'q': formatted_domain,
              'defaultQ': 'brightonseo.com'}

    result = {'citationFlow': None,
              'trustFlow': None,
              'error': None}
    try:
        with requests.Session() as session:
            session.proxies = proxy_formatted
            session.headers = headers
            session.params = params

            r = session.get('https://majestic.com/reports/site-explorer-search')
            match r.status_code:
                case 200:
                    result['citationFlow'], result['trustFlow'], result['error'] = retrieve_site_metrics(r.text)
                case 429:
                    result['error'] = 'Request limit reached, change proxy'
                case _:
                    result['error'] = 'Unknown error. Status code: ' + str(r.status_code)
    except Exception as e:
        result['error'] = type(e).__name__
    return result

def retrieve_site_metrics(html):
    soup = BeautifulSoup(html, 'html.parser')
    passtrough = soup.find('div', id='js-passthrough')

    if passtrough and (data := passtrough.get('data-index-item-info')):
        data = loads(data)
        return data['citationFlow'], data['trustFlow'], None
    return None, None, 'No data found'