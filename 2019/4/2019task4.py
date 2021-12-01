import unittest
import functools
import operator


class MyTestCase(unittest.TestCase):
    def test_something(self):
        cnt = 0
        for pwd in range(234208, 765869):
            spwd = str(pwd)
            if any([spwd[i] == spwd[i+1] for i in range(5)]) and all([spwd[i] <= spwd[i+1] for i in range(5)]):
                matching = dict()
                for s in spwd:
                    matching[s] = matching.setdefault(s, 0) + 1
                if any([sm == 2 for sm in matching.values()]):
                    cnt += 1
        print(cnt)

if __name__ == '__main__':
    unittest.main()
