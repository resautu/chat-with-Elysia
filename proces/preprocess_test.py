import unittest

from proces import get_all_pipelines
from proces import handle_blank_character
from proces import uppercase_to_lowercase
from proces import traditional_to_simplified
from proces import full_angle_to_half_angle
from proces import handle_substitute
from proces import preprocess


class TestPreprocess(unittest.TestCase):
    def setUp(self) -> None:
        self.all_pipelines = [
            "handle_blank_character",
            "uppercase_to_lowercase",
            "traditional_to_simplified",
            "full_angle_to_half_angle",
            "handle_substitute"
        ]

        self.hbc_data = {
            "删除 空白  字符": "删除空白字符",
            " 删除 空白 字符": "删除空白字符",
            " 删 除 空 白 字 符 ": "删除空白字符",
        }

        self.hbc_data_with_params = {
            "删除 空白  字符": {
                "params": [","],
                "result": "删除,空白,字符"
            },
            " 删除 空白 字符": {
                "params": [","],
                "result": ",删除,空白,字符"
            },
            " 删 除 空 白 字 符 ": {
                "params": [","],
                "result": ",删,除,空,白,字,符,"
            },
        }

        self.utl_data = {
            "UP": "up",
            "low": "low",
            "UPtoLOW": "uptolow",
        }

        self.tts_data = {
            "我幹什麼不干你事": "我干什么不干你事",
            "機械計算機的應用已經完全被電子計算機所取代": "机械计算机的应用已经完全被电子计算机所取代",
            "符號": "符号",
        }

        self.fth_data = {
            "（hi）": "(hi)",
            "你好：": "你好:",
            "！": "!",
        }

        self.hsub_data_with_params = {
            "hi/:": {
                "params": [r"/:", ""],
                "result": "hi"
            },
            "你好:": {
                "params": [r":", ""],
                "result": "你好"
            },
            "！/:": {
                "params": [r"！", "!"],
                "result": "!/:"
            }
        }

    def test_get_all_pipelines(self) -> None:
        self.assertEqual(get_all_pipelines(), self.all_pipelines)

    def test_handle_blank_character(self) -> None:
        for key, value in self.hbc_data.items():
            self.assertEqual(handle_blank_character(key), value)
        for key, value in self.hbc_data_with_params.items():
            self.assertEqual(handle_blank_character(key, *value["params"]), value["result"])

    def test_uppercase_to_lowercase(self) -> None:
        for key, value in self.utl_data.items():
            self.assertEqual(uppercase_to_lowercase(key), value)

    def test_traditional_to_simplified(self) -> None:
        for key, value in self.tts_data.items():
            self.assertEqual(traditional_to_simplified(key), value)

    def test_full_angle_to_half_angle(self) -> None:
        for key, value in self.fth_data.items():
            self.assertEqual(full_angle_to_half_angle(key), value)

    def test_handle_substitute(self) -> None:
        for key, value in self.hsub_data_with_params.items():
            self.assertEqual(handle_substitute(key, *value["params"]), value["result"])

    def test_preprocess(self) -> None:
        for key, value in self.hbc_data.items():
            self.assertEqual(preprocess(key), value)
        for key, value in self.hbc_data_with_params.items():
            self.assertEqual(preprocess(key, params={"handle_blank_character": value["params"]}), value["result"])
        for key, value in self.utl_data.items():
            self.assertEqual(preprocess(key), value)
        for key, value in self.tts_data.items():
            self.assertEqual(preprocess(key), value)
        for key, value in self.fth_data.items():
            self.assertEqual(preprocess(key), value)
        for key, value in self.hsub_data_with_params.items():
            self.assertEqual(
                preprocess(key, pipelines=["handle_substitute"], params={"handle_substitute": value["params"]}),
                value["result"]
            )


if __name__ == '__main__':
    unittest.main()
