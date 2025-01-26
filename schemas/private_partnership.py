from datetime import datetime
from enum import Enum
from typing import Annotated, List, Literal

from pydantic import AfterValidator, BaseModel, Field


def check_length_3(value: List[str]) -> List[str]:
    if len(value) > 3:
        raise ValueError("Wrong length")
    return value


class PostalAddressType(str, Enum):
    P_O_BOX = "P O BOX"
    PMB = "PMB"
    DTD = "DTD"


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class CategoryType(str, Enum):
    SELF_EMPLOYED = "Self Employed"
    EMPLOYEE = "Employee"
    FOREIGN_MISSION_EMPLOYEE = "Foreign Mission Employee"
    OTHER = "Other"


class MaritalStatus(str, Enum):
    SINGLE = "SINGLE"
    MARRIED = "MARRIED"
    DIVORCED = "DIVORCED"
    SEPARATED = "SEPARATED"
    WIDOWED = "WIDOWED"


class OtherInfo(str, Enum):
    NOT_APPLICABLE = "NOT_APPLICABLE"
    EXPORTER = "EXPORTER"
    MPORTER = "MPORTER"
    TAX_CONSULTANT = "TAX CONSULTANT"


class MotherInfo(BaseModel):
    maiden_last_name: str
    maiden_first_name: str


class TaxInfo(BaseModel):
    current_tax_office: str
    old_tin_number: str
    irs_tax_tax_file: str


class ID_Type(str, Enum):
    National_ID = "National ID"
    Voters_ID = "Voter's ID"
    Drivers_License = "Driver's License"
    Passport = "Passport"


class IdentificationInfo(BaseModel):
    id_type: ID_Type
    id_number: str
    issue_date: datetime
    expiry_date: datetime
    country_of_issue: str
    place_of_issue: str


class ResidentialAddressInfo(BaseModel):
    house_number: str
    house_name: str
    po_box: str
    street_name: str
    city: str
    district: str
    region: str
    location_area: str
    postal_code: str
    country: str
    is_postal_residentail: bool


class TaxContact(BaseModel):
    phone_number: str
    mobile_number: str
    fax: str
    email: str
    website: str
    prefered_contact: Literal["MOBILE", "EMAIL", "LETTER"]


class RGD_Registration(BaseModel):
    nature_of_business: str
    anual_turnover: str
    number_of_employees: str


class Partner(BaseModel):
    title: str
    first_name: str
    middle_name: str
    last_name: str
    tin: str
    ghana_card: str
    any_former_name: str
    previous_last_name: str
    gender: Gender
    date_of_birth: datetime
    nationality: str
    occupation: str
    mobile_number_1: str
    mobile_number_2: str
    email: str
    is_registered_tax_payer: bool
    tax_registration_info: TaxInfo
    category_types: List[CategoryType]
    employer_name: str
    marital_status: str
    birth_town: str
    birth_country: str
    birth_region: str
    birth_district: str
    is_resident: bool
    social_security_number: str
    other_information: OtherInfo
    mothers_info: MotherInfo
    id_info: IdentificationInfo
    residential_address: ResidentialAddressInfo
    tax_contact: TaxContact
    rgd_registration: RGD_Registration


class PrincipalBusinessActivities(BaseModel):
    isic: str
    commencement_date: datetime


class AddressInfo(BaseModel):
    digital_address: str
    house_number: str
    street_name: str
    city: str
    district: str
    region: str


class PostalAddress(BaseModel):
    c_o: str
    type: PostalAddressType
    number: str
    town: str
    region: str


class Contact(BaseModel):
    phone_number_1: str
    phone_number_2: str
    mobile_number_1: str
    mobile_number_2: str
    fax: str
    email: str
    website: str


class ChargesOnPartnershipAssets(BaseModel):
    description: str
    date: datetime
    amount: str


class MSME_Details(BaseModel):
    revenue_envisaged: str
    number_of_employees_envisaged: str


class PartnershipInfo(BaseModel):
    partnership_name: str
    sectors: Annotated[List[str], check_length_3]
    principal_business_activities: PrincipalBusinessActivities
    registered_office_address: AddressInfo
    principal_place_of_business: AddressInfo
    other_place_of_business: AddressInfo
    postal_address: PostalAddress
    contact: Contact
    charges_on_partnership_assets: ChargesOnPartnershipAssets
    msme_details: MSME_Details
