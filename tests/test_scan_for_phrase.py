import unittest

from src.pynonjishokei.scan_for_phrase import scan_for_phrase
from src.pynonjishokei.scan_for_phrase import find_phrase
from src.pynonjishokei.scan_for_phrase import longest_matching_scan


def get_nested_list_str_items(input_list: list[list[str]]) -> set[str]:
    """将列表组成的嵌套列表里的元素添加到一个新集合中
    由于 unitest 提供的判断方法无法准确判断这样列表，故将测试结果处理后再进行断言

    Args:
        input_list:由列表组成的嵌套列表，例：[["うそ"], ["つく", "付く"]]

    Returns:
        由原列表中的元素去重后组成的新集合，例：("うそ","つく", "付く")
    """
    output_set = set()
    for sublist in input_list:
        for element in sublist:
            output_set.add(element)
    return output_set


def get_nested_list_set_items(input_list: list[set[str]]) -> set[str]:
    """将集合组成的嵌套列表里的元素添加到一个新集合中
    由于 unitest 提供的判断方法无法准确判断这样列表，故将测试结果处理后再进行断言

    Args:
        input_list: 由集合组成的嵌套列表，例：[("嘘を付く",)]

    Returns:
        由原列表中的元素去重后组成的集合，例：("嘘を付く")
    """
    output_set = set()
    for sublist in input_list:
        for element in sublist:
            output_set.add(element)
    return output_set


