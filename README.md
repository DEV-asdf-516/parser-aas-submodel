# AAS Submodel json to excel program

> 해당 프로그램은 AASX Package Explorer V3.0을 기준으로 작성되었습니다.  
> ~~_문서작업 표 노가다 하기 싫어서 구현함_~~

<br>

## 👇 Download Here

> https://github.com/DEV-asdf-516/parser-aas-submodel/releases

<br>

## Use CLI

- 프로젝트 경로에서 다음 명령어 수행

```
git clone https://github.com/DEV-asdf-516/parser-aas-submodel.git

pip install -r requirements.txt

pyinstaller --onefile --noconsole --collect-data=aas_test_engines ./src/main.py
```

<br>

## 요구사항

- 서브모델에 대해 해당 필드 값만 추출

```
- modelType
- idShort
- semanticId
- description
```

- 항목에 대한 계층 단계를 SMC 필드에 표기

<br>

## 🔍HOW TO USE

```
1. .aasx 파일을 AASX Package Explorer에서 로드한 후, 특정 서브모델을 선택한 뒤에 다음 과정을 거쳐 json 파일을 추출합니다.

    - File > Export ... > Export Submodel to JSON ...

2. exe 파일을 실행하여 추출한 json 파일을 엑셀파일로 변환합니다.
```

<br>

## 🔧기술 스택

<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"><img src="https://img.shields.io/badge/VSC-007ACC?style=for-the-badge&logo=Visual Studio Code&logoColor=white">

<br>

## 🛠구현 기능

- [x] JSON 파일 불러오기 & Excel 변환
- [x] ~~OpenAI API를 활용하여 설명에 한국어 번역 추가~~
- [x] ~~API Key 암/복호화 적용~~
- [x] GUI 환경 구현
- [x] 로그 출력
- [x] 모델링 파일 테스트 엔진 추가

---

#### 📸 SCREEN SHOT

#### JSON to XLSX Convert

![Image](https://github.com/user-attachments/assets/ba17a019-0ea0-4d37-b8a5-5d1cf06a43b0)

#### Submodel_CarbonFootprint.xlsx

![Image](https://github.com/user-attachments/assets/139e1ef8-0b0c-40c8-b4b5-015a7ac2f345)

#### AAS File Test

![Image](https://github.com/user-attachments/assets/4dd8dc80-08d8-4e12-b5b3-8cd7d92d6933)
