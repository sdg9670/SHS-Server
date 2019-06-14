# -*- coding: utf-8 -*-

import wikipediaapi


class WikiCrawler:
    def __init__(self):
        self.wiki = wikipediaapi.Wikipedia('ko', extract_format=wikipediaapi.ExtractFormat.WIKI)

    def get(self, text):
        p_wiki = self.wiki.page(text)

        data = None
        if p_wiki.exists():
            print(p_wiki.text)
            divide = p_wiki.text.split('.')
            data = divide[0].strip() + '. '
            if len(divide) >=2 :
                data += divide[1].strip() + '. '
            if len(divide) >= 3:
                data += divide[2].strip() + '.'
        return data

