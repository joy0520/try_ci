import argparse
import logging
import os
from multiprocessing import Process, Queue
from typing import List

from logging_util.setup_logging import setup_logging
from process.num_catcher import NumCatcher
from process.num_thrower import NumThrower

logger = logging.getLogger()

parser = argparse.ArgumentParser()
parser.add_argument('-w', '--work-path')


class App:
    LOG_NAME = 'app.log'

    def __init__(self, args: argparse.Namespace):
        self.work_path = args.work_path

        self.processes: List[Process] = list()

        log_path = os.path.join(self.work_path, self.LOG_NAME)
        setup_logging(log_path)

    def run(self):
        try:
            num_q = Queue()

            self.processes.append(NumCatcher(num_q))
            self.processes.append(NumThrower(num_q))

            for p in self.processes:
                p.start()

            for p in self.processes:
                p.join()

        except KeyboardInterrupt:
            for p in self.processes:
                p.terminate()

        logger.warning('Closing all sub-processes.')


if __name__ == '__main__':
    app = App(parser.parse_args())
    app.run()
