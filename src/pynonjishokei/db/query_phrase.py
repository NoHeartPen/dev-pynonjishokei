import os
import re
import sqlite3


def do_query_phrase(statement: str, params: list[str]) -> list[set[str]]:
    """查询数据库并返回词组

    Args:
        statement: SQL 语句的固定部分，即：SELECT dict_index FROM kannyouku WHERE 1=1
        params: SQL 语句的拼接部分

    Returns:
        以 [("嘘を付く",)] 的格式返回查询结果
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "nonjishokei.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    phrase = cursor.execute(statement, params).fetchall()
    conn.close()
    return phrase


def is_all_kana(text: str) -> bool:
    """判断一个字符串是否全部由假名构成

    Args:
        text: 要判断的字符串

    Returns:
        如果字符串全部由假名构成返回 True，否则 False.
    """

    return re.match(r"^[\u3040-\u309F\u30A0-\u30FF]+$", text) is not None


def query_phrase(phrase_word_list: list[list[str]]) -> list[set[str]]:
    """通过传入的数据构建动态 SQL 在数据库中查询并返回词组

    Args:
        phrase_word_list: 组成词组的前后项单词，例：[["うそ", "嘘"], ["つく", "付く"]]
        即嵌套列表中的第一层列表用于区分组成词组的不同单词，第二层列表用于区分单词的不同写法
        TODO 注意： 目前只支持类似【嘘を付く】这样【名词+助词+动词】的形式的短语，能否支持其他形式的短语需要在实际的生产环境中进行测试

    Returns:
        以 [("嘘を付く",)] 的格式返回所有可能的词组，如果没有查到词组则返回空列表
    """
    if len(phrase_word_list) != 2:
        # TODO 暂时不支持非【名词+助词+动词】形式的短语查询
        return []

    statement = "SELECT dict_index FROM kannyouku WHERE 1=1"
    params = []
    # 【名词+助词+动词】形式的短语中，助词前面的部分
    pre_word_list = phrase_word_list[0]
    for word in pre_word_list:
        if is_all_kana(word):
            yomi01 = word
            statement += " AND yomi01=?"
            params.append(yomi01)
        else:
            kannji01 = word
            statement += " AND kannji01=?"
            params.append(kannji01)

    # 【名词+助词+动词】形式的短语中，助词后面的部分
    post_word_list = phrase_word_list[1]
    for word in post_word_list:
        if is_all_kana(word):
            yomi02 = word
            statement += " AND yomi02=?"
            params.append(yomi02)
        else:
            kannji02 = word
            statement += " AND kannji02=?"
            params.append(kannji02)
    phrases = do_query_phrase(statement, params)
    return phrases
