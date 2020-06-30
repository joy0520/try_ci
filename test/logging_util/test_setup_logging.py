import unittest
from unittest.mock import Mock, patch

import logging_util.setup_logging as src


class TestSetupLogging(unittest.TestCase):
    @patch('logging_util.setup_logging._setup_queue_handler_and_listener')
    @patch('logging_util.setup_logging._file_handler')
    @patch('logging_util.setup_logging._stream_handler')
    @patch('logging.Formatter')
    @patch('logging.getLogger')
    def test(self, *mock_funcs):
        src.setup_logging('fake log file path', 'fake logger name')

        for mock_func in mock_funcs:
            mock_func.assert_called_once()


class TestDailyFileHandler(unittest.TestCase):
    @patch('logging.handlers.TimedRotatingFileHandler')
    def test(self, mock_fh_ctr):
        mock_fh = mock_fh_ctr.return_value

        self.assertEqual(mock_fh, src._daily_file_handler('fake log file path'))


class TestFileHandler(unittest.TestCase):
    @patch('logging_util.setup_logging._hourly_file_handler')
    @patch('logging_util.setup_logging._daily_file_handler')
    def test_daily(self, mock_daily_fh, mock_hourly_fh):
        src._file_handler('fake log file path', Mock(), -1, daily=True)

        mock_daily_fh.assert_called_once()
        mock_hourly_fh.assert_not_called()

    @patch('logging_util.setup_logging._hourly_file_handler')
    @patch('logging_util.setup_logging._daily_file_handler')
    def test_hourly(self, mock_daily_fh, mock_hourly_fh):
        src._file_handler('fake log file path', Mock(), -1, daily=False)

        mock_daily_fh.assert_not_called()
        mock_hourly_fh.assert_called_once()


class TestHourlyFileHandler(unittest.TestCase):
    @patch('logging.handlers.TimedRotatingFileHandler')
    def test(self, mock_fh_ctr):
        mock_fh = mock_fh_ctr.return_value

        self.assertEqual(mock_fh, src._hourly_file_handler('fake log file path'))


class TestStreamHandler(unittest.TestCase):
    @patch('logging.StreamHandler')
    def test(self, mock_sh_ctr):
        mock_sh = mock_sh_ctr.return_value

        self.assertEqual(mock_sh, src._stream_handler(Mock(), -1))


class TestSetupQueueHandlerAndListener(unittest.TestCase):
    @patch('logging.handlers.QueueListener')
    @patch('logging.DEBUG', -1)
    @patch('logging.handlers.QueueHandler')
    @patch('logging_util.setup_logging.Queue')
    def test(self, mock_q, mock_qh, mock_ql):
        fake_logger = Mock()
        fake_handlers = [Mock(), Mock()]
        ql = mock_ql.return_value

        src._setup_queue_handler_and_listener(fake_logger, *fake_handlers)

        fake_logger.addHandler.assert_called_once()
        ql.start.assert_called_once()


if __name__ == '__main__':
    unittest.main()
