import re
import string
from collections import defaultdict

from lxml import html as ht

from .charset_detect import chaset_detect

whitespace = re.compile(rf'[{string.whitespace}]{{2,}}')
punctuation = re.compile(r'[,.«»]+')
blank_text = re.compile(rf'^[{string.whitespace}]+$')


def get_description(html):
    """Описание фильма"""
    description = dict()
    try:
        desc = html.xpath('.//div[@itemprop="description"]')[0].text
        desc = re.sub(rf'[{string.whitespace}]{{2,}}', ' ', desc)
        description['описание'] = [desc]
        return description
    except IndexError as e:
        # print(filename, '\n', str(e))
        return ''


def reformat_string(text):
    new_string = []
    for txt in text:
        txt = txt.replace('\n', '').strip()
        txt = whitespace.sub(' ', txt)
        txt = punctuation.sub('', txt)
        txt = blank_text.sub('', txt)
        if txt:
            if 'var' not in txt and txt != 'слова':
                new_string.append(txt)
    return new_string


def get_info(html):
    """Информация о фильме: режиссер, композитор, сборы и т.д."""
    try:
        info_dict = defaultdict(list)
        info_table = html.xpath('.//table[@class="info"]')[0]
        trs = info_table.xpath('.//tr')
        for tr in trs:
            tds = tr.xpath('.//td')
            key = tds[0].text.strip()
            values = reformat_string(tds[1].xpath('descendant-or-self::text()'))
            info_dict[key] = values
        return info_dict
    except IndexError as e:
        # print(filename, '\n', str(e))
        return ''


def parse_file(filename):
    info = defaultdict(dict)
    html_parser = ht.HTMLParser(encoding=chaset_detect(filename))
    html = ht.parse(filename, parser=html_parser).getroot()
    title = html.xpath('.//title')[0].text
    title = re.match(r'^([^—]+) —.*', title).group(1)
    info[title].update(get_info(html))
    info[title].update(get_description(html))
    return info


if __name__ == '__main__':
    import os
    import sys

    parse_file(os.path.abspath(sys.argv[1]))
