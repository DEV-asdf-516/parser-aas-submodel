from enum import Enum, auto


class KeyName(Enum):
    idShort = (auto(), True)
    modelType = (auto(), True)
    value = (auto(), True)
    statements = (auto(), True)
    description = (auto(), True)
    language = (auto(), False)
    text = (auto(), False)
    submodelElements = (auto(), False)
    semanticId = (auto(), False)
    keys = (auto(), False)
    index = (auto(), False)
    indent = (auto(), False)

    @classmethod
    def extract_names(cls):
        return [
            name for name, member in cls.__members__.items() if member.value[-1] is True
        ]


class ModelTypeName(Enum):
    SubmodelElementCollection = auto()
    Entity = auto()
    SubmodelElementList = auto()

    @classmethod
    def smc_group(cls):
        return [
            cls.SubmodelElementCollection.name,
            cls.Entity.name,
            cls.SubmodelElementList.name,
        ]

    @classmethod
    def smc_group_list(cls):
        return [
            cls.SubmodelElementCollection.name,
            cls.SubmodelElementList.name,
        ]


class ModelTypeShortend(Enum):
    Property = "Prop"
    MultiLanguageProperty = "MLP"
    SubmodelElementCollection = "SMC"
    Entity = "ENT"
    RelationshipElement = "Rel"
    ReferenceElement = "Ref"
    SubmodelElementList = "ElementList"

    @classmethod
    def replace_model_type_shortend(cls, type: str):
        return next((m.value for m in cls if m.name == type), type)


