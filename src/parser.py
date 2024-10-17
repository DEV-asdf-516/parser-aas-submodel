from pandas import DataFrame
import pandas as pd
from model import SubModelCollection, Property


class Parser:
    def __init__(self, json):
        self.extract_columns = [
            "idShort",
            "modelType",
            "value",
            "language",
            "text",
            "statements",
            "description",
        ]
        self.languages = ["kr", "KR", "en", "EN", "de", "fr", "jp"]
        self.json = json

    """
    - _create_smc_list
    - summary: SubmodelElementCollection 목록 생성
    """

    def _create_smc_list(self):
        elements = self.json["submodelElements"]
        smc_list = self._extract_smc(elements, [])
        extracted = [smc for smc in smc_list if smc.model_type is not None]
        return extracted

    """
    - _extract_smc
    - summary: SubmodelElementCollection의 모든 하위 항목을 추출
    """

    def _extract_smc(self, elements, smcs=[]):
        recursive_smc = SubModelCollection()
        if isinstance(elements, dict):
            for key, value in elements.items():
                if isinstance(value, dict) or isinstance(value, list):
                    if key in ["value", "statements"] and isinstance(value, list):
                        recursive_smc.children = [
                            (
                                f"#{i:02d}"
                                if not item.get("idShort", "")
                                else item.get("idShort")
                            )
                            for i, item in enumerate(value)
                        ]
                    self._extract_smc(value, smcs)
                else:
                    if key == "idShort":
                        recursive_smc.id_short = value
                    elif key == "modelType" and value in [
                        "SubmodelElementCollection",
                        "Entity",
                        "SubmodelElementList",
                    ]:
                        recursive_smc.model_type = value
        elif isinstance(elements, list):
            for element in elements:
                self._extract_smc(element, smcs)
        if recursive_smc.filled:
            smcs.append(recursive_smc)
        return smcs

    """
    _extract_smc_childeren
    summary: SubmodelElementCollection의 자식목록 추출
    """

    def _extract_smc_childeren(self, parents: SubModelCollection, rows: Property):
        for smc in parents:
            ref = [prop for prop in rows if prop.id_short == smc.id_short]
            sub_hierachies = [key for key in parents if key.id_short == smc.id_short]
            for i, r in enumerate(ref):
                if not r.is_allocated(r.reference):
                    r.reference = ", ".join(sub_hierachies[i].children)
                    r.model_type = sub_hierachies[i].model_type
                else:
                    break

    """
    - _to_flattend
    - summary: 깊이가 존재하는 json 형태를 list 형태로 평탄화 작업 수행
               각 depth는 공백으로 구분됨
    예)
    ========================================================================= [BEFORE > JSON] =========================================================================
    {
      "idShort": "ProductCarbonFootprint",
      "description": [
        {
          "language": "en",
          "text": "Balance of greenhouse gas emissions along the entire life cycle of a product in a defined application and in relation to a defined unit of use"
        }
      ],
      "semanticId": {
        "type": "ExternalReference",
        "keys": [
          {
            "type": "GlobalReference",
            "value": "https://admin-shell.io/idta/CarbonFootprint/ProductCarbonFootprint/0/9"
          }
        ]
      },
      "value": [
        {
          "idShort": "PCFCalculationMethod",
          "description": [
            {
              "language": "en",
              "text": "Standard, method for determining the greenhouse gas emissions of a product"
            },
            {
              "language": "de",
              "text": "Norm, Standard, Verfahren zur Ermittlung der Treibhausgas-Emissionen eines Produkts"
            }
          ],
          "semanticId": {
            "type": "ExternalReference",
            "keys": [
              {
                "type": "GlobalReference",
                "value": "0173-1#02-ABG854#001"
              }
            ]
          },
          "value": "",
          "modelType": "Property"
        },
        ...
      ],
      "modelType": "SubmodelElementCollection"
    }
    
    ========================================================================= [AFTER > LIST] =========================================================================
    [
      ['idShort', 'ProductCarbonFootprint'],
      ['description', 'en'],
      ['description', 'Balance of greenhouse gas emissions along the entire life cycle of a product in a defined application and in relation to a defined unit of use'],
      ['semanticId', 'https://admin-shell.io/idta/CarbonFootprint/ProductCarbonFootprint/0/9'],
      ['', 'idShort', 'PCFCalculationMethod'],
      ['', 'description', 'en'],
      ['', 'description', 'Standard, method for determining the greenhouse gas emissions of a product'],
      ['', 'description', 'de'],
      ['', 'description', 'Norm, Standard, Verfahren zur Ermittlung der Treibhausgas-Emissionen eines Produkts'],
      ['', 'semanticId', '0173-1#02-ABG854#001'],
      ['', 'value', ''],
      ['', 'modelType', 'Property'],
      ['modelType', 'SubmodelElementCollection'],
    ...
    ]
    """

    def _to_flattend(self, element, parent_depth: int, flattened=[]):
        if isinstance(element, dict):
            for key, value in element.items():
                indent = [""] * parent_depth  # depth 탐지
                if key in self.extract_columns:  # 원하는 키만 추출
                    if isinstance(value, dict):
                        flattened.append(indent + [key])  # 현재 키 추가
                        self._to_flattend(
                            value, parent_depth + 1, flattened
                        )  # 깊이를 증가시켜 재귀 호출
                    elif isinstance(value, list):
                        for item in value:
                            self._to_flattend(
                                item, parent_depth + 1, flattened
                            )  # 리스트 항목에 대해 재귀 호출
                    else:
                        if key in ["language", "text"]:
                            key = "description"
                            indent.pop()
                            flattened.append(indent + [key, value])
                        else:
                            flattened.append(indent + [key, value])  # 현재 키와 값 추가

                if (
                    key == "semanticId" and isinstance(value, dict) and "keys" in value
                ):  # semanticId의 keys에서 value값만 추가
                    indent = [""] * parent_depth
                    for key_entry in value.get("keys"):
                        flattened.append(indent + [key, key_entry.get("value")])

        elif isinstance(element, list):
            for sub_element in element:
                self._to_flattend(sub_element, parent_depth, flattened)

        return flattened

    """
    - create_indent_rows
    - summary: DataFrame 생성을 위해 json의 각 key-value를 depth에 따른 리스트 형태로 변형
    """

    def create_indent_rows(self):
        elements = self.json["submodelElements"]
        return self._to_flattend(elements, 0, [])

    """
    - df_to_sequence_dict
    - summary: DataFrame을 딕셔너리 형태로 변경
    예)
    ========================================================================= [BEFORE > DataFrame] =========================================================================
                   0                                                  1                                                  2     3
    0        idShort                             ProductCarbonFootprint                                               None  None
    1    description                                                 en                                               None  None
    2    description  Balance of greenhouse gas emissions along the ...                                               None  None
    3     semanticId  https://admin-shell.io/idta/CarbonFootprint/Pr...                                               None  None
    4                                                           idShort                               PCFCalculationMethod  None
    ..           ...                                                ...                                                ...   ...
    208                                                     description  Time at which something should no longer be us...  None
    209                                                      semanticId  https://admin-shell.io/idta/CarbonFootprint/Ex...  None
    210                                                           value                                                     None
    211                                                       modelType                                           Property  None
    212    modelType                          SubmodelElementCollection                                               None  None

    ========================================================================= [AFTER > Dictionary] =========================================================================
    {
      'ProductCarbonFootprint': [
          {'idShort': 'ProductCarbonFootprint'},
          {'index': 0},
          {'indent': 0},
          {'description': 'en'},
          {'index': 1},
          {'indent': 0},
          {'description': 'Balance of greenhouse gas emissions along the entire life cycle of a product in a defined application and in relation to a defined unit of use'},
          {'index': 2},
          {'indent': 0},
          {'semanticId': 'https://admin-shell.io/idta/CarbonFootprint/ProductCarbonFootprint/0/9'},
          {'index': 3},
          {'indent': 0},
          {'idShort': 'PCFCalculationMethod'},
          {'index': 4},
          {'indent': 1},
          {'description': 'en'},
          {'index': 5},
          {'indent': 1},
          {'description': 'Standard, method for determining the greenhouse gas emissions of a product'},
          {'index': 6},
          {'indent': 1},
          {'description': 'de'},
          {'index': 7},
          {'indent': 1},
          {'description': 'Norm, Standard, Verfahren zur Ermittlung der Treibhausgas-Emissionen eines Produkts'},
          {'index': 8},
          {'indent': 1},
          {'semanticId': '0173-1#02-ABG854#001'},
          {'index': 9},
          {'indent': 1},
          {'value': ''},
          {'index': 10},
          {'indent': 1},
          {'modelType': 'Property'},
          ...
          {'modelType': 'SubmodelElementCollection'},
          {'index': 212},
          {'indent': 0}
      ],
      ...
    }
    """

    def df_to_sequence_dict(self, df: DataFrame):
        parents = self._create_smc_list()

        sequence_dict = {}
        sequence = ""

        empty_ids = []
        # 데이터 프레임을 순회하면서 필요한 정보를 추출
        for index, row in df.iterrows():
            indent = int((row.eq("")).sum())

            key = ""
            value = ""

            row = [x for x in row if pd.notnull(x)]

            if len(row) < 2:
                key = row[0]
                value = ""
            else:
                key = row[-2]
                value = row[-1]
                if not value:
                    indent -= 1

            if key == "idShort":
                parent_key = [parent for parent in parents if parent.id_short == value]
                if parent_key:
                    empty_ids.clear()
                    sequence = parent_key[0].id_short
                    empty_ids = parent_key[0].children.copy()

            if sequence not in sequence_dict:
                sequence_dict[sequence] = []

            if key == "idShort" and not value and empty_ids:
                sequence_dict[sequence].append({key: empty_ids[0]})
                empty_ids.pop(0)
            else:
                sequence_dict[sequence].append({key: value})
            sequence_dict[sequence].append({"index": index})
            sequence_dict[sequence].append({"indent": indent})

        return sequence_dict, parents

    """
    - sequence_dict_to_properties
    - summary: 딕셔너리를 Property 객체로 변경
    예)
    ========================================================================= [BEFORE > Dictonary] =========================================================================
    {
      'ProductCarbonFootprint': [
          {'idShort': 'ProductCarbonFootprint'},
          {'index': 0},
          {'indent': 0},
          {'description': 'en'},
          {'index': 1},
          {'indent': 0},
          {'description': 'Balance of greenhouse gas emissions along the entire life cycle of a product in a defined application and in relation to a defined unit of use'},
          {'index': 2},
          {'indent': 0},
          {'semanticId': 'https://admin-shell.io/idta/CarbonFootprint/ProductCarbonFootprint/0/9'},
          {'index': 3},
          {'indent': 0},
          {'idShort': 'PCFCalculationMethod'},
          {'index': 4},
          {'indent': 1},
          {'description': 'en'},
          {'index': 5},
          {'indent': 1},
          {'description': 'Standard, method for determining the greenhouse gas emissions of a product'},
          {'index': 6},
          {'indent': 1},
          {'description': 'de'},
          {'index': 7},
          {'indent': 1},
          {'description': 'Norm, Standard, Verfahren zur Ermittlung der Treibhausgas-Emissionen eines Produkts'},
          {'index': 8},
          {'indent': 1},
          {'semanticId': '0173-1#02-ABG854#001'},
          {'index': 9},
          {'indent': 1},
          {'value': ''},
          {'index': 10},
          {'indent': 1},
          {'modelType': 'Property'},
          ...
          {'modelType': 'SubmodelElementCollection'},
          {'index': 212},
          {'indent': 0}
      ],
      ...
    }

    ========================================================================= [AFTER > Object] =========================================================================
    [
      {
       'index': 1,
       'depth': 1,
       'idShort': 'ProductCarbonFootprint',
       'semanticId': 'https://admin-shell.io/idta/CarbonFootprint/ProductCarbonFootprint/0/9',
       'modelType': 'SubmodelElementCollection',
       'description': '[en] Balance of greenhouse gas emissions along the entire life cycle of a product in a defined application and in relation to a defined unit of use',
       'value': None,
       'reference': 'PCFCalculationMethod, PCFCO2eq, PCFReferenceValueForCalculation, PCFQuantityOfMeasureForCalculation, PCFLifeCyclePhase, ExplanatoryStatement, PCFGoodsAddressHandover, PublicationDate, ExpirationDate'
      },
      {
       'index': 4,
       'depth': 2,
       'idShort': 'PCFCalculationMethod',
       'semanticId': '0173-1#02-ABG854#001',
       'modelType': 'Property',
       'description': '[en] Standard, method for determining the greenhouse gas emissions of a product [de] Norm, Standard, Verfahren zur Ermittlung der Treibhausgas-Emissionen eines Produkts',
       'value': '',
       'reference': None
      },
      ...
    ]
    """

    def sequence_dict_to_properties(
        self, sequence_dict: dict, parents: SubModelCollection
    ):
        rows = []
        for items in sequence_dict.values():

            prop = Property()

            for idx, item in enumerate(items):
                if isinstance(item, dict):
                    if "index" in item:
                        if not prop.is_allocated(prop.index):
                            prop.index = item.get("index", 0)
                    if "idShort" in item:
                        prop.id_short = item.get("idShort")
                    if "semanticId" in item:
                        prop.semantic_id = item.get("semanticId")
                    if "indent" in item:
                        if not prop.is_allocated(prop.depth):
                            prop.depth = item.get("indent") + 1
                    if "modelType" in item:
                        if not prop.is_allocated(prop.model_type):
                            prop.model_type = item.get("modelType")
                    if "description" in item:
                        desc = (
                            f'[{item.get("description")}]'
                            if item.get("description") in self.languages
                            else item.get("description")
                        )
                        if prop.is_allocated(prop.description):
                            prop.description += " " + desc
                        else:
                            prop.description = desc
                    if "value" in item:
                        prop.value = item.get("value")

                if (
                    idx < len(items) - 1
                    and isinstance(items[idx + 1], dict)
                    and "idShort" in items[idx + 1]
                ) or idx == len(items) - 1:
                    if prop.is_allocated(prop.id_short):
                        rows.append(prop)
                        prop = Property()

        self._extract_smc_childeren(parents, rows)

        return rows
