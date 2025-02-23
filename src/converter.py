from abc import ABC, abstractmethod
import json
from types import SimpleNamespace
from handler import QueueHandler
from tkinter import filedialog
import pandas as pd
from pandas import DataFrame

from model import Property
from parser_enum import (
    DescriptionType,
    Error,
    KeyName,
    Similarity,
    Status,
    ModelTypeName,
    ModelTypeShortend,
)
from parser import Parser
import re

from util import deprecated


class ExcelConverter:
    def __init__(self):
        self.jsons = []
        self.translator = None
        self.smc_group = ModelTypeName.smc_group()
        self._hierarchies = [
            RootHierarchy(),
            NoneHierarchy(),
            HasParentHierarchy(),
            NestingHierarchy(),
        ]

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
            return Error.NOT_EXIST_FILE

        for file_path in file_paths:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.jsons.append((data, file_path))
            except Exception as e:
                return Error.FAIL_LOAD_FILE
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
    - (deprecated) add_translate_description
    - summary: 설명에 대한 한글 번역을 추가
    """

    @deprecated
    def add_translate_description(self, properties: Property):
        extracted = []
        for idx, prop in enumerate(properties):
            if prop.description is None:
                extracted.append({idx: ""})
            else:
                extracted.append({idx: prop.description})
        to_translate = [
            self.translator.kr_translator(content=next(iter(eng.values())))
            for eng in extracted
        ]

        for i, res in enumerate(to_translate):
            if res and properties[i].description:
                properties[i].description += "" + res

    """
    - add_constant_description
    - summary: submodel의 idShort에 대한 설명이 고정적인 경우, 미리 등록해놓은 description으로 설정
    """

    def add_constant_description(self, properties: Property, parser: Parser):
        descriptions = DescriptionType.find_by_name(parser.name)
        if descriptions:
            for prop in properties:
                sim, desc = next(
                    (
                        (Similarity.EQUAL, d)
                        for d in descriptions
                        if d.name.lower() == prop.id_short.lower()
                    ),
                    next(
                        (
                            (Similarity.SIMILARITY, d)
                            for d in descriptions
                            if d.name.lower() in prop.id_short.lower()
                        ),
                        (Similarity.NONE, None),
                    ),
                )
                if sim != Similarity.NONE and prop.description is None:
                    if sim == Similarity.EQUAL or (
                        sim == Similarity.SIMILARITY
                        and bool(re.search(r"[\d{]", prop.id_short))
                    ):
                        prop.description = desc.value[-1]

    """
    - apply_model_type_shortend
    - summary: 모델 타입 명에 약어를 적용
    """

    def apply_model_type_shortend(self, df: DataFrame):
        df.loc[:, KeyName.modelType.name] = df[KeyName.modelType.name].apply(
            ModelTypeShortend.replace_model_type_shortend
        )

    """
    - apply_depth_hierarchy
    - summary: depth를 기준으로 table을 트리구조로 변경
    """

    def apply_depth_hierarchy(self, df: DataFrame):
        _df = df.apply(lambda row: SimpleNamespace(**row), axis=1)
        max_depth = max(row.depth for row in _df)

        for i in range(1, max_depth):
            df[f"{ModelTypeShortend.SubmodelElementCollection.value}{i:02d}"] = None

        prev_r = None

        for i, r in df.iterrows():  # 25/02/12 - [fix] 부모 설정된 이전 행 관리
            r = SimpleNamespace(**r)
            prev_r = self._apply_parent_to_df(i, row=r, prev_row=prev_r, df=df)
            if prev_r is None:
                prev_r = r

        columns = [
            f"{ModelTypeShortend.SubmodelElementCollection.value}{i:02d}"
            for i in range(1, max_depth)
        ] + [
            KeyName.modelType.name,
            KeyName.idShort.name,
            KeyName.semanticId.name,
            KeyName.description.name,
        ]

        return df[columns]

    """
    - _apply_parent_from_df
    - summary: 데이터 프레임에 부모(SMC) 설정
    """

    def _apply_parent_to_df(
        self, index, row: SimpleNamespace, prev_row: SimpleNamespace, df: DataFrame
    ):
        for strategy in self._hierarchies:
            update_row, result = strategy.apply(index, row, prev_row, df)
            if result:
                return update_row

    """
    - convert_json_to_excel
    - summary: json 데이터를 엑셀파일로 변환하여 저장하고 성공한 목록을 반환
    """

    def convert_json_to_excel(self, queue_handler: QueueHandler):
        if self.jsons in [error for error in Error]:
            return
        try:
            for json, file_path in self.jsons:
                queue_handler.add({f"start converting {file_path}.": Status.START})
                parser = Parser(json)
                submodels = parser.create_indent_rows()
                df = pd.DataFrame(submodels)
                elements, hierarchy = parser.df_to_sequence_dict(df)

                properties = parser.sequence_dict_to_properties(elements, hierarchy)

                self.add_constant_description(properties, parser)

                table = [prop.to_json() for prop in properties]
                result_df = pd.DataFrame(table).sort_values(by="index")

                required_columns = [
                    "index",
                    "depth",
                    "modelType",
                    "idShort",
                    "reference",
                    "semanticId",
                    "description",
                    "parent",
                ]

                result_df = result_df.reindex(columns=required_columns, fill_value="")

                tree_df = self.apply_depth_hierarchy(result_df)

                tree_df = tree_df.dropna(how="all")

                self.apply_model_type_shortend(tree_df)

                saved = self.save_to_xlsx(tree_df, file_path)

                queue_handler.add(
                    {
                        f"{file_path.replace('.json', '.xlsx')} was successfully converted.": saved
                    }
                )
        except Exception as e:
            print(f"convert error : {e}")
            queue_handler.add(
                {
                    f"An error occurred while converting the file at {file_path}.": Status.ERROR
                }
            )


class HierarchyApply(ABC):
    @abstractmethod
    def apply(
        self, index, row: SimpleNamespace, prev_row: SimpleNamespace, df: DataFrame
    ):
        pass


class RootHierarchy(HierarchyApply):
    def apply(
        self, index, row: SimpleNamespace, prev_row: SimpleNamespace, df: DataFrame
    ):
        if (
            prev_row
            and row.modelType in ModelTypeName.smc_group_list()
            and prev_row.modelType not in ModelTypeName.smc_group_list()
            and not re.match(r"^[,\s]+$", row.reference)
        ) or (not prev_row and row.modelType in ModelTypeName.smc_group()):
            df.loc[index] = None
            return (row, True)
        return (row, False)


class NoneHierarchy(HierarchyApply):
    def apply(
        self, index, row: SimpleNamespace, prev_row: SimpleNamespace, df: DataFrame
    ):
        if not row.parent and row.depth < 2:
            if row.modelType not in ModelTypeName.smc_group():
                df.at[
                    index,
                    f"{ModelTypeShortend.SubmodelElementCollection.value}{row.depth:02d}",
                ] = "-"
            else:
                df.loc[index] = None
            return (row, True)
        return (row, False)


class HasParentHierarchy(HierarchyApply):
    def apply(
        self, index, row: SimpleNamespace, prev_row: SimpleNamespace, df: DataFrame
    ):
        if row.parent and prev_row.depth != row.depth and prev_row.parent != row.parent:
            df.at[
                index,
                f"{ModelTypeShortend.SubmodelElementCollection.value}{row.depth-1:02}",
            ] = row.parent
            return (row, True)
        return (row, False)


class NestingHierarchy(HierarchyApply):
    def apply(
        self, index, row: SimpleNamespace, prev_row: SimpleNamespace, df: DataFrame
    ):
        if (
            prev_row.modelType in ModelTypeName.smc_group()
            and row.modelType in ModelTypeName.smc_group()
            and prev_row.depth < row.depth
        ) or (
            not row.parent
            and row.depth - 1 == prev_row.depth
            and prev_row.modelType in ModelTypeName.smc_group()
            and row.modelType not in ModelTypeName.smc_group()
        ):
            df.at[
                index,
                f"{ModelTypeShortend.SubmodelElementCollection.value}{row.depth-1:02}",
            ] = prev_row.idShort
            return (row, True)
        return (row, False)
