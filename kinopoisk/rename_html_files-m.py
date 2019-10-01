"""
Переименовывает сохраненные html-страницы в зависимости от тега <title> в этой странице.
Так же находит название файла изображения постера к фильму. Создает json-файл с данными о
постере и названии фильма.

Используется модуль multiprocessing. Создается несколько процессов. Количество процессов можно
задать с помощью переменной count.
"""

import multiprocessing
import os
import re
import sys

from lxml import html as ht

from .charset_detect import chaset_detect


class Worker(multiprocessing.Process):

    def __init__(self, work_queue):
        super(Worker, self).__init__()
        self.work_queue = work_queue
        self.daemon = True
        self.sub = re.compile(r'([^—]+) —.*')

    def run(self) -> None:
        while True:
            try:
                filename = self.work_queue.get()
                self.process(filename)
            finally:
                self.work_queue.task_done()

    def process(self, filename):
        try:
            parser = ht.HTMLParser(encoding=chaset_detect(filename))
            root = ht.parse(filename, parser=parser).getroot()
            title = self.get_page_title(root)
            print(title)
            self.rename_file(filename, title)
        except Exception as e:
            sys.stderr.write(str(e))

    def get_page_title(self, root_tag):
        title = root_tag.xpath('//title')[0].text
        title = self.sub.search(title).group(1)
        return title

    def rename_file(self, old_filename, new_filename):
        path = os.path.dirname(old_filename)
        os.rename(old_filename, os.path.join(path, new_filename + '.html'))


def main(path=None):
    if not path:
        path = '/home/alexandr/PycharmProjects/parsing_k_poisk/src/html_pages'
    else:
        path = os.path.abspath(path)
    work_queue = multiprocessing.JoinableQueue()

    # количество процессов
    count = 5

    for i in range(count):
        worker = Worker(work_queue)
        worker.start()

    for file in os.listdir(path):
        if file.endswith('.html'):
            work_queue.put(os.path.join(path, file))

    work_queue.join()


if __name__ == '__main__':
    from datetime import datetime

    t1 = datetime.now()
    main()
    t2 = datetime.now()
    print(t1, t2)
