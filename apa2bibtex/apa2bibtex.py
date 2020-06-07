#!/usr/bin/env python
# -_- coding: utf-8 -_-

import warnings
import sys
import random
from time import sleep

import requests
from bs4 import BeautifulSoup


class NotFoundOnGoogleScholarError(Exception):
    pass


class APA2BibTeX(object):

    def __init__(self, lines):
        self.lines = [line.strip() for line in lines if line.strip()]
        self.s = requests.session()
        agents = ['Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                  'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36',
                  'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246']

        self.s.headers.update({'user-agent': random.choice(agents),
                               'referer': 'https://scholar.google.com/',
                               'sec-fetch-dest': 'document',
                               'sec-fetch-mode': 'navigate',
                               'sec-fetch-site': 'same-origin',
                               'sec-fetch-user': '?1',
                               'upgrade-insecure-requests': '1',
                               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                               'accept-encoding': 'gzip, deflate, br',
                               'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,es;q=0.6,zh-TW;q=0.5',
                               'cache-control': 'no-cache'})

    def get_bibtex(self, line):
        r = self.s.get('https://scholar.google.com/scholar', params={'q': line, 'hl': 'en', 'btnG': '', 'as_sdt': '0,5'})
        soup = BeautifulSoup(r.text, 'html.parser')
        d = soup.find('div', {'class': 'gs_r gs_or gs_scl'})
        try:
            q = 'info:' + d.attrs['data-cid'] + ':scholar.google.com/'
        except AttributeError:
            print(soup)
            raise NotFoundOnGoogleScholarError
        sleep(random.uniform(1, 3))
        nr = self.s.get('https://scholar.google.com/scholar', params={'q': q, 'output': 'cite', 'scirp': 0, 'hl': 'en'})
        soup = BeautifulSoup(nr.text, 'html.parser')

        try:
            url = soup.find('a', string='BibTeX').attrs['href']
        except AttributeError:
            warnings.warn('Hit by anti-crawler policy. Trying again in 10 seconds...')
            sleep(10)
            nr = self.s.get('https://scholar.google.com/scholar', params={'q': q, 'output': 'cite', 'scirp': 0, 'hl': 'en'})
            soup = BeautifulSoup(nr.text, 'html.parser')
            a = soup.find('a', string='BibTeX')
            if a:
                url = soup.find('a', string='BibTeX').attrs['href']
            else:
                raise NotFoundOnGoogleScholarError

        sleep(random.uniform(0.5, 2))
        nr = self.s.get(url)
        return nr.text.encode('utf-8')

    def convert(self):
        self.cites = []
        self.errors = []
        for line in self.lines:
            try:
                bib = self.get_bibtex(line)
                self.cites.append(bib)
                sleep(random.uniform(1, 5))
            except NotFoundOnGoogleScholarError:
                self.errors.append(line)

    def output(self):
        for err in self.errors:
            warnings.warn('No citation found for line "%s"' % err)
        for cite in self.cites:
            print(cite)


def main():
    lines = []
    for line in sys.stdin:
        lines.append(line)
    a = APA2BibTeX(lines)
    a.convert()
    a.output()

if __name__ == '__main__':
    main()
