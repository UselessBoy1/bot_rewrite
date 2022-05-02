import typing
import requests

class SearchResult:
    def __init__(self, vid, title, author):
        self.vid = vid
        self.title = title
        self.author = author

HEADERS = {
    'authority': 'invidious.snopyta.org',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Mobile Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7'
}

def search(title) -> typing.Optional[SearchResult]:
    response = requests.get(f"https://invidious.snopyta.org/api/v1/search?q={title}&fields=type,title,videoId,author", headers=HEADERS)
    json = response.json()
    for film in json:
        if film['type'] == 'video':
            return SearchResult(film['videoId'], film['title'], film['author'])
    return None


def get_formats(search_results: SearchResult) -> dict:
    response = requests.get(f"https://invidious.snopyta.org/api/v1/videos/{search_results.vid}?fields=adaptiveFormats", headers=HEADERS)
    return response.json()['adaptiveFormats']

def get_format(search_results: SearchResult):
    af = get_formats(search_results)
    for f in af:
        if f['encoding'] == 'opus':
            return f
    return af[0]