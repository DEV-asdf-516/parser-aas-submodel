import json
from handler import QueueHandler
from tkinter import filedialog
import pandas as pd
from pandas import DataFrame

from model import Property
from parser_enum import Parser_Error, Status
from parser import Parser
from translator import GptService as GPT


class ExcelConverter:
    def __init__(self, translator=None):
        self.jsons = []
        self.translator = translator

    """
    - load_json_file
    - summary: json 파일 선택
    """

    def load_json_file(self):
        file_paths = filedialog.askopenfilenames(
            title="load to json file",
            filetypes=[("JSON", "*.json")],
            defaultextension=".json",
        )

        if not file_paths:
            return Parser_Error.NOT_EXIST_FILE

        for file_path in file_paths:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.jsons.append((data, file_path))
            except Exception as e:
                return Parser_Error.FAIL_LOAD_FILE
        return self.jsons

    """
    - save_to_xlsx
    - summary: DataFrame을 엑셀 형식으로 변환하여 저장
    """

    def save_to_xlsx(self, df: DataFrame, file_path):
        excel_file_path = file_path.replace(".json", ".xlsx")
        df.to_excel(excel_file_path, index=False)
        return Status.END

    """
    - add_translate_description
    - summary: 설명에 대한 한글 번역을 추가
    """

    def add_translate_description(self, properties: Property):
        if isinstance(self.translator, GPT):
            extracted = []
            for idx, prop in enumerate(properties):
                if prop.description is None or "[kr]" in prop.description:
                    extracted.append({idx: ""})
                else:
                    extracted.append({idx: prop.description})

            to_translate = [
                self.translator.kr_translator(content=next(iter(eng.values())))
                for eng in extracted
            ]

            for i, res in enumerate(to_translate):
                if res and properties[i].description:
                    properties[i].description += " [kr] " + res

    """
    - convert_json_to_excel
    - summary: json 데이터를 엑셀파일로 변환하여 저장하고 성공한 목록을 반환
    """

    def convert_json_to_excel(self, queue_handler: QueueHandler):
        if self.jsons in [error for error in Parser_Error]:
            return

        for json, file_path in self.jsons:
            queue_handler.add({f"start converting {file_path}.": Status.START})
            parser = Parser(json)
            submodels = parser.create_indent_rows()
            df = pd.DataFrame(submodels)
            elements, hierarchy = parser.df_to_sequence_dict(df)
            properties = parser.sequence_dict_to_properties(elements, hierarchy)
            # 한글 번역 추가
            self.add_translate_description(properties)
            table = [prop.to_json() for prop in properties]

            result_df = pd.DataFrame(table).sort_values(by="index")

            required_columns = [
                "index",
                "depth",
                "modelType",
                "idShort",
                "reference",
                "semanticId",
                "value",
                "description",
            ]

            result_df = result_df.reindex(columns=required_columns, fill_value="")

            rm_index_df = result_df.drop(columns=["index"])

            saved = self.save_to_xlsx(rm_index_df, file_path)

            queue_handler.add(
                {
                    f"{file_path.replace('.json', '.xlsx')} was successfully converted.": saved
                }
            )
