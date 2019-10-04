import json
import multiprocessing
import os
import tempfile

from .get_info_about_films import parse_file


class Worker(multiprocessing.Process):
    def __init__(self, work_queue, results_queue):
        super(Worker, self).__init__()
        self.work_queue = work_queue
        self.results_queue = results_queue
        self.daemon = True

    def run(self) -> None:
        while True:
            try:
                filename = self.work_queue.get()
                self.process(filename)
            finally:
                self.work_queue.task_done()

    def process(self, filename):
        info = parse_file(filename)
        self.results_queue.put(info)


def get_results(results_queue, filename):
    results_dict = dict()
    while True:
        result = results_queue.get()
        if result is None:
            break
        results_dict.update(result)
        results_queue.task_done()
    with open(filename, 'w') as f:
        json.dump(results_dict, f, ensure_ascii=False, indent=4, sort_keys=True)
    results_queue.task_done()


def main(path=None):
    if not path:
        path = '/home/alexandr/PycharmProjects/parsing_k_poisk/src/html_pages'
    else:
        path = os.path.abspath(path)
    _, tmpfile = tempfile.mkstemp(prefix='kinopoisk-', suffix='.json', text=True)
    work_queue = multiprocessing.JoinableQueue()
    results_queue = multiprocessing.JoinableQueue()
    count = 5

    results_process = multiprocessing.Process(target=get_results, args=(results_queue, tmpfile))
    results_process.daemon = True
    results_process.start()

    for i in range(count):
        worker = Worker(work_queue, results_queue)
        worker.start()

    for filename in os.listdir(path):
        if filename.endswith('.html'):
            work_queue.put(os.path.join(path, filename))

    work_queue.join()
    results_queue.put(None)
    results_queue.join()

    # os.remove(tmpfile)


if __name__ == '__main__':
    from datetime import datetime

    t1 = datetime.now()
    main()
    t2 = datetime.now()
    print(t1, t2)
