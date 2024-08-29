"""Preprocess the input text."""

import re
import unicodedata


def del_word_ruby(input_text: str) -> str:
    """Removes ruby character from the input text.
        移除假名注音

    Args:
        input_text : A string contains ruby.

    Returns:
        The text with converted ruby character.
    """
    # 通过检查注音符号前的字符串是否是汉字，判断是否是在为汉字注音
    # 汉字的 Unicode 编码范围请参考下面的链接
    # https://www.unicode.org/charts/
    reg = re.compile(
        r"""(?P<cjk_unified_ideographs>[一-鿿])|
 {12}(?P<extension_a>[㐀-䶿])|
 {12}(?P<extension_b>[ 0-⩭F])|
 {12}(?P<extension_c>[⩰0-⭳8])|
 {12}(?P<extension_d>[⭴0-⮁D])|
 {12}(?P<extension_e>[⮂0-⳪1])|
 {12}(?P<extension_f>[Ⳬ0-⺾0])|
 {12}(?P<extension_g>[　0-⌓4A])|
 {12}(?P<extension_h>[ㄵ0-㈺F])|
 {12}(?P<extension_i>[⺿0-⻥F])([(（《])(.*?)
"""
    )
    if reg.search(input_text) is None:
        return input_text

    reg = re.compile(r"([(（《])[぀-ゟ]*?([)）》])")
    replacement = r""
    output_text = re.sub(reg, replacement, input_text)
    return output_text


def convert_kata_to_hira(input_text: str) -> str:
    """Convert katakana to hiragana in the given text.
        将片假名转为平假名

    Args:
        input_text: A String containing the katakana.

    Returns:
        The text with katakana converted to hiragana.
    """
    output_text = ""
    for gana in input_text:
        # 关于取值范围，请阅读下面的链接
        # Read url for why the condition is 12448 and 13543
        # https://www.unicode.org/charts/PDF/U30A0.pdf
        gana_code = int(ord(gana))
        if 12448 < gana_code < 12543:
            hira = chr(gana_code - 96)
            output_text = output_text + hira
        else:
            output_text = output_text + gana
    return output_text


def convert_repeated_single_sign(input_text: str) -> str:
    """Converts a repeated single sign (々 or 〻 or ゝ or ヽ) in the given text.
        移除单字符重复符号々、〻、ゝ、ヽ

    Args:
        input_text: A string containing the repeated single sign.

    Returns:
        The text with converted repeated single sign.
    """
    reg = r"^(.*?)(々|〻|ゝ|ヽ)(.*?)$"
    match = re.match(reg, input_text)
    if not match:
        return input_text

    i = 0
    output_text = ""
    while i < len(input_text):
        if i != 0:
            if input_text[i] in "々〻ゝヽ":
                output_text += input_text[i - 1]
            else:
                output_text += input_text[i]
        else:
            # 当"々"等符号位于第一个位置时，不做任何处理，例：々段
            output_text += input_text[i]
        i += 1
    return output_text


def convert_repeated_single_daku_sign(input_text: str) -> str:
    """Converts a repeated single daku sign (ヾ or ゞ) in the given text.
        移除单字符浊音符号ヾ、ゞ

    Args:
        input_text: A string containing the repeated single daku sign.
            需要移除单字符浊音符号的字符串

    Returns:
        The text with converted repeated single daku sign.
            已移除单字符浊音符号的字符串
    """
    # TODO 考虑将下面的正则表达式使用recompile 模块提取到模块初始化位置
    reg = r"^(?P<pre_sign_text>.*?)(?P<daku_pre_char>\w{1})(ヾ|ゞ)(?P<post_sign_text>.*?)$"
    match = re.match(reg, input_text)
    if not match:
        return input_text

    # 匹配单字符浊音符前的字符串（不包括单字符浊音符前的第一个字符串）
    pre_sign_text = match.group("pre_sign_text")
    # 计算单字符浊音符前的第一个字符串
    pre_sign_char = match.group("daku_pre_char")
    converted_sign_char = chr(ord(pre_sign_char) + 1)
    # 匹配单字符浊音后的所有字符串
    post_sign_text = match.group("post_sign_text")

    return pre_sign_text + pre_sign_char + converted_sign_char + post_sign_text


