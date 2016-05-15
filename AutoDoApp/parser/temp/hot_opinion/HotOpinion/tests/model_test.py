from HotOpinion import app as hot_opinion
import database
import os
import tempfile
import unittest


class BasicTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fs = tempfile.mkdtemp()
        self.app = hot_opinion.test_client()
        database.init_db()

    def tearDown(self):
        os.close(self.db_fs)
