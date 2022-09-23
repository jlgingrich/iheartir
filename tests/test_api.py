import iheartir
import unittest

class Test_TestIncrementDecrement(unittest.TestCase):
    def test_get(self):
        target_url = "https://www.iheart.com/live/alt-1045-3401/"
        print(iheartir.cli.get(target_url))

if __name__ == '__main__':
    unittest.main()