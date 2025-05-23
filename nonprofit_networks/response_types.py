from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, field_validator


def convert_amount_to_float(v):
    """Convert a value to float, returning 0.0 if conversion fails."""
    if v is None:
        return 0.0
    try:
        return float(v)
    except (ValueError, TypeError):
        return v


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
    DiscussWithPaidPreparerInd: Optional[str] = None
    PhoneNum: Optional[str] = None


class PersonFullName_(BaseModel):
    PersonFirstNm: str
    PersonLastNm: str


class SigningOfficerGrp_(BaseModel):
    PersonFullName: PersonFullName_
    SSN: str


class PreparerPersonGrp_(BaseModel):
    PreparerPersonNm: Optional[str] = None
    PTIN: str
    PhoneNum: str
    PreparationDt: Optional[str] = None


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
    SigningOfficerGrp: Optional[SigningOfficerGrp_] = None
    IRSResponsiblePrtyInfoCurrInd: Optional[str] = None
    PreparerPersonGrp: PreparerPersonGrp_
    AdditionalFilerInformation: Optional[AdditionalFilerInformation_] = None
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
    AvlblPost2017NOLCarryoverAmt: Union[str, float]

    @field_validator("AvlblPost2017NOLCarryoverAmt", mode="before")
    @classmethod
    def validate_amount(cls, v):
        return convert_amount_to_float(v)


class NetOperatingLossDeductionAmt_(BaseModel):
    referenceDocumentId: str = Field(alias="@referenceDocumentId")
    text: Union[str, float] = Field(alias="#text")

    @field_validator("text", mode="before")
    @classmethod
    def validate_amount(cls, v):
        return convert_amount_to_float(v)


class IRS990T_(BaseModel):
    documentId: str = Field(alias="@documentId")
    Organization501IndicatorGrp: Organization501IndicatorGrp_
    BookValueAssetsEOYAmt: str
    OrgStateCollegeUniversityInd: Optional[str] = None
    Form990TScheduleAAttachedCnt: str
    SubsidiaryCorporationInd: str
    BooksInCareOfDetail: BooksInCareOfDetail_
    TotalUBTIComputedAmt: str
    CharitableContributionsDedAmt: str
    NetOperatingLossDeductionAmt: Optional[NetOperatingLossDeductionAmt_] = None
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
    Post2017NOLCarryoverGrp: Optional[Post2017NOLCarryoverGrp_] = None
    ChangeInMethodOfAccountingInd: Optional[str] = None

    class Config:
        extra = "allow"


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
    SalariesAndWagesAmt: Optional[str] = None
    EmployeeBenefitProgramAmt: Optional[str] = None
    OtherDeductionsAmt: Optional[OtherDeductionsAmt_] = None
    TotalDeductionsAmt: str
    UBIBeforeNOLDedAmt: str
    NetOperatingLossDeductionAmt: Optional[Union[str, float]] = None
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
    AverageHoursPerWeekRt: Union[str, float]
    AverageHoursPerWeekRltdOrgRt: Optional[Union[str, float]] = None
    IndividualTrusteeOrDirectorInd: Optional[str] = None
    OfficerInd: Optional[str] = None
    KeyEmployeeInd: Optional[str] = None
    HighestCompensatedEmployeeInd: Optional[str] = None
    ReportableCompFromOrgAmt: Union[str, float]
    ReportableCompFromRltdOrgAmt: Union[str, float]
    OtherCompensationAmt: Union[str, float]

    @field_validator(
        "AverageHoursPerWeekRt",
        "AverageHoursPerWeekRltdOrgRt",
        "ReportableCompFromOrgAmt",
        "ReportableCompFromRltdOrgAmt",
        "OtherCompensationAmt",
        mode="before",
    )
    @classmethod
    def validate_amounts(cls, v):
        return convert_amount_to_float(v)


class ContractorCompensationGrp_(BaseModel):
    ContractorName: Dict[str, Any]
    ContractorAddress: Dict[str, Any]
    ServicesDesc: str
    CompensationAmt: Union[str, float]

    @field_validator("CompensationAmt", mode="before")
    @classmethod
    def validate_amount(cls, v):
        return convert_amount_to_float(v)


class ProgramServiceRevenueGrp_(BaseModel):
    Desc: str
    BusinessCd: str
    TotalRevenueColumnAmt: Union[str, float]
    RelatedOrExemptFuncIncomeAmt: Union[str, float]

    @field_validator(
        "TotalRevenueColumnAmt", "RelatedOrExemptFuncIncomeAmt", mode="before"
    )
    @classmethod
    def validate_amounts(cls, v):
        return convert_amount_to_float(v)


