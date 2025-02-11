from enum import Enum, auto


class Level(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2
    CRITICAL = 3
    TRACE = 4

    def color(self) -> str:
        if self.value == 0:
            return "black"
        if self.value == 1:
            return "brown"
        if self.value == 2 or self.value == 3:
            return "red"
        return "blue"


class TestFormat(Enum):
    JSON = ".json"
    XML = ".xml"
    AASX = ".aasx"

    @classmethod
    def find_by_name(cls, name):
        return next((f.value for f in cls if f.name.lower() == name.lower()), [])


class Error(Enum):
    NOT_EXIST_FILE = auto()
    FAIL_LOAD_FILE = auto()


class Status(Enum):
    START = "===============================================================================\n[START]"
    END = "[END]"
    ERROR = "[FAIL]"


class Similarity(Enum):
    EQUAL = auto()
    SIMILARITY = auto()


class IdentificationDescription(Enum):
    ManufacturerName = (
        auto(),
        "[en] The company's name that makes the product. [kr] 제품을 만드는 회사 이름.",
    )
    ManufacturerId = (
        auto(),
        "[en] Internationally unique identification number for the manufacturer of the device or the product and for the physical location. [kr] 장치 또는 제품 제조업체와 물리적 위치에 대한 국제 고유 식별 번호.",
    )
    ManufacturerIdProvider = (
        auto(),
        "[en] DUNS-no., supplier number, or other number as identifier of an offeror or supplier of the identification. [kr] DUNS 번호, 공급업체 번호 또는 식별 제공자 또는 공급업체의 식별자로 사용되는 기타 번호.",
    )
    ManufacturerTypId = (
        auto(),
        "[en] unique product identifier of the manufacturer. [kr] 제조업체의 고유 제품 식별자.",
    )
    ManufacturerTypName = (
        auto(),
        "[en] Short description of the product. [kr] 제품에 대한 간단한 설명.",
    )
    ManufacturerTypDescription = (
        auto(),
        "[en] Description of the product, it's technical features and implementation if needed. [kr] 제품 설명, 기술적 특징 및 필요한 경우 구현.",
    )
    SupplierName = (
        auto(),
        "[en] name of supplier which provides the customer with a product or a service. [kr] 고객에게 제품이나 서비스를 제공하는 공급자 이름.",
    )
    SupplierId = (
        auto(),
        "[en] Internationally unique identification number for the supplier of the device or the product and for the physical location. [kr] 장치 또는 제품 공급업체와 물리적 위치에 대한 국제 고유 식별 번호.",
    )
    SupplierIdProvider = (
        auto(),
        "[en] The unique identifier for the supplier. [kr] 공급업체의 고유 식별자.",
    )
    SupplierTypId = (
        auto(),
        "[en] unique product order identifier of the supplier. [kr] 공급자의 고유한 제품 주문 식별자.",
    )
    SupplierTypName = (
        auto(),
        "[en] Short description of the product. [kr] 제품에 대한 간단한 설명.",
    )
    SupplierTypDescription = (
        auto(),
        "[en] Description of the product, it's technical features and implementation if needed. [kr] 제품 설명, 기술적 특징 및 필요한 경우 구현.",
    )
    TypClass = (
        auto(),
        "[en] Class of type or category . [kr] 유형이나 카테고리의 분류.",
    )
    ClassificationSystem = (
        auto(),
        "[en] system used to categorize products or information. [kr] 제품이나 정보를 분류하는데 사용되는 시스템.",
    )
    SecondaryKeyTyp = (
        auto(),
        "[en] type of key used for additional data categorization. [kr] 추가 데이터 분류에 사용되는 키 유형.",
    )
    TypThumbnail = (
        auto(),
        "[en] small preview image representing a type or category. [kr] 유형이나 카테고리를 나타내는 작은 미리보기 이미지.",
    )
    AssetId = (
        auto(),
        "[en] A unique identifier for an asset. [kr] 자산의 고유 식별자.",
    )
    InstanceId = (
        auto(),
        "[en] A unique code for an instance or version of an asset. [kr] 자산의 인스턴스나 버전을 위한 고유 코드.",
    )
    ChargeId = (
        auto(),
        "[en] Number assigned by the manufacturer of a material to identify the manufacturer's batch. [kr] 제조업체의 배치를 식별하기 위해 자재 제조업체가 할당한 번호.",
    )
    SecondaryKeyInstance = (
        auto(),
        "[en] An additional unique identifier for an asset instance. [kr] 자산 인스턴스의 추가 고유 식별자.",
    )
    ManufacturingDate = (
        auto(),
        "[en] Date from which the production and / or development process is completed or from which a service is provided completely. [kr] 생산 및/또는 개발 프로세스가 완료되거나 서비스가 완전히 제공되는 날짜.",
    )
    DeviceRevision = (
        auto(),
        "[en] an updated version of Device. [kr] 업데이트된 버전의 장치.",
    )
    SoftwareRevision = (
        auto(),
        "[en] an updated version of Software. [kr] 업데이트된 버전의 소프트웨어.",
    )
    HardwareRevision = (
        auto(),
        "[en] a modified version or modification of Hardware for Problem correction. [kr] 문제 해결을 위한 하드웨어 수정 또는 수정.",
    )
    QrCode = (
        auto(),
        "[en] a type of two-dimensional matrix barcode. [kr] 2차원 매트릭스 바코드의 일종.",
    )
    Name = (
        auto(),
        "[en] The name of the supplier that provides the customer with a product or a service. [kr] 고객에게 제품이나 서비스를 제공하는 공급자 이름.",
    )
    Role = (
        auto(),
        "[en] The specific part or function they have in the context. [kr] 맥락에 따른 특정 역할 또는 기능.",
    )
    CountryCode = (
        auto(),
        "[en] Agreed upon symbol for unambiguous identification of a country. [kr] 국가를 명확하게 식별하기 위해 합의된 기호.",
    )
    Street = (auto(), "[en] The street part of an address. [kr] 주소의 거리 부분.")
    PostalCode = (
        auto(),
        "[en] The code for mail delivery within their area. [kr] 해당 지역 내 우편 배송을 위한 코드.",
    )
    City = (auto(), "[en] The city part of an address. [kr] 주소의 도시 부분.")
    StateCounty = (
        auto(),
        "[en] The state or county part of an address. [kr] 주소의 주 또는 군 부분.",
    )
    Email = (auto(), "[en] The electronic mailing address. [kr] 전자 메일 주소.")
    URL = (
        auto(),
        "[en] Stated as a link to a home page. The home page is the starting page or table of contents of a web site with offerings. It usually has the name index.htm or index.html. [kr] 홈페이지 링크로 명시되어 있습니다. 홈페이지는 제공 사항이 포함된 웹 사이트의 시작 페이지 또는 목차입니다. 일반적으로 이름은 index.htm 또는 index.html입니다.",
    )
    Phone = (auto(), "[en] The telephone contact number. [kr] 전화 연락처 번호.")
    Fax = (
        auto(),
        "[en] The number used for sending/receiving documents electronically. [kr] 팩스 번호.",
    )
    CompanyLogo = (
        auto(),
        "[en] a symbol made up of text and images that identifies a business. [kr] 비즈니스를 식별하는 텍스트와 이미지로 구성된 기호.",
    )


class DocumentationDescription(Enum):
    # https://industrialdigitaltwin.org/en/wp-content/uploads/sites/2/2023/03/IDTA-02004-1-2_Submodel_Handover-Documentation.pdf
    DocumentId = (
        auto(),
        "[en] Set of document identifiers for the Document. One ID in this collection should be used as a preferred ID (see isPrimary below). [kr] Document에 대한 문서 식별자 세트. 이 컬렉션의 한 ID는 기본 ID로 사용해야 함(아래 isPrimary 참조).",
    )
    DocumentClassification = (
        auto(),
        "[en] Set of information for describing the classification of the Document according to ClassificationSystems.",
    )
    DocumentedEntity = (
        auto(),
        "[en] Identifies entities, which are subject to the Document.",
    )
    DocumentDomainId = (
        auto(),
        "[en] Identification of the domain in which the given DocumentId is unique. [kr] 고유한 도메인의 식별ID",
    )
    ValueId = (
        auto(),
        "[en] Identification number of the Document within a given domain, e.g. the providing organization. [kr] 특정 도메인 내 문서의 식별 번호(예: 제공하는 기관.)",
    )
    IsPrimary = (
        auto(),
        "[en] Flag indicating that a DocumentId within a collection of at least two Documentids is the 'primary' identifier for the document. [kr] DocumentId 컬렉션 내 Documentid가 2개 이상인 경우 문서의 '기본' 식별자임을 나타내는 플래그",
    )
    IsPrimaryDocumentId = (
        auto(),
        "[en] Flag indicating that a DocumentId within a collection of at least two Documentids is the 'primary' identifier for the document. [kr] DocumentId 컬렉션 내 Documentid가 2개 이상인 경우 문서의 '기본' 식별자임을 나타내는 플래그",
    )
    ClassId = (
        auto(),
        "[en] Unique ID of the document class within a Classification System.",
    )
    ClassName = (
        auto(),
        "[en] List of language-dependent names of the selected ClassId.",
    )
    ClassificationSystem = (auto(), "[en] Identification of the classification system.")
    DocumentClassId = (
        auto(),
        "[en] Unique ID of the document class within a ClassificationSystem. [kr] ClassificationSystem 내 문서 클래스의 고유 ID",
    )
    DocumentClassName = (
        auto(),
        "[en] List of language-dependent names of the selected ClassID. [kr] 문서의 분류명",
    )
    DocumentClassificationSystem = (
        auto(),
        "[en] Identification of the classification system. [kr] 문서에 사용되는 분류 시스템",
    )
    DocumentVersion = (
        auto(),
        "[en] Information elements of individual VDI 2770 DocumentVersion entities. at the time of handover, this collection shall include at least one DocumentVersion. [kr] 각 문서에는 하나 이상의 문서 버전이 있어야 합니다. 여러 버전의 문서를 제공할 수도 있습니다.",
    )
    DocumentVersionId = (
        auto(),
        "[en] Unambiguous identification number of a DocumentVersion.",
    )
    Title = (auto(), "[en] List of language-dependent titles of the Document.")
    Summary = (auto(), "[en] List of language-dependent summaries of the Document.")
    SubTitle = (auto(), "[en] List of language-dependent subtitles of the Document.")
    KeyWords = (auto(), "[en] List of language-dependent keywords of the Document.")
    StatusSetDate = (
        auto(),
        "[en] Date when the document status was set. Format is YYYY-MM-dd.",
    )
    StatusValue = (
        auto(),
        "[en] Each document version represents a point in time in the document lifecycle. This status value refers to the milestones in the document lifecycle. The following two values should be used for the application of this guideline: InReview (under review), Released (released).",
    )
    OrganizationName = (
        auto(),
        "[en] Organization short name of the author of the Document.",
    )
    OrganizationOfficialName = (
        auto(),
        "[en] Official name of the organization of author of the Document.",
    )
    DigitalFile = (
        auto(),
        "[en] MIME-Type, file name, and file contents given by the File SubmodelElement.",
    )
    PreviewFile = (
        auto(),
        "[en] Provides a preview image of the DocumentVersion, e.g. first page, in a commonly used image format and in low resolution.",
    )
    RefersTo = (
        auto(),
        "[en] Forms a generic RefersTo relationship to another Document or DocumentVersion. They have a loose relationship.",
    )
    BasedOn = (
        auto(),
        "[en] Forms a BasedOn relationship to another Document or DocumentVersion. Typically states that the content of the document is based on another document (e.g. specification requirements). Both have a strong relationship.",
    )
    TranslationOf = (
        auto(),
        "[en] Forms a TranslationOf relationship to another Document or DocumentVersion. Both have a strong relationship.",
    )


class TechnicalDataDescription(Enum):
    # https://industrialdigitaltwin.org/en/wp-content/uploads/sites/2/2022/10/IDTA-02003-1-2_Submodel_TechnicalData.pdf
    GeneralInformation = (
        auto(),
        "[en] General information, for example ordering and manufacturer information.",
    )
    ProductClassifications = (
        auto(),
        "[en] Product classifications by association of product classes with common classification systems.",
    )
    TechnicalProperties = (
        auto(),
        "[en] Technical and product properties. Individual characteristics that describe the product and its technical properties.",
    )
    FurtherInformation = (
        auto(),
        "[en] Further information on the product, the validity of the information provided and this data record.",
    )
    ManufacturerName = (
        auto(),
        "[en] Legally valid designation of the natural or judicial body which is directly responsible for the design, production, packaging and labeling of a product in respect to its being brought into the market. [kr] 생산자 혹은 생산 기업의 정식 명칭",
    )
    ManufacturerLogo = (
        auto(),
        "[en] Imagefile for logo of manufacturer provided in common format (.png, .jpg). [kr] 일반적인 양식의 생산자 로고 이미지",
    )
    ManufacturerProductDesignation = (
        auto(),
        "[en] Product designation as given by the manufacturer. Short description of the product, product group or function (short text) in common language. [kr] 제품에 대한 짧은 설명",
    )
    ManufacturerArticleNumber = (
        auto(),
        "[en] unique product identifier of the manufacturer [kr] 생산자의 구별번호",
    )
    ManufacturerOrderCode = (
        auto(),
        "[en] By manufactures issued unique combination of numbers and letters used to identify the device for ordering [kr] 같은 제품을 다시 구매할 때 사용할 수 있는 제품 식별코드",
    )
    ProductImage = (
        auto(),
        "[en] Image file for associated product provided in common format (.png, .jpg). [kr] 일반적인 양식의 제품 이미지",
    )
    ProductClassificationItem = (
        auto(),
        "[en] Single product classification item by association with product class in a particular classification system or property dictionary.",
    )
    ProductClassificationSystem = (
        auto(),
        "[en] Common name of the classification system. [kr] 분류 체계의 이름",
    )
    ClassificationSystemVersion = (
        auto(),
        "[en] Common version identifier of the used classification system, in order to distinguish different version of the property dictionary. [kr] 분류 체계의 버전",
    )
    ProductClassId = (
        auto(),
        "[en] Class of the associated product or industrial equipment in the classification system. According to the notation of the system. [kr] 분류 체계 상 관련 상품의 범주",
    )
    TextStatement = (
        auto(),
        "[en] Statement by the manufacturer in text form, e.g. scope of validity of the statements, scopes of application, conditions of operation. [kr] 텍스트 형태의 선언(선언의 유효 범위 등)",
    )
    ValidDate = (
        auto(),
        "[en] Denotes a date on which the data specified in the Submodel was valid from for the associated asset. [kr] 데이터의 최신 갱신일",
    )


class DigitalNameplateDescription(Enum):
    # https://industrialdigitaltwin.org/en/wp-content/uploads/sites/2/2024/11/IDTA-02006-3-0_Submodel_Digital-Nameplate.pdf
    URIOFTheProduct = (
        auto(),
        "[en] unique global identification of the product using an universal resource identifier (URI)",
    )
    ManufacturerName = (
        auto(),
        "[en] legally valid designation of the natural or judicial person which is directly responsible for the design, production, packaging and labeling of a product in respect to its being brought into circulation",
    )
    ManufacturerProductDesignation = (
        auto(),
        "[en] Short description of the product (short text)",
    )
    ContactInformation = (
        auto(),
        "[en] contains information on how to contact the manufacturer or an authorised service provider, e.g. when a maintenance service is required",
    )
    ManufacturerProductRoot = (
        auto(),
        "[en] Top level of a 3 level manufacturer specific product hierarchy",
    )
    ManufacturerProductFamily = (
        auto(),
        "[en] 2nd level of a 3 level manufacturer specific product hierarchy",
    )
    ManufacturerProductType = (
        auto(),
        "[en] Characteristic to differentiate between different products of a product family or special variants",
    )
    OrderCodeOfManufacturer = (
        auto(),
        "[en] By manufactures issued unique combination of numbers and letters used to identify the device for ordering",
    )
    ProductArticleNumberOfManufacturer = (
        auto(),
        "[en] unique product identifier of the manufacturer",
    )
    SerialNumber = (
        auto(),
        "[en] unique combination of numbers and letters used to identify the device once it has been manufactured",
    )
    YearOfConstruction = (auto(), "[en] Year as completion date of object")
    DateOfManufacture = (
        auto(),
        "[en] Date from which the production and / or development process is completed or from which a service is provided completely",
    )
    HardwareVersion = (auto(), "[en] Version of the hardware supplied with the device")
    FirmwareVersion = (auto(), "[en] Version of the firmware supplied with the device")
    SoftwareVersion = (auto(), "[en] Version of the software used by the device")
    CountryOfOrigin = (auto(), "[en] Country where the product was manufactured")
    CompanyLogo = (
        auto(),
        "[en] A graphic mark used to represent a company, an organisation or a product",
    )
    Markings = (auto(), "[en] Collection of product markings")
    AssetSpecificProperties = (
        auto(),
        "[en] Group of properties that are listed on the asset's nameplate and are grouped based on guidelines",
    )
    Street = (auto(), "[en] street name and house number")
    Zipcode = (auto(), "[en] ZIP code of address")
    CityTown = (auto(), "[en] town or city")
    NationalCode = (auto(), "[en] code of a country")
    Marking = (
        auto(),
        "[en] contains information about the marking labelled on the device",
    )
    MarkingName = (auto(), "[en] common name of the marking")
    DesignationOfCertificateOrApproval = (
        auto(),
        "[en] alphanumeric character sequence identifying a certificate or approval",
    )
    IssueDate = (auto(), "[en] Date, at which the specified certificate is issued")
    ExpiryDate = (auto(), "[en] Date, at which the specified certificate expires")
    ExplosionSafety = (
        auto(),
        "[en] contains information related to explosion safety according to device nameplate",
    )
    TypeOfApproval = (
        auto(),
        "[en] classification according to the standard or directive to which the approval applies",
    )
    ApprovalAgencyTestingAgency = (
        auto(),
        "[en] certificates and approvals pertaining to general usage and compliance with constructional standards and directives",
    )
    RatedInsulationVoltage = (
        auto(),
        "[en] from the manufacturer for the capital assets limited isolation with given(indicated) operating conditions",
    )
    InstructionsControlDrawing = (
        auto(),
        "[en] designation used to uniquely identify a control/reference drawing stored in a file system",
    )
    SpecificConditionsForUse = (auto(), "[en] Note: X if any, otherwise no entry")
    IncompleteDevice = (auto(), "[en] U if any, otherwise no entry")
    AmbientConditions = (
        auto(),
        "[en] Contains properties which are related to the ambient conditions of the device.",
    )
    ProcessConditions = (
        auto(),
        "[en] Contains properties which are related to the process conditions of the device.",
    )
    ExternalElectricalCircuit = (
        auto(),
        "[en] specifies the parameters of external electrical circuits.",
    )
    DeviceCategory = (
        auto(),
        "[en] category of device in accordance with directive 94/9/EC",
    )
    EquipmentProtectionLevel = (
        auto(),
        "[en] part of a hazardous area classification system indicating the likelihood of the existence of a classified hazard",
    )
    RegionalSpecificMarking = (
        auto(),
        '[en] Marking used only in specific regions, e.g. North America: class/divisions, EAC: "1" or NEC: "AIS"',
    )
    TypeOfProtection = (
        auto(),
        "[en] classification of an explosion protection according to the specific measures applied to avoid ignition of a surrounding explosive atmosphere",
    )
    ExplosionGroup = (
        auto(),
        "[en] classification of dangerous gaseous substances based on their ability to cause an explosion",
    )
    MinimumAmbientTemperature = (
        auto(),
        "[en] lower limit of the temperature range of the surrounding space in which the component, the pipework or the system can be operated",
    )
    MaxAmbientTemperature = (
        auto(),
        "[en] upper limit of the temperature range of the surrounding space in which the component, the pipework or the system can be operated",
    )
    MaxSurfaceTemperatureForDustProof = (
        auto(),
        "[en] maximum permissible surface temperature of a device used in an explosion hazardous area with combustible dust",
    )
    TemperatureClass = (
        auto(),
        "[en] classification system of electrical apparatus, based on its maximum surface temperature, related to the specific explosive atmosphere for which it is intended to be used",
    )
    DesignationOfElectricalTerminal = (
        auto(),
        "[en] alphanumeric character sequence identifying an electrical terminal",
    )
    Characteristics = (auto(), "[en] Characteristic of the intrinsically safe circuit")
    Fisco = (
        auto(),
        "[en] FISCO certified intrinsically safe fieldbus circuit (IEC 60079-11)",
    )
    TwoWISE = (
        auto(),
        "[en] 2-WISE certified intrinsically safe circuit (IEC 60079-47)",
    )
    SafetyRelatedPropertiesForPassiveBehaviour = (
        auto(),
        "[en] properties characterizing the safety related parameters of a loop-powered, intrinsically safe input or output circuit",
    )
    SafetyRelatedPropertiesForActiveBehaviour = (
        auto(),
        "[en] properties characterizing the safety related parameters of an intrinsically safe circuit",
    )
    MaxInputPower = (
        auto(),
        "[en] maximum power that can be applied to the connection facilities of the apparatus without invalidating the type of protection",
    )
    MaxInputVoltage = (
        auto(),
        "[en] maximum voltage (peak a.c. or d.c.) that can be applied to the connection facilities of the apparatus without invalidating the type of protection",
    )
    MaxInputCurrent = (
        auto(),
        "[en] maximum current (peak a.c. or d.c.) that can be applied to the connection facilities of the apparatus without invalidating the type of protection",
    )
    MaxInternalCapacitance = (
        auto(),
        "[en] maximum equivalent internal capacitance of the apparatus which is considered as appearing across the connection facilities",
    )
    MaxInternalInductance = (
        auto(),
        "[en] maximum equivalent internal inductance of the apparatus which is considered as appearing across the connection facilities",
    )
    MaxOutputPower = (
        auto(),
        "[en] maximum electrical power that can be taken from the apparatus",
    )
    MaxOutputVoltage = (
        auto(),
        "[en] maximum voltage (peak a.c. or d.c.) that can occur at the connection facilities of the apparatus at any applied voltage up to the maximum voltage",
    )
    MaxOutputCurrent = (
        auto(),
        "[en] maximum current (peak a.c. or d.c.) in the apparatus that can be taken from the connection facilities of the apparatus",
    )
    MaxExternalCapacitance = (
        auto(),
        "[en] maximum capacitance that can be connected to the connection facilities of the apparatus without invalidating the type of protection",
    )
    MaxExternalInductance = (
        auto(),
        "[en] maximum value of inductance that can be connected to the connection facilities of the apparatus without invalidating the type of protection",
    )
    MaxExternalInductanceRatio = (
        auto(),
        "[en] maximum value of ratio of inductance (Lo) to resistance (Ro) of any external circuit that can be connected to the connection facilities of the electrical apparatus without invalidating intrinsic safety",
    )
    MaxExternalInductanceResistanceRatio = (
        auto(),
        "[en] maximum value of ratio of inductance (Lo) to resistance (Ro) of any external circuit that can be connected to the connection facilities of the electrical apparatus without invalidating intrinsic safety",
    )
    GuidelineSpecificProperties = (
        auto(),
        "[en] Asset specific nameplate information required by guideline, stipulation or legislation.",
    )
    arbitrary = (
        auto(),
        "[en] semanticId = {arbitrary, representing information required by further standards}; Properties which are not required by any legislations but provided due to best practice.",
    )
    GuidelineForConformityDeclaration = (
        auto(),
        "[en] guideline, stipulation or legislation used for determining conformity",
    )


class NameplateDescription(Enum):
    # https://industrialdigitaltwin.org/en/wp-content/uploads/sites/2/2024/11/IDTA-02006-3-0_Submodel_Digital-Nameplate.pdf
    URIOfTheProduct = (
        auto(),
        "[en] Unique global identification of the product using a universal resource identifier (URI)",
    )
    ManufacturerName = (
        auto(),
        "[en] Legally valid designation of the natural or judicial person which is directly responsible for the design, production, packaging and labeling of a product in respect to its being brought into circulation [kr] 제품 유통과 관련하여 제품의 디자인, 생산, 포장 및 라벨링에 직접적으로 책임이 있는 자연인 또는 사법인의 법적으로 유효한 지정입니다.",
    )
    ManufacturerProductDesignation = (
        auto(),
        "[en] The name of the product, provided by the manufacturer",
    )
    AddressInformation = (
        auto(),
        '[en] Note: this set of information is defined by SMT drop-in "Address Information"',
    )
    ManufacturerProductDescription = (
        auto(),
        "[en] Description of the product, it's technical features and implementation if needed (long text)",
    )
    ManufacturerProductRoot = (
        auto(),
        "[en] top level of a 3 level manufacturer specific product hierarchy",
    )
    ManufacturerProductFamily = (
        auto(),
        "[en] second level of a 3 level manufacturer specific product hierarchy",
    )
    ManufacturerProductType = (
        auto(),
        "[en] Characteristic to differentiate between different products of a product family or special variants",
    )
    OrderCodeOfManufacturer = (
        auto(),
        "[en] unique combination of numbers and letters issued by the manufacturer that is used to identify the device for ordering",
    )
    ProductArticleNumberOfManufacturer = (
        auto(),
        "[en] unique product identifier of the manufacturer",
    )
    SerialNumber = (
        auto(),
        "[en] unique combination of numbers and letters used to identify the device once it has been manufactured",
    )
    YearOfConstruction = (
        auto(),
        "[en] year in which the manufacturing process is completed",
    )
    DateOfManufacture = (auto(), "[en] date when an item was manufactured")
    HardwareVersion = (auto(), "[en] version of the hardware supplied with the device")
    FirmwareVersion = (auto(), "[en] version of the firmware supplied with the device")
    SoftwareType = (
        auto(),
        "[en] The type of the software (category, e.g. Runtime, Application, Firmware, Driver, etc.)",
    )
    SoftwareVersion = (auto(), "[en] version of the software used by the device")
    CountryOfOrigin = (
        auto(),
        "[en] country where the product was manufactured Note: Country codes defined accord. to DIN EN ISO 3166-1 alpha-2 codes",
    )
    UniqueFacilityIdentifier = (
        auto(),
        "[en] unique string of characters for the identification of locations or buildings involved in a product's value chain or used by actors involved in a product's value chain",
    )
    Version = (
        auto(),
        "[en] The complete version information consisting of Major Version, Minor Version, Revision and Build Number",
    )
    VersionName = (auto(), "[en] The name this particular version is given")
    VersionInfo = (
        auto(),
        "[en] Provides a textual description of most relevant characteristics of the version of the software",
    )
    ReleaseDate = (
        auto(),
        "[en] The moment in time, when this version of the software was made publicly available",
    )
    ReleaseNotes = (auto(), "[en] Contains information about this release")
    BuildDate = (
        auto(),
        "[en] The moment in time, when this particular build of software was created",
    )
    InstallationURI = (
        auto(),
        "[en] Indicates the resource, where the software is being provided by the manufacturer",
    )
    InstallationFile = (auto(), "[en] Contains the installation code as BLOB.")
    InstallerType = (auto(), "[en] Indicates the type of installation package")
    InstallationChecksum = (
        auto(),
        "[en] Provides the checksum for the software available at InstallationURI",
    )
    InstanceName = (auto(), "[en] The name of the software instance")
    InstalledVersion = (
        auto(),
        "[en] The version information of the installed instance, consisting of Major Version, Minor Version, Revision and Build Number indicates the actual version of the instance",
    )
    InstallationDate = (auto(), "[en] Date of Installation")
    InstallationPath = (
        auto(),
        "[en] Indicates the path to the installed instance of the software",
    )
    InstallationSource = (
        auto(),
        "[en] Indicates the path to the installation files used in this instance of the software",
    )
    InstalledOnArchitecture = (
        auto(),
        "[en] Indicates the processor architecture this instance is installed on",
    )
    InstalledOnOS = (
        auto(),
        "[en] Indicates the operating system this instance is installed on",
    )
    InstalledOnHost = (
        auto(),
        "[en] Indicates the host system in case of a virtual environment",
    )
    InstalledModules = (auto(), "[en] Collection of installed modules")
    ConfigurationPaths = (
        auto(),
        "[en] Indicates the path to the configuration information",
    )
    SLAInformation = (auto(), "[en] Indicates the actual service level agreements")
    Contact = (auto(), "[en] Collection for general contact data")
    InventoryTag = (
        auto(),
        "[en] Specifies an information used for inventory of the software",
    )
    InstalledModule = (auto(), "[en] The name of a particular module installed")
    ConfigurationPath = (auto(), "[en] Contains a single configuration entry")
    ConfigurationURI = (auto(), "[en] Indicates the path to the configuration")
    ConfigurationType = (
        auto(),
        "[en] Indicates the type of configuration (e.g. general configuration, user configuration)",
    )
    Marking = (
        auto(),
        "[en] contains information about the marking labelled on the device",
    )
    MarkingName = (auto(), "[en] common name of the marking")
    AssetSpecificProperties = (
        auto(),
        "[en] Group of properties that are listed on the asset's nameplate and are grouped based on guidelines",
    )
    CompanyLogo = (
        auto(),
        "[en] a graphic mark used to represent a company, an organisation or a product",
    )
    Markings = (
        auto(),
        "[en] Note: CE marking is declared as mandatory according to EU Blue Guide",
    )


class HierarchicalStructuresDescription(Enum):
    # https://industrialdigitaltwin.org/en/wp-content/uploads/sites/2/2024/06/IDTA-02011-1-1_Submodel_HierarchicalStructuresEnablingBoM.pdf
    EntryNode = (
        auto(),
        "[en] Base entry point for the Entity tree in this Submodel, this must be a Self-managed Entity reflecting the Assets administered in the AAS this Submodel is part of.",
    )
    ArcheType = (
        auto(),
        '[en] Arche Type of the Submodel, there are three allowed enumeration entries: 1. "Full", 2. "OneDown" and 3. "OneUp" These entries reflect the structure of the Submodel as defined in 1.5.1.3 & 1.5.1.4.',
    )
    Node = (
        auto(),
        '[en] The Entity Node can be a co-managed or self-managed entity representing an asset in the hierarchical structure. At least one nested Node shall be created as a Submodel Element for the EntryNode. In relation to the Arche Type, either the Relationship "IsPartOf" or "HasPart" shall be created using this Node as Second attribute.',
    )
    SameAs = (
        auto(),
        '[en] Reference between two Entities in the same Submodel or across Submodels. "First" and "Second" attributes must contain either an EntryNode or a Node.',
    )
    IsPartOf = (
        auto(),
        '[en] Modelling of logical connections between asset and sub-asset. Either this or "HasPart" must be used, not both. "First" and "Second" attributes must contain either a EntryNode or a Node. The relationships shall only reference EntryNodes or Nodes in the same submodel instance.',
    )
    HasPart = (
        auto(),
        '[en] Modelling of logical connections between components and sub-components. Either this or "IsPartOf" must be used, not both. "First" and "Second" attributes must contain either a EntryNode or a Node. The relationships shall only reference EntryNodes or Nodes in the same submodel instance.',
    )
    BulkCount = (
        auto(),
        "[en] To be used if bulk components are referenced, e.g., a 10x M4x30 screw. Additional constraint: With bulk count only a reference to an asset with kind type is allowed, e.g., the M4x30 type asset.",
    )


class CarbonFootprintDescription(Enum):
    # https://industrialdigitaltwin.org/en/wp-content/uploads/sites/2/2024/01/IDTA-2023-0-9-_Submodel_CarbonFootprint.pdf
    ProductCarbonFootprint = (
        auto(),
        "[en] Balance of greenhouse gas emissions along the entire life cycle of a product in a defined application and in relation to a defined unit of use",
    )
    TransportCarbonFootprint = (
        auto(),
        "[en] Balance of greenhouse gas emissions generated by a transport service of a product",
    )
    PCFCalculationMethod = (
        auto(),
        "[en] Standard, method for determining the greenhouse gas emissions of a product",
    )
    PCFCO2eq = (
        auto(),
        "[en] Sum of all greenhouse gas emissions of a product according to the quantification requirements of the standard",
    )
    PCFReferenceValueForCalculation = (
        auto(),
        "[en] Quantity unit of the product to which the PCF information on the CO2 footprint refers",
    )
    PCFQuantityOfMeasureForCalculation = (
        auto(),
        "[en] Quantity of the product to which the PCF information on the CO2 footprint refers",
    )
    PCFLifeCyclePhase = (
        auto(),
        "[en] Life cycle stages of the product according to the quantification requirements of the standard to which the PCF carbon footprint statement refers",
    )
    ExplanatoryStatement = (
        auto(),
        "[en] definition@en: Explanation which is needed or given so that a footprint communication can be properly understood by a purchaser, potential purchaser or user of the product",
    )
    PCFGoodsAddressHandover = (
        auto(),
        "[en] Indicates the place of hand-over of the goods (use structure defined in section 2.5 SMC Address)",
    )
    PublicationDate = (
        auto(),
        "[en] Time at which something was first published or made available",
    )
    ExpirationDate = (
        auto(),
        "[en] Time at which something should no longer be used effectively because it may lose its validity, quality or safety",
    )
    TCFCalculationMethod = (
        auto(),
        "[en] Standard, method for determining the greenhouse gas emissions for the transport of a product",
    )
    TCFCO2eq = (
        auto(),
        "[en] Sum of all greenhouse gas emissions from vehicle operation",
    )
    TCFReferenceValueForCalculation = (
        auto(),
        "[en] Amount of product to which the TCF carbon footprint statement relates",
    )
    TCFQuantityOfMeasureForCalculation = (
        auto(),
        "[en] Quantity of the product to which the TCF information on the CO2 footprint refers",
    )
    TCFProcessesForGreenhouseGasEmissionInATransportService = (
        auto(),
        "[en] Processes in a transport service to determine the sum of all direct or indirect greenhouse gas emissions from fuel supply and vehicle operation",
    )
    TCFGoodsTransportAddressTakeover = (
        auto(),
        "[en] Indication of the place of receipt of goods (use structure defined in 2.5 SMC Address)",
    )
    TCFGoodsTransportAddressHandover = (
        auto(),
        "[en] Indicates the hand-over address of the goods transport (use structure defined in 2.5 SMC Address)",
    )
    Street = (auto(), "[en] Street indication of the place of transfer of goods")
    HouseNumber = (
        auto(),
        "[en] Number for identification or differentiation of individual houses of a street",
    )
    ZipCode = (auto(), "[en] Zip code of the goods transfer address")
    CityTown = (auto(), "[en] Indication of the city or town of the transfer of goods")
    Country = (auto(), "[en] Country where the product is transmitted")


class DescriptionType(Enum):
    Identification = [desc for desc in IdentificationDescription]
    Documentation = [desc for desc in DocumentationDescription]
    HandOverDocumentation = [desc for desc in DocumentationDescription]
    TechnicalData = [desc for desc in TechnicalDataDescription]
    DigitalNameplate = [desc for desc in DigitalNameplateDescription]
    HierarchicalStructures = [desc for desc in HierarchicalStructuresDescription]
    CarbonFootprint = [desc for desc in CarbonFootprintDescription]
    Nameplate = [desc for desc in NameplateDescription]

    @classmethod
    def find_by_name(cls, name):
        return next((d.value for d in cls if d.name.lower() == name.lower()), [])
