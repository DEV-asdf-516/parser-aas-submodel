import json
from handler import QueueHandler
from tkinter import filedialog
import pandas as pd
from pandas import DataFrame

from model import Property
from parser_enum import (
    DescriptionType,
    ParserError,
    Status,
)
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
            return ParserError.NOT_EXIST_FILE

        for file_path in file_paths:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.jsons.append((data, file_path))
            except Exception as e:
                return ParserError.FAIL_LOAD_FILE
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
    - add_constant_description
    - summary: submodel의 idShort에 대한 설명이 고정적인 경우, 미리 등록해놓은 description으로 설정
    """

    def add_constant_description(self, properties: Property, parser: Parser):
        descriptions = DescriptionType.find_by_name(parser.name)
        if descriptions:
            for prop in properties:
                desc = next(
                    (
                        d
                        for d in descriptions
                        if d.name.lower() == prop.id_short.lower()
                    ),
                    next(
                        (
                            d
                            for d in descriptions
                            if d.name.lower() in prop.id_short.lower()
                        ),
                        None,
                    ),
                )
                if desc is not None:
                    if prop.description is None or (
                        prop.description is not None and "[kr]" not in prop.description
                    ):
                        prop.description = desc.value[-1]

    """
    - apply_depth_hierarchy
    - summary: depth를 기준으로 table을 트리구조로 변경
    """

    def apply_depth_hierarchy(self, df: DataFrame):
        max_depth = df["depth"].max()

        for i in range(1, max_depth + 1):
            df[f"depth{i:02d}"] = None

        for i, r in df.iterrows():
            depth = r["depth"]
            id_short = r["idShort"]
            df.at[i, f"depth{depth:02d}"] = id_short

        columns = [f"depth{i:02d}" for i in range(1, max_depth + 1)] + [
            "modelType",
            "semanticId",
            "value",
            "description",
        ]
        return df[columns]

    """
    - convert_json_to_excel
    - summary: json 데이터를 엑셀파일로 변환하여 저장하고 성공한 목록을 반환
    """

    def convert_json_to_excel(self, queue_handler: QueueHandler):
        if self.jsons in [error for error in ParserError]:
            return

        for json, file_path in self.jsons:
            queue_handler.add({f"start converting {file_path}.": Status.START})
            parser = Parser(json)
            submodels = parser.create_indent_rows()
            df = pd.DataFrame(submodels)
            elements, hierarchy = parser.df_to_sequence_dict(df)

            properties = parser.sequence_dict_to_properties(elements, hierarchy)

            self.add_constant_description(properties, parser)
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

            tree_df = self.apply_depth_hierarchy(rm_index_df)

            saved = self.save_to_xlsx(tree_df, file_path)

            queue_handler.add(
                {
                    f"{file_path.replace('.json', '.xlsx')} was successfully converted.": saved
                }
            )
