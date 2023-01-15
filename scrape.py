import requests
from bs4 import BeautifulSoup
import pprint

def show_hn(pages):
    hn = []
    for p in range(1, pages+1):
        res = requests.get(f'https://news.ycombinator.com/news?p={p}')
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.titleline > a')
        subtext = soup.select('.subtext')
        hn.append(create_custom_hn(links, subtext))

    flat_hn = [item for sublist in hn for item in sublist]
    pprint.pprint(sort_stories_by_votes(flat_hn))


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k:k['votes'], reverse=True)

def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return hn

show_hn(1)