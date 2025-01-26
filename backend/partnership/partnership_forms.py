from datetime import datetime, timedelta

import fitz
import streamlit as st

from ..shapes import PDFOptionField, PDFTextFinder, TextBox


def get_date_input(
    key,
    label,
    min_value=datetime.now() - timedelta(days=100 * 365),
    default_value=datetime.now(),
):
    min_value = min_value.date()
    default_value = default_value.date()

    if key not in st.session_state.inputs:
        st.session_state.inputs[key] = default_value

    date_value = st.date_input(
        label, min_value=min_value, value=st.session_state.inputs[key]
    )
    if date_value < min_value or date_value > datetime.now().date():
        date_value = datetime.now().date()

    if date_value != st.session_state.inputs[key]:
        st.session_state.inputs[key] = date_value


# A - FIELD
def generate_form(page):
    num = st.session_state.part_num
    # if 'inputs' not in st.session_state:
    # st.session_state.inputs  = {}
    # st.session_state.inputs["confirm"] = confirm

    if "page" not in st.session_state:
        st.session_state.page = ""

    st.session_state.page = 8

    def field_plain_template(
        label, search_text, maxi, c_x, c_y=8, r_h=15, t_rows=2, value=""
    ):
        instance_field = PDFTextFinder(
            search_text,
            maxi,
            control_x=c_x,
            control_y=c_y,
            row_height=r_h,
            max_rows=t_rows,
        )
        if label == 0:
            return instance_field
        instance = st.text_input(
            f"{label}", max_chars=instance_field.total_space, value=value
        )
        return instance_field, instance

    options_d = {"box_width": 18, "control_x": 0.5}

    def field_D_template(
        search_text,
        label="",
        row_height=0,
        total_rows=1,
        y_offset=5,
        x_offset=134,
        boxes_per_row=17,
        value="",
    ):
        instance_field = TextBox(
            boxes_per_row,
            search_text=search_text,
            row_height=row_height,
            total_rows=total_rows,
            y_offset=y_offset,
            x_offset=x_offset,
            **options_d,
        )
        if label:
            instance = st.text_input(
                f"{label}:", max_chars=instance_field.total_boxes, value=value
            )
            return instance_field, instance
        return instance_field

    def field_option_template(
        options, label="", control_x=11, control_y=4, value=""
    ):
        instance_field = PDFOptionField(control_x, control_y)

        if label:
            instance = st.selectbox(f"{label}", options, index=value)
            return instance_field, instance

        return instance_field

    def field_box_template(
        search_text, label="", bpr=38, x_offset=94, y_offset=3, value=""
    ):
        instance_field = TextBox(
            bpr,
            search_text,
            x_offset=x_offset,
            y_offset=y_offset,
            box_width=10,
            row_height=0,
            control_x=0.35,
        )
        if label:
            instance = st.text_input(
                f"{label}:", max_chars=instance_field.total_boxes, value=value
            )
            return instance_field, instance

        return instance_field

    def field_multi_options(
        options, label, control_x=11, control_y=4, value=[]
    ):
        instance_field = PDFOptionField(control_x, control_y)
        instance = st.multiselect(f"{label}", options, default=value)
        return instance_field, instance

    if page == 2:
        for i in range(1, num + 1):
            options_t = ["Mr", "Mrs", "Miss", "Ms", "Dr"]
            (
                st.session_state.inputs[f"title_field{i}"],
                st.session_state.inputs[f"title{i}"],
            ) = PDFOptionField(control_x=24, control_y=5), st.selectbox(
                f"Select Title_Part{i}*:",
                options_t,
                index=options_t.index(
                    st.session_state.inputs.get(f"title{i}", "Mr")
                ),
            )
            (
                st.session_state.inputs[f"first_name_field_part{i}"],
                st.session_state.inputs[f"first_name_part{i}"],
            ) = field_D_template(
                "First Name*",
                f"First Name_Part{i}*",
                value=st.session_state.inputs.get(f"first_name_part{i}", ""),
            )
            (
                st.session_state.inputs[f"middle_name_field_part{i}"],
                st.session_state.inputs[f"middle_name_part{i}"],
            ) = field_D_template(
                "Middle Name",
                f"Middle Name_Part{i}",
                value=st.session_state.inputs.get(f"middle_name_part{i}", ""),
            )
            (
                st.session_state.inputs[f"last_name_field_part{i}"],
                st.session_state.inputs[f"last_name_part{i}"],
            ) = field_D_template(
                "Last Name*",
                f"Last Name_Part{i}:*",
                value=st.session_state.inputs.get(f"last_name_part{i}", ""),
            )
            st.session_state.inputs[f"name_identifier{i}"] = (
                st.session_state.inputs[f"first_name_part{i}"].title()
                + " "
                + st.session_state.inputs[f"middle_name_part{i}"].title()
                + " "
                + st.session_state.inputs[f"last_name_part{i}"].title()
            )

    elif page == 3:
        st.write(
            """Name should not be duplicated, similar,
        misleading or undesirable.
        The Registrar of Partnerships shall have
        the final approval regarding the name
        which is eventually submitted for
        registration.
        A list of registered names can be found
        on our portal www.rgdeservices.com"""
        )

        partnership_name_field = TextBox(
            boxes_per_row=19,
            total_rows=2,
            search_text="Partnership Name",
            x_offset=97,
            y_offset=5,
            box_width=17,
            row_height=14.8,
            control_x=1.2,
        )

        proposed_name = st.text_input(
            "Enter partnership name*",
            max_chars=partnership_name_field.total_boxes,
            value=st.session_state.inputs.get("proposed_name", ""),
        )
        st.session_state.inputs["proposed_name"] = proposed_name
        st.session_state.inputs["partnership_name_field"] = (
            partnership_name_field
        )

        # B - Nature of Business/Sector(s)*
        business_options = [
            "Estate/Housing",
            "Education",
            "Quarry / Mining",
            "Entertainment",
            "Food Industry",
            "Manufacturing",
            "Pharmaceutical",
            "Security",
            "Media",
            "Transport/Aerospace",
            "Shipping & Port",
            "Estate/Housing",
            "Hospitality",
            "Fashion/Beautification",
            "Health Care",
            "Refinery of Minerals",
            "Others(Please Specify)",
            "Securities/Brokers",
            "Commerce/Trading",
            "Banking and Finance",
            "Sanitation",
        ]

        st.write(
            """ Choose your sector(s) by selecting from the options
        below.
        If your sector is not listed, select "other" and write your
        sector in the space provided for
        “others”."""
        )
        selected_option = st.multiselect(
            "Select General Nature of Business/Sectors*: (Choose up to 3 options:)",
            business_options,
            default=st.session_state.inputs.get("selected_option", []),
        )
        general_nature_field = PDFOptionField(control_x=17, control_y=5)
        st.session_state.inputs["selected_option"] = selected_option
        st.session_state.inputs["general_nature_field"] = general_nature_field

    elif page == 4:
        if "Others(Please Specify)" in st.session_state.inputs.get(
            "selected_option", []
        ):
            st.session_state.inputs["other"] = st.text_input(
                "Please specify the nature of your business",
                max_chars=72,
                value=st.session_state.inputs.get("other", ""),
            )
            other_text = PDFTextFinder(
                "Others(Please Specify)",
                max_chars_per_row=28,
                control_x=0,
                control_y=23,
                row_height=15,
                max_rows=3,
            )
            # st.session_state.inputs["other"] = other
            st.session_state.inputs["other_text"] = other_text

        # C-Principal Business Activities*

        st.markdown(
            "<h6 style='text-align: center;'>Principal Business Activities*</h6>",
            unsafe_allow_html=True,
        )
        st.write(
            """ISIC or classification code is a standard
        classification for economic or business
        activities so that establishments could
        be classified based on the activity they
        carry out.
        A detailed list of ISIC or Classification
        Codes can be found on our website at
        www.orc.gov.gh"""
        )
        for i, item in enumerate(
            st.session_state.inputs["selected_option"][0:3], start=1
        ):
            st.session_state.inputs[f"iso_field_{item}"] = TextBox(
                boxes_per_row=19,
                total_rows=1,
                search_text=f"ISIC code {i}",
                x_offset=97,
                y_offset=4,
                box_width=17,
                row_height=14.8,
                control_x=1.2,
            )
            st.session_state.inputs[f"iso_{item}"] = st.text_input(
                f"Enter ISIC code for {item}",
                max_chars=st.session_state.inputs[
                    f"iso_field_{item}"
                ].total_boxes,
                value=st.session_state.inputs.get(f"iso_{item}", ""),
            )
        describe_company_field = PDFTextFinder(
            "If you cannot determine a code, please give",
            control_y=25,
            max_chars_per_row=63,
            row_height=15,
            control_x=0,
            max_rows=8,
        )

        describe_company = st.text_input(
            "If you cannot determine a code, please give a brief description of the company's business activities below",
            max_chars=describe_company_field.total_space,
            value=st.session_state.inputs.get("describe_company", ""),
        )
        st.session_state.inputs["describe_company_field"] = (
            describe_company_field
        )
        st.session_state.inputs["describe_company"] = describe_company
        get_date_input("date_commence", "Date of Commencement*")
        st.session_state.inputs["date_commence_field"] = PDFTextFinder(
            "Date of Commencement", control_x=300, control_y=10
        )

    elif page == 5:
        # # D- Business Address Information
        st.markdown(
            "<h6 style='text-align: center;'>Business Address Information</h6>",
            unsafe_allow_html=True,
        )
        st.write(
            """Every partner must have a Business
        Address, Principal Place of Business. The
        Registrar of Partnerships may send
        correspondence.
        Obtain a digital address by downloading
        the Ghana Post GPS app onto any smart
        phone."""
        )
        digital_address_field, digital_address = field_D_template(
            "Digital Address",
            "Enter Digital Address*",
            value=st.session_state.inputs.get("digital_address", ""),
        )
        st.session_state.inputs["digital_address_field"] = (
            digital_address_field
        )
        st.session_state.inputs["digital_address"] = digital_address
        house_field, house_flat = field_D_template(
            "House/Building/Flat",
            "House/Building/Flat*(Name or House No.)/LMB",
            total_rows=2,
            row_height=15,
            value=st.session_state.inputs.get("house_flat", ""),
        )
        st.session_state.inputs["house_field"] = house_field
        st.session_state.inputs["house_flat"] = house_flat
        street_field, street = field_D_template(
            "Street Name",
            "Enter Street Name*",
            total_rows=2,
            row_height=15,
            value=st.session_state.inputs.get("street", ""),
        )
        st.session_state.inputs["street_field"] = street_field
        st.session_state.inputs["street"] = street
        city_field, city = field_D_template(
            "City",
            "Enter City*",
            value=st.session_state.inputs.get("city", ""),
        )
        st.session_state.inputs["city_field"] = city_field
        st.session_state.inputs["city"] = city
        district_field, district = field_D_template(
            "District",
            "Enter District*",
            row_height=15,
            value=st.session_state.inputs.get("district", ""),
        )
        st.session_state.inputs["district_field"] = district_field
        st.session_state.inputs["district"] = district
        region_field, region = field_D_template(
            "Region",
            "Enter Region*",
            row_height=15,
            value=st.session_state.inputs.get("region", ""),
        )
        st.session_state.inputs["region_field"] = region_field
        st.session_state.inputs["region"] = region
        # # E-FIELD(Dependent on YES or NO)
        st.markdown(
            "<h6 style='text-align: center;'>Registered Office Address*</h6>",
            unsafe_allow_html=True,
        )
        user_option = ["Yes", "No"]
        user_response = st.selectbox(
            "Is the Principal place of Business the same as the Registered Office Address?",
            user_option,
            index=user_option.index(
                st.session_state.inputs.get("user_response", "Yes")
            ),
        )
        st.session_state.inputs["user_response"] = user_response
        other_place = st.selectbox(
            "Partnerships that have multiple operational locations must select 'Yes', if not select 'No'",
            user_option,
            index=user_option.index(
                st.session_state.inputs.get("other_place", "No")
            ),
        )
        st.session_state.inputs["other_place"] = other_place

    elif page == 6:
        if st.session_state.inputs["user_response"] == "No":
            st.write("Fill the address for the Principal place of Business")
            digital_address_field1, digital_address1 = field_D_template(
                "Digital Address",
                "Enter Digital Address1*",
                value=st.session_state.inputs.get("digital_address1", ""),
            )
            st.session_state.inputs["digital_address_field1"] = (
                digital_address_field1
            )
            st.session_state.inputs["digital_address1"] = digital_address1
            house_field1, house_flat1 = field_D_template(
                "House/Building/Flat",
                "Enter House No.1*",
                total_rows=2,
                row_height=15,
                value=st.session_state.inputs.get("house_flat1", ""),
            )
            st.session_state.inputs["house_field1"] = house_field1
            st.session_state.inputs["house_flat1"] = house_flat1
            street_field1, street1 = field_D_template(
                "Street Name",
                "Enter Street Name1*",
                total_rows=2,
                row_height=15,
                value=st.session_state.inputs.get("street1", ""),
            )
            st.session_state.inputs["street_field1"] = street_field1
            st.session_state.inputs["street1"] = street1
            city_field1, city1 = field_D_template(
                "City",
                "Enter City1*",
                value=st.session_state.inputs.get("city1", ""),
            )
            st.session_state.inputs["city_field1"] = city_field1
            st.session_state.inputs["city1"] = city1
            district_field1, district1 = field_D_template(
                "District",
                "Enter District1*",
                row_height=15,
                value=st.session_state.inputs.get("district1", ""),
            )
            st.session_state.inputs["district_field1"] = district_field1
            st.session_state.inputs["district1"] = district1
            region_field1, region1 = field_D_template(
                "District",
                "Enter Region1*",
                row_height=15,
                y_offset=20,
                value=st.session_state.inputs.get("region1", ""),
            )
            st.session_state.inputs["region_field1"] = region_field1
            st.session_state.inputs["region1"] = region1

        else:
            st.session_state.inputs["yes"] = PDFOptionField(
                control_x=12, control_y=4
            )

        # F-FIELD -Other Place of Business
        if st.session_state.inputs["other_place"] == "Yes":
            st.markdown(
                "<h6 style='text-align: center;'>Other Place of Business</h6>",
                unsafe_allow_html=True,
            )
            # st.write("""Partnerships that have multiple
            # operational locations must complete
            # this section.
            # """)
            digital_address_field2, digital_address2 = field_D_template(
                "Digital Address",
                "Enter Digital Address2",
                value=st.session_state.inputs.get("digital_address2", ""),
            )
            st.session_state.inputs["digital_address_field2"] = (
                digital_address_field2
            )
            st.session_state.inputs["digital_address2"] = digital_address2
            house_field2, house_flat2 = field_D_template(
                "House/Building/Flat",
                "Enter House No.2",
                total_rows=2,
                row_height=15,
                value=st.session_state.inputs.get("house_flat2", ""),
            )
            st.session_state.inputs["house_field2"] = house_field2
            st.session_state.inputs["house_flat2"] = house_flat2
            street_field2, street2 = field_D_template(
                "Street Name",
                "Enter Street Name2",
                total_rows=2,
                row_height=15,
                value=st.session_state.inputs.get("street2", ""),
            )
            st.session_state.inputs["street_field2"] = street_field2
            st.session_state.inputs["street2"] = street2
            city_field2, city2 = field_D_template(
                "City",
                "Enter City2",
                value=st.session_state.inputs.get("city2", ""),
            )
            st.session_state.inputs["city_field2"] = city_field2
            st.session_state.inputs["city2"] = city2
            district_field2, district2 = field_D_template(
                "District",
                "Enter District2",
                row_height=15,
                value=st.session_state.inputs.get("district2", ""),
            )
            st.session_state.inputs["district_field2"] = district_field2
            st.session_state.inputs["district2"] = district2
            region_field2, region2 = field_D_template(
                "District",
                "Enter Region2",
                row_height=15,
                y_offset=20,
                value=st.session_state.inputs.get("region2", ""),
            )
            st.session_state.inputs["region_field2"] = region_field2
            st.session_state.inputs["region2"] = region2

        # #GGG- POSTAL ADDRESS
        st.markdown(
            "<h6 style='text-align: center;'>Postal Address</h6>",
            unsafe_allow_html=True,
        )
        st.write(
            """Please select either Post Office Box (P O
        BOX), Private Mail Bag (PMB) or Door to
        Door (DTD) and provide details as
        applicable."""
        )
        c_o_field, c_o = field_D_template(
            "C/O",
            "C/O",
            total_rows=3,
            row_height=15,
            value=st.session_state.inputs.get("c_o", ""),
        )
        st.session_state.inputs["c_o_field"] = c_o_field
        st.session_state.inputs["c_o"] = c_o

        # TYPE
        options_g = ["P O BOX", "PMB", "DTD"]
        type = st.selectbox(
            "Select Type of Postal Address:*",
            options_g,
            index=options_g.index(
                st.session_state.inputs.get("type", "P O BOX")
            ),
        )
        type_field = PDFOptionField(control_x=15, control_y=5)
        st.session_state.inputs["type"] = type
        st.session_state.inputs["type_field"] = type_field
        number_field, number = field_D_template(
            "Number",
            "Number*",
            value=st.session_state.inputs.get("number", ""),
        )
        st.session_state.inputs["number_field"] = number_field
        st.session_state.inputs["number"] = number

        town_field, town = field_D_template(
            "Town", "Town*", value=st.session_state.inputs.get("town", "")
        )
        st.session_state.inputs["town_field"] = town_field
        st.session_state.inputs["town"] = town

        regionx_field, regionx = field_D_template(
            "Region",
            "Region*",
            value=st.session_state.inputs.get("regionx", ""),
        )
        st.session_state.inputs["regionx_field"] = regionx_field
        st.session_state.inputs["regionx"] = regionx

        # #HHHHHHHH CONTACT
        st.markdown(
            "<h6 style='text-align: center;'>Contact</h6>",
            unsafe_allow_html=True,
        )
        st.write(
            """Partners are to provide at least, one
        mobile phone number and an email
        address.
        This is to assist the Registrar of
        Partnerships send out notices."""
        )
        phone_num_field, phone_num = field_D_template(
            "Phone No 1",
            "Phone No 1*",
            value=st.session_state.inputs.get("phone_num", ""),
        )
        st.session_state.inputs["phone_num_field"] = phone_num_field
        st.session_state.inputs["phone_num"] = phone_num

        phone_num_field2, phone_num2 = field_D_template(
            "Phone No 2",
            " Phone No 2",
            value=st.session_state.inputs.get("phone_num2", ""),
        )
        st.session_state.inputs["phone_num_field2"] = phone_num_field2
        st.session_state.inputs["phone_num2"] = phone_num2

        mobile_num_field, mobile_num = field_D_template(
            "Mobile No 1",
            "Mobile No 1*",
            value=st.session_state.inputs.get("mobile_num", ""),
        )
        st.session_state.inputs["mobile_num_field"] = mobile_num_field
        st.session_state.inputs["mobile_num"] = mobile_num

        mobile_num_field2, mobile_num2 = field_D_template(
            "Mobile No 2",
            "Mobile No 2",
            value=st.session_state.inputs.get("mobile_num2", ""),
        )
        st.session_state.inputs["mobile_num_field2"] = mobile_num_field2
        st.session_state.inputs["mobile_num2"] = mobile_num2

        fax_field, fax = field_D_template(
            "Fax", "Fax", value=st.session_state.inputs.get("fax", "")
        )
        st.session_state.inputs["fax_field"] = fax_field
        st.session_state.inputs["fax"] = fax

        email_field, email = field_D_template(
            "Email Address*",
            "Email Address*",
            value=st.session_state.inputs.get("email", ""),
        )
        st.session_state.inputs["email_field"] = email_field
        st.session_state.inputs["email"] = email

        website_field, website = field_D_template(
            "Email Address*",
            "Website",
            row_height=15,
            y_offset=20,
            value=st.session_state.inputs.get("website", ""),
        )
        st.session_state.inputs["website_field"] = website_field
        st.session_state.inputs["website"] = website

    # #I-FIELD  Particulars of Charges on Partnership Assets
    elif page == 7:
        st.markdown(
            "<h6 style='text-align: center;'>Particulars of Charges on Partnership Assets</h6>",
            unsafe_allow_html=True,
        )
        st.write("""Clearly state any charge(s) on all assets""")
        (
            st.session_state.inputs["asset_field"],
            st.session_state.inputs["asset"],
        ) = field_D_template(
            "Description of Asset:",
            "Description of Asset",
            total_rows=3,
            row_height=14.8,
            value=st.session_state.inputs.get("asset", ""),
        )

        st.session_state.inputs["date_of_charges_field"] = field_D_template(
            "Date of creation of the charges", x_offset=154
        )
        get_date_input("date_of_charges", "Date of creation of the charges")

        (
            st.session_state.inputs["amount_of_charges_field"],
            st.session_state.inputs["amount_of_charges"],
        ) = field_D_template(
            "Amount of the Charge",
            "Amount of the Charge",
            value=st.session_state.inputs.get("amount_of_charges", ""),
        )

        # J FIELD MSME Details
        st.markdown(
            "<h6 style='text-align: center;'>MSME Details</h6>",
            unsafe_allow_html=True,
        )
        st.write(
            """This is to determine the size of the
        Partnership i.e. small scale business,
        medium scale business or large scale
        business"""
        )
        (
            st.session_state.inputs["revenue_field"],
            st.session_state.inputs["revenue"],
        ) = field_D_template(
            "Revenue Envisaged*",
            "Revenue Envisaged*",
            value=st.session_state.inputs.get("revenue", ""),
        )
        (
            st.session_state.inputs["employees_envisaged_field"],
            st.session_state.inputs["employees_envisaged"],
        ) = field_D_template(
            "No. of Employees Envisaged*",
            "No. of Employees Envisaged*",
            value=st.session_state.inputs.get("employees_envisaged", ""),
        )
        #     # K Business Operating Permit (BOP) Request
        st.markdown(
            "<h6 style='text-align: center;'>Business Operating Permit (BOP) Request</h6>",
            unsafe_allow_html=True,
        )
        options_revenue = ["Apply for BOP Later", "Already have a BOP"]
        st.session_state.inputs["apply_bop"] = st.selectbox(
            "Apply for BOP Now",
            options_revenue,
            index=options_revenue.index(
                st.session_state.inputs.get("apply_bop", "Apply for BOP Later")
            ),
        )

    if 7 < page < 8 + (5 * st.session_state.part_num):
        if page == 8:
            if st.session_state.inputs["apply_bop"] == "Already have a BOP":
                st.session_state.inputs["apply_bop_field"] = PDFOptionField(
                    control_x=17, control_y=5
                )
                (
                    st.session_state.inputs["bop_ref_field"],
                    st.session_state.inputs["bop_ref"],
                ) = field_D_template(
                    "Provide BOP Reference No.",
                    "Provide BOP Reference No.",
                    value=st.session_state.inputs.get("bop_ref", ""),
                )
            # Partner 1-Partner(s) Details 2 field to be worked on
            st.markdown(
                "<h6 style='text-align: center;'>Partner(s) Details</h6>",
                unsafe_allow_html=True,
            )

        for i in range(1, num + 1):
            if 13 <= page < 18:
                st.session_state.page += 5
                i += 1
            if 18 <= page < 23:
                st.session_state.page += 10
                i += 2
            if 23 <= page < 28:
                st.session_state.page += 15
                i += 3
            if 28 <= page < 33:
                st.session_state.page += 20
                i += 4
            if 33 <= page < 38:
                st.session_state.page += 25
                i += 5

            if page == st.session_state.page:
                if (
                    st.session_state.inputs[f"name_identifier{i}"].strip()
                    != ""
                ):
                    st.markdown(
                        f"<h6 style='text-align: center;'>Partner {i}: {st.session_state.inputs[f'title{i}']} {st.session_state.inputs[f'name_identifier{i}']}</h6>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<h6 style='text-align: center;'>Partner {i}: {st.session_state.inputs[f'name_identifier{i}']}</h6>",
                        unsafe_allow_html=True,
                    )

                st.write(
                    "NOTE: Partners without TIN should Fill the GRA TIN Form attached"
                )
                (
                    st.session_state.inputs[f"tin_field_part{i}"],
                    st.session_state.inputs[f"tin_part{i}"],
                ) = field_D_template(
                    "TIN*",
                    f"TIN_Part{i}*",
                    boxes_per_row=11,
                    value=st.session_state.inputs.get(f"tin_part{i}", ""),
                )
                (
                    st.session_state.inputs[f"gh_card_field_part{i}"],
                    st.session_state.inputs[f"gh_card_part{i}"],
                ) = field_D_template(
                    "Ghana Card(National Identity Card)*",
                    f"Ghana Card(National Identity Card)_Part{i} eg: GHA-********, input only the numbers*",
                    x_offset=245,
                    boxes_per_row=11,
                    value=st.session_state.inputs.get(f"gh_card_part{i}", ""),
                )

                (
                    st.session_state.inputs[f"former_name_field_part{i}"],
                    st.session_state.inputs[f"former_name_part{i}"],
                ) = field_D_template(
                    "Any Former Name",
                    f"Any Former Nam_Part{i}",
                    value=st.session_state.inputs.get(
                        f"former_name_part{i}", ""
                    ),
                )
                (
                    st.session_state.inputs[f"previous_name_field_tax{i}"],
                    st.session_state.inputs[f"previous_name_{i}"],
                ) = field_box_template(
                    "PREVIOUS LAST NAME",
                    f"PREVIOUS LAST NAME_{i}",
                    value=st.session_state.inputs.get(f"previous_name_{i}"),
                )

                options_gender = ["Male", "Female"]
                if i > 2:
                    st.session_state.inputs[f"gender_field{i}"] = (
                        PDFOptionField(control_x=38, control_y=5)
                    )
                else:
                    st.session_state.inputs[f"gender_field{i}"] = (
                        PDFOptionField(control_x=-32, control_y=5)
                    )
                st.session_state.inputs[f"gender{i}"] = st.selectbox(
                    f"Gender_Part{i}:*",
                    options_gender,
                    index=options_gender.index(
                        st.session_state.inputs.get(f"gender{i}", "Male")
                    ),
                )
                st.session_state.inputs[f"dob_field_part{i}"] = (
                    field_D_template("Date of Birth*")
                )
                get_date_input(f"dob_part{i}", f"Date of Birth_Part{i}")
                (
                    st.session_state.inputs[f"nationality_field_part{i}"],
                    st.session_state.inputs[f"nationality_part{i}"],
                ) = field_D_template(
                    "Nationality*",
                    f"Nationality_Part{i}*",
                    value=st.session_state.inputs.get(
                        f"former_name_part{i}", ""
                    ),
                )
                (
                    st.session_state.inputs[f"occupation_field_part{i}"],
                    st.session_state.inputs[f"occupation_part{i}"],
                ) = field_D_template(
                    "Occupation*",
                    f"Occupation_Part{i}*",
                    value=st.session_state.inputs.get(
                        f"occupation_part{i}", ""
                    ),
                )
                (
                    st.session_state.inputs[f"mobile1_field_part{i}"],
                    st.session_state.inputs[f"mobile1_part{i}"],
                ) = field_D_template(
                    "Mobile No 1*",
                    f"Mobile No 1*_Part{i}",
                    value=st.session_state.inputs.get(f"mobile1_part{i}", ""),
                )
                (
                    st.session_state.inputs[f"mobile2_field_part{i}"],
                    st.session_state.inputs[f"mobile2_part{i}"],
                ) = field_D_template(
                    "Mobile No 2",
                    f"Mobile No 2_Part{i}",
                    value=st.session_state.inputs.get(f"mobile2_part{i}", ""),
                )
                (
                    st.session_state.inputs[f"email_field_part{i}"],
                    st.session_state.inputs[f"email_part{i}"],
                ) = field_D_template(
                    "Email Address*",
                    f"Email Address*{i}",
                    value=st.session_state.inputs.get(f"email_part{i}", ""),
                )

                ###############TAX

                st.session_state.inputs[f"declare_name{i}"] = (
                    f"{ st.session_state.inputs[f'first_name_part{i}']} { st.session_state.inputs[f'middle_name_part{i}']} { st.session_state.inputs[f'last_name_part{i}']}"
                )

                option_taxpayer = ["YES", "NO"]
                st.session_state.inputs[f"tax_payer_field{i}"] = (
                    PDFOptionField(control_x=11, control_y=4)
                )
                st.session_state.inputs[f"tax_payer_{i}"] = st.selectbox(
                    f"ARE YOU A REGISTERED TAXPAYER?_part{i}",
                    option_taxpayer,
                    index=option_taxpayer.index(
                        st.session_state.inputs.get(f"tax_payer_{i}", "YES")
                    ),
                )

                # SECTION 2: INDIVIDUAL CATEGORY
                option_category = [
                    "Self employed",
                    "Employee",
                    "Foreign mission employee",
                    "Other",
                ]
                st.session_state.inputs[f"category_field{i}"] = PDFOptionField(
                    control_x=11, control_y=4
                )
                st.session_state.inputs[f"category_{i}"] = st.multiselect(
                    f"CATEGORY TYPE (Select as applicable) - part{i}",
                    option_category,
                    default=st.session_state.inputs.get(f"category_{i}", []),
                )

            elif page == st.session_state.page + 1:
                if st.session_state.inputs[f"name_identifier{i}"].strip():
                    st.markdown(
                        f"<h6 style='text-align: center;'>Partner {i}: {st.session_state.inputs[f'title{i}']} {st.session_state.inputs[f'name_identifier{i}']}</h6>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<h6 style='text-align: center;'>Partner {i}: {st.session_state.inputs[f'name_identifier{i}']}</h6>",
                        unsafe_allow_html=True,
                    )
                st.session_state.page += 1
                if "Other" in st.session_state.inputs[f"category_{i}"]:
                    st.session_state.inputs[f"specify_field{i}"] = (
                        PDFTextFinder(
                            "If OTHER specify",
                            max_chars_per_row=14,
                            control_x=65,
                            control_y=7,
                        )
                    )
                    st.session_state.inputs[f"specify_{i}"] = st.text_input(
                        f"If OTHER specify - part{i}:",
                        max_chars=st.session_state.inputs[
                            f"specify_field{i}"
                        ].max_chars_per_row,
                        value=st.session_state.inputs.get(f"specify_{i}", ""),
                    )
                st.session_state.inputs[f"employer_field{i}"] = PDFTextFinder(
                    f"Employer's Name",
                    max_chars_per_row=32,
                    control_x=70,
                    control_y=7,
                )
                st.session_state.inputs[f"employer_{i}"] = st.text_input(
                    f"Employer's Name - part{i}:",
                    max_chars=st.session_state.inputs[
                        f"employer_field{i}"
                    ].max_chars_per_row,
                    value=st.session_state.inputs.get(f"employer_{i}", ""),
                )

                # SECTION 3: PERSONAL DETAILS
                st.markdown(
                    "<h6 style='text-align: center;'> PERSONAL DETAILS</h6>",
                    unsafe_allow_html=True,
                )
                st.session_state.inputs[f"title_field_tax{i}"] = (
                    PDFOptionField(control_x=11, control_y=4)
                )
                st.session_state.inputs[f"title_{i}"] = (
                    st.session_state.inputs[f"title{i}"]
                )

                if (
                    st.session_state.inputs[f"title{i}"] == "Dr"
                    or st.session_state.inputs[f"title{i}"] == "Miss"
                ):
                    res = st.session_state.inputs[f"title{i}"]
                    st.session_state.inputs[f"title_{i}"] = "OTHER"
                    st.session_state.inputs[f"specify_title_field_tax{i}"] = (
                        PDFTextFinder(
                            "SPECIFY", control_x=33, max_chars_per_row=22
                        )
                    )
                    st.session_state.inputs[f"specify_title_{i}"] = res

                st.session_state.inputs[f"first_name_field_tax{i}"] = (
                    field_box_template("FIRST NAME")
                )
                st.session_state.inputs[f"middle_name_field_tax{i}"] = (
                    field_box_template("MIDDLE NAME(S)")
                )
                st.session_state.inputs[f"last_name_field_tax{i}"] = (
                    field_box_template("LAST NAME")
                )

                option_gender = ["MALE", "FEMALE"]
                (
                    st.session_state.inputs[f"gender_field_tax{i}"],
                    st.session_state.inputs[f"gender_{i}"],
                ) = (
                    field_option_template(option_gender),
                    st.session_state.inputs[f"gender{i}"],
                )
                (
                    st.session_state.inputs[f"occupation_field_tax{i}"],
                    st.session_state.inputs[f"occupation_{i}"],
                ) = (
                    field_box_template("MAIN OCCUPATION", x_offset=73, bpr=19),
                    st.session_state.inputs[f"occupation_part{i}"],
                )
                (
                    st.session_state.inputs[f"dob_field_tax{i}"],
                    st.session_state.inputs[f"dob_tax{i}"],
                ) = (
                    field_box_template("DATE OF BIRTH", bpr=10),
                    st.session_state.inputs[f"dob_part{i}"],
                )

                option_marital = [
                    "SINGLE",
                    "MARRIED",
                    "DIVORCED",
                    "SEPARATED",
                    "WIDOWED",
                ]
                (
                    st.session_state.inputs[f"marital_field{i}"],
                    st.session_state.inputs[f"marital_{i}"],
                ) = field_option_template(
                    option_marital,
                    f"MARITAL STATUS (tick one)_{i}",
                    value=option_marital.index(
                        st.session_state.inputs.get(f"marital_{i}", "SINGLE")
                    ),
                )
                (
                    st.session_state.inputs[f"birth_town_field{i}"],
                    st.session_state.inputs[f"birth_town_{i}"],
                ) = field_box_template(
                    "BIRTH TOWN",
                    f"BIRTH TOWN_{i}",
                    value=st.session_state.inputs.get(f"birth_town_{i}", ""),
                )
                (
                    st.session_state.inputs[f"birth_country_field_tax{i}"],
                    st.session_state.inputs[f"birth_country_{i}"],
                ) = field_box_template(
                    "BIRTH COUNTRY",
                    f"BIRTH COUNTRY_{i}",
                    value=st.session_state.inputs.get(
                        f"birth_country_{i}", ""
                    ),
                )
                (
                    st.session_state.inputs[f"birth_region_field_tax{i}"],
                    st.session_state.inputs[f"birth_region_{i}"],
                ) = field_box_template(
                    "BIRTH REGION",
                    f"BIRTH REGION_{i}",
                    value=st.session_state.inputs.get(f"birth_region_{i}", ""),
                )
                (
                    st.session_state.inputs[f"birth_district_field_tax{i}"],
                    st.session_state.inputs[f"birth_district_{i}"],
                ) = field_box_template(
                    "BIRTH DISTRICT",
                    f"BIRTH DISTRICT{i}",
                    value=st.session_state.inputs.get(
                        f"birth_district_{i}", ""
                    ),
                )
                (
                    st.session_state.inputs[f"nationality_field_tax{i}"],
                    st.session_state.inputs[f"nationality_{i}"],
                ) = (
                    field_box_template("NATIONALITY"),
                    st.session_state.inputs[f"nationality_part{i}"],
                )

                option_residents = ["YES", "NO"]
                (
                    st.session_state.inputs[f"residents_field_tax{i}"],
                    st.session_state.inputs[f"residents_{i}"],
                ) = field_option_template(
                    option_residents,
                    f"RESIDENT (select one)_{i}",
                    value=option_residents.index(
                        st.session_state.inputs.get(f"residents_{i}", "YES")
                    ),
                )
                (
                    st.session_state.inputs[f"security_field_tax{i}"],
                    st.session_state.inputs[f"security_{i}"],
                ) = field_box_template(
                    "SOCIAL SECURITY NUMBER",
                    f"SOCIAL SECURITY NUMBER_{i}",
                    bpr=13,
                    x_offset=98,
                    value=st.session_state.inputs.get(f"security_{i}", ""),
                )
                options_info = [
                    "IMPORTER",
                    "EXPORTER",
                    "TAX CONSULTANT",
                    "NOT APPLICABLE",
                ]
                (
                    st.session_state.inputs[f"info_field{i}"],
                    st.session_state.inputs[f"info_{i}"],
                ) = field_multi_options(
                    options_info,
                    f"OTHER INFORMATION (tick applicable ones)_{i}",
                    value=st.session_state.inputs.get(f"info_{i}", []),
                )

                st.markdown(
                    "<h6 style='text-align: center;'>MOTHER'S INFORMATION</h6>",
                    unsafe_allow_html=True,
                )
                (
                    st.session_state.inputs[f"mother_maiden_field{i}"],
                    st.session_state.inputs[f"mother_maiden_{i}"],
                ) = field_box_template(
                    "MAIDEN LAST NAME",
                    f"MAIDEN LAST NAME_{i}",
                    x_offset=84,
                    value=st.session_state.inputs.get(
                        f"mother_maiden_{i}", ""
                    ),
                )
                (
                    st.session_state.inputs[f"mother_first_field{i}"],
                    st.session_state.inputs[f"mother_first_{i}"],
                ) = field_box_template(
                    "FIRST NAME",
                    f"M_FIRST NAME_{i}",
                    x_offset=84,
                    value=st.session_state.inputs.get(f"mother_first_{i}", ""),
                )

            elif page == st.session_state.page + 2:
                if st.session_state.inputs[f"name_identifier{i}"].strip():
                    st.markdown(
                        f"<h6 style='text-align: center;'>Partner {i}: {st.session_state.inputs[f'title{i}']} {st.session_state.inputs[f'name_identifier{i}']}</h6>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<h6 style='text-align: center;'>Partner {i}: {st.session_state.inputs[f'name_identifier{i}']}</h6>",
                        unsafe_allow_html=True,
                    )

                st.session_state.page += 2
                # SECTION 4: TAX REGISTRATION INFORMATION (Complete this section if you are a registered taxpayer)
                st.markdown(
                    "<h6 style='text-align: center;'>TAX REGISTRATION INFORMATION (Complete this section if you are a registered taxpayer)</h6>",
                    unsafe_allow_html=True,
                )

                (
                    st.session_state.inputs[f"tax_office_field{i}"],
                    st.session_state.inputs[f"tax_office_{i}"],
                ) = field_box_template(
                    "CURRENT TAX OFFICE",
                    f"CURRENT TAX OFFICE_{i}",
                    value=st.session_state.inputs.get(f"tax_office_{i}", ""),
                )
                (
                    st.session_state.inputs[f"old_tin_field{i}"],
                    st.session_state.inputs[f"old_tin_{i}"],
                ) = field_box_template(
                    "OLD TIN NUMBER",
                    f"OLD TIN NUMBER_{i}",
                    bpr=10,
                    value=st.session_state.inputs.get(f"old_tin_{i}", ""),
                )
                (
                    st.session_state.inputs[f"tax_fee_field{i}"],
                    st.session_state.inputs[f"tax_fee_{i}"],
                ) = field_box_template(
                    "IRS TAX FILE #",
                    f"IRS TAX FILE #_{i}",
                    bpr=19,
                    x_offset=53,
                    value=st.session_state.inputs.get(f"tax_fee_{i}", ""),
                )

                # SECTION 5: IDENTIFICATION INFORMATION/ check boxes
                st.markdown(
                    "<h6 style='text-align: center;'>IDENTIFICATION INFORMATION</h6>",
                    unsafe_allow_html=True,
                )

                options_id = [
                    "National ID",
                    "Voter's ID",
                    "Driver's License (ID # is certificate of competence)",
                    "Passport",
                ]
                (
                    st.session_state.inputs[f"id_type_field{i}"],
                    st.session_state.inputs[f"id_type_{i}"],
                ) = field_option_template(
                    options_id,
                    f"ID TYPE (tick one)_{i}",
                    value=options_id.index(
                        st.session_state.inputs.get(
                            f"id_type_{i}", "National ID"
                        )
                    ),
                )
                (
                    st.session_state.inputs[f"id_num_field{i}"],
                    st.session_state.inputs[f"id_num_{i}"],
                ) = field_box_template(
                    "ID NUMBER",
                    f"ID NUMBER_{i}",
                    bpr=16,
                    value=st.session_state.inputs.get(f"id_num_{i}", ""),
                )

                st.session_state.inputs[f"issue_date_field{i}"] = TextBox(
                    10,
                    "ISSUE DATE",
                    x_offset=42,
                    row_height=0,
                    box_width=10,
                    control_x=0.35,
                    y_offset=3,
                )
                get_date_input(f"issue_date_{i}", f"ISSUE DATE_{i}")
                st.session_state.inputs[f"expiry_date_field{i}"] = TextBox(
                    10,
                    "EXPIRY DATE",
                    x_offset=73,
                    row_height=0,
                    box_width=10,
                    control_x=0.35,
                    y_offset=3,
                )
                get_date_input(f"expiry_d{i}", f"EXPIRY DATE_{i}")
                (
                    st.session_state.inputs[f"country_of_issue_field{i}"],
                    st.session_state.inputs[f"country_of_issue_{i}"],
                ) = field_box_template(
                    "COUNTRY OF ISSUE",
                    f"COUNTRY OF ISSUE_{i}",
                    bpr=16,
                    x_offset=67,
                    value=st.session_state.inputs.get(
                        f"country_of_issue_{i}", ""
                    ),
                )
                (
                    st.session_state.inputs[f"place_of_issue_field{i}"],
                    st.session_state.inputs[f"place_of_issue_{i}"],
                ) = field_box_template(
                    "PLACE OF ISSUE",
                    f"PLACE OF ISSUE_{i}",
                    bpr=25,
                    x_offset=93,
                    value=st.session_state.inputs.get(
                        f"place_of_issue_{i}", ""
                    ),
                )

                # SECTION 6: RESIDENTIAL ADDRESS
                st.markdown(
                    "<h6 style='text-align: center;'>RESIDENTIAL ADDRESS</h6>",
                    unsafe_allow_html=True,
                )
                st.session_state.inputs[f"house_num{i}"] = st.text_input(
                    f"House/Building/Flat*(House No.){i}",
                    value=st.session_state.inputs.get(f"house_num{i}", ""),
                    max_chars=8,
                )
                (
                    st.session_state.inputs[f"house_no_field_part{i}"],
                    st.session_state.inputs[f"house_no_part{i}"],
                ) = field_D_template(
                    "House/Building/Flat",
                    f"House/Building/Flat(Name)/LMB_Part{i}",
                    total_rows=2,
                    row_height=14.8,
                    boxes_per_row=12,
                    value=st.session_state.inputs.get(f"house_no_part{i}", ""),
                )
                (
                    st.session_state.inputs[f"street_field_part{i}"],
                    st.session_state.inputs[f"street_part{i}"],
                ) = field_D_template(
                    "Street Name*",
                    f"Street Name_Part{i}*",
                    value=st.session_state.inputs.get(f"street_part{i}", ""),
                )
                (
                    st.session_state.inputs[f"address_field_part{i}"],
                    st.session_state.inputs[f"address_part{i}"],
                ) = field_D_template(
                    "PMB/DTD/P.O.BOX",
                    f"PMB/DTD/P.O.BOX_Part{i}*",
                    total_rows=3,
                    row_height=14.8,
                    value=st.session_state.inputs.get(f"address_part{i}", ""),
                )
                (
                    st.session_state.inputs[f"city_field_part{i}"],
                    st.session_state.inputs[f"city_part{i}"],
                ) = field_D_template(
                    "City",
                    f"City_Part{i}",
                    value=st.session_state.inputs.get(f"district_part{i}", ""),
                )
                (
                    st.session_state.inputs[f"district_field_part{i}"],
                    st.session_state.inputs[f"district_part{i}"],
                ) = field_D_template(
                    "District",
                    f"District{i}",
                    value=st.session_state.inputs.get(f"district_part{i}", ""),
                )
                (
                    st.session_state.inputs[f"region_field_part{i}"],
                    st.session_state.inputs[f"region_part{i}"],
                ) = field_D_template(
                    "Region",
                    f"Region_Part{i}",
                    value=st.session_state.inputs.get(f"region_part{i}", ""),
                )

                st.session_state.inputs[f"house_num_field_tax{i}"] = (
                    field_box_template("HOUSE NUMBER", bpr=8)
                )
                st.session_state.inputs[f"building_name_field_tax{i}"] = (
                    field_box_template("BUILDING NAME", bpr=24, x_offset=62)
                )
                (
                    st.session_state.inputs[f"location_area_field_tax{i}"],
                    st.session_state.inputs[f"location_area_{i}"],
                ) = field_box_template(
                    "LOCATION / AREA",
                    f"Location / Area_{i}",
                    value=st.session_state.inputs.get(
                        f"location_area_{i}", ""
                    ),
                )
                (
                    st.session_state.inputs[f"postal_field_tax{i}"],
                    st.session_state.inputs[f"postal_{i}"],
                ) = field_box_template(
                    "POSTAL CODE",
                    f"Postal Code_{i}",
                    value=st.session_state.inputs.get(f"postal_{i}", ""),
                )
                (
                    st.session_state.inputs[f"country_field_tax{i}"],
                    st.session_state.inputs[f"country_{i}"],
                ) = field_box_template(
                    "COUNTRY",
                    f"Country_{i}",
                    value=st.session_state.inputs.get(f"country_{i}", ""),
                )
                (
                    st.session_state.inputs[f"landmark_field_tax{i}"],
                    st.session_state.inputs[f"landmark_{i}"],
                ) = (
                    field_box_template(
                        "STREET NAME/PROMINENT LANDMARK", x_offset=135
                    ),
                    st.session_state.inputs[f"street_part{i}"],
                )
                (
                    st.session_state.inputs[f"town_city_field_tax{i}"],
                    st.session_state.inputs[f"town_city_{i}"],
                ) = (
                    field_box_template("TOWN / CITY", bpr=25),
                    st.session_state.inputs[f"city_part{i}"],
                )
                (
                    st.session_state.inputs[f"region_field_tax{i}"],
                    st.session_state.inputs[f"region_{i}"],
                ) = (
                    field_box_template("REGION"),
                    st.session_state.inputs[f"region_part{i}"],
                )
                (
                    st.session_state.inputs[f"district_field_tax{i}"],
                    st.session_state.inputs[f"district_{i}"],
                ) = (
                    field_box_template("DISTRICT"),
                    st.session_state.inputs[f"district_part{i}"],
                )

                # SECTION 7: POSTAL ADDRESS
                option_postal = ["YES", "NO"]
                (
                    st.session_state.inputs[f"postal_address_taxfield{i}"],
                    st.session_state.inputs[f"postal_address_tax{i}"],
                ) = field_option_template(
                    option_postal,
                    f"IS POSTAL ADDRESS SAME AS RESIDENTIAL ADDRESS?_part{i}",
                    value=option_postal.index(
                        st.session_state.inputs.get(
                            f"postal_address_tax{i}", "YES"
                        )
                    ),
                )
            elif page == st.session_state.page + 3:
                if st.session_state.inputs[f"name_identifier{i}"].strip():
                    st.markdown(
                        f"<h6 style='text-align: center;'>Partner {i}: {st.session_state.inputs[f'title{i}']} {st.session_state.inputs[f'name_identifier{i}']}</h6>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<h6 style='text-align: center;'>Partner {i}: {st.session_state.inputs[f'name_identifier{i}']}</h6>",
                        unsafe_allow_html=True,
                    )

                st.session_state.page += 3
                if st.session_state.inputs[f"postal_address_tax{i}"] == "NO":
                    st.markdown(
                        "<h6 style='text-align: center;'>POSTAL ADDRESS</h6>",
                        unsafe_allow_html=True,
                    )
                    (
                        st.session_state.inputs[f"c_o_field_tax{i}"],
                        st.session_state.inputs[f"c_o_{i}"],
                    ) = field_box_template(
                        "C/O",
                        f"C/O_{i}",
                        bpr=30,
                        value=st.session_state.inputs.get(f"c_o_{i}", ""),
                    )
                    options_postal_type = [
                        "P. 0. BOX",
                        "PMB",
                        "DTD",
                        "POSTAL NUMBER",
                    ]
                    (
                        st.session_state.inputs[f"postal_type_taxfield{i}"],
                        st.session_state.inputs[f"postal_type_tax{i}"],
                    ) = field_multi_options(
                        options_postal_type,
                        f"POSTAL TYPE (tick as applicable)_part{i}",
                        value=st.session_state.inputs.get(
                            f"postal_type_tax{i}", []
                        ),
                    )

                    if (
                        "POSTAL NUMBER"
                        in st.session_state.inputs[f"postal_type_tax{i}"]
                    ):
                        (
                            st.session_state.inputs[f"postal_num_taxfield{i}"],
                            st.session_state.inputs[f"postal_num_tax{i}"],
                        ) = field_box_template(
                            "POSTAL NUMBER",
                            f"POSTAL NUMBER_{i}-start with Prefix, followed by number",
                            bpr=13,
                            x_offset=65,
                            value=st.session_state.inputs.get(
                                f"postal_num_tax{i}", ""
                            ),
                        )

                    (
                        st.session_state.inputs[f"box_region_field_tax{i}"],
                        st.session_state.inputs[f"box_region_{i}"],
                    ) = field_box_template(
                        "BOX REGION",
                        f"BOX REGION_{i}",
                        value=st.session_state.inputs.get(
                            f"box_region_{i}", ""
                        ),
                    )
                    (
                        st.session_state.inputs[f"box_town_field{i}"],
                        st.session_state.inputs[f"box_town_{i}"],
                    ) = field_box_template(
                        "BOX TOWN",
                        f"BOX TOWN_{i}",
                        value=st.session_state.inputs.get(f"box_town_{i}", ""),
                    )
                    (
                        st.session_state.inputs[f"box_location_field{i}"],
                        st.session_state.inputs[f"box_location_{i}"],
                    ) = field_box_template(
                        "BOX LOCATION/AREA",
                        f"BOX LOCATION/AREA_{i}",
                        value=st.session_state.inputs.get(
                            f"box_location_{i}", ""
                        ),
                    )

                # SECTION 8: CONTACT METHOD Indicate purpose of contact within the thick outlined box provided (P - Personal; B - Business; H - Home)- work on this to ensure user gets the format
                st.markdown(
                    "<h6 style='text-align: center;'>CONTACT METHOD FOR TAX REGISTRATION</h6>",
                    unsafe_allow_html=True,
                )
                st.write(
                    "Indicate purpose of contact as Prefix (P - Personal; B - Business; H - Home) for all st.session_state.inputs under this section. Eg: P-020*******"
                )

                (
                    st.session_state.inputs[f"phone_num_taxfield{i}"],
                    st.session_state.inputs[f"phone_num_tax{i}"],
                ) = field_box_template(
                    "PHONE/LANDLINE NUMBER",
                    f"PHONE/LANDLINE NUMBER_{i}",
                    x_offset=93,
                    bpr=12,
                    value=st.session_state.inputs.get(f"phone_num_tax{i}", ""),
                )
                (
                    st.session_state.inputs[f"fax_num_taxfield{i}"],
                    st.session_state.inputs[f"fax_num_tax{i}"],
                ) = field_box_template(
                    "FAX NUMBER",
                    f"FAX NUMBER_{i}",
                    bpr=12,
                    x_offset=93,
                    value=st.session_state.inputs.get(f"fax_num_tax{i}", ""),
                )
                (
                    st.session_state.inputs[f"mobile_num_taxfield{i}"],
                    st.session_state.inputs[f"mobile_num_tax{i}"],
                ) = field_box_template(
                    "MOBILE NUMBER",
                    f"MOBILE NUMBER{i}",
                    bpr=12,
                    x_offset=62,
                    value=st.session_state.inputs.get(
                        f"mobile_num_tax{i}", ""
                    ),
                )
                (
                    st.session_state.inputs[f"email_taxfield{i}"],
                    st.session_state.inputs[f"email_tax{i}"],
                ) = field_box_template(
                    "E-MAIL",
                    f"E-MAIL{i}",
                    x_offset=94,
                    value=st.session_state.inputs.get(f"email_tax{i}", ""),
                )
                (
                    st.session_state.inputs[f"website_taxfield{i}"],
                    st.session_state.inputs[f"website_tax{i}"],
                ) = field_box_template(
                    "WEBSITE",
                    f"WEBSITE_tax{i}",
                    x_offset=94,
                    value=st.session_state.inputs.get(f"website_tax{i}", ""),
                )
                option_contact = ["MOBILE", "EMAIL", "LETTER"]
                (
                    st.session_state.inputs[f"contact_taxfield{i}"],
                    st.session_state.inputs[f"contact_tax{i}"],
                ) = field_option_template(
                    option_contact,
                    f"PREFERRED CONTACT METHOD (tick one)_part{i}",
                    value=option_contact.index(
                        st.session_state.inputs.get(
                            f"contact_tax{i}", "MOBILE"
                        )
                    ),
                )

                # SECTION 9: BUSINESS ( COMPLETE THIS SECTION IF YOU ARE SELF EMPLOYED)
                # SECTION: BUSINESS
                st.markdown(
                    "<h6 style='text-align: center;'>BUSINESS</h6>",
                    unsafe_allow_html=True,
                )
                option_employee = [
                    "NO",
                    "YES",
                ]  # fix repetitive yes or no, currently used because of the order
                st.session_state.inputs[f"self_employed_{i}"] = st.selectbox(
                    f"Are you self-employed?_{i}",
                    option_employee,
                    index=option_employee.index(
                        st.session_state.inputs.get(f"self_employed_{i}", "NO")
                    ),
                )
                (
                    st.session_state.inputs[f"registered_field{i}"],
                    st.session_state.inputs[f"registered_{i}"],
                ) = field_option_template(
                    option_employee,
                    f"IF YES HAVE YOU REGISTERED YOUR BUSINESS NAME(S) WITH RGD?_{i}",
                    value=option_employee.index(
                        st.session_state.inputs.get(f"registered_{i}", "NO")
                    ),
                )
                if (
                    st.session_state.inputs[f"self_employed_{i}"] == "NO"
                    and st.session_state.inputs[f"registered_{i}"] == "NO"
                ):
                    st.session_state.inputs[f"skip_rendering_part{i}"] = "YES"
                else:
                    st.session_state.inputs[f"skip_rendering_part{i}"] = "NO"

            elif page == st.session_state.page + 4:
                if st.session_state.inputs[f"name_identifier{i}"].strip():
                    st.markdown(
                        f"<h6 style='text-align: center;'>Partner {i}: {st.session_state.inputs[f'title{i}']} {st.session_state.inputs[f'name_identifier{i}']}</h6>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<h6 style='text-align: center;'>Partner {i}: {st.session_state.inputs[f'name_identifier{i}']}</h6>",
                        unsafe_allow_html=True,
                    )

                st.session_state.page += 4
                if st.session_state.inputs[f"self_employed_{i}"] == "YES":
                    (
                        st.session_state.inputs[
                            f"business_nature_taxfield{i}"
                        ],
                        st.session_state.inputs[f"business_nature_tax{i}"],
                    ) = field_plain_template(
                        f"NATURE OF BUSINESS_{i}",
                        "NATURE OF BUSINESS",
                        maxi=70,
                        c_x=95,
                        value=st.session_state.inputs.get(
                            f"business_nature_tax{i}", ""
                        ),
                    )
                    (
                        st.session_state.inputs[f"annual_field{i}"],
                        st.session_state.inputs[f"annual_{i}"],
                    ) = field_box_template(
                        "ANNUAL TURNOVER IN GH¢",
                        f"ANNUAL TURNOVER IN GH¢_{i}",
                        bpr=13,
                        value=st.session_state.inputs.get(f"annual_{i}", ""),
                    )
                    (
                        st.session_state.inputs[f"num_employee_field{i}"],
                        st.session_state.inputs[f"num_employee_{i}"],
                    ) = field_box_template(
                        "NO. OF EMPLOYEES",
                        f"NO. OF EMPLOYEES_{i}",
                        bpr=15,
                        x_offset=73,
                        value=st.session_state.inputs.get(
                            f"num_employee_{i}", ""
                        ),
                    )

                if (
                    st.session_state.inputs[f"self_employed_{i}"] == "YES"
                    and st.session_state.inputs[f"registered_{i}"] == "YES"
                ):
                    (
                        st.session_state.inputs[f"reg_buss_field{i}"],
                        st.session_state.inputs[f"reg_buss_{i}"],
                    ) = field_plain_template(
                        f"BUSINESS NAME_{i}",
                        "BUSINESS NAME",
                        maxi=57,
                        c_x=-125,
                        c_y=20,
                        value=st.session_state.inputs.get(
                            f"reg_buss_{i}",
                        ),
                    )
                    (
                        st.session_state.inputs[f"reg_tin_field{i}"],
                        st.session_state.inputs[f"reg_tin_{i}"],
                    ) = field_box_template(
                        "OLD TIN",
                        f"OLD TIN_{i}",
                        bpr=9,
                        x_offset=-38,
                        y_offset=17,
                        value=st.session_state.inputs.get(f"reg_tin_{i}", ""),
                    )
                    (
                        st.session_state.inputs[f"reg_rgd_field{i}"],
                        st.session_state.inputs[f"reg_rgd_{i}"],
                    ) = field_box_template(
                        "RGD NUMBER",
                        f"RGD NUMBER_{i}",
                        bpr=8,
                        x_offset=-18,
                        y_offset=16,
                        value=st.session_state.inputs.get(f"reg_rgd_{i}", ""),
                    )
                    st.write("BUSINESS ADDRESS")
                    (
                        st.session_state.inputs[f"reg_house_field{i}"],
                        st.session_state.inputs[f"reg_house_{i}"],
                    ) = field_box_template(
                        "HOUSE NUMBER",
                        f"HOUSE NUMBER_buss_{i}",
                        bpr=9,
                        value=st.session_state.inputs.get(
                            f"reg_house_{i}", ""
                        ),
                    )
                    (
                        st.session_state.inputs[f"reg_build_field{i}"],
                        st.session_state.inputs[f"reg_build_{i}"],
                    ) = field_box_template(
                        "BUILDING NAME",
                        f"BUILDING NAME_buss_{i}",
                        bpr=22,
                        x_offset=63,
                        value=st.session_state.inputs.get(
                            f"reg_build_{i}", ""
                        ),
                    )
                    (
                        st.session_state.inputs[f"reg_street_field{i}"],
                        st.session_state.inputs[f"reg_street_{i}"],
                    ) = field_box_template(
                        "STREET NAME/PROMINENT LANDMARK",
                        f"STREET NAME/PROMINENT LANDMARK_buss_{i}",
                        bpr=29,
                        x_offset=135,
                        value=st.session_state.inputs.get(
                            f"reg_street_{i}", ""
                        ),
                    )
                    (
                        st.session_state.inputs[f"reg_town_field{i}"],
                        st.session_state.inputs[f"reg_town_{i}"],
                    ) = field_box_template(
                        "TOWN / CITY",
                        f"TOWN / CITY_buss_{i}",
                        bpr=36,
                        value=st.session_state.inputs.get(f"reg_town_{i}", ""),
                    )
                    (
                        st.session_state.inputs[f"reg_location_field{i}"],
                        st.session_state.inputs[f"reg_location_{i}"],
                    ) = field_box_template(
                        "LOCATION / AREA",
                        f"LOCATION / AREA_buss_{i}",
                        value=st.session_state.inputs.get(
                            f"reg_location_{i}", ""
                        ),
                    )
                    (
                        st.session_state.inputs[f"reg_postal_field_tax{i}"],
                        st.session_state.inputs[f"reg_postal_{i}"],
                    ) = field_box_template(
                        "POSTAL CODE",
                        f"POSTAL CODE_buss_{i}",
                        bpr=10,
                        value=st.session_state.inputs.get(
                            f"reg_postal_{i}", ""
                        ),
                    )
                    (
                        st.session_state.inputs[f"reg_country_field_tax{i}"],
                        st.session_state.inputs[f"reg_country_{i}"],
                    ) = field_box_template(
                        "COUNTRY",
                        f"COUNTRY_buss_{i}",
                        bpr=25,
                        value=st.session_state.inputs.get(
                            f"reg_country_{i}", ""
                        ),
                    )
                    (
                        st.session_state.inputs[f"reg_region_field_tax{i}"],
                        st.session_state.inputs[f"reg_region_{i}"],
                    ) = field_box_template(
                        "REGION",
                        f"REGION_buss_{i}",
                        bpr=36,
                        value=st.session_state.inputs.get(
                            f"reg_region_{i}", ""
                        ),
                    )
                    (
                        st.session_state.inputs[f"reg_district_field_tax{i}"],
                        st.session_state.inputs[f"reg_district_{i}"],
                    ) = field_box_template(
                        "DISTRICT",
                        f"DISTRICT_buss_{i}",
                        bpr=36,
                        value=st.session_state.inputs.get(
                            f"reg_district_{i}", ""
                        ),
                    )
            st.session_state.page += 1

    elif page == 8 + (5 * st.session_state.part_num):

        # DECLARATION FOR THIRD PARTIES
        if st.session_state.inputs["confirm"] == "NO":
            st.markdown(
                "<h6 style='text-align: center;'>Please fill where Applicant cannot read or write. Details of third party</h6>",
                unsafe_allow_html=True,
            )
            (
                st.session_state.inputs[f"illiterate_h_field"],
                st.session_state.inputs[f"illiterate_h"],
            ) = field_plain_template(
                "Name in full:",
                "resident of .",
                26,
                -240,
                7,
                r_h=0,
                t_rows=1,
                value=st.session_state.inputs.get(f"illiterate_h", ""),
            )
            (
                st.session_state.inputs[f"illiterate_resident_field"],
                st.session_state.inputs[f"illiterate_resident"],
            ) = field_plain_template(
                "Resident:",
                "resident of .",
                16,
                55,
                7,
                r_h=0,
                t_rows=1,
                value=st.session_state.inputs.get(f"illiterate_resident", ""),
            )
            (
                st.session_state.inputs[f"illiterate_language_field"],
                st.session_state.inputs[f"illiterate_language"],
            ) = field_plain_template(
                "Language read in",
                "resident of .",
                45,
                -100,
                19,
                r_h=0,
                t_rows=1,
                value=st.session_state.inputs.get(f"illiterate_language", ""),
            )
            st.session_state.inputs[f"illiterate_field"] = (
                field_plain_template(
                    0, "resident of .", 57, -225, 33, r_h=0, t_rows=1
                )
            )

            # st.markdown("<h6 style='text-align: center;'>THIRD PARTY COMPLETION OF FORM</h6>", unsafe_allow_html=True)
            st.session_state.inputs[f"third_party_field"] = (
                field_plain_template(
                    0,
                    "THIRD PARTY COMPLETION OF FORM",
                    27,
                    -29,
                    c_y=19,
                    t_rows=1,
                    r_h=0,
                )
            )
            (
                st.session_state.inputs[f"tp_tin_field"],
                st.session_state.inputs[f"tp_tin"],
            ) = field_box_template(
                "CELL NUMBER",
                f"TIN-",
                bpr=11,
                x_offset=-123,
                value=st.session_state.inputs.get(f"tp_tin", ""),
            )
            (
                st.session_state.inputs[f"tp_cell_field"],
                st.session_state.inputs[f"tp_cell"],
            ) = field_box_template(
                "CELL NUMBER",
                f"CELL NUMBER_",
                bpr=10,
                x_offset=52,
                value=st.session_state.inputs.get(f"tp_cell", ""),
            )
            st.session_state.inputs[f"tp_date_field"] = TextBox(
                10,
                "DATE",
                x_offset=21,
                row_height=0,
                box_width=10,
                control_x=0.35,
                y_offset=3,
            )
            get_date_input(f"tp_d", f"DATE:")

        # SECTION: DECLARATION FOR TAX FORM
        if st.session_state.inputs["confirm"] == "YES":
            st.markdown(
                "<h6 style='text-align: center;'>DECLARATION</h6>",
                unsafe_allow_html=True,
            )
            st.session_state.inputs[f"declare_field_tax"] = PDFTextFinder(
                "declare that the information", 35, control_x=-192
            )
            st.session_state.inputs[f"declare_date_taxfield"] = TextBox(
                10,
                "DATE",
                x_offset=21,
                row_height=0,
                box_width=10,
                control_x=0.35,
                y_offset=3,
            )
            get_date_input(f"declare_date_tax", f"DATE_")


