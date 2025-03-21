import unittest
from tests.Sidebar import main

class TestMain(unittest.TestCase):
    def test_main(self):
        # Test the main function
        self.assertIsNone(main())

if __name__ == '__main__':
    unittest.main()
