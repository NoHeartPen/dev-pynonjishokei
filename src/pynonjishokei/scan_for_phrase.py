import logging
import sys
import time

from .src.pynonjishokei.db.query_phrase import query_phrase

from .src.pynonjishokei.main import scan_input_string

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
# TODO 应该从数据库中自动读取 yomi 和 kanji 2列，生成下面的集合
phrase_words_set = {"うそ", "つく", "嘘", "付く"}


def longest_matching_scan(input_text: str) -> list[list[str]]:
    """用最长一致法扫描并提取出一句话中可能是词组搭配的单词

    Args:
        input_text:可能含有词组的一句话

    Returns:
        以[["うそ","嘘"], ["つく", "付く"]]的格式返回提取结果
        如果输入中不含词组搭配，那么返回空列表
    """
    # 使用二维数组保存结果
    scanned_output_list: list[list[str]] = []
    # 切片扫描字符串时的前索引值
    pre_scanning_index = 0
    # 切片扫描字符串时的后索引值
    post_scanning_index = 0
    input_length = len(input_text)
    while post_scanning_index <= input_length and pre_scanning_index <= input_length:
        if post_scanning_index == input_length:
            if pre_scanning_index == post_scanning_index:
                # 前后索引值重合，说明已经完成扫描
                break
            # 后索引已到达字符串末端，接下来只移动前索引
            pre_scanning_index += 1
        else:
            post_scanning_index += 1
        # 记录当前正在扫描的字符串
        scanning_string = input_text[pre_scanning_index:post_scanning_index]
        logging.debug(
            "scanning input string: %s",
            scanning_string,
        )
        jishokei_scanning_list = scan_input_string(scanning_string)

        scanned_word_list = []
        for jishokei_string in jishokei_scanning_list:
            if jishokei_string in phrase_words_set:
                logging.debug("add %s to %s", jishokei_string, scanned_word_list)
                scanned_word_list.append(jishokei_string)
                # 成功识别出词汇，将前索引移动到后索引所在的位置，继续移动后索引向后扫描识别剩下的字符串
                pre_scanning_index = post_scanning_index

        if len(scanned_word_list) > 0:
            # 将单次的识别结果单独保存到一个列表中
            logging.debug("add %s to %s", scanned_word_list, scanned_output_list)
            scanned_output_list.append(scanned_word_list)
    return scanned_output_list


def find_phrase(scanned_word_list: [str]) -> list[set[str]]:
    """根据扫描的结果查询数据库

    Args:
        scanned_word_list ():

    Returns:

    """
    # TODO 句型与固定搭配也可以采用类似的做法
    query_phrase(scanned_word_list)
    return query_phrase(scanned_word_list)


def scan_for_phrase(input_text: str) -> list[set[str]]:
    """扫描并识别一句话中含有的词组

    Args:
        input_text: 可能含有词组的一句话

    Returns:
        以 [("嘘を付く",)] 的格式返回所有可能的词组，如果没有查到词组则返回空列表
    """
    return find_phrase(longest_matching_scan(input_text))