# FILLING FORMS


def fill_form():
    ###COVER LETTER
    input = st.session_state.inputs
    tin_gha_properties = {
        "boxes_per_row": 11,
        "total_rows": 1,
        "x_offset": 40,
        "y_offset": 10,
    }
    proposed_name_field = TextBox(
        boxes_per_row=24,
        total_rows=2,
        search_text="PROPOSED NAME:",
        x_offset=8,
        y_offset=30,
    )

    try:
        proposed_name = input["proposed_name"]
    except:
        pass

    partner_fields = {}
    partner_names = {}
    tin_nums = {}
    gha_nums = {}

    for i in range(1, input["part_num"] + 1):
        try:
            partner_key = f"PARTNER{i}(Name)"
            partner_fields[partner_key] = PDFTextFinder(
                search_text=partner_key, max_chars_per_row=55, control_x=100
            )
            partner_names[partner_key] = (
                input[f"first_name_part{i}"]
                + " "
                + input[f"middle_name_part{i}"]
                + " "
                + input[f"last_name_part{i}"]
            )

            tin_num_field = TextBox(**tin_gha_properties, search_text="TIN")
            tin_nums[partner_key] = input[f"tin_part{i}"]

            gha_num_field = TextBox(**tin_gha_properties, search_text="GHA")
            gha_nums[partner_key] = input[f"gh_card_part{i}"]
        except:
            pass

    try:
        pdf_file = "backend/partnership/data/COVER NOTE Partnership.pdf"
        doc = fitz.open(pdf_file)
        page = doc[0]
        try:
            proposed_name_field.fill_field(page, proposed_name.upper(), 0)
            n = 0
            for partner_key in partner_names.keys():
                partner_fields[partner_key].fill_field(
                    page, partner_names[partner_key].upper()
                )
                tin_num_field.fill_field(
                    page, tin_nums[partner_key].upper(), n
                )
                gha_num_field.fill_field(
                    page, gha_nums[partner_key].upper(), n
                )
                n += 1
        except:
            pass

        cover_page = "output/cover_page.pdf"
        doc.save(cover_page)
        doc.close()
    except:
        pass

        ############FORM B

    try:
        pdf_file = "backend/partnership/data/Form B.pdf"
        doc = fitz.open(pdf_file)
        page1 = doc[0]
        page2 = doc[1]
        page3 = doc[2]
        page4 = doc[3]
        # AAAAA
        try:
            input["partnership_name_field"].fill_field(
                page1, input["proposed_name"].upper(), 0
            )
        except:
            pass

        # BBBB
        try:
            for item in input["selected_option"][0:3]:
                if item == "Others(Please Specify)":
                    input["other_text"].fill_field(
                        page1, input["other"].upper(), fs=7
                    )
                input["general_nature_field"].fill_option(page1, item)
                input[f"iso_field_{item}"].fill_field(
                    page1, input[f"iso_{item}"].upper()
                )

            # CCCCC
            input["describe_company_field"].fill_field(
                page1, input["describe_company"].upper()
            )
            input["date_commence_field"].fill_field(
                page1, input["date_commence"].strftime("%d-%m-%Y")
            )
        except:
            pass

        # DDDDD
        try:
            input["digital_address_field"].fill_field(
                page1, input["digital_address"].upper(), 0
            )
            input["house_field"].fill_field(
                page1, input["house_flat"].upper(), 0
            )
            input["street_field"].fill_field(page1, input["street"].upper(), 0)
            input["city_field"].fill_field(page1, input["city"].upper(), 0)
            input["district_field"].fill_field(
                page2, input["district"].upper(), 0
            )
            input["region_field"].fill_field(page2, input["region"].upper(), 0)
        except:
            pass

        # DEPENDENT ON YES OR NO
        try:
            if input["user_response"] == "No":
                input["digital_address_field1"].fill_field(
                    page2, input["digital_address1"].upper(), 0
                )
                input["house_field1"].fill_field(
                    page2, input["house_flat1"].upper(), 0
                )
                input["street_field1"].fill_field(
                    page2, input["street1"].upper(), 0
                )
                input["city_field1"].fill_field(
                    page2, input["city1"].upper(), 0
                )
                input["district_field1"].fill_field(
                    page2, input["district1"].upper(), ind=1
                )
                input["region_field1"].fill_field(
                    page2, input["region1"].upper(), 1
                )
            else:
                input["yes"].fill_option(page2, "If Yes")

            # OPTIONAL FIELDS
            if input["other_place"] == "Yes":
                input["digital_address_field2"].fill_field(
                    page2, input["digital_address2"].upper(), 1
                )
                input["house_field2"].fill_field(
                    page2, input["house_flat2"].upper(), 1
                )
                input["street_field2"].fill_field(
                    page2, input["street2"].upper(), 1
                )
                input["city_field2"].fill_field(
                    page2, input["city2"].upper(), 1
                )
                input["district_field2"].fill_field(
                    page2, input["district2"].upper(), 2
                )
                input["region_field2"].fill_field(
                    page2, input["region2"].upper(), 2
                )

            input["c_o_field"].fill_field(page2, input["c_o"].upper(), 0)
            input["type_field"].fill_option(page2, input["type"])
            input["number_field"].fill_field(page2, input["number"], 0)
            input["town_field"].fill_field(page2, input["town"].upper(), 0)
            input["regionx_field"].fill_field(
                page2, input["regionx"].upper(), 1
            )

            # HHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
            input["phone_num_field"].fill_field(page2, input["phone_num"])
            input["phone_num_field2"].fill_field(page2, input["phone_num2"])
            input["mobile_num_field"].fill_field(page2, input["mobile_num"])
            input["mobile_num_field2"].fill_field(page2, input["mobile_num2"])
            input["fax_field"].fill_field(page2, input["fax"])
            input["email_field"].fill_field(page2, input["email"])
            input["website_field"].fill_field(page2, input["website"])
        except Exception as e:
            print(e, "failed")

        # ### Partner(s) Details

        try:
            for i in range(1, 3):
                input[f"tin_field_part{i}"].fill_field(
                    page3 if i == 2 else page2, input[f"tin_part{i}"].upper()
                )
                input[f"gh_card_field_part{i}"].fill_field(
                    page3 if i == 2 else page2,
                    input[f"gh_card_part{i}"].upper(),
                )
                input[f"title_field{i}"].fill_option(
                    page3 if i == 2 else page2, input[f"title{i}"]
                )
                input[f"first_name_field_part{i}"].fill_field(
                    page3 if i == 2 else page2,
                    input[f"first_name_part{i}"].upper(),
                )
                input[f"middle_name_field_part{i}"].fill_field(
                    page3 if i == 2 else page2,
                    input[f"middle_name_part{i}"].upper(),
                )
                input[f"last_name_field_part{i}"].fill_field(
                    page3 if i == 2 else page2,
                    input[f"last_name_part{i}"].upper(),
                )
                input[f"former_name_field_part{i}"].fill_field(
                    page3 if i == 2 else page2,
                    input[f"former_name_part{i}"].upper(),
                )
                input[f"gender_field{i}"].fill_option(
                    page3 if i == 2 else page2, input[f"gender{i}"]
                )
                input[f"dob_field_part{i}"].fill_field(
                    page3 if i == 2 else page2,
                    input[f"dob_part{i}"].strftime("%d%m%Y"),
                )
                input[f"nationality_field_part{i}"].fill_field(
                    page3 if i == 2 else page2,
                    input[f"nationality_part{i}"].upper(),
                )

                input[f"house_no_field_part{i}"].fill_field(
                    page3 if i == 2 else page2,
                    input[f"house_no_part{i}"].upper()
                    + " "
                    + input[f"house_num{i}"].upper(),
                    2 if i == 1 else 0,
                )
                input[f"street_field_part{i}"].fill_field(
                    page3, input[f"street_part{i}"].upper(), 1 if i == 2 else 0
                )
                input[f"address_field_part{i}"].fill_field(
                    page3,
                    input[f"address_part{i}"].upper(),
                    1 if i == 1 else 0,
                )
                input[f"city_field_part{i}"].fill_field(
                    page3, input[f"city_part{i}"].upper(), 1 if i == 2 else 0
                )
                input[f"district_field_part{i}"].fill_field(
                    page3,
                    input[f"district_part{i}"].upper(),
                    1 if i == 2 else 0,
                )
                input[f"region_field_part{i}"].fill_field(
                    page3, input[f"region_part{i}"].upper(), 1 if i == 2 else 0
                )
                input[f"occupation_field_part{i}"].fill_field(
                    page3,
                    input[f"occupation_part{i}"].upper(),
                    1 if i == 2 else 0,
                )
                input[f"mobile1_field_part{i}"].fill_field(
                    page3, input[f"mobile1_part{i}"], 1 if i == 2 else 0
                )
                input[f"mobile2_field_part{i}"].fill_field(
                    page3, input[f"mobile2_part{i}"], 1 if i == 2 else 0
                )
                input[f"email_field_part{i}"].fill_field(
                    page3, input[f"email_part{i}"], 1 if i == 2 else 0
                )
        except Exception as e:
            print(e)
            print("error filling partner info")
        # ####### IIIIIIIIIIIIIII
        try:
            input["asset_field"].fill_field(page3, input["asset"].upper())
            input["date_of_charges_field"].fill_field(
                page3, input["date_of_charges"].strftime("%d%m%Y")
            )
            input["amount_of_charges_field"].fill_field(
                page4, input["amount_of_charges"].upper()
            )

            # JJJJJJJJJJ
            input["revenue_field"].fill_field(page4, input["revenue"].upper())
            input["employees_envisaged_field"].fill_field(
                page4, input["employees_envisaged"].upper()
            )

            # KKKKKKKKKKKKKKKKK
            input["apply_bop_field"].fill_option(page4, input["apply_bop"])
        except:
            pass

        try:
            if input["apply_bop"] == "Already have a BOP":
                input["bop_ref_field"].fill_field(
                    page4, input["bop_ref"].upper()
                )
            # Declaration section

            if st.session_state.inputs["confirm"] == "NO":
                input["illiterate_h_field"].fill_field(
                    page4, input["illiterate_h"].upper()
                )
                input["illiterate_resident_field"].fill_field(
                    page4, input["illiterate_resident"].upper()
                )
                input["illiterate_language_field"].fill_field(
                    page4, input["illiterate_language"].upper()
                )
                illiterate = (
                    input[f"first_name_part1"].upper()
                    + " "
                    + input[f"last_name_part1"].upper()
                    + " "
                    + "and"
                    + " "
                    + input[f"first_name_part2"].upper()
                    + " "
                    + input[f"last_name_part2"].upper()
                )
                input["illiterate_field"].fill_field(page4, illiterate)
        except:
            pass
        formB = "output/formB.pdf"
        doc.save(formB)
        doc.close()

    except:
        pass

    #############FORM SUPPL
    suppl_forms = []
    if input["part_num"] > 2:
        for i in range(3, input["part_num"] + 1):
            try:
                pdf_file = "backend/partnership/data/Form B1-Supplementary Partner Form.pdf"
                doc = fitz.open(pdf_file)
                page = doc[0]
                input[f"tin_field_part{i}"].fill_field(
                    page, input[f"tin_part{i}"].upper()
                )
                input[f"gh_card_field_part{i}"].fill_field(
                    page, input[f"gh_card_part{i}"].upper()
                )
                input[f"title_field{i}"].fill_option(page, input[f"title{i}"])
                input[f"first_name_field_part{i}"].fill_field(
                    page, input[f"first_name_part{i}"].upper()
                )
                input[f"middle_name_field_part{i}"].fill_field(
                    page, input[f"middle_name_part{i}"].upper()
                )
                input[f"last_name_field_part{i}"].fill_field(
                    page, input[f"last_name_part{i}"].upper()
                )
                input[f"former_name_field_part{i}"].fill_field(
                    page, input[f"former_name_part{i}"].upper()
                )
                input[f"gender_field{i}"].fill_option(
                    page, input[f"gender{i}"]
                )
                input[f"dob_field_part{i}"].fill_field(
                    page, input[f"dob_part{i}"].strftime("%d%m%Y")
                )
                input[f"nationality_field_part{i}"].fill_field(
                    page, input[f"nationality_part{i}"].upper()
                )
                input[f"house_no_field_part{i}"].fill_field(
                    page,
                    input[f"house_no_part{i}"].upper()
                    + " "
                    + input[f"house_num{i}"].upper(),
                )
                input[f"street_field_part{i}"].fill_field(
                    page, input[f"street_part{i}"].upper()
                )
                input[f"address_field_part{i}"].fill_field(
                    page, input[f"address_part{i}"].upper()
                )
                input[f"city_field_part{i}"].fill_field(
                    page, input[f"city_part{i}"].upper()
                )
                input[f"district_field_part{i}"].fill_field(
                    page, input[f"district_part{i}"].upper()
                )
                input[f"region_field_part{i}"].fill_field(
                    page, input[f"region_part{i}"].upper()
                )
                input[f"occupation_field_part{i}"].fill_field(
                    page, input[f"occupation_part{i}"].upper()
                )
                input[f"mobile1_field_part{i}"].fill_field(
                    page, input[f"mobile1_part{i}"]
                )
                input[f"mobile2_field_part{i}"].fill_field(
                    page, input[f"mobile2_part{i}"]
                )
                input[f"email_field_part{i}"].fill_field(
                    page, input[f"email_part{i}"]
                )
                if input["confirm"] == "NO":
                    input["illiterate_h_field"].fill_field(
                        page, input["illiterate_h"].upper()
                    )
                    input["illiterate_resident_field"].fill_field(
                        page, input["illiterate_resident"].upper()
                    )
                    input["illiterate_language_field"].fill_field(
                        page, input["illiterate_language"].upper()
                    )
                    illiterate = (
                        input[f"first_name_part{i}"].upper()
                        + " "
                        + input[f"middle_name_part{i}"].upper()
                        + " "
                        + input[f"last_name_part{i}"].upper()
                    )
                    input["illiterate_field"].fill_field(
                        page, illiterate.upper()
                    )

                suppl = f"output/supplementary_partner_{i}.pdf"
                doc.save(suppl)
                doc.close()
                suppl_forms.append(suppl)
            except Exception as e:
                print(e)

    ################## TAX FORM
    tax_forms = []
    for i in range(1, input["part_num"] + 1):

        pdf_file = "backend/partnership/data/Taxpayer-registration-form-individual.pdf"
        doc = fitz.open(pdf_file)
        page = doc[0]
        page1 = doc[1]

        # SECTION 1: PRIOR REGISTRATION
        try:
            st.session_state.inputs[f"tax_payer_field{i}"].fill_option(
                page, st.session_state.inputs[f"tax_payer_{i}"]
            )

            # SECTION 2: INDIVIDUAL CATEGORY
            for category_item in input[f"category_{i}"]:
                input[f"category_field{i}"].fill_option(page, category_item)
        except:
            pass

        try:

            if "Other" in input[f"category_{i}"]:
                input[f"specify_field{i}"].fill_field(
                    page, input[f"specify_{i}"].upper()
                )
                input[f"employer_field{i}"].fill_field(
                    page, input[f"employer_{i}"].upper()
                )

            # SECTION 3: PERSONAL DETAILS
            input[f"title_field_tax{i}"].fill_option(
                page, input[f"title_{i}"].upper()
            )
            if input[f"title_{i}"] == "OTHER":
                input[f"title_field_tax{i}"].fill_option(page, "OTHER", ind=2)
                input[f"specify_title_field_tax{i}"].fill_field(
                    page, input[f"specify_title_{i}"].upper(), 1
                )
            input[f"first_name_field_tax{i}"].fill_field(
                page, input[f"first_name_part{i}"].upper(), fs=8
            )
            input[f"middle_name_field_tax{i}"].fill_field(
                page, input[f"middle_name_part{i}"].upper(), fs=8
            )
            input[f"last_name_field_tax{i}"].fill_field(
                page, input[f"last_name_part{i}"].upper(), fs=8
            )
            input[f"gender_field_tax{i}"].fill_option(
                page, input[f"gender_{i}"].upper()
            )
            input[f"occupation_field_tax{i}"].fill_field(
                page, input[f"occupation_{i}"].upper(), fs=8
            )
            input[f"dob_field_tax{i}"].fill_field(page, input[f"dob_tax{i}"])
            input[f"nationality_field_tax{i}"].fill_field(
                page, input[f"nationality_{i}"].upper(), fs=8
            )
        except:
            pass

        try:
            input[f"previous_name_field_tax{i}"].fill_field(
                page, input[f"previous_name_{i}"].upper(), fs=8
            )

            input[f"marital_field{i}"].fill_option(page, input[f"marital_{i}"])

            input[f"birth_town_field{i}"].fill_field(
                page, input[f"birth_town_{i}"].upper(), fs=8
            )
            input[f"birth_country_field_tax{i}"].fill_field(
                page, input[f"birth_country_{i}"].upper(), fs=8
            )
            input[f"birth_region_field_tax{i}"].fill_field(
                page, input[f"birth_region_{i}"].upper(), fs=8
            )
            input[f"birth_district_field_tax{i}"].fill_field(
                page, input[f"birth_district_{i}"].upper(), fs=8
            )
            input[f"residents_field_tax{i}"].fill_option(
                page, input[f"residents_{i}"].upper(), 1
            )
            input[f"security_field_tax{i}"].fill_field(
                page, input[f"security_{i}"].upper(), fs=8
            )

            for info_item in input[f"info_{i}"]:
                input[f"info_field{i}"].fill_option(page, info_item)

            input[f"mother_maiden_field{i}"].fill_field(
                page, input[f"mother_maiden_{i}"].upper(), fs=8
            )
            input[f"mother_first_field{i}"].fill_field(
                page, input[f"mother_first_{i}"].upper(), 1, fs=8
            )

            # SECTION 4: TAX REGISTRATION INFORMATION
            input[f"tax_office_field{i}"].fill_field(
                page, input[f"tax_office_{i}"].upper(), fs=8
            )
            input[f"old_tin_field{i}"].fill_field(
                page, input[f"old_tin_{i}"].upper()
            )
            input[f"tax_fee_field{i}"].fill_field(
                page, input[f"tax_fee_{i}"].upper(), fs=8
            )

            # SECTION 5: IDENTIFICATION INFORMATION
            input[f"id_type_field{i}"].fill_option(page, input[f"id_type_{i}"])
            input[f"id_num_field{i}"].fill_field(
                page, input[f"id_num_{i}"].upper(), fs=8
            )
            input[f"issue_date_field{i}"].fill_field(
                page, input[f"issue_date_{i}"].strftime("%d-%m-%Y")
            )
            input[f"expiry_date_field{i}"].fill_field(
                page, input[f"expiry_date_{i}"].strftime("%d-%m-%Y")
            )
            input[f"place_of_issue_field{i}"].fill_field(
                page, input[f"place_of_issue_{i}"].upper(), fs=8
            )
            input[f"country_of_issue_field{i}"].fill_field(
                page, input[f"country_of_issue_{i}"].upper(), fs=8
            )
        except:
            pass
        try:
            # SECTION 6: RESIDENTIAL ADDRESS
            input[f"house_num_field_tax{i}"].fill_field(
                page, input[f"house_num{i}"].upper(), fs=8
            )
            input[f"building_name_field_tax{i}"].fill_field(
                page, input[f"house_no_part{i}"].upper(), fs=8
            )
            input[f"landmark_field_tax{i}"].fill_field(
                page, input[f"landmark_{i}"].upper(), fs=8
            )
            input[f"town_city_field_tax{i}"].fill_field(
                page, input[f"town_city_{i}"].upper(), fs=8
            )
            input[f"location_area_field_tax{i}"].fill_field(
                page, input[f"location_area_{i}"].upper(), fs=8
            )
            input[f"postal_field_tax{i}"].fill_field(
                page, input[f"postal_{i}"].upper(), fs=8
            )
            input[f"country_field_tax{i}"].fill_field(
                page, input[f"country_{i}"].upper(), 1, fs=8
            )
            input[f"region_field_tax{i}"].fill_field(
                page, input[f"region_{i}"].upper(), 1, fs=8
            )
            input[f"district_field_tax{i}"].fill_field(
                page, input[f"district_{i}"].upper(), 1, fs=8
            )
        except Exception as e:
            print(e)

        # SECTION 7: POSTAL ADDRESS

        try:
            if input[f"postal_address_tax{i}"] == "YES":
                input[f"postal_address_taxfield{i}"].fill_option(
                    page1, "TICK IF SAME AS RESIDENTIAL ADDRESS"
                )
            else:
                input[f"c_o_field_tax{i}"].fill_field(page1, input[f"c_o_{i}"])
                if "POSTAL NUMBER" in input[f"postal_type_tax{i}"]:
                    input[f"postal_num_taxfield{i}"].fill_field(
                        page1, input[f"postal_num_tax{i}"].upper(), fs=8
                    )
                input[f"box_region_field_tax{i}"].fill_field(
                    page1, input[f"box_region_{i}"].upper(), fs=8
                )
                input[f"box_town_field{i}"].fill_field(
                    page1, input[f"box_town_{i}"].upper(), fs=8
                )
                input[f"box_location_field{i}"].fill_field(
                    page1, input[f"box_location_{i}"].upper(), fs=8
                )

            # SECTION 8: CONTACT METHOD
            input[f"phone_num_taxfield{i}"].fill_field(
                page1, input[f"phone_num_tax{i}"].upper(), fs=9
            )
            input[f"mobile_num_taxfield{i}"].fill_field(
                page1, input[f"mobile_num_tax{i}"].upper(), fs=9
            )
            input[f"fax_num_taxfield{i}"].fill_field(
                page1, input[f"fax_num_tax{i}"].upper(), fs=9
            )
            input[f"email_taxfield{i}"].fill_field(
                page1, input[f"email_tax{i}"], fs=8
            )
            input[f"website_taxfield{i}"].fill_field(
                page1, input[f"website_tax{i}"], fs=8
            )
            new = ["LETTER", "EMAIL"]
            input[f"contact_taxfield{i}"].fill_option(
                page1,
                input[f"contact_tax{i}"],
                0 if input[f"contact_tax{i}"] in new else 1,
            )

        # SECTION 9: BUSINESS ( COMPLETE THIS SECTION IF YOU ARE SELF EMPLOYED)
        except:
            pass

        try:
            if input[f"self_employed_{i}"] == "YES":
                input[f"business_nature_taxfield{i}"].fill_field(
                    page1, input[f"business_nature_tax{i}"].upper(), fs=8
                )
                input[f"annual_field{i}"].fill_field(
                    page1, input[f"annual_{i}"].upper(), fs=9
                )
                input[f"num_employee_field{i}"].fill_field(
                    page1, input[f"num_employee_{i}"].upper(), fs=9
                )

                if input[f"registered_{i}"] == "YES":
                    input[f"registered_field{i}"].fill_option(
                        page1, input[f"registered_{i}"]
                    )
                    input[f"reg_buss_field{i}"].fill_field(
                        page1, input[f"reg_buss_{i}"].upper(), 1, fs=8
                    )
                    input[f"reg_tin_field{i}"].fill_field(
                        page1, input[f"reg_tin_{i}"]
                    )
                    input[f"reg_rgd_field{i}"].fill_field(
                        page1, input[f"reg_rgd_{i}"]
                    )
                else:
                    input[f"registered_field{i}"].fill_option(
                        page1, input[f"registered_{i}"], 2
                    )

        except:
            pass

        try:
            input[f"reg_house_field{i}"].fill_field(
                page1, input[f"reg_house_{i}"].upper(), fs=8
            )
            input[f"reg_build_field{i}"].fill_field(
                page1, input[f"reg_build_{i}"].upper(), fs=8
            )
            input[f"reg_street_field{i}"].fill_field(
                page1, input[f"reg_street_{i}"].upper(), fs=8
            )
            input[f"reg_town_field{i}"].fill_field(
                page1, input[f"reg_town_{i}"].upper(), fs=8
            )
            input[f"reg_location_field{i}"].fill_field(
                page1, input[f"reg_location_{i}"].upper(), fs=8
            )
            input[f"reg_postal_field_tax{i}"].fill_field(
                page1, input[f"reg_postal_{i}"].upper(), fs=8
            )
            input[f"reg_country_field_tax{i}"].fill_field(
                page1, input[f"reg_country_{i}"].upper(), fs=8
            )
            input[f"reg_region_field_tax{i}"].fill_field(
                page1, input[f"reg_region_{i}"].upper(), 1, fs=8
            )
            input[f"reg_district_field_tax{i}"].fill_field(
                page1, input[f"reg_district_{i}"].upper(), fs=8
            )
        except:
            pass

        # SECTION 10: DECLARATION
        try:
            if input["confirm"] == "YES":

                input[f"declare_field_tax"].fill_field(
                    page1, input[f"declare_name{i}"].upper(), 1, fs=8
                )
                input[f"declare_date_taxfield"].fill_field(
                    page1, input[f"declare_date_tax"].strftime("%d-%m-%Y")
                )

            # SECTION 11: THIRD PARTY COMPLETION OF FORM
            if input["confirm"] == "NO":
                input[f"third_party_field"].fill_field(
                    page1, input[f"illiterate_h"].upper()
                )
                input[f"tp_date_field"].fill_field(
                    page1, input[f"tp_d"].strftime("%d-%m-%Y"), 1
                )
                input[f"tp_tin_field"].fill_field(
                    page1, input[f"tp_tin"].upper()
                )
                input[f"tp_cell_field"].fill_field(
                    page1, input[f"tp_cell"].upper()
                )

            tax_file = f"output/tax_form{i}.pdf"
            doc.save(tax_file)
            doc.close()

            tax_forms.append(tax_file)
        except Exception as e:
            print(f"Exception type: {type(e).__name__}, {e}")

    return cover_page, formB, suppl_forms, tax_forms
