from abc import ABC, abstractmethod
from pandas import DataFrame
import pandas as pd
from model import SubModelCollection, Property
from parser_enum import KeyName, ModelTypeName


class Parser:
    def __init__(self, json: dict):
        self.extract_columns = KeyName.extract_names()
        self.no_recursive_columns = [KeyName.language.name, KeyName.text.name]
        self.json = json
        self.name = None
        self._properties = {
            KeyName.index.name: PropertyIndex(),
            KeyName.idShort.name: PropertyIdShort(),
            KeyName.semanticId.name: PropertySemanticId(),
            KeyName.indent.name: PropertyIndent(),
            KeyName.modelType.name: PropertyModelType(),
            KeyName.description.name: PropertyDescription(),
            KeyName.value.name: PropertyValue(),
        }

    """
    - _create_smc_list
    - summary: SubmodelElementCollection 목록 생성
    """

    def _create_smc_list(self):
        elements = self.json.get(KeyName.submodelElements.name)
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
                    if key in [
                        KeyName.value.name,
                        KeyName.statements.name,
                    ] and isinstance(value, list):
                        recursive_smc.children = [
                            item.get(KeyName.idShort.name) for item in value
                        ]
                    self._extract_smc(value, smcs)
                else:
                    if key == KeyName.idShort.name:
                        recursive_smc.id_short = value
                    elif (
                        key == KeyName.modelType.name
                        and value in ModelTypeName.smc_group()
                    ):
                        recursive_smc.model_type = value
        elif isinstance(elements, list):
            for element in elements:
                self._extract_smc(element, smcs)
        if recursive_smc.filled:
            smcs.append(recursive_smc)
        return smcs

    """
    - _extract_smc_childeren
    - summary: SubmodelElementCollection의 자식목록 추출
    """

    def _extract_smc_childeren(self, parents: SubModelCollection, rows: Property):
        for smc in parents:
            ref = [prop for prop in rows if prop.id_short == smc.id_short]
            sub_hierachies = [key for key in parents if key.id_short == smc.id_short]
            for i, r in enumerate(ref):
                try:
                    if not r.is_allocated(r.reference):
                        r.reference = ", ".join(sub_hierachies[i].children)
                        r.model_type = sub_hierachies[i].model_type
                    else:
                        break
                except IndexError as e:
                    # [fix] 24/12/05 - 자식목록 없는 경우 예외처리
                    r.refrence = ""
                    r.model_type = sub_hierachies[0].model_type

    """
    - _allocated_parent
    - summary: Property에 부모가 존재하는 경우 부모 설정
    """

    def _allocated_parent(self, parents: SubModelCollection, rows: Property):
        # 상위 SMC 추가
        indexing_rows = sorted(
            rows, key=lambda r: r.index
        )  # 25/01/13 - [fix] rows 인덱스 순서 보장
        allocated_count = {p.id_short: 0 for p in parents}
        for r in indexing_rows:
            parent = [
                (
                    p.id_short,
                    len(p.children or []),
                )
                for p in parents
                if r.id_short in (p.children or [])
            ]
            if not parent:
                continue
            else:  # 25/01/06 - [fix] 부모 설정 알고리즘 개선
                for p, max_children in parent:
                    if allocated_count[p] < max_children:
                        r.parent = p
                        allocated_count[p] += 1
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
      ['description', 'Balance of greenhouse gas emissions along the entire life cycle of a product in a defined application and in relation to a defined unit of use'],
      ['semanticId', 'https://admin-shell.io/idta/CarbonFootprint/ProductCarbonFootprint/0/9'],
      ['', 'idShort', 'PCFCalculationMethod'],
      ['', 'description', 'Standard, method for determining the greenhouse gas emissions of a product'], 
      ['', 'description', 'Norm, Standard, Verfahren zur Ermittlung der Treibhausgas-Emissionen eines Produkts']
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
                        flattened.append(indent + [key, value])  # 현재 키와 값 추가

                if (
                    key == KeyName.semanticId.name
                    and isinstance(value, dict)
                    and KeyName.keys.name in value
                ):  # semanticId의 keys에서 value값만 추가
                    indent = [""] * parent_depth
                    for key_entry in value.get(KeyName.keys.name):
                        flattened.append(
                            indent + [key, key_entry.get(KeyName.value.name)]
                        )
                if (
                    key in [KeyName.description.name, KeyName.value.name]
                    and isinstance(value, list)
                    and value
                ):
                    indent = [""] * parent_depth
                    for v in value:
                        if key == KeyName.description.name or (
                            key
                            == KeyName.value.name  # multiLanguageProperty value값 추출
                            and any(k in v for k in self.no_recursive_columns)
                        ):
                            flattened.append(
                                indent + [key, f"{v.get(KeyName.text.name)}"]
                            )

        elif isinstance(element, list):
            for sub_element in element:
                self._to_flattend(sub_element, parent_depth, flattened)

        return flattened

    """
    - create_indent_rows
    - summary: DataFrame 생성을 위해 json의 각 key-value를 depth에 따른 리스트 형태로 변형
    """

    def create_indent_rows(self):
        self.name = self.json.get(KeyName.idShort.name)
        elements = self.json.get(KeyName.submodelElements.name)
        return self._to_flattend(elements, 0, [])

    """
    - df_to_sequence_dict
    - summary: DataFrame을 딕셔너리 형태로 변경
    예)
    ========================================================================= [BEFORE > DataFrame] =========================================================================
                    0                                                  1                                                  2     3
        0        idShort                             ProductCarbonFootprint                                               None  None
        1    description  Balance of greenhouse gas emissions along...                                               None  None
        2     semanticId  https://admin-shell.io/idta/CarbonFootprint/Pr...                                               None  None
        3                                                           idShort                               PCFCalculationMethod  None
        4                                                       description  Standard, method for determining the gree...  None
        ..           ...                                                ...                                                ...   ...
        171                                                     description  Time at which something should no longer ...  None
        172                                                      semanticId  https://admin-shell.io/idta/CarbonFootprint/Ex...  None
        173                                                           value                                                     None
        174                                                       modelType                                           Property  None
        175    modelType                          SubmodelElementCollection                                               None  None

    ========================================================================= [AFTER > Dictionary] =========================================================================
    {
      'ProductCarbonFootprint': [
          {'idShort': 'ProductCarbonFootprint'},
          {'index': 0},
          {'indent': 0},
          {'description': 'Balance of greenhouse gas emissions along the entire life cycle of a product in a defined application and in relation to a defined unit of use'}, 
          {'index': 1}, 
          {'indent': 0},
          {'semanticId': 'https://admin-shell.io/idta/CarbonFootprint/ProductCarbonFootprint/0/9'},
          {'index': 2},
          {'indent': 0},
          {'idShort': 'PCFCalculationMethod'},
          {'index': 3},
          {'indent': 1},
          {'description': 'Standard, method for determining the greenhouse gas emissions of a product'}, 
          {'index': 4}, 
          {'indent': 1}, 
          {'description': 'Norm, Standard, Verfahren zur Ermittlung der Treibhausgas-Emissionen eines Produkts'}, 
          {'index': 5}, 
          {'indent': 1},
          {'semanticId': '0173-1#02-ABG854#001'},
          {'index': 6},
          {'indent': 1},
          {'value': ''},
          {'index': 7},
          {'indent': 1},
          {'modelType': 'Property'},
          ...
          {'modelType': 'SubmodelElementCollection'},
          {'index': 175},
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

            if key == KeyName.idShort.name:
                parent_key = [parent for parent in parents if parent.id_short == value]
                if parent_key:
                    empty_ids.clear()
                    sequence = parent_key[0].id_short
                    empty_ids = parent_key[0].children.copy()

            if sequence not in sequence_dict:
                sequence_dict[sequence] = []

            if key == KeyName.idShort.name and not value and empty_ids:
                sequence_dict[sequence].append({key: empty_ids[0]})
                empty_ids.pop(0)
            else:
                sequence_dict[sequence].append({key: value})
            sequence_dict[sequence].append({KeyName.index.name: index})
            sequence_dict[sequence].append({KeyName.indent.name: indent})

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
          {'description': 'Balance of greenhouse gas emissions along the entire life cycle of a product in a defined application and in relation to a defined unit of use'}, 
          {'index': 1}, 
          {'indent': 0},
          {'semanticId': 'https://admin-shell.io/idta/CarbonFootprint/ProductCarbonFootprint/0/9'},
          {'index': 2},
          {'indent': 0},
          {'idShort': 'PCFCalculationMethod'},
          {'index': 3},
          {'indent': 1},
          {'description': 'Standard, method for determining the greenhouse gas emissions of a product'}, 
          {'index': 4}, 
          {'indent': 1}, 
          {'description': 'Norm, Standard, Verfahren zur Ermittlung der Treibhausgas-Emissionen eines Produkts'}, 
          {'index': 5}, 
          {'indent': 1},
          {'semanticId': '0173-1#02-ABG854#001'},
          {'index': 6},
          {'indent': 1},
          {'value': ''},
          {'index': 7},
          {'indent': 1},
          {'modelType': 'Property'},
          ...
          {'modelType': 'SubmodelElementCollection'},
          {'index': 175},
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
       'description': 'Balance of greenhouse gas emissions along the entire life cycle of a product in a defined application and in relation to a defined unit of use',
       'value': None,
       'reference': 'PCFCalculationMethod, PCFCO2eq, PCFReferenceValueForCalculation, PCFQuantityOfMeasureForCalculation, PCFLifeCyclePhase, ExplanatoryStatement, PCFGoodsAddressHandover, PublicationDate, ExpirationDate'
      },
      {
       'index': 3,
       'depth': 2,
       'idShort': 'PCFCalculationMethod',
       'semanticId': '0173-1#02-ABG854#001',
       'modelType': 'Property',
       'description': 'Standard, method for determining the greenhouse gas emissions of a product Norm, Standard, Verfahren zur Ermittlung der Treibhausgas-Emissionen eines Produkts',
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
                    self._apply_property_value_from_dict(prop, item)

                if (
                    idx < len(items) - 1
                    and isinstance(items[idx + 1], dict)
                    and KeyName.idShort.name in items[idx + 1]
                ) or idx == len(items) - 1:
                    if prop.is_allocated(prop.id_short):
                        rows.append(prop)
                    prop = Property()

        self._extract_smc_childeren(parents, rows)
        self._allocated_parent(parents, rows)

        return rows

    """
    - _apply_property_value_from_dict
    - summary: 딕셔너리 값을 Property 객체에 할당
    """

    def _apply_property_value_from_dict(self, prop, item):
        for key, strategy in self._properties.items():
            if key in item:
                strategy.apply(prop, item)


class PropertyApply(ABC):
    @abstractmethod
    def apply(self, prop: Property, item: dict):
        pass


class PropertyIndex(PropertyApply):
    def apply(self, prop: Property, item: dict):
        if not prop.is_allocated(prop.index):
            prop.index = item.get(KeyName.index.name, 0)


class PropertyIdShort(PropertyApply):
    def apply(self, prop: Property, item: dict):
        prop.id_short = item.get(KeyName.idShort.name)


class PropertySemanticId(PropertyApply):
    def apply(self, prop: Property, item: dict):
        prop.semantic_id = item.get(KeyName.semanticId.name)


class PropertyIndent(PropertyApply):
    def apply(self, prop: Property, item: dict):
        if not prop.is_allocated(prop.depth):
            prop.depth = item.get(KeyName.indent.name) + 1


class PropertyModelType(PropertyApply):
    def apply(self, prop: Property, item: dict):
        if not prop.is_allocated(prop.model_type):
            prop.model_type = item.get(KeyName.modelType.name)


class PropertyDescription(PropertyApply):
    def apply(self, prop: Property, item: dict):
        if prop.is_allocated(prop.description):
            prop.description += "\n" + item.get(KeyName.description.name)
        else:
            prop.description = item.get(KeyName.description.name)


class PropertyValue(PropertyApply):
    def apply(self, prop: Property, item: dict):
        prop.value = item.get(KeyName.value.name)