class IRS990_(BaseModel):
    documentId: str = Field(alias="@documentId")
    PrincipalOfficerNm: str
    USAddress: Address_
    GrossReceiptsAmt: Union[str, float]
    Organization501c3Ind: Optional[str] = None
    Organization501cInd: Optional[Dict[str, Any]] = None
    WebsiteAddressTxt: Optional[str] = None
    TypeOfOrganizationCorpInd: Optional[str] = None
    TypeOfOrganizationTrustInd: Optional[str] = None
    FormationYr: str
    LegalDomicileStateCd: str
    ActivityOrMissionDesc: str
    VotingMembersGoverningBodyCnt: str
    VotingMembersIndependentCnt: str
    TotalEmployeeCnt: str
    TotalVolunteersCnt: Optional[str] = None
    CYContributionsGrantsAmt: Union[str, float]
    CYProgramServiceRevenueAmt: Union[str, float]
    CYInvestmentIncomeAmt: Union[str, float]
    CYOtherRevenueAmt: Union[str, float]
    CYTotalRevenueAmt: Union[str, float]
    CYGrantsAndSimilarPaidAmt: Union[str, float]
    CYSalariesCompEmpBnftPaidAmt: Union[str, float]
    CYTotalFundraisingExpenseAmt: Union[str, float]
    CYOtherExpensesAmt: Union[str, float]
    CYTotalExpensesAmt: Union[str, float]
    CYRevenuesLessExpensesAmt: Union[str, float]
    TotalAssetsEOYAmt: Union[str, float]
    TotalLiabilitiesEOYAmt: Union[str, float]
    NetAssetsOrFundBalancesEOYAmt: Union[str, float]
    Form990PartVIISectionAGrp: List[Form990PartVIISectionAGrp_]
    ContractorCompensationGrp: Optional[
        Union[List[ContractorCompensationGrp_], ContractorCompensationGrp_]
    ] = None
    ProgramServiceRevenueGrp: Optional[
        ProgramServiceRevenueGrp_ | List[ProgramServiceRevenueGrp_]
    ] = None

    @field_validator(
        "GrossReceiptsAmt",
        "CYContributionsGrantsAmt",
        "CYProgramServiceRevenueAmt",
        "CYInvestmentIncomeAmt",
        "CYOtherRevenueAmt",
        "CYTotalRevenueAmt",
        "CYGrantsAndSimilarPaidAmt",
        "CYSalariesCompEmpBnftPaidAmt",
        "CYTotalFundraisingExpenseAmt",
        "CYOtherExpensesAmt",
        "CYTotalExpensesAmt",
        "CYRevenuesLessExpensesAmt",
        "TotalAssetsEOYAmt",
        "TotalLiabilitiesEOYAmt",
        "NetAssetsOrFundBalancesEOYAmt",
        mode="before",
    )
    @classmethod
    def validate_amounts(cls, v):
        return convert_amount_to_float(v)

    class Config:
        extra = "allow"


class IRS990ScheduleA_(BaseModel):
    documentId: str = Field(alias="@documentId")
    SchoolInd: Optional[str] = None


class IRS990ScheduleD_(BaseModel):
    documentId: str = Field(alias="@documentId")
    LandGrp: Optional[Dict[str, Any]] = None
    BuildingsGrp: Optional[Dict[str, Any]] = None
    EquipmentGrp: Optional[Dict[str, Any]] = None
    TotalBookValueLandBuildingsAmt: Optional[str] = None


class IRS990ScheduleJ_(BaseModel):
    documentId: str = Field(alias="@documentId")
    CompensationCommitteeInd: Optional[str] = None
    SeverancePaymentInd: str
    SupplementalNonqualRtrPlanInd: str


class DisregardedEntityName_(BaseModel):
    BusinessNameLine1Txt: str


class DirectControllingEntityName_(BaseModel):
    BusinessNameLine1Txt: str


class DisregardedEntitiesGrp_(BaseModel):
    DisregardedEntityName: DisregardedEntityName_
    USAddress: Address_
    EIN: str
    PrimaryActivitiesTxt: str
    LegalDomicileStateCd: str
    DirectControllingEntityName: DirectControllingEntityName_


class IdRelatedTaxExemptOrgGrp_(BaseModel):
    DisregardedEntityName: DisregardedEntityName_
    USAddress: Optional[Address_] = None
    EIN: Optional[str] = None
    PrimaryActivitiesTxt: Optional[str] = None
    LegalDomicileStateCd: Optional[str] = None
    ExemptCodeSectionTxt: Optional[str] = None
    PublicCharityStatusTxt: Optional[str] = None
    DirectControllingEntityName: Optional[DirectControllingEntityName_] = None
    ControlledOrganizationInd: Optional[str] = None

    class Config:
        extra = "allow"  # Allow additional fields