class TestMain(unittest.TestCase):
    def do_longest_matching_scan_test(
        self, test_cases: list[tuple[str, list[list[str]]]]
    ):
        """执行 longest_matching_scan 单元测试

        Args:
            test_cases: 测试表数据，例：[("うそをつく", [["うそ"], ["つく", "付く"]])]
        """
        for test_text, expected_result in test_cases:
            with self.subTest(test_text=test_text, expected_result=expected_result):
                result = longest_matching_scan(test_text)
                self.assertCountEqual(
                    get_nested_list_str_items(result),
                    get_nested_list_str_items(expected_result),
                )

    def do_find_phrase_test(self, test_cases: [set[list[str]]]):
        """执行 find_phrase 单元测试

        Args:
            test_cases: 测试表数据
        """
        for test_text, expected_result in test_cases:
            with self.subTest(test_text=test_text, expected_result=expected_result):
                result = find_phrase(test_text)
                self.assertCountEqual(
                    get_nested_list_set_items(result),
                    get_nested_list_set_items(expected_result),
                )

    def do_scan_for_phrase_test(self, test_cases: [set[list[str]]]):
        """执行 scan_for_phrase 单元测试

        Args:
            test_cases: 测试表数据
        """
        for test_text, expected_result in test_cases:
            with self.subTest(test_text=test_text, expected_result=expected_result):
                result = scan_for_phrase(test_text)
                self.assertCountEqual(
                    get_nested_list_set_items(result),
                    get_nested_list_set_items(expected_result),
                )

    def test_longest_matching_scan(self):
        result_pre_hira = [["うそ"], ["つく", "付く"]]
        pre_hira_test_cases = [
            ("うそをつく", result_pre_hira),
            # FROM https://www.amazon.co.jp/%E3%81%BC%E3%81%A3%E3%81%A1%E3%83%BB%E3%81%96%E3%83%BB%E3%82%8D%E3%81%A3%E3%81%8F%EF%BC%81/dp/B0B6Q93B2C
            # 「（虹夏）そこ ウソつかない」『ぼっち・ざ・ろっく』02 また明日
            ("ウソつかない", result_pre_hira),
            # FROM: https://www.immersionkit.com/
            # 「うそつけ」 『Fullmetal Alchemist Brotherhood』
            ("うそつけ", result_pre_hira),
            # 「オレはうそをつかねぇのを信条にしている」 『Fullmetal Alchemist Brotherhood』
            ("うそをつかねぇ", result_pre_hira),
            # 「ウソまでつくし」『Toradora!』
            ("ウソまでつくし", result_pre_hira),
            # 「遠坂にもウソはつかない」『Fate Stay Night Unlimited Blade Works』
            ("ウソはつかない", result_pre_hira),
            # 「ウソがつけなくなる結界を 張ればいいんだわ」『Wandering Witch The Journey of Elaina』
            ("ウソがつけなくなる結界を", result_pre_hira),
            # 「俺をかばってみんなの前で ウソつかせたこと」『Weakest Beast』
            ("ウソつかせたこと", result_pre_hira),
        ]

        self.do_longest_matching_scan_test(pre_hira_test_cases)

        result_pre_kannji = [["嘘"], ["つく", "付く"]]
        pre_kanji_test_cases = [
            # FROM: https://www.immersionkit.com/
            # 「かっ　嘘つけぇーっ！　てめぇにはわかるハズだぁぁっ！」
            ("嘘つけぇーっ！", result_pre_kannji),
            # 「上手に嘘(うそ)をつくのよ」『Million Yen Woman』
            ("嘘(うそ)をつくのよ", result_pre_kannji),
            # 「福ちゃんを庇って嘘ついたんだと思う」『Hyouka』
            ("嘘ついたんだと思う", result_pre_kannji),
            # 「里志が嘘を付いているわけではなさそうだ」『Hyouka』
            ("嘘を付いているわけではなさそうだ", result_pre_kannji),
        ]

        self.do_longest_matching_scan_test(pre_kanji_test_cases)

    def test_find_phrase(self):
        phrase_result = [("嘘を付く",)]
        phrase_test_cases = [
            ([["うそ"], ["つく"]], phrase_result),
            ([["うそ"], ["付く"]], phrase_result),
            ([["うそ"], ["つく", "付く"]], phrase_result),
            ([["嘘"], ["つく"]], phrase_result),
            ([["嘘"], ["付く"]], phrase_result),
            ([["嘘"], ["つく", "付く"]], phrase_result),
        ]

        self.do_find_phrase_test(phrase_test_cases)

    def test_scan_for_phrase(self):
        phrase_result = [("嘘を付く",)]
        test_cases = [
            ("うそをつく", phrase_result),
            # FROM https://www.amazon.co.jp/%E3%81%BC%E3%81%A3%E3%81%A1%E3%83%BB%E3%81%96%E3%83%BB%E3%82%8D%E3%81%A3%E3%81%8F%EF%BC%81/dp/B0B6Q93B2C
            # 「（虹夏）そこ ウソつかない」『ぼっち・ざ・ろっく』02 また明日
            ("ウソつかない", phrase_result),
            # FROM: https://www.immersionkit.com/
            # 「うそつけ」 『Fullmetal Alchemist Brotherhood』
            ("うそつけ", phrase_result),
            # 「オレはうそをつかねぇのを信条にしている」 『Fullmetal Alchemist Brotherhood』
            ("うそをつかねぇ", phrase_result),
            # 「ウソまでつくし」『Toradora!』
            ("ウソまでつくし", phrase_result),
            # 「遠坂にもウソはつかない」『Fate Stay Night Unlimited Blade Works』
            ("ウソはつかない", phrase_result),
            # 「ウソがつけなくなる結界を 張ればいいんだわ」『Wandering Witch The Journey of Elaina』
            ("ウソがつけなくなる結界を", phrase_result),
            # 「俺をかばってみんなの前で ウソつかせたこと」『Weakest Beast』
            ("ウソつかせたこと", phrase_result),
            # FROM: https://www.immersionkit.com/
            # 「かっ　嘘つけぇーっ！　てめぇにはわかるハズだぁぁっ！」
            ("嘘つけぇーっ！", phrase_result),
            # 「上手に嘘(うそ)をつくのよ」『Million Yen Woman』
            ("嘘(うそ)をつくのよ", phrase_result),
            # 「福ちゃんを庇って嘘ついたんだと思う」『Hyouka』
            ("嘘ついたんだと思う", phrase_result),
            # 「里志が嘘を付いているわけではなさそうだ」『Hyouka』
            ("嘘を付いているわけではなさそうだ", phrase_result),
            # 不含任何词组
            ("", []),
        ]

        self.do_scan_for_phrase_test(test_cases)


if __name__ == "__main__":
    unittest.main()
