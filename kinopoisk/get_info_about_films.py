import os
import re
import string
from collections import defaultdict

from lxml import html as ht

from .charset_detect import chaset_detect

whitespace = re.compile(rf'[{string.whitespace}]{{2,}}')
punctuation = re.compile(r'^[,.«»]+|.*«')
blank_text = re.compile(rf'^[{string.whitespace}]+$')


def get_actors_list(html):
    """Актеры и роли дублировали"""
    actors = ''
    dub = ''
    try:
        div = html.xpath('.//div[@id="actorList"]')[0]
        ul = div.xpath('.//ul')
    except IndexError:
        return dict(актеры=actors, дубляж=dub)

    try:
        # список актеров
        actors = ul[0]
        actors = actors.xpath('descendant-or-self::text()')
        actors = reformat_string(actors)
    except IndexError:
        actors = ''

    # дубляж
    try:
        dub = ul[1]
        dub = dub.xpath('descendant-or-self::text()')
        dub = reformat_string(dub)
    except IndexError:
        dub = ""
    return dict(актеры=actors, дубляж=dub)


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
        return dict(описание='')


def get_image_name(html):
    """Название файла изображения постера к фильму"""
    imgs = html.xpath('//img[contains(@src, "st.kp.yandex.net/images/sm_film/")]')
    return dict(image=[os.path.basename(imgs[0].get('src'))]) if imgs else dict(image='')


def reformat_string(text):
    """Обрабатывает список строк из таблицы info"""
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
        info_dict = defaultdict(dict)
        info_table = html.xpath('.//table[@class="info"]')[0]
        trs = info_table.xpath('.//tr')
        for tr in trs:
            tds = tr.xpath('.//td')
            key = tds[0].text.strip()
            values = reformat_string(tds[1].xpath('descendant-or-self::text()'))
            info_dict['about'].update({key: values})
        return info_dict
    except IndexError as e:
        # print(filename, '\n', str(e))
        return dict(about='')


def get_raiting(html):
    div = html.xpath('.//div[@class="criticsRating"]')
    try:
        ratingNum = div.xpath('.//*[@class="ratingNum"')
        ratingNum = reformat_string(ratingNum[0].xpath('descendant-or-self::text()'))
    except IndexError:
        ratingNum = ''
    try:
        star = div.xpath('.//*[@class="star"]')
        star = reformat_string(star[0].xpath('descendant-or-self::text()'))
    except IndexError:
        star = ''
    return dict(рейтинг=ratingNum, критики=star)


def get_facts(html):
    """Факты о фильме"""
    try:
        div = html.xpath('.//div[contains(@class, "triviaBlock fact")]')[0]
        text = div.xpath('descendant-or-self::text()')
        text = [text.strip() for text in text]
        text = [whitespace.sub(' ', text) for text in text]
        text = [blank_text.sub('', text) for text in text]
        text = ' '.join([text for text in text if text])
        text = re.sub(rf' ([{string.punctuation}]+)', r'\1', text)
        return dict(факты=[text])
    except IndexError:
        return dict(факты='')


def get_bloopers(html):
    """Ошибки в фильме"""
    try:
        div = html.xpath('.//div[@class="triviaBlock blooper"]')[0]
        text = div.xpath('descendant-or-self::text()')
        text = [text.strip() for text in text]
        text = [whitespace.sub(' ', text) for text in text]
        text = [blank_text.sub('', text) for text in text]
        text = ' '.join([text for text in text if text])
        text = re.sub(rf' ([{string.punctuation}]+)', r'\1', text)
        return dict(ошибки=[text])
    except IndexError:
        return dict(ошибки='')


def parse_file(filename):
    info = defaultdict(dict)
    html_parser = ht.HTMLParser(encoding=chaset_detect(filename))
    html = ht.parse(filename, parser=html_parser).getroot()
    title = html.xpath('.//title')[0].text
    title = re.match(r'^([^—]+) —.*', title).group(1)

    # сводная информация о фильме
    info[title].update(get_info(html))

    # описание фильма
    info[title].update(get_description(html))

    # название файла изображени постера к фильму
    info[title].update(get_image_name(html))

    # актеры
    info[title].update(get_actors_list(html))

    # факты о фильме
    info[title].update(get_facts(html))

    # ошибки в фильме
    info[title].update(get_bloopers(html))

    return info


if __name__ == '__main__':
    # import os
    import sys

    parse_file(os.path.abspath(sys.argv[1]))
