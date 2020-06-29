import logging
import random
import time
from multiprocessing import Process, Queue

logger = logging.getLogger()


class NumThrower(Process):
    def __init__(self, num_q: Queue):
        super().__init__(daemon=True, name=self.__class__.__name__)
        self.num_q = num_q

        self._while_cond: bool = True

    @property
    def while_cond(self) -> bool:
        return self._while_cond

    @while_cond.setter
    def while_cond(self, new_val: bool):
        self._while_cond = new_val

    def run(self) -> None:
        while self.while_cond:
            time.sleep(random.random())
            new_num = self.generate_random_integer()
            self.num_q.put(new_num)
            logger.info('New number {} threw.'.format(new_num))

    @staticmethod
    def generate_random_integer(max_integer: int = 100) -> int:
        return random.randint(0, max_integer)
