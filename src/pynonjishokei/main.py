"""convert a pynonjishokei to a jishokei"""

import json
import logging
import os
import sys
import time
from typing import Dict, List

# pylint: disable=E0402
from .preprocess import preprocess  # type: ignore

logging.basicConfig(
    handlers=[
        logging.FileHandler(
            f"{time.strftime('%Y-%m-%d', time.localtime())}.log", encoding="utf-8"
        ),
        logging.StreamHandler(sys.stderr),
    ],
    level=logging.DEBUG,
    format="%(asctime)s %(filename)s %(levelname)s %(message)s",
    datefmt="%a %d %b %Y %H:%M:%S",
)


def read_rule_file(rule_file: str) -> Dict[str, list[str]]:
    """read json file
        加载规则文件

    Args:
        rule_file: input file path

    Returns:
        json file content
    """
    with open(rule_file, "r", encoding="utf-8") as f:
        return json.loads(f.read())


def convert_orthography(input_text: str) -> list | None:
    """convert input text to the form of a word that appears as an entry in a dictionary,
        for example, convert【気づく】to【気付く】
        通过查询确认推导结果是否正确，同时消除假名书写造成的非辞書型，比如【気づく】和【気付く】

    Args:
        input_text: a form of a word that will not appear as an entry in a dictionary

    Returns:
        the form of a word that appears as an entry in a dictionary
    """
    if input_text in orthography_rule_dict:
        return orthography_rule_dict[input_text]
    else:
        return None


def convert_conjugate(input_text: str) -> list | None:
    """convert a verb conjugation and adj declension to basic form.
        还原用言的活用变形

    Args:
        input_text: A String containing the conjugation.

    Returns:
        The list with conjugation converted to the basic form.
    """
    if len(input_text) == 0:
        return None
    input_stem = input_text[0:-1]
    input_last_letter = input_text[-1]
    process_output_list: list[str] = []
    # TODO 一段动词的词干必定是え段假名，对于見る这样汉字就是词干的动词特殊
    # 本程序的 input_stem 概念对应的不是一段动词语法意义上的词干
    # 今日は、寿司を**食べ**に銀座に行いきます。
    process_text = input_text + "る"
    process_output_list.append(process_text)
    logging.debug("add %s to %s: for v1", process_text, process_output_list)

    jishokei_last_letter_list = conjugate_rule_dict.get(input_last_letter)
    if jishokei_last_letter_list is not None:
        for jishokei_last_letter in jishokei_last_letter_list:
            process_output_list.append(input_stem + jishokei_last_letter)
            logging.debug(
                "add %s to %s: for conjugate rule",
                input_stem + jishokei_last_letter,
                process_output_list,
            )

    # 将输入的字符串作为最后一个结果返回
    # 因为输入的字符串可能就是正确的辞書型
    if input_text not in process_output_list:
        process_output_list.append(input_text)

    # 删除其中的重复值，只保留第一次的结果
    output_list: List[str] = []
    for i in process_output_list:
        if i not in output_list:
            output_list.append(i)

    return output_list


def convert_nonjishokei(input_text: str) -> list:
    """Convert pynonjishokei to jishokei.
        将非辞书形还原为辞书形

    Args:
        input_text: A String containing the pynonjishokei.

    Returns:
        The list with pynonjishokei converted to the jishokei.
    """
    # 还原动词的活用变形
    converted_conjugate_list = convert_conjugate(input_text)
    if converted_conjugate_list is None:
        return []
    # 检查还原结果
    orthography_list: list[str] = []
    logging.debug("all converted conjugate list: %s", converted_conjugate_list)
    for converted_word in converted_conjugate_list:
        orthography_text = convert_orthography(converted_word)
        if orthography_text is not None:
            # 获取辞书形
            # TODO 注意这里的逻辑其实可以优化233
            orthography_list.extend(set(orthography_text))
    output_list = []
    # TODO 列表推导式重写
    # TODO 这里可以试着读取用户配置的默认最大推导输出数量，然后返回列表的前几项
    # 注意能这样做的前提是列表的排序有一定的规则可循
    for orthography_word in orthography_list:
        output_list.append(orthography_word)
    return output_list


def scan_input_string(input_text: str) -> list:
    """Scans the input string by Maximum Matching and returns a list of possible jishokei.
        采用最长一致法扫描字符串，推导并返回所有可能的辞书形

    Args:
        input_text: The string to scan.

    Returns:
        A list of converted jishokei.
    """
    if input_text == "":
        return []

    # 预处理
    input_text = preprocess(input_text)

    # TODO
    # 判断是否含有日文相关字符，比如假名和日文汉字，如果没有直接退出

    # 记录扫描的临时字符串
    scanned_input_list: List[str] = []
    # 记录扫描过程中的推导结果
    scanned_process_list: List[str] = []
    for input_index in range(len(input_text) + 1):
        scanned_input_text = input_text[0 : input_index + 1]
        logging.debug("scanned_input_text: %s", scanned_input_text)
        scanned_input_list.append(scanned_input_text)

        # 特殊规则
        special_output_list = special_rule_dict.get(scanned_input_text)
        if special_output_list is not None:
            for special_output_text in special_output_list:
                logging.debug(
                    "add %s to scanned_process_list for special rule",
                    special_output_text,
                )
                scanned_process_list.append(special_output_text)

        # TODO 用户自定义的转换规则

        converted_jishokei_list = convert_nonjishokei(scanned_input_text)
        for converted_jishokei_text in converted_jishokei_list:
            logging.debug(
                "add %s to scanned_process_list for converted jishokei",
                converted_jishokei_text,
            )
            scanned_process_list.append(converted_jishokei_text)

    # 返回给用户的扫描结果
    scanned_output_list: List[str] = []
    # 优先展示更长字符串的扫描结果，提高复合动词的使用体验
    for scanned_process_text in reversed(scanned_process_list):
        # 只添加第一次的推导结果
        if scanned_process_text not in scanned_output_list:
            # 不添加扫描过程中的临时字符串
            # TODO 直接删除可能会导致意想不到的问题
            # 如果输入的字符串就是原型：食べる。
            # 更好的做法应该是同时判断是否在用户自己构建的辞典索引中
            # if i not in scanned_input_list:
            scanned_output_list.append(scanned_process_text)

    # 将输入的字符串作为最后一个结果返回
    # 方便用户在程序无法推导出正确结果时快速编辑
    if input_text not in scanned_output_list:
        logging.debug("add input_text %s to scanned_output_list", input_text)
        scanned_output_list.append(input_text)

    return scanned_output_list


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
RULE_PATH = os.path.join(CURRENT_PATH, "rule")
orthography_rule_path: str = os.path.join(RULE_PATH, "index.json")
orthography_rule_dict: Dict[str, list[str]] = read_rule_file(orthography_rule_path)
conjugate_rule_path: str = os.path.join(RULE_PATH, "conjugate_rule.json")
conjugate_rule_dict: Dict[str, list[str]] = read_rule_file(conjugate_rule_path)
special_rule_path: str = os.path.join(RULE_PATH, "special_rule.json")
special_rule_dict: Dict[str, list[str]] = read_rule_file(special_rule_path)

if __name__ == "__main__":
    print("Hello there.\n  This is indented.")
