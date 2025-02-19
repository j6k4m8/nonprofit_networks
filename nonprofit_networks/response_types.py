from typing import List, Optional
from pydantic import BaseModel, Field


class Address_(BaseModel):
    AddressLine1Txt: str
    CityNm: str
    StateAbbreviationCd: str
    ZIPCd: str


class BusinessName_(BaseModel):
    BusinessNameLine1Txt: str
    BusinessNameLine2Txt: Optional[str] = None


class PreparerFirmName_(BaseModel):
    BusinessNameLine1Txt: str


class PreparerFirmGrp_(BaseModel):
    PreparerFirmEIN: str
    PreparerFirmName: PreparerFirmName_
    PreparerUSAddress: Address_


class Filer_(BaseModel):
    EIN: str
    BusinessName: BusinessName_
    BusinessNameControlTxt: str
    USAddress: Address_


class BusinessOfficerGrp_(BaseModel):
    PersonNm: str
    PersonTitleTxt: str
    SignatureDt: str
    DiscussWithPaidPreparerInd: str


class PersonFullName_(BaseModel):
    PersonFirstNm: str
    PersonLastNm: str


class SigningOfficerGrp_(BaseModel):
    PersonFullName: PersonFullName_
    SSN: str


class PreparerPersonGrp_(BaseModel):
    PreparerPersonNm: str
    PTIN: str
    PhoneNum: str
    PreparationDt: str


class TrustedCustomerGrp_(BaseModel):
    TrustedCustomerCd: str
    AuthenticationAssuranceLevelCd: str
    IdentityAssuranceLevelCd: str


class AdditionalFilerInformation_(BaseModel):
    TrustedCustomerGrp: TrustedCustomerGrp_


class ReturnHeader_(BaseModel):
    binaryAttachmentCnt: str = Field(alias="@binaryAttachmentCnt")
    ReturnTs: str
    TaxPeriodEndDt: str
    PreparerFirmGrp: PreparerFirmGrp_
    ReturnTypeCd: str
    TaxPeriodBeginDt: str
    Filer: Filer_
    BusinessOfficerGrp: BusinessOfficerGrp_
    SigningOfficerGrp: SigningOfficerGrp_
    IRSResponsiblePrtyInfoCurrInd: str
    PreparerPersonGrp: PreparerPersonGrp_
    AdditionalFilerInformation: AdditionalFilerInformation_
    TaxYr: str
    BuildTS: str


class Organization501IndicatorGrp_(BaseModel):
    Organization501Ind: str
    Organization501cTypeTxt: str


class BooksInCareOfDetail_(BaseModel):
    PersonNm: str
    USAddress: Address_
    PhoneNum: str


class Post2017NOLCarryoverGrp_(BaseModel):
    PrincipalBusinessActivityCd: str
    AvlblPost2017NOLCarryoverAmt: str


class IRS990T_(BaseModel):
    documentId: str = Field(alias="@documentId")
    Organization501IndicatorGrp: Organization501IndicatorGrp_
    BookValueAssetsEOYAmt: str
    OrgStateCollegeUniversityInd: str
    Form990TScheduleAAttachedCnt: str
    SubsidiaryCorporationInd: str
    BooksInCareOfDetail: BooksInCareOfDetail_
    TotalUBTIComputedAmt: str
    CharitableContributionsDedAmt: str
    NetOperatingLossDeductionAmt: str
    SpecificDeductionAmt: str
    TotalDeductionAmt: str
    TotalUBTIAmt: str
    TaxableCorporationAmt: str
    TotalTaxComputationAmt: str
    TaxLessCreditsAmt: str
    TotalTaxAmt: str
    PaidTaxLiabilityAmt: str
    ForeignAccountsQuestionInd: str
    ForeignTrustQuestionInd: str
    AvlblPre2018NOLCarryoverAmt: str
    Post2017NOLCarryoverGrp: List[Post2017NOLCarryoverGrp_]
    ChangeInMethodOfAccountingInd: str


class OtherIncomeAmt_(BaseModel):
    referenceDocumentId: str = Field(alias="@referenceDocumentId")
    text: str = Field(alias="#text")


class OtherDeductionsAmt_(BaseModel):
    referenceDocumentId: str = Field(alias="@referenceDocumentId")
    text: str = Field(alias="#text")


class RentIncomePropertyGrp_(BaseModel):
    USAddress: Optional[Address_]
    RentPersonalPropertyAmt: Optional[str] = None
    RentRealPersonalPropertyAmt: Optional[str] = None
    TotalRentsByPropertyAmt: Optional[str] = None
    DeductionsConnectedRentIncmAmt: Optional[str] = None


class IRS990TScheduleA_(BaseModel):
    documentId: str = Field(alias="@documentId")
    PrincipalBusinessActivityCd: str
    SequenceReferenceNum: str
    SequenceTotalNum: str
    TradeOrBusinessDesc: str
    OtherIncomeAmt: Optional[OtherIncomeAmt_] = None
    TotUnrltTrdBusIncmAmt: str
    TotUnrltTrdBusIncmExpnssAmt: str
    TotNetUnrltTrdBusIncmAmt: str
    SalariesAndWagesAmt: str
    EmployeeBenefitProgramAmt: Optional[str] = None
    OtherDeductionsAmt: Optional[OtherDeductionsAmt_]
    TotalDeductionsAmt: str
    UBIBeforeNOLDedAmt: str
    NetOperatingLossDeductionAmt: str
    UnrelatedBusinessTaxblIncmAmt: str
    TotalRentIncomeAmt: str
    TotalRentDeductionsAmt: str
    TotalGrossDebtFinancedIncmAmt: str
    TotalAllocableDeductionsAmt: str
    TotalDividendsReceivedDedAmt: str
    TotalCtrlOrgPymtGrossIncmAmt: str
    TotalCtrlOrgDeductionAmt: str
    TotalInvestmentIncomeAmt: str
    TotalDeductionSetAsidesAmt: str
    TotalGrossAdvertisingIncomeAmt: str
    TotalDirectAdvertisingCostAmt: str
    TotExcessReadershipCostsDedAmt: str
    TotalUnrelatedBusinessCompAmt: str
    RentIncomePropertyGrp: Optional[RentIncomePropertyGrp_] = None

    # Allow anything to be missing
    class Config:
        extra = "allow"


class ReturnData_(BaseModel):
    documentCnt: str = Field(alias="@documentCnt")
    IRS990T: IRS990T_
    IRS990TScheduleA: List[IRS990TScheduleA_]


class Return_(BaseModel):
    xmlns: str = Field(alias="@xmlns")
    xmlns_xsi: str = Field(alias="@xmlns:xsi")
    xsi_schemaLocation: str = Field(alias="@xsi:schemaLocation")
    returnVersion: str = Field(alias="@returnVersion")
    ReturnHeader: ReturnHeader_
    ReturnData: ReturnData_


class FullFiling(BaseModel):
    Return: Return_

    def get_board_members(self):
        return [
            x
            for x in self.Return.ReturnData.IRS990TScheduleA
            if x.TradeOrBusinessDesc == "Board Members"
        ]
