from aas_test_engines import file
from tkinter import filedialog
from parser_enum import Error, TestFormat, Status, Level
from pathlib import Path
from handler import QueueHandler
import re


class TestAasEngine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TestAasEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.files = []

    def _open_type(self, extension):
        if extension == TestFormat.JSON.value or extension == TestFormat.XML.value:
            return "r"
        else:
            return "rb"

    """
    - load_test_file
    - summary: test할 aas 파일 선택
    """

    def load_test_file(self, queue_handler: QueueHandler):
        file_paths = filedialog.askopenfilenames(
            title="load to test file",
            filetypes=[("AASX", ".aasx"), ("JSON", "*.json"), ("XML", ".xml")],
        )

        if not file_paths:
            return Error.NOT_EXIST_FILE

        for file_path in file_paths:
            extension = Path(file_path).suffix
            try:
                with open(file_path, self._open_type(extension)) as file:
                    self.detect(extension, test_file=file, path=file_path)
            except Exception as e:
                queue_handler.add({e: Status.ERROR})
        return self.files

    """
    - detect
    - summary: 확장자에 따른 테스트 엔진 적용
    """

    def detect(self, extension, test_file, path):
        test_result = None
        if extension == TestFormat.AASX.value:
            test_result = file.check_aasx_file(test_file)
        if extension == TestFormat.JSON.value:
            test_result = file.check_json_file(test_file)
        if extension == TestFormat.XML.value:
            test_result = file.check_xml_file(test_file)

        if test_result:
            self.files.append((path, test_result))

    """
    - test_log
    - summary: 테스트 결과에 대한 로그 출력
    """

    def test_log(self, queue_handler: QueueHandler):
        test: file.AasTestResult
        pattern = re.compile(r"\033\[[0-9;]*m")
        for path, test in self.files:
            queue_handler.add({f"start test {path}.": Status.START})
            for line in test.to_lines():
                queue_handler.add(
                    {f"{pattern.sub('',line.strip())}": Level.color(Level.INFO)}
                )
            if test.ok():
                queue_handler.add(
                    {
                        f"{Status.END.value} {path} successfully passed.": Level.color(
                            Level.SUCCESS
                        )
                    }
                )
            else:
                queue_handler.add(
                    {
                        f"{Status.END.value} {path} pass failed.": Level.color(
                            Level.ERROR
                        )
                    }
                )