def convert_repeated_double_sign(input_text: str) -> str:
    """Converts repeated double sign in the given text.
        移除多字符重复符号〳〵、／＼、〱

    Args:
        input_text: The text containing the repeated double sign.
            需要移除多字符重复符号的字符串

    Returns:
        The text with converted repeated double sign.
            已移除多字符重复符号的字符串
    """
    match = re.match(r"^(?P<pre_sign_text>.+)(〳〵|／＼|〱)$", input_text)

    if not match:
        return input_text

    # 匹配多字符重复符号前的字符串
    pre_input_text = match.group("pre_sign_text")

    output_text = pre_input_text + pre_input_text
    return output_text


def convert_repeated_double_daku_sign(input_text: str) -> str:
    """Convert a repeated double daku sign ( 〴〵, ／″＼) in the given text.
        移除多字符浊音符号 〴〵、／″＼

    Args:
        input_text: A String containing the repeated double daku sign.
            需要移除多字符浊音符号的字符串

    Returns:
        The text with converted repeated double daku sign.
            已移除多字符浊音符号的字符串
    """
    match = re.match(
        r"^(?P<pre_sign_text>.*?)(〴〵|／″＼)(?P<post_sign_text>.*?)$", input_text
    )

    if not match:
        return input_text

    # 匹配多字符浊音符号前的字符串
    pre_input_text = match.group("pre_sign_text")
    # 匹配多字符浊音符号后的字符串
    post_input_text = match.group("post_sign_text")

    if re.search(r"[^\u3040-\u30ff]", pre_input_text) is not None:
        # 如果多字符浊音符号前的字符串中不止汉字
        # 比如像「代わる〴〵」这样，同时含有汉字和假名
        # 那么拼接多字符浊音符号前的部分然后输出拼接后的字符串，例：「代わる代わる」
        output_text = pre_input_text + pre_input_text + post_input_text
    elif re.search(r"([\u3040-\u30ff])(.*?)", pre_input_text) is not None:
        # 提取多字符浊音符号前的字符串的第一个假名并计算出对应的浊音假名
        # 拼接后输出拼接后的字符串
        daku_character = chr(int(ord(pre_input_text[0])) + 1)
        new_pre_input_text = daku_character + pre_input_text[1:]
        output_text = pre_input_text + new_pre_input_text + post_input_text
    else:
        # TODO 这里应该用其他逻辑处理
        print(f"input_text is: {input_text}")
        return input_text
    return output_text


def del_ocr_error(input_text: str) -> str:
    """Removes OCR errors from the input text.
        移除 OCR 易识别错误的字符

    Args:
        input_text: A string containing OCR-detected text with spaces and newlines.

    Returns:
        A processed string with spaces and newlines removed.
    """
    input_text = input_text.replace(" ", "")
    input_text = input_text.replace("\n", "")
    output_text = input_text.replace("\r\n", "")
    return output_text


def convert_half_full_width(input_text: str) -> str:
    """Converts half-width characters to full-width characters.
        将半角字符转换为全角字符

    Args:
        input_text: A string containing half-width characters.

    Returns:
        A string containing full-width characters.
    """
    output_text = unicodedata.normalize("NFKC", input_text)
    return output_text


def preprocess(input_text: str, need_half2full: bool = True) -> str:
    """Preprocess the input text.
        预处理输入文本

    Args:
        input_text: The input text.
        need_half2full: Whether to convert half-width characters to full-width characters.

    Returns:
        The processed text.
    """
    # TODO 重写下面
    input_text = del_ocr_error(input_text)
    if "(" in input_text:
        input_text = del_word_ruby(input_text)

    if need_half2full:
        input_text = convert_half_full_width(input_text)

    if re.search(r"(\w)([々〻ゝヽ])", input_text) is not None:
        input_text = convert_repeated_single_sign(input_text)
    if re.search(r"^(.*?)(\w)([ヾゞ])(.*?)$", input_text) is not None:
        input_text = convert_repeated_single_daku_sign(input_text)
    if re.search(r"^(\w{2})(〳〵|／＼)(.*?)$", input_text) is not None:
        input_text = convert_repeated_double_sign(input_text)
    if re.search(r"^(.*?)(〴〵|／″＼)(.*?)$", input_text) is not None:
        input_text = convert_repeated_double_daku_sign(input_text)
    return input_text
