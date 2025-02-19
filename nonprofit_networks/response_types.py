from typing import List, Optional, Dict, Any
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


class Form990PartVIISectionAGrp_(BaseModel):
    PersonNm: str
    TitleTxt: str
    AverageHoursPerWeekRt: str
    AverageHoursPerWeekRltdOrgRt: Optional[str] = None
    IndividualTrusteeOrDirectorInd: Optional[str] = None
    OfficerInd: Optional[str] = None
    KeyEmployeeInd: Optional[str] = None
    HighestCompensatedEmployeeInd: Optional[str] = None
    ReportableCompFromOrgAmt: str
    ReportableCompFromRltdOrgAmt: str
    OtherCompensationAmt: str


class ContractorCompensationGrp_(BaseModel):
    ContractorName: Dict[str, Any]
    ContractorAddress: Dict[str, Any]
    ServicesDesc: str
    CompensationAmt: str


class ProgramServiceRevenueGrp_(BaseModel):
    Desc: str
    BusinessCd: str
    TotalRevenueColumnAmt: str
    RelatedOrExemptFuncIncomeAmt: str


class IRS990_(BaseModel):
    documentId: str = Field(alias="@documentId")
    PrincipalOfficerNm: str
    USAddress: Address_
    GrossReceiptsAmt: str
    Organization501c3Ind: str
    WebsiteAddressTxt: str
    TypeOfOrganizationCorpInd: str
    FormationYr: str
    LegalDomicileStateCd: str
    ActivityOrMissionDesc: str
    VotingMembersGoverningBodyCnt: str
    VotingMembersIndependentCnt: str
    TotalEmployeeCnt: str
    TotalVolunteersCnt: str
    CYContributionsGrantsAmt: str
    CYProgramServiceRevenueAmt: str
    CYInvestmentIncomeAmt: str
    CYOtherRevenueAmt: str
    CYTotalRevenueAmt: str
    CYGrantsAndSimilarPaidAmt: str
    CYSalariesCompEmpBnftPaidAmt: str
    CYTotalFundraisingExpenseAmt: str
    CYOtherExpensesAmt: str
    CYTotalExpensesAmt: str
    CYRevenuesLessExpensesAmt: str
    TotalAssetsEOYAmt: str
    TotalLiabilitiesEOYAmt: str
    NetAssetsOrFundBalancesEOYAmt: str
    Form990PartVIISectionAGrp: List[Form990PartVIISectionAGrp_]
    ContractorCompensationGrp: List[ContractorCompensationGrp_]
    ProgramServiceRevenueGrp: ProgramServiceRevenueGrp_

    class Config:
        extra = "allow"


class IRS990ScheduleA_(BaseModel):
    documentId: str = Field(alias="@documentId")
    SchoolInd: str


class IRS990ScheduleD_(BaseModel):
    documentId: str = Field(alias="@documentId")
    LandGrp: Dict[str, Any]
    BuildingsGrp: Dict[str, Any]
    EquipmentGrp: Dict[str, Any]
    TotalBookValueLandBuildingsAmt: str


class IRS990ScheduleJ_(BaseModel):
    documentId: str = Field(alias="@documentId")
    CompensationCommitteeInd: str
    SeverancePaymentInd: str
    SupplementalNonqualRtrPlanInd: str


class ReturnData_(BaseModel):
    documentCnt: str = Field(alias="@documentCnt")
    IRS990: Optional[IRS990_] = None
    IRS990ScheduleA: Optional[IRS990ScheduleA_] = None
    IRS990ScheduleD: Optional[IRS990ScheduleD_] = None
    IRS990ScheduleJ: Optional[IRS990ScheduleJ_] = None
    IRS990T: Optional[IRS990T_] = None
    IRS990TScheduleA: Optional[List[IRS990TScheduleA_]] = None

    # Allow anything to be missing
    class Config:
        extra = "allow"


class Return_(BaseModel):
    xmlns: str = Field(alias="@xmlns")
    xmlns_xsi: str = Field(alias="@xmlns:xsi")
    xsi_schemaLocation: str = Field(alias="@xsi:schemaLocation")
    returnVersion: str = Field(alias="@returnVersion")
    ReturnHeader: ReturnHeader_
    ReturnData: ReturnData_


class FullFiling(BaseModel):
    Return: Return_

    def get_compensations(self):
        """
        Get a list of all reported compensation from Part VII Section A of the
        990 form.

        See ReturnData.IRS990.Form990PartVIISectionAGrp

        Returns:
            List[Form990PartVIISectionAGrp_]: List of compensation
        """
        return (
            [
                person
                for person in self.Return.ReturnData.IRS990.Form990PartVIISectionAGrp
            ]
            if self.Return.ReturnData.IRS990
            and self.Return.ReturnData.IRS990.Form990PartVIISectionAGrp
            else []
        )

    def get_contractor_compensation(self):
        """
        Get a list of all reported compensation from Part VII Section A of the
        990 form.

        See ReturnData.IRS990.ContractorCompensationGrp

        Returns:
            List[ContractorCompensationGrp_]: List of compensation
        """
        return (
            [
                contractor
                for contractor in self.Return.ReturnData.IRS990.ContractorCompensationGrp
            ]
            if self.Return.ReturnData.IRS990
            and self.Return.ReturnData.IRS990.ContractorCompensationGrp
            else []
        )
