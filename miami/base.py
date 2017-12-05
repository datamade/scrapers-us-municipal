from pupa.scrape import Scraper

import requests

import lxml.html



class ToArabic(str):
    '''
    From: https://gist.github.com/riverrun/ac91218bb1678b857c12
    '''
    def __init__(self, roman):
        roman = self.check_valid(roman)
        keys = ['IV', 'IX', 'XL', 'XC', 'CD', 'CM', 'I', 'V', 'X', 'L', 'C', 'D', 'M']
        to_arabic = {'IV': '4', 'IX': '9', 'XL': '40', 'XC': '90', 'CD': '400', 'CM': '900',
                'I': '1', 'V': '5', 'X': '10', 'L': '50', 'C': '100', 'D': '500', 'M': '1000'}

        for key in keys:
            if key in roman:
                roman = roman.replace(key, ' {}'.format(to_arabic.get(key)))

        self.arabic = sum(int(num) for num in roman.split())

    def check_valid(self, roman):
        roman = roman.upper()
        invalid = ['IIII', 'VV', 'XXXX', 'LL', 'CCCC', 'DD', 'MMMM']
        if any(sub in roman for sub in invalid):
            raise ValueError('Numerus invalidus est: {}'.format(roman))

        return roman


class MiamiScraper(Scraper, requests.Session):

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.timeout = 600

    def lxmlize(self, url, payload=None):
        if payload :
            response = self.post(url, payload, verify=False)
        else :
            response = self.get(url, verify=False)
        entry = response.text
        page = lxml.html.fromstring(entry)
        page.make_links_absolute(url)
        return page
