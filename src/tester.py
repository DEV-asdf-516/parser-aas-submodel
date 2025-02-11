from aas_test_engines import file
from tkinter import filedialog
from parser_enum import Error, TestFormat, Status, Level
from pathlib import Path
from handler import QueueHandler
import io
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
    - test_detail_log
    - summary: 테스트 결과에 대한 상세 로그 출력
    """

    def test_detail_log(self, queue_handler: QueueHandler):
        for path, test in self.files:
            queue_handler.add({f"start test {path}.": Status.START})
            queue_handler.add({f"{test.message.strip()}": Level.color(Level.TRACE)})
            message = self.record(test)
            queue_handler.add({f"{message}": Level.color(test.sub_results[-1].level)})
            if test.ok():
                queue_handler.add({f"{path} successfully passed.": Status.END})
            else:
                queue_handler.add({f"{path} pass failed.": Status.END})

    """
    - test_simple_log
    - summary: 테스트 결과에 대한 간략한 로그 출력
    """

    def test_simple_log(self, queue_handler: QueueHandler):
        for path, test in self.files:
            queue_handler.add({f"start test {path}.": Status.START})
            queue_handler.add({f"{test.message.strip()}": Level.color(Level.TRACE)})

            for sub in test.sub_results:
                queue_handler.add({f"{sub.message}": Level.color(sub.level)})
            if test.ok():
                queue_handler.add({f"{path} successfully passed.": Status.END})
            else:
                queue_handler.add({f"{path} pass failed.": Status.END})

    """
    - record
    - summary: 테스트 결과를 기록
    """

    def record(self, test: file.AasTestResult):
        buffer = io.StringIO()
        for line in test.to_lines():
            pattern = r"\033\[[0-9;]*m"
            buffer.write(f"{re.sub(pattern,'',line.strip())}\n")
        message = buffer.getvalue().rstrip()
        buffer.close()
        return message
