import logging
from multiprocessing import Process, Queue
from queue import Empty
from typing import Optional, Union

logger = logging.getLogger()


class NumCatcher(Process):
    TIMEOUT_GET_FROM_Q = 0.5

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
            try:
                num = self.get_num_from_q()
                if num is None:
                    logger.debug('Caught a None')
                    continue
                logger.info('Caught new number {}'.format(num))
            except KeyboardInterrupt:
                break

    def get_num_from_q(self) -> Optional[Union[int, float]]:
        try:
            return self.num_q.get(block=True, timeout=self.TIMEOUT_GET_FROM_Q)
        except Empty:
            return
