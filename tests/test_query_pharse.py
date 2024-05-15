import unittest

from src.pynonjishokei.db.query_phrase import query_phrase

result = [("嘘を付く",)]


class MyTestCase(unittest.TestCase):
    def test_query_phrase(self):
        self.assertEqual(result, query_phrase([["うそ"], ["つく"]]))
        self.assertEqual(result, query_phrase([["うそ"], ["付く"]]))
        self.assertEqual(result, query_phrase([["うそ"], ["つく", "付く"]]))
        self.assertEqual(result, query_phrase([["嘘"], ["つく"]]))
        self.assertEqual(result, query_phrase([["嘘"], ["付く"]]))
        self.assertEqual(result, query_phrase([["嘘"], ["つく", "付く"]]))

        self.assertEqual(result, query_phrase([["うそ", "嘘"], ["つく"]]))
        self.assertEqual(result, query_phrase([["うそ", "嘘"], ["付く"]]))
        self.assertEqual(result, query_phrase([["うそ", "嘘"], ["つく", "付く"]]))

        # 边界情况测试
        # 未以短语的形式出现
        self.assertEqual([], query_phrase([["うそ"]]))
        self.assertEqual([], query_phrase([[""]]))


if __name__ == "__main__":
    unittest.main()