class Level(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2
    CRITICAL = 3
    TRACE = 4
    SUCCESS = 5

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
    NONE = auto()


class IdentificationDescription(Enum):
    ManufacturerName = (
        auto(),
        " The company's name that makes the product.\n제품을 만드는 회사 이름.",
    )
    ManufacturerId = (
        auto(),
        " Internationally unique identification number for the manufacturer of the device or the product and for the physical location.\n장치 또는 제품 제조업체와 물리적 위치에 대한 국제 고유 식별 번호.",
    )
    ManufacturerIdProvider = (
        auto(),
        " DUNS-no., supplier number, or other number as identifier of an offeror or supplier of the identification.\nDUNS 번호, 공급업체 번호 또는 식별 제공자 또는 공급업체의 식별자로 사용되는 기타 번호.",
    )
    ManufacturerTypId = (
        auto(),
        " unique product identifier of the manufacturer.\n제조업체의 고유 제품 식별자.",
    )
    ManufacturerTypName = (
        auto(),
        " Short description of the product.\n제품에 대한 간단한 설명.",
    )
    ManufacturerTypDescription = (
        auto(),
        " Description of the product, it's technical features and implementation if needed.\n제품 설명, 기술적 특징 및 필요한 경우 구현.",
    )
    SupplierName = (
        auto(),
        " name of supplier which provides the customer with a product or a service.\n고객에게 제품이나 서비스를 제공하는 공급자 이름.",
    )
    SupplierId = (
        auto(),
        " Internationally unique identification number for the supplier of the device or the product and for the physical location.\n장치 또는 제품 공급업체와 물리적 위치에 대한 국제 고유 식별 번호.",
    )
    SupplierIdProvider = (
        auto(),
        " The unique identifier for the supplier.\n공급업체의 고유 식별자.",
    )
    SupplierTypId = (
        auto(),
        " unique product order identifier of the supplier.\n공급자의 고유한 제품 주문 식별자.",
    )
    SupplierTypName = (
        auto(),
        " Short description of the product.\n제품에 대한 간단한 설명.",
    )
    SupplierTypDescription = (
        auto(),
        " Description of the product, it's technical features and implementation if needed.\n제품 설명, 기술적 특징 및 필요한 경우 구현.",
    )
    TypClass = (
        auto(),
        " Class of type or category .\n유형이나 카테고리의 분류.",
    )
    ClassificationSystem = (
        auto(),
        " system used to categorize products or information.\n제품이나 정보를 분류하는데 사용되는 시스템.",
    )
    SecondaryKeyTyp = (
        auto(),
        " type of key used for additional data categorization.\n추가 데이터 분류에 사용되는 키 유형.",
    )
    TypThumbnail = (
        auto(),
        " small preview image representing a type or category.\n유형이나 카테고리를 나타내는 작은 미리보기 이미지.",
    )
    AssetId = (
        auto(),
        " A unique identifier for an asset.\n자산의 고유 식별자.",
    )
    InstanceId = (
        auto(),
        " A unique code for an instance or version of an asset.\n자산의 인스턴스나 버전을 위한 고유 코드.",
    )
    ChargeId = (
        auto(),
        " Number assigned by the manufacturer of a material to identify the manufacturer's batch.\n제조업체의 배치를 식별하기 위해 자재 제조업체가 할당한 번호.",
    )
    SecondaryKeyInstance = (
        auto(),
        " An additional unique identifier for an asset instance.\n자산 인스턴스의 추가 고유 식별자.",
    )
    ManufacturingDate = (
        auto(),
        " Date from which the production and / or development process is completed or from which a service is provided completely.\n생산 및/또는 개발 프로세스가 완료되거나 서비스가 완전히 제공되는 날짜.",
    )
    DeviceRevision = (
        auto(),
        " an updated version of Device.\n업데이트된 버전의 장치.",
    )
    SoftwareRevision = (
        auto(),
        " an updated version of Software.\n업데이트된 버전의 소프트웨어.",
    )
    HardwareRevision = (
        auto(),
        " a modified version or modification of Hardware for Problem correction.\n문제 해결을 위한 하드웨어 수정 또는 수정.",
    )
    QrCode = (
        auto(),
        " a type of two-dimensional matrix barcode.\n2차원 매트릭스 바코드의 일종.",
    )
    Name = (
        auto(),
        " The name of the supplier that provides the customer with a product or a service.\n고객에게 제품이나 서비스를 제공하는 공급자 이름.",
    )
    Role = (
        auto(),
        " The specific part or function they have in the context.\n맥락에 따른 특정 역할 또는 기능.",
    )
    CountryCode = (
        auto(),
        " Agreed upon symbol for unambiguous identification of a country.\n국가를 명확하게 식별하기 위해 합의된 기호.",
    )
    Street = (auto(), " The street part of an address.\n주소의 거리 부분.")
    PostalCode = (
        auto(),
        " The code for mail delivery within their area.\n해당 지역 내 우편 배송을 위한 코드.",
    )
    City = (auto(), " The city part of an address.\n주소의 도시 부분.")
    StateCounty = (
        auto(),
        " The state or county part of an address.\n주소의 주 또는 군 부분.",
    )
    Email = (auto(), " The electronic mailing address.\n전자 메일 주소.")
    URL = (
        auto(),
        " Stated as a link to a home page. The home page is the starting page or table of contents of a web site with offerings. It usually has the name index.htm or index.html.\n홈페이지 링크로 명시되어 있습니다. 홈페이지는 제공 사항이 포함된 웹 사이트의 시작 페이지 또는 목차입니다. 일반적으로 이름은 index.htm 또는 index.html입니다.",
    )
    Phone = (auto(), " The telephone contact number.\n전화 연락처 번호.")
    Fax = (
        auto(),
        " The number used for sending/receiving documents electronically.\n팩스 번호.",
    )
    CompanyLogo = (
        auto(),
        " a symbol made up of text and images that identifies a business.\n비즈니스를 식별하는 텍스트와 이미지로 구성된 기호.",
    )


class DocumentationDescription(Enum):
    # https://industrialdigitaltwin.org/en/wp-content/uploads/sites/2/2023/03/IDTA-02004-1-2_Submodel_Handover-Documentation.pdf
    DocumentId = (
        auto(),
        " Set of document identifiers for the Document. One ID in this collection should be used as a preferred ID (see isPrimary below).\nDocument에 대한 문서 식별자 세트. 이 컬렉션의 한 ID는 기본 ID로 사용해야 함(아래 isPrimary 참조).",
    )
    DocumentClassification = (
        auto(),
        " Set of information for describing the classification of the Document according to ClassificationSystems.",
    )
    DocumentedEntity = (
        auto(),
        " Identifies entities, which are subject to the Document.",
    )
    DocumentDomainId = (
        auto(),
        " Identification of the domain in which the given DocumentId is unique.\n고유한 도메인의 식별ID",
    )
    ValueId = (
        auto(),
        " Identification number of the Document within a given domain, e.g. the providing organization.\n특정 도메인 내 문서의 식별 번호(예: 제공하는 기관.)",
    )
    IsPrimary = (
        auto(),
        " Flag indicating that a DocumentId within a collection of at least two Documentids is the 'primary' identifier for the document.\nDocumentId 컬렉션 내 Documentid가 2개 이상인 경우 문서의 '기본' 식별자임을 나타내는 플래그",
    )
    IsPrimaryDocumentId = (
        auto(),
        " Flag indicating that a DocumentId within a collection of at least two Documentids is the 'primary' identifier for the document.\nDocumentId 컬렉션 내 Documentid가 2개 이상인 경우 문서의 '기본' 식별자임을 나타내는 플래그",
    )
    ClassId = (
        auto(),
        " Unique ID of the document class within a Classification System.",
    )
    ClassName = (
        auto(),
        " List of language-dependent names of the selected ClassId.",
    )
    ClassificationSystem = (auto(), " Identification of the classification system.")
    DocumentClassId = (
        auto(),
        " Unique ID of the document class within a ClassificationSystem.\nClassificationSystem 내 문서 클래스의 고유 ID",
    )
    DocumentClassName = (
        auto(),
        " List of language-dependent names of the selected ClassID.\n문서의 분류명",
    )
    DocumentClassificationSystem = (
        auto(),
        " Identification of the classification system.\n문서에 사용되는 분류 시스템",
    )
    DocumentVersion = (
        auto(),
        " Information elements of individual VDI 2770 DocumentVersion entities. at the time of handover, this collection shall include at least one DocumentVersion.\n각 문서에는 하나 이상의 문서 버전이 있어야 합니다. 여러 버전의 문서를 제공할 수도 있습니다.",
    )
    DocumentVersionId = (
        auto(),
        " Unambiguous identification number of a DocumentVersion.",
    )
    Title = (auto(), " List of language-dependent titles of the Document.")
    Summary = (auto(), " List of language-dependent summaries of the Document.")
    SubTitle = (auto(), " List of language-dependent subtitles of the Document.")
    KeyWords = (auto(), " List of language-dependent keywords of the Document.")
    StatusSetDate = (
        auto(),
        " Date when the document status was set. Format is YYYY-MM-dd.",
    )
    StatusValue = (
        auto(),
        " Each document version represents a point in time in the document lifecycle. This status value refers to the milestones in the document lifecycle. The following two values should be used for the application of this guideline: InReview (under review), Released (released).",
    )
    OrganizationName = (
        auto(),
        " Organization short name of the author of the Document.",
    )
    OrganizationOfficialName = (
        auto(),
        " Official name of the organization of author of the Document.",
    )
    DigitalFile = (
        auto(),
        " MIME-Type, file name, and file contents given by the File SubmodelElement.",
    )
    PreviewFile = (
        auto(),
        " Provides a preview image of the DocumentVersion, e.g. first page, in a commonly used image format and in low resolution.",
    )
    RefersTo = (
        auto(),
        " Forms a generic RefersTo relationship to another Document or DocumentVersion. They have a loose relationship.",
    )
    BasedOn = (
        auto(),
        " Forms a BasedOn relationship to another Document or DocumentVersion. Typically states that the content of the document is based on another document (e.g. specification requirements). Both have a strong relationship.",
    )
    TranslationOf = (
        auto(),
        " Forms a TranslationOf relationship to another Document or DocumentVersion. Both have a strong relationship.",
    )


class TechnicalDataDescription(Enum):
    # https://industrialdigitaltwin.org/en/wp-content/uploads/sites/2/2022/10/IDTA-02003-1-2_Submodel_TechnicalData.pdf
    GeneralInformation = (
        auto(),
        " General information, for example ordering and manufacturer information.",
    )
    ProductClassifications = (
        auto(),
        " Product classifications by association of product classes with common classification systems.",
    )
    TechnicalProperties = (
        auto(),
        " Technical and product properties. Individual characteristics that describe the product and its technical properties.",
    )
    FurtherInformation = (
        auto(),
        " Further information on the product, the validity of the information provided and this data record.",
    )
    ManufacturerName = (
        auto(),
        " Legally valid designation of the natural or judicial body which is directly responsible for the design, production, packaging and labeling of a product in respect to its being brought into the market.\n생산자 혹은 생산 기업의 정식 명칭",
    )
    ManufacturerLogo = (
        auto(),
        " Imagefile for logo of manufacturer provided in common format (.png, .jpg).\n일반적인 양식의 생산자 로고 이미지",
    )
    ManufacturerProductDesignation = (
        auto(),
        " Product designation as given by the manufacturer. Short description of the product, product group or function (short text) in common language.\n제품에 대한 짧은 설명",
    )
    ManufacturerArticleNumber = (
        auto(),
        " unique product identifier of the manufacturer\n생산자의 구별번호",
    )
    ManufacturerOrderCode = (
        auto(),
        " By manufactures issued unique combination of numbers and letters used to identify the device for ordering\n같은 제품을 다시 구매할 때 사용할 수 있는 제품 식별코드",
    )
    ProductImage = (
        auto(),
        " Image file for associated product provided in common format (.png, .jpg).\n일반적인 양식의 제품 이미지",
    )
    ProductClassificationItem = (
        auto(),
        " Single product classification item by association with product class in a particular classification system or property dictionary.",
    )
    ProductClassificationSystem = (
        auto(),
        " Common name of the classification system.\n분류 체계의 이름",
    )
    ClassificationSystemVersion = (
        auto(),
        " Common version identifier of the used classification system, in order to distinguish different version of the property dictionary.\n분류 체계의 버전",
    )
    ProductClassId = (
        auto(),
        " Class of the associated product or industrial equipment in the classification system. According to the notation of the system.\n분류 체계 상 관련 상품의 범주",
    )
    TextStatement = (
        auto(),
        " Statement by the manufacturer in text form, e.g. scope of validity of the statements, scopes of application, conditions of operation.\n텍스트 형태의 선언(선언의 유효 범위 등)",
    )
    ValidDate = (
        auto(),
        " Denotes a date on which the data specified in the Submodel was valid from for the associated asset.\n데이터의 최신 갱신일",
    )


class DigitalNameplateDescription(Enum):
    # https://industrialdigitaltwin.org/en/wp-content/uploads/sites/2/2024/11/IDTA-02006-3-0_Submodel_Digital-Nameplate.pdf
    URIOFTheProduct = (
        auto(),
        " unique global identification of the product using an universal resource identifier (URI)",
    )
    ManufacturerName = (
        auto(),
        " legally valid designation of the natural or judicial person which is directly responsible for the design, production, packaging and labeling of a product in respect to its being brought into circulation",
    )
    ManufacturerProductDesignation = (
        auto(),
        " Short description of the product (short text)",
    )
    ContactInformation = (
        auto(),
        " contains information on how to contact the manufacturer or an authorised service provider, e.g. when a maintenance service is required",
    )
    ManufacturerProductRoot = (
        auto(),
        " Top level of a 3 level manufacturer specific product hierarchy",
    )
    ManufacturerProductFamily = (
        auto(),
        " 2nd level of a 3 level manufacturer specific product hierarchy",
    )
    ManufacturerProductType = (
        auto(),
        " Characteristic to differentiate between different products of a product family or special variants",
    )
    OrderCodeOfManufacturer = (
        auto(),
        " By manufactures issued unique combination of numbers and letters used to identify the device for ordering",
    )
    ProductArticleNumberOfManufacturer = (
        auto(),
        " unique product identifier of the manufacturer",
    )
    SerialNumber = (
        auto(),
        " unique combination of numbers and letters used to identify the device once it has been manufactured",
    )
    YearOfConstruction = (auto(), " Year as completion date of object")
    DateOfManufacture = (
        auto(),
        " Date from which the production and / or development process is completed or from which a service is provided completely",
    )
    HardwareVersion = (auto(), " Version of the hardware supplied with the device")
    FirmwareVersion = (auto(), " Version of the firmware supplied with the device")
    SoftwareVersion = (auto(), " Version of the software used by the device")
    CountryOfOrigin = (auto(), " Country where the product was manufactured")
    CompanyLogo = (
        auto(),
        " A graphic mark used to represent a company, an organisation or a product",
    )
    Markings = (auto(), " Collection of product markings")
    AssetSpecificProperties = (
        auto(),
        " Group of properties that are listed on the asset's nameplate and are grouped based on guidelines",
    )
    Street = (auto(), " street name and house number")
    Zipcode = (auto(), " ZIP code of address")
    CityTown = (auto(), " town or city")
    NationalCode = (auto(), " code of a country")
    Marking = (
        auto(),
        " contains information about the marking labelled on the device",
    )
    MarkingName = (auto(), " common name of the marking")
    DesignationOfCertificateOrApproval = (
        auto(),
        " alphanumeric character sequence identifying a certificate or approval",
    )
    IssueDate = (auto(), " Date, at which the specified certificate is issued")
    ExpiryDate = (auto(), " Date, at which the specified certificate expires")
    ExplosionSafety = (
        auto(),
        " contains information related to explosion safety according to device nameplate",
    )
    TypeOfApproval = (
        auto(),
        " classification according to the standard or directive to which the approval applies",
    )
    ApprovalAgencyTestingAgency = (
        auto(),
        " certificates and approvals pertaining to general usage and compliance with constructional standards and directives",
    )
    RatedInsulationVoltage = (
        auto(),
        " from the manufacturer for the capital assets limited isolation with given(indicated) operating conditions",
    )
    InstructionsControlDrawing = (
        auto(),
        " designation used to uniquely identify a control/reference drawing stored in a file system",
    )
    SpecificConditionsForUse = (auto(), " Note: X if any, otherwise no entry")
    IncompleteDevice = (auto(), " U if any, otherwise no entry")
    AmbientConditions = (
        auto(),
        " Contains properties which are related to the ambient conditions of the device.",
    )
    ProcessConditions = (
        auto(),
        " Contains properties which are related to the process conditions of the device.",
    )
    ExternalElectricalCircuit = (
        auto(),
        " specifies the parameters of external electrical circuits.",
    )
    DeviceCategory = (
        auto(),
        " category of device in accordance with directive 94/9/EC",
    )
    EquipmentProtectionLevel = (
        auto(),
        " part of a hazardous area classification system indicating the likelihood of the existence of a classified hazard",
    )
    RegionalSpecificMarking = (
        auto(),
        ' Marking used only in specific regions, e.g. North America: class/divisions, EAC: "1" or NEC: "AIS"',
    )
    TypeOfProtection = (
        auto(),
        " classification of an explosion protection according to the specific measures applied to avoid ignition of a surrounding explosive atmosphere",
    )
    ExplosionGroup = (
        auto(),
        " classification of dangerous gaseous substances based on their ability to cause an explosion",
    )
    MinimumAmbientTemperature = (
        auto(),
        " lower limit of the temperature range of the surrounding space in which the component, the pipework or the system can be operated",
    )
    MaxAmbientTemperature = (
        auto(),
        " upper limit of the temperature range of the surrounding space in which the component, the pipework or the system can be operated",
    )
    MaxSurfaceTemperatureForDustProof = (
        auto(),
        " maximum permissible surface temperature of a device used in an explosion hazardous area with combustible dust",
    )
    TemperatureClass = (
        auto(),
        " classification system of electrical apparatus, based on its maximum surface temperature, related to the specific explosive atmosphere for which it is intended to be used",
    )
    DesignationOfElectricalTerminal = (
        auto(),
        " alphanumeric character sequence identifying an electrical terminal",
    )
    Characteristics = (auto(), " Characteristic of the intrinsically safe circuit")
    Fisco = (
        auto(),
        " FISCO certified intrinsically safe fieldbus circuit (IEC 60079-11)",
    )
    TwoWISE = (
        auto(),
        " 2-WISE certified intrinsically safe circuit (IEC 60079-47)",
    )
    SafetyRelatedPropertiesForPassiveBehaviour = (
        auto(),
        " properties characterizing the safety related parameters of a loop-powered, intrinsically safe input or output circuit",
    )
    SafetyRelatedPropertiesForActiveBehaviour = (
        auto(),
        " properties characterizing the safety related parameters of an intrinsically safe circuit",
    )
    MaxInputPower = (
        auto(),
        " maximum power that can be applied to the connection facilities of the apparatus without invalidating the type of protection",
    )
    MaxInputVoltage = (
        auto(),
        " maximum voltage (peak a.c. or d.c.) that can be applied to the connection facilities of the apparatus without invalidating the type of protection",
    )
    MaxInputCurrent = (
        auto(),
        " maximum current (peak a.c. or d.c.) that can be applied to the connection facilities of the apparatus without invalidating the type of protection",
    )
    MaxInternalCapacitance = (
        auto(),
        " maximum equivalent internal capacitance of the apparatus which is considered as appearing across the connection facilities",
    )
    MaxInternalInductance = (
        auto(),
        " maximum equivalent internal inductance of the apparatus which is considered as appearing across the connection facilities",
    )
    MaxOutputPower = (
        auto(),
        " maximum electrical power that can be taken from the apparatus",
    )
    MaxOutputVoltage = (
        auto(),
        " maximum voltage (peak a.c. or d.c.) that can occur at the connection facilities of the apparatus at any applied voltage up to the maximum voltage",
    )
    MaxOutputCurrent = (
        auto(),
        " maximum current (peak a.c. or d.c.) in the apparatus that can be taken from the connection facilities of the apparatus",
    )
    MaxExternalCapacitance = (
        auto(),
        " maximum capacitance that can be connected to the connection facilities of the apparatus without invalidating the type of protection",
    )
    MaxExternalInductance = (
        auto(),
        " maximum value of inductance that can be connected to the connection facilities of the apparatus without invalidating the type of protection",
    )
    MaxExternalInductanceRatio = (
        auto(),
        " maximum value of ratio of inductance (Lo) to resistance (Ro) of any external circuit that can be connected to the connection facilities of the electrical apparatus without invalidating intrinsic safety",
    )
    MaxExternalInductanceResistanceRatio = (
        auto(),
        " maximum value of ratio of inductance (Lo) to resistance (Ro) of any external circuit that can be connected to the connection facilities of the electrical apparatus without invalidating intrinsic safety",
    )
    GuidelineSpecificProperties = (
        auto(),
        " Asset specific nameplate information required by guideline, stipulation or legislation.",
    )
    arbitrary = (
        auto(),
        " semanticId = {arbitrary, representing information required by further standards}; Properties which are not required by any legislations but provided due to best practice.",
    )
    GuidelineForConformityDeclaration = (
        auto(),
        " guideline, stipulation or legislation used for determining conformity",
    )


class NameplateDescription(Enum):
    # https://industrialdigitaltwin.org/en/wp-content/uploads/sites/2/2024/11/IDTA-02006-3-0_Submodel_Digital-Nameplate.pdf
    URIOfTheProduct = (
        auto(),
        " Unique global identification of the product using a universal resource identifier (URI)",
    )
    ManufacturerName = (
        auto(),
        " Legally valid designation of the natural or judicial person which is directly responsible for the design, production, packaging and labeling of a product in respect to its being brought into circulation\n제품 유통과 관련하여 제품의 디자인, 생산, 포장 및 라벨링에 직접적으로 책임이 있는 자연인 또는 사법인의 법적으로 유효한 지정입니다.",
    )
    ManufacturerProductDesignation = (
        auto(),
        " The name of the product, provided by the manufacturer",
    )
    AddressInformation = (
        auto(),
        ' Note: this set of information is defined by SMT drop-in "Address Information"',
    )
    ManufacturerProductDescription = (
        auto(),
        " Description of the product, it's technical features and implementation if needed (long text)",
    )
    ManufacturerProductRoot = (
        auto(),
        " top level of a 3 level manufacturer specific product hierarchy",
    )
    ManufacturerProductFamily = (
        auto(),
        " second level of a 3 level manufacturer specific product hierarchy",
    )
    ManufacturerProductType = (
        auto(),
        " Characteristic to differentiate between different products of a product family or special variants",
    )
    OrderCodeOfManufacturer = (
        auto(),
        " unique combination of numbers and letters issued by the manufacturer that is used to identify the device for ordering",
    )
    ProductArticleNumberOfManufacturer = (
        auto(),
        " unique product identifier of the manufacturer",
    )
    SerialNumber = (
        auto(),
        " unique combination of numbers and letters used to identify the device once it has been manufactured",
    )
    YearOfConstruction = (
        auto(),
        " year in which the manufacturing process is completed",
    )
    DateOfManufacture = (auto(), " date when an item was manufactured")
    HardwareVersion = (auto(), " version of the hardware supplied with the device")
    FirmwareVersion = (auto(), " version of the firmware supplied with the device")
    SoftwareType = (
        auto(),
        " The type of the software (category, e.g. Runtime, Application, Firmware, Driver, etc.)",
    )
    SoftwareVersion = (auto(), " version of the software used by the device")
    CountryOfOrigin = (
        auto(),
        " country where the product was manufactured Note: Country codes defined accord. to DIN EN ISO 3166-1 alpha-2 codes",
    )
    UniqueFacilityIdentifier = (
        auto(),
        " unique string of characters for the identification of locations or buildings involved in a product's value chain or used by actors involved in a product's value chain",
    )
    Version = (
        auto(),
        " The complete version information consisting of Major Version, Minor Version, Revision and Build Number",
    )
    VersionName = (auto(), " The name this particular version is given")
    VersionInfo = (
        auto(),
        " Provides a textual description of most relevant characteristics of the version of the software",
    )
    ReleaseDate = (
        auto(),
        " The moment in time, when this version of the software was made publicly available",
    )
    ReleaseNotes = (auto(), " Contains information about this release")
    BuildDate = (
        auto(),
        " The moment in time, when this particular build of software was created",
    )
    InstallationURI = (
        auto(),
        " Indicates the resource, where the software is being provided by the manufacturer",
    )
    InstallationFile = (auto(), " Contains the installation code as BLOB.")
    InstallerType = (auto(), " Indicates the type of installation package")
    InstallationChecksum = (
        auto(),
        " Provides the checksum for the software available at InstallationURI",
    )
    InstanceName = (auto(), " The name of the software instance")
    InstalledVersion = (
        auto(),
        " The version information of the installed instance, consisting of Major Version, Minor Version, Revision and Build Number indicates the actual version of the instance",
    )
    InstallationDate = (auto(), " Date of Installation")
    InstallationPath = (
        auto(),
        " Indicates the path to the installed instance of the software",
    )
    InstallationSource = (
        auto(),
        " Indicates the path to the installation files used in this instance of the software",
    )
    InstalledOnArchitecture = (
        auto(),
        " Indicates the processor architecture this instance is installed on",
    )
    InstalledOnOS = (
        auto(),
        " Indicates the operating system this instance is installed on",
    )
    InstalledOnHost = (
        auto(),
        " Indicates the host system in case of a virtual environment",
    )
    InstalledModules = (auto(), " Collection of installed modules")
    ConfigurationPaths = (
        auto(),
        " Indicates the path to the configuration information",
    )
    SLAInformation = (auto(), " Indicates the actual service level agreements")
    Contact = (auto(), " Collection for general contact data")
    InventoryTag = (
        auto(),
        " Specifies an information used for inventory of the software",
    )
    InstalledModule = (auto(), " The name of a particular module installed")
    ConfigurationPath = (auto(), " Contains a single configuration entry")
    ConfigurationURI = (auto(), " Indicates the path to the configuration")
    ConfigurationType = (
        auto(),
        " Indicates the type of configuration (e.g. general configuration, user configuration)",
    )
    Marking = (
        auto(),
        " contains information about the marking labelled on the device",
    )
    MarkingName = (auto(), " common name of the marking")
    AssetSpecificProperties = (
        auto(),
        " Group of properties that are listed on the asset's nameplate and are grouped based on guidelines",
    )
    CompanyLogo = (
        auto(),
        " a graphic mark used to represent a company, an organisation or a product",
    )
    Markings = (
        auto(),
        " Note: CE marking is declared as mandatory according to EU Blue Guide",
    )


class HierarchicalStructuresDescription(Enum):
    # https://industrialdigitaltwin.org/en/wp-content/uploads/sites/2/2024/06/IDTA-02011-1-1_Submodel_HierarchicalStructuresEnablingBoM.pdf
    EntryNode = (
        auto(),
        " Base entry point for the Entity tree in this Submodel, this must be a Self-managed Entity reflecting the Assets administered in the AAS this Submodel is part of.",
    )
    ArcheType = (
        auto(),
        ' Arche Type of the Submodel, there are three allowed enumeration entries: 1. "Full", 2. "OneDown" and 3. "OneUp" These entries reflect the structure of the Submodel as defined in 1.5.1.3 & 1.5.1.4.',
    )
    Node = (
        auto(),
        ' The Entity Node can be a co-managed or self-managed entity representing an asset in the hierarchical structure. At least one nested Node shall be created as a Submodel Element for the EntryNode. In relation to the Arche Type, either the Relationship "IsPartOf" or "HasPart" shall be created using this Node as Second attribute.',
    )
    SameAs = (
        auto(),
        ' Reference between two Entities in the same Submodel or across Submodels. "First" and "Second" attributes must contain either an EntryNode or a Node.',
    )
    IsPartOf = (
        auto(),
        ' Modelling of logical connections between asset and sub-asset. Either this or "HasPart" must be used, not both. "First" and "Second" attributes must contain either a EntryNode or a Node. The relationships shall only reference EntryNodes or Nodes in the same submodel instance.',
    )
    HasPart = (
        auto(),
        ' Modelling of logical connections between components and sub-components. Either this or "IsPartOf" must be used, not both. "First" and "Second" attributes must contain either a EntryNode or a Node. The relationships shall only reference EntryNodes or Nodes in the same submodel instance.',
    )
    BulkCount = (
        auto(),
        " To be used if bulk components are referenced, e.g., a 10x M4x30 screw. Additional constraint: With bulk count only a reference to an asset with kind type is allowed, e.g., the M4x30 type asset.",
    )


class CarbonFootprintDescription(Enum):
    # https://industrialdigitaltwin.org/en/wp-content/uploads/sites/2/2024/01/IDTA-2023-0-9-_Submodel_CarbonFootprint.pdf
    ProductCarbonFootprint = (
        auto(),
        " Balance of greenhouse gas emissions along the entire life cycle of a product in a defined application and in relation to a defined unit of use",
    )
    TransportCarbonFootprint = (
        auto(),
        " Balance of greenhouse gas emissions generated by a transport service of a product",
    )
    PCFCalculationMethod = (
        auto(),
        " Standard, method for determining the greenhouse gas emissions of a product",
    )
    PCFCO2eq = (
        auto(),
        " Sum of all greenhouse gas emissions of a product according to the quantification requirements of the standard",
    )
    PCFReferenceValueForCalculation = (
        auto(),
        " Quantity unit of the product to which the PCF information on the CO2 footprint refers",
    )
    PCFQuantityOfMeasureForCalculation = (
        auto(),
        " Quantity of the product to which the PCF information on the CO2 footprint refers",
    )
    PCFLifeCyclePhase = (
        auto(),
        " Life cycle stages of the product according to the quantification requirements of the standard to which the PCF carbon footprint statement refers",
    )
    ExplanatoryStatement = (
        auto(),
        " definition@en: Explanation which is needed or given so that a footprint communication can be properly understood by a purchaser, potential purchaser or user of the product",
    )
    PCFGoodsAddressHandover = (
        auto(),
        " Indicates the place of hand-over of the goods (use structure defined in section 2.5 SMC Address)",
    )
    PublicationDate = (
        auto(),
        " Time at which something was first published or made available",
    )
    ExpirationDate = (
        auto(),
        " Time at which something should no longer be used effectively because it may lose its validity, quality or safety",
    )
    TCFCalculationMethod = (
        auto(),
        " Standard, method for determining the greenhouse gas emissions for the transport of a product",
    )
    TCFCO2eq = (
        auto(),
        " Sum of all greenhouse gas emissions from vehicle operation",
    )
    TCFReferenceValueForCalculation = (
        auto(),
        " Amount of product to which the TCF carbon footprint statement relates",
    )
    TCFQuantityOfMeasureForCalculation = (
        auto(),
        " Quantity of the product to which the TCF information on the CO2 footprint refers",
    )
    TCFProcessesForGreenhouseGasEmissionInATransportService = (
        auto(),
        " Processes in a transport service to determine the sum of all direct or indirect greenhouse gas emissions from fuel supply and vehicle operation",
    )
    TCFGoodsTransportAddressTakeover = (
        auto(),
        " Indication of the place of receipt of goods (use structure defined in 2.5 SMC Address)",
    )
    TCFGoodsTransportAddressHandover = (
        auto(),
        " Indicates the hand-over address of the goods transport (use structure defined in 2.5 SMC Address)",
    )
    Street = (auto(), " Street indication of the place of transfer of goods")
    HouseNumber = (
        auto(),
        " Number for identification or differentiation of individual houses of a street",
    )
    ZipCode = (auto(), " Zip code of the goods transfer address")
    CityTown = (auto(), " Indication of the city or town of the transfer of goods")
    Country = (auto(), " Country where the product is transmitted")


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
