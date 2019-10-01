"""
Переименовывает сохраненные html-страницы в зависимости от тега <title> в этой странице.
Так же находит название файла изображения постера к фильму. Создает json-файл с данными о
постере и названии фильма.

Используются потоки.
"""

import collections
import os
import queue
import re
import threading
from datetime import datetime
from pprint import pprint

import chardet
from lxml import html as ht


class Worker(threading.Thread):
    Locker = threading.Lock()

    def __init__(self, work_queue, results_queue):
        super(Worker, self).__init__()
        self.work_queue = work_queue
        self.results_dict = collections.defaultdict(dict)
        self.daemon = True
        self.sub = re.compile(r'([^—]+) —.*')
        self.results_queue = results_queue

    def run(self) -> None:
        while True:
            try:
                filename = self.work_queue.get()
                self.process(filename)
            finally:
                self.work_queue.task_done()

    def process(self, filename):
        try:
            parser = ht.HTMLParser(encoding=self.chaset_detect(filename))
            root = ht.parse(filename, parser=parser).getroot()
            title = self.get_page_title(root)
            img = self.get_image_name(root)
            self.rename_file(filename, title)
            self.results_dict[filename].update(image=img, title=title)
            # with self.Locker:
            #     self.results_dict[filename].update(src=img, title=title)
            self.results_queue.put(self.results_dict)
        except Exception:
            pass

    def get_image_name(self, root_tag):
        imgs = root_tag.xpath('//img[contains(@src, "st.kp.yandex.net/images/sm_film/")]')
        return os.path.basename(imgs[0].get('src')) if imgs else ''

    def get_page_title(self, root_tag):
        title = root_tag.xpath('//title')[0].text
        title = self.sub.search(title).group(1)
        return title

    def rename_file(self, old_filename, new_filename):
        path = os.path.dirname(old_filename)
        os.rename(old_filename, os.path.join(path, new_filename + '.html'))

    def chaset_detect(self, filename):
        with open(filename, 'rb') as f:
            charset = chardet.detect(f.read())['encoding']
        return charset


def get_results(results_queue, results_dict):
    while True:
        try:
            results_dict.update(results_queue.get())
        finally:
            results_queue.task_done()


def main():
    path = '/home/alexandr/PycharmProjects/parsing_k_poisk/src/html_pages'
    results_dict = collections.defaultdict(dict)
    work_queue = queue.Queue()
    results_queue = queue.Queue()
    count = 3

    results_thread = threading.Thread(target=get_results, args=(results_queue, results_dict))
    results_thread.daemon = True
    results_thread.start()

    for i in range(count):
        worker = Worker(work_queue, results_queue)
        worker.start()

    for file in os.listdir(path):
        if file.endswith('.html'):
            work_queue.put(os.path.join(path, file))
    work_queue.join()
    results_queue.join()
    pprint(dict(results_dict))


def without_threads():
    """поиск названия файла изображения к фильму"""
    path = '/home/alexandr/PycharmProjects/parsing_k_poisk/src/html_pages'
    lst = collections.defaultdict(str)
    for file in os.listdir(path):
        if file.endswith('.html'):
            root = ht.parse(os.path.join(path, file))
            imgs = root.xpath('//img[contains(@src, "st.kp.yandex.net/images/sm_film/")]')
            if imgs:
                lst[file] = os.path.basename(imgs[0].get('src'))
    pprint(dict(lst))


if __name__ == '__main__':
    t1 = datetime.now()
    main()
    t2 = datetime.now()
    print(t1, t2)
