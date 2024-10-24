# AAS Submodel json to excel program

> 해당 프로그램은 AASX Package Explorer V3.0을 기준으로 작성되었습니다.  
> ~~_문서작업 표 노가다 하기 싫어서 구현함_~~

#### _❗❗❗ 업로드된 .exe 파일에는 한국어 번역 기능이 제거되었습니다._

<br>

## 요구사항

- 서브모델에 대해 해당 필드 값만 추출

```
- modelType
- idShort
- semanticId
- description
- value
```

- 어떤 항목에 하위 항목이 존재하는 경우, refrence 필드에 하위 항목 표기
- 항목에 대한 계층 단계를 depth 필드에 표기

<br>

## 🔍HOW TO USE

```
1. .aasx 파일을 AASX Package Explorer에서 로드한 후, 특정 서브모델을 선택한 뒤에 다음 과정을 거쳐 json 파일을 추출합니다.

    - File > Export ... > Export Submodel to JSON ...

2. parser.exe를 실행하여 추출한 json 파일을 엑셀파일로 변환합니다.
```

<br>

## 🔧기술 스택

<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"><img src="https://img.shields.io/badge/VSC-007ACC?style=for-the-badge&logo=Visual Studio Code&logoColor=white">

<br>

## 🛠구현 기능

- [x] JSON 파일 불러오기 & Excel 변환
- [x] OpenAI API를 활용하여 설명에 한국어 번역 추가
- [x] API Key 암/복호화 적용
- [x] tkinter로 GUI 환경 구현
- [x] Queue를 활용한 비동기 로그 처리
- [x] 표에 계층구조 적용

---

#### 📸 SCREEN SHOT

##### 복수 파일 선택

![res2](https://github.com/user-attachments/assets/bae3faf5-c4ba-4097-a02b-ac4a0479e080)

##### 로깅

![res1](https://github.com/user-attachments/assets/3445b531-fa22-45d8-818b-ed0996d0d078)

##### 변환 결과

![res3](https://github.com/user-attachments/assets/ba95441a-4150-4fff-8858-ce6f9e9ac4e0)

##### Submodel_Documentation.xlsx

![res4](https://github.com/user-attachments/assets/8e08e89c-1340-4532-9d49-894b81dbaeb7)

##### [24/10/22] Submodel_Documentation.xlsx 👉 계층구조 적용

![image](https://github.com/user-attachments/assets/fb0ce3a0-dc47-4872-9d1b-c0c58fbe3447)