class OtherOrganizationName_(BaseModel):
    BusinessNameLine1Txt: str


class TransactionsRelatedOrgGrp_(BaseModel):
    OtherOrganizationName: OtherOrganizationName_
    TransactionTypeTxt: str
    InvolvedAmt: Union[str, float]
    MethodOfAmountDeterminationTxt: str

    @field_validator("InvolvedAmt", mode="before")
    @classmethod
    def validate_amount(cls, v):
        return convert_amount_to_float(v)


class IRS990ScheduleR_(BaseModel):
    documentId: str = Field(alias="@documentId")
    IdDisregardedEntitiesGrp: Optional[List[DisregardedEntitiesGrp_]] = None
    IdRelatedTaxExemptOrgGrp: Optional[
        Union[List[IdRelatedTaxExemptOrgGrp_], IdRelatedTaxExemptOrgGrp_]
    ] = None
    ReceiptOfIntAnntsRntsRyltsInd: str
    GiftGrntOrCapContriToOthOrgInd: str
    GiftGrntCapContriFromOthOrgInd: str
    LoansOrGuaranteesToOtherOrgInd: str
    LoansOrGuaranteesFromOthOrgInd: str
    DivRelatedOrganizationInd: str
    AssetSaleToOtherOrgInd: str
    AssetPurchaseFromOtherOrgInd: str
    AssetExchangeInd: str
    RentalOfFacilitiesToOthOrgInd: str
    RentalOfFcltsFromOthOrgInd: str
    PerformOfServicesForOthOrgInd: str
    PerformOfServicesByOtherOrgInd: str
    SharingOfFacilitiesInd: str
    PaidEmployeesSharingInd: str
    ReimbursementPaidToOtherOrgInd: str
    ReimbursementPaidByOtherOrgInd: str
    TransferToOtherOrgInd: str
    TransferFromOtherOrgInd: str
    TransactionsRelatedOrgGrp: Optional[List[TransactionsRelatedOrgGrp_]] = None

    def get_related_tax_exempt_orgs(self):
        """
        Get a list of related tax exempt orgs from the 990-T form.

        See Schedule R Part II, and IdRelatedTaxExemptOrgGrp

        Returns:
            List[IdRelatedTaxExemptOrgGrp_]: List of related tax exempt orgs
        """
        if not self.IdRelatedTaxExemptOrgGrp:
            return []

        if isinstance(self.IdRelatedTaxExemptOrgGrp, list):
            return self.IdRelatedTaxExemptOrgGrp
        return [self.IdRelatedTaxExemptOrgGrp]


class RecipientBusinessName_(BaseModel):
    BusinessNameLine1Txt: str


class RecipientTable_(BaseModel):
    RecipientBusinessName: RecipientBusinessName_
    USAddress: Address_
    RecipientEIN: Optional[str] = None
    IRCSectionDesc: str
    CashGrantAmt: Union[str, float]
    NonCashAssistanceAmt: Union[str, float, None] = None
    PurposeOfGrantTxt: str

    @field_validator("CashGrantAmt", "NonCashAssistanceAmt", mode="before")
    @classmethod
    def validate_amounts(cls, v):
        return convert_amount_to_float(v) if v is not None else None


class SupplementalInformationDetail_(BaseModel):
    FormAndLineReferenceDesc: str
    ExplanationTxt: str


class IRS990ScheduleI_(BaseModel):
    documentId: str = Field(alias="@documentId")
    GrantRecordsMaintainedInd: str
    RecipientTable: Union[List[RecipientTable_], RecipientTable_]
    Total501c3OrgCnt: str
    TotalOtherOrgCnt: str
    SupplementalInformationDetail: Optional[SupplementalInformationDetail_] = None

    def get_grant_recipients(self):
        """
        Get a list of all grant recipients from Schedule I of the 990 form.

        Returns:
            List[RecipientTable_]: List of grant recipients
        """
        if not self.RecipientTable:
            return []

        if isinstance(self.RecipientTable, list):
            return self.RecipientTable
        return [self.RecipientTable]


class ReturnData_(BaseModel):
    documentCnt: str = Field(alias="@documentCnt")
    IRS990: Optional[IRS990_] = None
    IRS990ScheduleA: Optional[IRS990ScheduleA_] = None
    IRS990ScheduleD: Optional[IRS990ScheduleD_] = None
    IRS990ScheduleJ: Optional[IRS990ScheduleJ_] = None
    IRS990ScheduleR: Optional[IRS990ScheduleR_] = None
    IRS990T: Optional[IRS990T_] = None
    IRS990TScheduleA: Optional[List[IRS990TScheduleA_]] = None
    IRS990ScheduleI: Optional[IRS990ScheduleI_] = None

    # Allow anything to be missing
    class Config:
        extra = "allow"


