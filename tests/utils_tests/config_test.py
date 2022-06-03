import json
from tempfile import TemporaryDirectory, TemporaryFile
from unittest import TestCase
from unittest.mock import patch

from utils.config import Config


class TestConfig(TestCase):
    @patch.object(Config, '__init__', lambda *_: None)
    def test_check_file_dir(self):
        config = Config()
        config.file = ''
        with TemporaryDirectory() as tempdir:
            with self.assertRaises(ValueError):
                config.check_file(tempdir)
