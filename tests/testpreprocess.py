"""单元测试框架 """

import unittest
from textwrap import dedent

from ..src.pynonjishokei.preprocess import (
    convert_half_full_width,
    convert_kata_to_hira,
    convert_repeated_double_daku_sign,
    convert_repeated_double_sign,
    convert_repeated_single_daku_sign,
    convert_repeated_single_sign,
    del_ocr_error,
    del_word_ruby,
)


class TestMain(unittest.TestCase):
    """
    单元测试，考虑到时间成本，部分测试的优先度不高，暂时用TODO进行标记，之后结合用户反馈进行修复。

    """

    def test_del_word_ruby(self):
        """移除假名注音"""
        # ()
        self.assertEqual("始む", del_word_ruby("始(はじ)む"))
        # （）
        self.assertEqual("始む", del_word_ruby("始（はじ）む"))
        # 《》
        # 其れはまだ人々が「愚《おろか》」と云う貴い徳を持って居て、世の中が今のように激しく軋《きし》み合わない時分であった。
        # https://www.aozora.gr.jp/cards/001383/card56641.html
        self.assertEqual("「愚」", del_word_ruby("「愚《おろか》」"))
        self.assertEqual("軋み合わない", del_word_ruby("軋《きし》み合わない"))
        # 非正常输入测试
        # https://kotobank.jp/word/%E3%81%BC%E3%82%84%E3%81%BC%E3%82%84-631393
        # ぼやぼや（と）しないでさっさと荷物を運べ
        self.assertEqual("ぼやぼや（と）", del_word_ruby("ぼやぼや（と）"))

    def test_convert_kata_to_hira(self):
        """将片假名转为平假名"""
        self.assertEqual("くま", convert_kata_to_hira("クマ"))
        self.assertEqual("ちょこちょこ", convert_kata_to_hira("チョコチョコ"))
        # アニメ「ヴァイオレット・エヴァーガーデン」：会えない日が続くと　胸がグッと重くなったりしないか？
        self.assertEqual("ぐっと", convert_kata_to_hira("グッと"))

    def test_convert_repeated_single_sign(self):
        """单字符重复符号"""
        # https://ja.wikipedia.org/wiki/%E8%B8%8A%E3%82%8A%E5%AD%97
        # 々
        self.assertEqual("々", convert_repeated_single_sign("々"))
        self.assertEqual("正正堂堂", convert_repeated_single_sign("正々堂々"))
        self.assertEqual("段段", convert_repeated_single_sign("段々"))
        self.assertEqual("赤裸裸", convert_repeated_single_sign("赤裸々"))
        self.assertEqual("告別式式場", convert_repeated_single_sign("告別式々場"))

        # 非正常输入测试
        self.assertEqual("正正堂", convert_repeated_single_sign("正々堂"))
        self.assertEqual("々段", convert_repeated_single_sign("々段"))
        self.assertEqual("々堂堂", convert_repeated_single_sign("々堂々"))
        # TODO 极少数特例
        # self.assertEqual("複複複線", convert_repeated_single_sign("複々々線"))
        # self.assertEqual("部分部分", convert_repeated_single_sign("部分々々"))
        # TODO 古く（奈良時代）は記法が異なり
        # self.assertEqual("部分部分", convert_repeated_single_sign("部々分々"))

        # 〻 現代では「〻」は「々」と書き換えられ、主に縦書きの文章に用いる。
        self.assertEqual("〻", convert_repeated_single_sign("〻"))
        self.assertEqual("屡屡", convert_repeated_single_sign("屡〻"))

        # ゝ 平仮名繰返し記号
        self.assertEqual("ゝ", convert_repeated_single_sign("ゝ"))
        self.assertEqual("ここ", convert_repeated_single_sign("こゝ"))
        self.assertEqual("こころ", convert_repeated_single_sign("こゝろ"))
        self.assertEqual("わななかした", convert_repeated_single_sign("わなゝかした"))

        # ヽ 片仮名繰返し記号
        self.assertEqual("ヽ", convert_repeated_single_sign("ヽ"))
        self.assertEqual("ハハヽヽ", convert_repeated_single_sign("ハヽヽヽ"))
        # 曾ては、妣 （ ハヽ ） が国として、恋慕の思ひをよせた此国は、現実の悦楽に満ちた楽土として、見かはすばかりに変つて了うた。
        # https://www.aozora.gr.jp/cards/000933/files/13212_14465.html
        self.assertEqual("ハハ", convert_repeated_single_sign("ハヽ"))

    def test_convert_repeated_single_daku_sign(self):
        """单字符浊音重复符号"""
        self.assertEqual("ゞ", convert_repeated_single_daku_sign("ゞ"))
        # https://ja.wikipedia.org/wiki/%E8%B8%8A%E3%82%8A%E5%AD%97#%E3%82%9D%E3%81%A8%E3%83%BD%EF%BC%88%E4%B8%80%E3%81%AE%E5%AD%97%E7%82%B9%EF%BC%89
        self.assertEqual("ただ", convert_repeated_single_daku_sign("たゞ"))
        self.assertEqual("みすず飴", convert_repeated_single_daku_sign("みすゞ飴"))
        # FIXME 注意这个字符的定义：代表一个浊音假名，当前浊音符前的第一个假名就是浊音时，直接拼接返回即可
        # self.assertEqual("ぶぶ漬け", convert_repeated_single_daku_sign("ぶゞ漬け"))

    def test_convert_repeated_double_sign(self):
        """多字符重复符号"""
        # ／＼
        # Unicodeのブロックでは、収録されているの〳〵だが、
        self.assertEqual("〳〵", convert_repeated_double_sign("〳〵"))
        # https://ja.wikipedia.org/wiki/CJK%E3%81%AE%E8%A8%98%E5%8F%B7%E5%8F%8A%E3%81%B3%E5%8F%A5%E8%AA%AD%E7%82%B9
        # 青空文庫では「／＼」を使っている。
        self.assertEqual("／＼", convert_repeated_double_sign("／＼"))
        # https://www.aozora.gr.jp/cards/001383/files/56641_59496.html
        # 時々両国で催される刺青会では参会者おの／＼肌を叩いて、互に奇抜な意匠を誇り合い、評しあった。
        self.assertEqual("おのおの", convert_repeated_double_sign("おの／＼"))
        # 〳〵
        self.assertEqual("おのおの", convert_repeated_double_sign("おの〳〵"))
        self.assertEqual("くり返しくり返し", convert_repeated_double_sign("くり返し〳〵"))
        # 〱
        self.assertEqual("〱", convert_repeated_double_sign("〱"))
        self.assertEqual("見る見る", convert_repeated_double_sign("見る〱"))
        # https://ja.wikipedia.org/wiki/%E8%B8%8A%E3%82%8A%E5%AD%97#%E3%80%B1%EF%BC%88%E3%81%8F%E3%81%AE%E5%AD%97%E7%82%B9%EF%BC%89
        self.assertEqual("どうしてどうして", convert_repeated_double_sign("どうして〱"))
        # 非正常输入测试
        self.assertEqual("おの／＼肌", convert_repeated_double_sign("おの／＼肌"))

    def test_convert_repeated_double_daku_sign(self):
        """多字符浊音符号"""
        # https://ja.wikisource.org/wiki/%E3%81%8F%E3%82%8A%E3%81%8B%E3%81%B8%E3%81%97%E7%AC%A6%E5%8F%B7%E3%81%AE%E4%BD%BF%E3%81%B2%E6%96%B9
        self.assertEqual("〴〵", convert_repeated_double_daku_sign("〴〵"))
        self.assertEqual("散り散り", convert_repeated_double_daku_sign("散り〴〵"))
        self.assertEqual("代わる代わる", convert_repeated_double_daku_sign("代わる〴〵"))
        # 请注意，这个样例并非来自真实的使用场景，仅用作测试
        self.assertEqual("かわるがわる", convert_repeated_double_daku_sign("かわる〴〵"))
        # https://www.aozora.gr.jp/cards/001383/files/56641_59496.html
        # 彼は今始めて女の妙相みょうそうをしみ／″＼味わう事が出来た。
        self.assertEqual("しみじみ", convert_repeated_double_daku_sign("しみ／″＼"))
        # 其の瞳は夕月の光を増すように、だん／＼と輝いて男の顔に照った。
        # TODO　以下のURLでは、
        # https://ja.wikipedia.org/wiki/%E8%B8%8A%E3%82%8A%E5%AD%97#%E3%80%B1%EF%BC%88%E3%81%8F%E3%81%AE%E5%AD%97%E7%82%B9%EF%BC%89
        # 濁点の付く文字を繰り返す場合は、濁点の付いていない「くの字点」を用いる場合と、濁点の付いている「くの字点」を用いる場合がある。
        # 濁点の付く文字を繰り返すが、繰り返し箇所は濁点がつかない場合は、濁点の付いていない「くの字点」を用いる（擬音などでは少ないが児童向け文学などで漢字を仮名表記する場合に用いられる）。
        # self.assertEqual("だんだん", convert_repeated_double_daku_sign("だん／＼"))
        # self.assertEqual("だんだん", convert_repeated_double_daku_sign("だん／″＼"))

    def test_del_ocr_error(self):
        """注意空格往往不止一个"""
        self.assertEqual("食べた", del_ocr_error(" 食べた"))
        self.assertEqual("食べた", del_ocr_error("食 べた"))
        self.assertEqual("食べた", del_ocr_error("食べた "))
        self.assertEqual("食べた", del_ocr_error(" 食べた "))
        self.assertEqual("食べた", del_ocr_error(" 食 べ た "))
        self.assertEqual("", del_ocr_error(" "))

    def test_convert_half_full_width(self):
        """半角转全角"""
        half_width_text = (
            "ｧｱｨｲｩｳｪｴｫｵｶｶﾞｷｷﾞｸｸﾞｹｹﾞｺｺﾞｻｻﾞｼｼﾞｽｽﾞｾｾﾞｿｿﾞ"
            "ﾀﾀﾞﾁﾁﾞｯﾂﾂﾞﾃﾃﾞﾄﾄﾞﾅﾆﾇﾈﾉﾊﾊﾞﾊﾟﾋﾋﾞﾋﾟﾌﾌﾞﾌﾟﾍﾍﾞﾍﾟﾎﾎﾞﾎﾟ"
            "ﾏﾐﾑﾒﾓｬﾔｭﾕｮﾖﾗﾘﾙﾚﾛﾜｦﾝｳﾞﾞﾟ"
        )
        full_width_text = dedent(
            "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾ"
            "タダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポ"
            "マミムメモャヤュユョヨラリルレロワヲンヴ゙゚"
        )
        self.assertEqual(full_width_text, convert_half_full_width(half_width_text))


if __name__ == "__main__":
    unittest.main()