class Return_(BaseModel):
    xmlns: str = Field(alias="@xmlns")
    xmlns_xsi: str = Field(alias="@xmlns:xsi")
    xsi_schemaLocation: Optional[str] = Field(None, alias="@xsi:schemaLocation")
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
        if (
            not self.Return.ReturnData.IRS990
            or not self.Return.ReturnData.IRS990.ContractorCompensationGrp
        ):
            return []

        contractors = self.Return.ReturnData.IRS990.ContractorCompensationGrp
        if isinstance(contractors, list):
            return contractors
        return [contractors]

    def get_total_revexp(self):
        """
        Get the total revenue and expenses from the 990 form.

        Returns:
            Tuple[float, float]: Total revenue and expenses
        """
        return (
            (
                self.Return.ReturnData.IRS990.CYTotalRevenueAmt,
                self.Return.ReturnData.IRS990.CYTotalExpensesAmt,
            )
            if self.Return.ReturnData.IRS990
            else (None, None)
        )

    def get_net_assets(self):
        """
        Get the net assets from the 990 form.

        # NetAssetsOrFundBalancesEOYAmt

        Returns:
            float: Net assets

        """
        return (
            self.Return.ReturnData.IRS990.NetAssetsOrFundBalancesEOYAmt
            if self.Return.ReturnData.IRS990
            else None
        )

    def get_rent_income(self):
        """
        Get a list of rent income from the 990-T form.

        See Schedule A Part I

        Returns:
            List[RentIncomePropertyGrp_]: List of rent income
        """
        return (
            [rent for rent in self.Return.ReturnData.IRS990TScheduleA]
            if self.Return.ReturnData.IRS990TScheduleA
            else []
        )

    def get_disregarded_entities(self):
        """
        Get a list of disregarded entities from the 990-T form.

        See Schedule R Part I, and IdDisregardedEntitiesGrp

        Returns:
            List[DisregardedEntitiesGrp_]: List of disregarded entities
        """
        return (
            [
                entity
                for entity in self.Return.ReturnData.IRS990ScheduleR.IdDisregardedEntitiesGrp
            ]
            if self.Return.ReturnData.IRS990ScheduleR
            and self.Return.ReturnData.IRS990ScheduleR.IdDisregardedEntitiesGrp
            else []
        )

    def get_related_tax_exempt_orgs(self):
        """
        Get a list of related tax exempt orgs from the 990-T form.

        See Schedule R Part II, and IdRelatedTaxExemptOrgGrp

        Returns:
            List[IdRelatedTaxExemptOrgGrp_]: List of related tax exempt orgs
        """
        if (
            not self.Return.ReturnData.IRS990ScheduleR
            or not self.Return.ReturnData.IRS990ScheduleR.IdRelatedTaxExemptOrgGrp
        ):
            return []

        orgs = self.Return.ReturnData.IRS990ScheduleR.IdRelatedTaxExemptOrgGrp
        if isinstance(orgs, list):
            return orgs
        return [orgs]

    def get_transactions_related_orgs(self):
        """
        Get a list of transactions with related orgs from the 990-T form.

        See Schedule R Part III, and TransactionsRelatedOrgGrp

        Returns:
            List[TransactionsRelatedOrgGrp_]: List of transactions with related orgs
        """
        return (
            [
                transaction
                for transaction in self.Return.ReturnData.IRS990ScheduleR.TransactionsRelatedOrgGrp
            ]
            if self.Return.ReturnData.IRS990ScheduleR
            and self.Return.ReturnData.IRS990ScheduleR.TransactionsRelatedOrgGrp
            else []
        )

    def get_grant_recipients(self):
        """
        Get a list of all grant recipients from Schedule I of the 990 form.

        Returns:
            List[RecipientTable_]: List of grant recipients
        """
        if not self.Return.ReturnData.IRS990ScheduleI:
            return []

        recipients = self.Return.ReturnData.IRS990ScheduleI.RecipientTable
        if isinstance(recipients, list):
            return recipients
        return [recipients]

    def get_description(self):
        """
        Get the description of the organization from the 990 form.

        Returns:
            str: Description of the organization
        """
        return (
            self.Return.ReturnData.IRS990.ActivityOrMissionDesc
            if self.Return.ReturnData.IRS990
            else None
        )

    def get_name(self):
        """
        Get the name of the organization from the 990 form.

        Returns:
            str: Name of the organization
        """
        return self.Return.ReturnHeader.Filer.BusinessName.BusinessNameLine1Txt + (
            self.Return.ReturnHeader.Filer.BusinessName.BusinessNameLine2Txt
            if self.Return.ReturnHeader.Filer.BusinessName.BusinessNameLine2Txt
            else ""
        )
