# AAS Submodel json to excel program

> 해당 프로그램은 AASX Package Explorer V3.0을 기준으로 작성되었습니다.  
> ~~_문서작업 표 노가다 하기 싫어서 구현함_~~

<br>

## ❌ 25.02.22 번역 및 암호화 기능 삭제

## ❌ 24.11.15 EXE 직접 배포 중단

<br>

- 프로젝트 경로에서 다음 명령어 수행

```
pyinstaller --onefile --noconsole --collect-data=aas_test_engine ./src/main.py
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

##### 복수 파일 선택

![res2](https://github.com/user-attachments/assets/bae3faf5-c4ba-4097-a02b-ac4a0479e080)

##### 로깅

![res1](https://github.com/user-attachments/assets/3445b531-fa22-45d8-818b-ed0996d0d078)

##### 변환 결과

![res3](https://github.com/user-attachments/assets/ba95441a-4150-4fff-8858-ce6f9e9ac4e0)

##### Submodel_CarbonFootprint.xlsx

![Image](https://github.com/user-attachments/assets/f588bd73-9cb3-4b4f-b191-e863467462f4)
