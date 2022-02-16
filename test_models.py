import unittest
from models import *


class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = User("Dfdf", "Dfdf", "dfdfdf", "dfdf")


if __name__ == '__main__':
    unittest.main()


class TestBlog(unittest.TestCase):
    def setUp(self):
        self.blog = Blog("vcvcv", "sdsd", "dsd","sdsd", 12/3/2020, "dsd")


if __name__ == '__main__':
    unittest.main()


class TestComment(unittest.TestCase):
    def setUp(self):
        self.comment = Comment(1, "sdsd", "dsd")


if __name__ == '__main__':
    unittest.main()