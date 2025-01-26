import streamlit as st 
import fitz
from ..shapes import TextBox
from ..shapes import PDFTextFinder 
from ..shapes import PDFOptionField
from datetime import  timedelta, datetime
import pandas as pd
       



isic_data = { "Legal": { "Legal representation": "6910", "Notary services": "6910", "Patent law services": "6910", "Advice on labour disputes": "6910", "Drafting of legal documents": "6910", "Legal consultancy and advisory": "6910", "Others":None},
                        "Estate/Housing": { "Real estate activities with own or leased property": "6810","Real estate management on a fee basis": "6820", "Appraisal services for real estate": "6820", "Activities of real estate agents and brokers": "6820", "Operation of apartment buildings": "6810", "Development of building projects": "6810", "Subdividing real estate into lots": "6810", "Others":None },
                        "Media": { "Publishing of books": "5811", "Publishing of newspapers": "5813", "Television broadcasting": "6020", "Radio broadcasting": "6010", "Online publishing of content": "5819", "Motion picture production": "5911", "Video post-production activities": "5912", "Others":None },
                        "Transport/Aerospace": { "Passenger air transport": "5110", "Freight air transport": "5120", "Urban and suburban passenger land transport": "4921", "Freight transport by road": "4923", "Transport via pipelines": "4930", "Operation of bus stations": "5221", "Airport operations": "5223",  "Others":None  }, 
                        "Utilities": { "Electric power generation, transmission and distribution": "3510", "Water collection, treatment and supply": "3600", "Sewage treatment and disposal": "3700", "Waste collection and management": "3811", "Recycling of materials": "3830", "Gas distribution through mains": "3520",  "Others":None  },
                        "Education": { "Primary education": "8510", "General secondary education": "8521", "Higher education": "8530", "Technical and vocational education": "8522", "Educational support activities": "8550", "Adult literacy programs": "8510",  "Others":None  },
                        "Shipping & Port": { "Sea and coastal passenger water transport": "5011", "Sea and coastal freight water transport": "5012", "Inland passenger water transport": "5021", "Cargo handling": "5224", "Port and harbor operation services": "5222", "Navigation and pilotage activities": "5222",  "Others":None  }, 
                        "Tourism": { "Travel agency activities": "7911", "Tour operator activities": "7912", "Activities of tourist guides": "7990", "Reservation services": "7990", "Tourism promotion activities": "7990", "Operation of tourist information offices": "7990",  "Others":None  }, 
                        "Quarry / Mining": { "Stone quarrying": "0810", "Mining of metal ores": "0729", "Extraction of crude petroleum": "0610", "Mining support services": "0990", "Mining of non-ferrous metal ores": "0723",  "Others":None  }, 
                        "Hospitality": { "Hotel and accommodation services": "5510", "Food and beverage serving activities": "5610", "Event catering": "5621", "Beverage serving activities": "5630", "Camping and recreational vehicle parks": "5520",  "Others":None  }, 
                        "Fashion/Beautification": { "Hairdressing and beauty treatment": "9602", "Fashion design activities": "7410", "Manufacture of wearing apparel": "1410", "Jewelry and accessory design": "3211", "Textile and fabric design": "7410", "Spa and wellness activities": "9604",  "Others":None  }, 
                        "Insurance": { "Life insurance": "6511", "Non-life insurance": "6512", "Reinsurance": "6520", "Pension funding": "6530", "Insurance brokerage services": "6622",  "Risk and damage evaluation": "6621" },
                        "Entertainment": { "Motion picture production": "5911", "Sound recording activities": "5920", "Performing arts activities": "9000", "Operation of sports facilities": "9311", "Amusement parks and theme parks": "9321", "Gambling and betting activities": "9200",  "Others":None  }, 
                        "Health Care": { "General medical practice activities": "8620", "Specialized medical practice activities": "8620", "Hospital activities": "8610", "Traditional herbal medicine activities": "8630", "Medical laboratory services": "8690", "Ambulance services": "8690",  "Others":None  }, 
                        "Refinery of Minerals": { "Petroleum refining": "1920", "Processing of mineral ores": "0729", "Manufacture of basic metals": "2410", "Alumina and aluminum production": "2420",  "Others":None  }, 
                        "Agriculture": { "Growing of crops": "0111", "Animal farming": "0141", "Forestry activities": "0210", "Fishing and aquaculture": "0311", "Agricultural support services": "0161", "Post-harvest crop activities": "0163",  "Others":None  }, 
                        "Food Industry": { "Processing and preserving of meat": "1010", "Manufacture of dairy products": "1050", "Manufacture of bakery products": "1071", "Production of beverages": "1104", "Processing of edible oils": "1040", "Manufacture of sugar": "1072",  "Others":None  }, 
                        "Securities/Brokers": { "Stock brokerage services": "6612", "Investment advisory services": "6619", "Financial market administration": "6611", "Activities of forex bureaux": "6612", "Security dealing on own account": "6499",  "Others":None  }, 
                        "Oil and Gas": { "Extraction of crude petroleum": "0610", "Natural gas extraction": "0620", "Support services for oil and gas": "0910", "Oil and gas pipeline transport": "4930", "Manufacture of refined petroleum products": "1920",  "Others":None  }, 
                        "Manufacturing": { "Manufacture of textiles": "1310", "Manufacture of pharmaceuticals": "2100", "Manufacture of chemicals": "2011", "Manufacture of furniture": "3100", "Manufacture of machinery": "2810", "Manufacture of rubber products": "2211",  "Others":None  }, 
                        "Commerce/Trading": { "Wholesale of consumer goods": "4630", "Retail sale in non-specialized stores": "4719", "Online retail sales": "4791", "Auctioning of goods": "4774", "Automobile trading": "4510",  "Others":None  },
                        "Construction": { "General construction of buildings": "4100", "Civil engineering projects": "4210", "Electrical installation": "4321", "Plumbing and HVAC installation": "4322", "Demolition and site preparation": "4310",  "Others":None  }, 
                        "Pharmaceutical": { "Manufacture of pharmaceuticals": "2100", "Retail sale of pharmaceuticals": "4772", "Wholesale of pharmaceutical goods": "4649", "Biotechnology research and development": "7210", "Medical device manufacturing": "3250",  "Others":None  }, 
                        "Banking and Finance": { "Commercial banking": "6419", "Credit unions": "6419", "Mortgage lending": "6492", "Financial leasing": "6491", "Factoring services": "6499",  "Others":None  },
                        "Telecom/ICT": { "Wired telecommunications activities": "6110", "Wireless telecommunications activities": "6120", "Internet service provision": "6311", "Computer programming activities": "6201", "Data processing and hosting": "6311",  "Others":None },
                        "Security": { "Private security activities": "8010", "Investigation services": "8030", "Security systems services": "8020", "Bodyguard services": "8010", "Armored car services": "8010",  "Others":None },
                        "Sanitation": {"Waste collection": "3811","Sewage treatment": "3700","Street cleaning": "8129","Disinfection services": "8129","Recycling services": "3830",  "Others":None },
                        "Others(Please Specify)":None}


def get_date_input(key, label, min_value= datetime.now()-timedelta(days=100*365), default_value=datetime.now()):
    min_value = min_value.date()
    default_value = default_value.date()

    if key not in st.session_state.inputs_limitedc:
        st.session_state.inputs_limitedc[key] = default_value

    date_value = st.date_input(label, min_value=min_value, value=st.session_state.inputs_limitedc[key])
    if date_value < min_value or date_value > datetime.now().date():
        date_value = datetime.now().date()

    if date_value != st.session_state.inputs_limitedc[key]:
        st.session_state.inputs_limitedc[key] = date_value


def boxes(stext, label='', bpr=17,t_row=1, c_x=133, c_y=5, find='', control=1.4):
    instance_field =TextBox(
        boxes_per_row=bpr,
        search_text=stext,
        total_rows=t_row,
        x_offset=c_x,
        y_offset=c_y,
        box_width=17,
        row_height=14.8,
        control_x=control
    )
    if label != '':
        instance =  st.text_input(label, max_chars=instance_field.total_boxes, value=st.session_state.inputs_limitedc.get(find, ""))
        return instance_field, instance
    return instance_field 


def field_box_template(search_text, label='',bpr=38, x_offset=94,y_offset=3, value=''):
            instance_field = TextBox(
                bpr,
                search_text,
                x_offset = x_offset,
                y_offset = y_offset,
                box_width=10,
                row_height=0, 
                control_x=0.35
                )
            if label:
                    instance = st.text_input(f"{label}:", max_chars=instance_field.total_boxes, value=value)     
                    return instance_field, instance
            
            return instance_field
        

def field_plain_template(label, search_text, maxi, c_x, c_y=8, r_h=15, t_rows=2,value=''):
    instance_field = PDFTextFinder(
        search_text,
        maxi,
        control_x=c_x,
        control_y=c_y,
        row_height=r_h,
        max_rows=t_rows 
    )
    if label == 0:
        return instance_field
    instance = st.text_input(f"{label}", max_chars=instance_field.total_space, value=value)
    return instance_field, instance 


options_d ={
    "box_width":18,
    "control_x":0.5
    
    }        
def field_D_template(search_text, label='', row_height=0, total_rows=1, y_offset=5,x_offset=134, boxes_per_row=17, value=''):
    instance_field = TextBox(
            boxes_per_row,
            search_text=search_text,
            row_height = row_height,
            total_rows = total_rows,
            y_offset=y_offset,
            x_offset=x_offset,
            **options_d
    )
    if label:
        instance = st.text_input(f"{label}:", max_chars=instance_field.total_boxes, value=value)
        return instance_field, instance
    return instance_field


def field_option_template(options='', label='', control_x=11, control_y=4, value=''):
    instance_field = PDFOptionField(control_x, control_y)
    
    if label:
        instance = st.radio(label, options,horizontal=True, index=options.index(value)) 
        return instance_field, instance
        
    return instance_field

def field_multi_options(options, label, control_x=11, control_y=4, value=[]):
    instance_field = PDFOptionField(
        control_x,
        control_y
    )
    instance = st.multiselect(f"{label}", options, default=value)
    return instance_field, instance
    

option_yesno=["NO", "YES"]

def address(n, country="no", p = 1,split=False,fill=False,form3=False,page=0,ind=0, tax=False, ind1=1):
    if not fill:
        st.session_state.inputs_limitedc[f"digital_address_field{n}"], st.session_state.inputs_limitedc[f"digital_address{n}"]= boxes("Digital Address*",label=f"Digital Address*{p*' '}", find=f"digital_address{n}")
        if split:
            st.session_state.inputs_limitedc[f"house_num_field{n}"], st.session_state.inputs_limitedc[f"house_num{n}"]= boxes("House/Building/Flat",label=f"House No.*  (this is the number of the house on the street. For example for 250 Ako Adjei Street the house number is 250 and Ako Adjei street is the street name.){p*' '}", find=f"house_num{n}", bpr=9)
            st.session_state.inputs_limitedc[f"house_address_field{n}"], st.session_state.inputs_limitedc[f"house_address{n}"]= boxes("House/Building/Flat",label=f"House/Building/Flat*(Name)/LMB  (Conspicuously and recognizable labelled building, for example VAT HOUSE.){p*' '}", find=f"house_address{n}", t_row=2)
        else:
            st.session_state.inputs_limitedc[f"house_address_field{n}"], st.session_state.inputs_limitedc[f"house_address{n}"]= boxes("House/Building/Flat",label=f"House/Building/Flat*(Name or House No.)/LMB{p*' '}", find=f"house_address{n}", t_row=2)
        st.session_state.inputs_limitedc[f"street_name_field{n}"], st.session_state.inputs_limitedc[f"street_name{n}"]= boxes("Street Name*",label=f"Street Name*{p*' '}", find=f"street_name{n}")
        if n > (5+2* st.session_state.inputs_limitedc['dir_num']) :
            st.session_state.inputs_limitedc[f"city_field{n}"], st.session_state.inputs_limitedc[f"city{n}"]= boxes("City*",label=f"City of work*{p*' '}", find=f"city{n}")
            st.session_state.inputs_limitedc[f"district_field{n}"], st.session_state.inputs_limitedc[f"district{n}"]= boxes("District",label=f"District of work*{p*' '}", find=f"district{n}")
            st.session_state.inputs_limitedc[f"region_field{n}"], st.session_state.inputs_limitedc[f"region{n}"]= boxes("Region",label=f"Region of work*{p*' '}", find=f"region{n}")
        else:
            st.session_state.inputs_limitedc[f"city_field{n}"], st.session_state.inputs_limitedc[f"city{n}"]= boxes("City*",label=f"City*{p*' '}", find=f"city{n}")
            st.session_state.inputs_limitedc[f"district_field{n}"], st.session_state.inputs_limitedc[f"district{n}"]= boxes("District",label=f"District*{p*' '}", find=f"district{n}")
            st.session_state.inputs_limitedc[f"region_field{n}"], st.session_state.inputs_limitedc[f"region{n}"]= boxes("Region",label=f"Region*{p*' '}", find=f"region{n}")
            

        if country =="yes":
            st.session_state.inputs_limitedc[f"country_field{n}"], st.session_state.inputs_limitedc[f"country{n}"]= boxes("Country",label=f"Country*{p*' '}", find=f"country{n}")
        if tax:
            st.session_state.inputs_limitedc[f"location_area_field_tax{n}"],st.session_state.inputs_limitedc[f'location_area_{n}'] = field_box_template("LOCATION / AREA", f"Location / Area - Location / area - Name of location - suburb and description of area within a city or town. For example DANSOMAN (AKOKOFOTO) or NORTH KANESHIE (LAST STOP)", value=st.session_state.inputs_limitedc.get(f"location_area_{n}",''))
            st.session_state.inputs_limitedc[f"postal_field_tax{n}"],st.session_state.inputs_limitedc[f'postal_{n}'] = field_box_template("POSTAL CODE", f"Postal Code (applicable to only applicants with foreign postal addresses.)", value=st.session_state.inputs_limitedc.get(f'postal_{n}',''))

            # st.session_state.inputs_limitedc[f'postal_number'].upper() if st.session_state.inputs_limitedc[f'type']=='P O Box' else ''


    else:
        if form3:
            if country=='yes':
                st.session_state.inputs_limitedc[f"country_field{n}"].fill_field(page,st.session_state.inputs_limitedc[f"country{n}"].upper(),ind=ind)

            if split:
                house_address = st.session_state.inputs_limitedc[f"house_num{n}"] +  st.session_state.inputs_limitedc[f"house_address{n}"]
                st.session_state.inputs_limitedc[f"house_address_field{n}"].fill_field(page, house_address.upper(), ind1)             

                  
            if n ==1:
                st.session_state.inputs_limitedc[f"digital_address_field{n}"]= boxes("Per section 13 (2) (d) o",c_x=-309)
                st.session_state.inputs_limitedc[f"house_address_field{n}"]= boxes("Per section 13 (2) (d) o",c_x=-309,c_y=20)
                st.session_state.inputs_limitedc[f"street_name_field{n}"]= boxes("Per section 13 (2) (d) o",c_x=-309,c_y=64)
                st.session_state.inputs_limitedc[f"city_field{n}"]= boxes("Per section 13 (2) (d) o",c_x=-309,c_y=91.5)
                st.session_state.inputs_limitedc[f"district_field{n}"]= boxes("Per section 13 (2) (d) o",c_x=-309,c_y=106)
                st.session_state.inputs_limitedc[f"region_field{n}"]= boxes("Per section 13 (2) (d) o",c_x=-309, c_y=121)
            if n==2:
                st.session_state.inputs_limitedc[f"street_name_field{n}"]= boxes("Per section 13 (2) (d) o",c_x=-309,c_y=239)

            if n==3:
                st.session_state.inputs_limitedc[f"digital_address_field{n}"]= boxes("Per section 13 (2) (d) o",c_x=-309,c_y=326)
                st.session_state.inputs_limitedc[f"house_address_field{n}"]= boxes("Per section 13 (2) (d) o",c_x=-309,c_y=340)
                st.session_state.inputs_limitedc[f"street_name_field{n}"]= boxes("Per section 13 (2) (d) o",c_x=-309,c_y=368)
                st.session_state.inputs_limitedc[f"city_field{n}"]= boxes("Per section 13 (2) (d) o",c_x=-309,c_y=398)
                st.session_state.inputs_limitedc[f"district_field{n}"]= boxes("Per section 13 (2) (d) o",c_x=-309,c_y=412)
                st.session_state.inputs_limitedc[f"region_field{n}"]= boxes("Per section 13 (2) (d) o",c_x=-309, c_y=426)
          

            if n==4:
                st.session_state.inputs_limitedc[f"house_address_field{n}"]= boxes("House/Building/Flat",c_y=472)
                st.session_state.inputs_limitedc[f"street_name_field{n}"] = boxes("Street Name",c_y=455)
                st.session_state.inputs_limitedc[f"district_field{n}"] = boxes("District",c_y=440)
                st.session_state.inputs_limitedc[f"region_field{n}"] = boxes("Region",c_y=136)
    


           
            st.session_state.inputs_limitedc[f"digital_address_field{n}"].fill_field(page,st.session_state.inputs_limitedc[f"digital_address{n}"].upper(),ind=ind)  
            if not split:          
                st.session_state.inputs_limitedc[f"house_address_field{n}"].fill_field(page, st.session_state.inputs_limitedc[f"house_address{n}"].upper(),ind=ind)
            st.session_state.inputs_limitedc[f"street_name_field{n}"].fill_field(page,st.session_state.inputs_limitedc[f"street_name{n}"].upper(),ind=ind)
            st.session_state.inputs_limitedc[f"city_field{n}"].fill_field(page,st.session_state.inputs_limitedc[f"city{n}"].upper(),ind=ind)
            st.session_state.inputs_limitedc[f"district_field{n}"].fill_field(page,st.session_state.inputs_limitedc[f"district{n}"].upper(),ind=ind)
            st.session_state.inputs_limitedc[f"region_field{n}"].fill_field(page,st.session_state.inputs_limitedc[f"region{n}"].upper(),ind=ind)    

        

def consent(n=1):
    st.write("A person shall not be appointed a director if")
    st.session_state.inputs_limitedc[f"consent_fieldi{n}"], st.session_state.inputs_limitedc[f"consenti{n}"] = PDFOptionField(control_x=-40, control_y=6), st.radio(f"i.That person within the preceding five years of the application for incorporation has been a director or senior manager of a Company that has become insolvent.{n*' '}", option_yesno, horizontal=True, index=option_yesno.index(st.session_state.inputs_limitedc.get(f"consenti{n}",option_yesno[0])))
    st.session_state.inputs_limitedc[f"consent_fieldii{n}"], st.session_state.inputs_limitedc[f"consentii{n}"] = PDFOptionField(control_x=-40, control_y=6),st.radio(f"ii. Convicted of a criminal offence involving fraud or dishonesty.{n*' '}", option_yesno, horizontal=True, index=option_yesno.index(st.session_state.inputs_limitedc.get(f"consentii{n}",option_yesno[0])))
    st.session_state.inputs_limitedc[f"consent_fieldiii{n}"], st.session_state.inputs_limitedc[f"consentiii{n}"] = PDFOptionField(control_x=-40, control_y=6),st.radio(f"iii. Convicted of a criminal offence relating to the promotion, incorporation or management of a company that has become insolvent.{n*' '}.", option_yesno, horizontal=True, index=option_yesno.index(st.session_state.inputs_limitedc.get(f"consentiii{n}",option_yesno[0])))






def personal(pn,n=1,fill=False, form3=False, place_ob=True, page=0, ind=0, dob=True, dir=False, add_dir=False, add_sub=0, sec=False, trust=False):
    if not fill:
        st.session_state.inputs_limitedc[f"title_field{n}"]= PDFOptionField(control_x=-30, control_y=5)
        st.session_state.inputs_limitedc[f"first_name_field{n}"]= boxes("First Name*",label='')
        st.session_state.inputs_limitedc[f"middle_name_field{n}"]= boxes("Middle Name",label='')
        st.session_state.inputs_limitedc[f"last_name_field{n}"]= boxes("Last Name*",label='')
        st.session_state.inputs_limitedc[f"former_name_field{n}"], st.session_state.inputs_limitedc[f"former_name{n}"]= boxes("Any Former Name",label=f"Any former name aside names given earlier{n*' '}", find=f"former_name{n}")
        option_gender = [" Male ", "Female"]
        st.session_state.inputs_limitedc[f"gender{n}"] = " Male "
        st.session_state.inputs_limitedc[f"gender_field{n}"], st.session_state.inputs_limitedc[f"gender{n}"] = PDFOptionField(control_x=-33, control_y=5), st.radio(f"Choose gender{n*' '}", option_gender, horizontal=True, index=option_gender.index(st.session_state.inputs_limitedc.get(f"gender{n}",option_gender[0])))
        get_date_input(f"dob{n}", "Date of Birth*")
        st.session_state.inputs_limitedc[f"dob_field{n}"]= boxes("Date of Birth*")
        st.session_state.inputs_limitedc[f"pob_field{n}"]= boxes("Place of Birth*",label="")
        st.session_state.inputs_limitedc[f"nationality_field{n}"], st.session_state.inputs_limitedc[f"nationality{n}"]= boxes("Nationality*",label=f"Nationality*{n*' '}", find=f"nationality{n}")
        st.session_state.inputs_limitedc[f"occupation_field{n}"], st.session_state.inputs_limitedc[f"occupation{n}"]= boxes("Occupation*",label=f"Occupation*{n*' '}", find=f"occupation{n}")
        option_marital = ["SINGLE", "MARRIED", "DIVORCED", "SEPARATED", "WIDOWED"]
        st.session_state.inputs_limitedc[f'marital_field{n}'], st.session_state.inputs_limitedc[f'marital_{n}'] = PDFOptionField(control_x=11, control_y=4), st.radio("Choose marital status", option_marital, horizontal=True, index=option_marital.index(st.session_state.inputs_limitedc.get(f'marital_{n}',option_marital[0])))
        st.session_state.inputs_limitedc[f"birth_country_field_tax{n}"], st.session_state.inputs_limitedc[f'birth_country_{n}'] = field_box_template("BIRTH COUNTRY", f"BIRTH COUNTRY{' ' *n}",  value=st.session_state.inputs_limitedc.get(f'birth_country_{n}',''))
        st.session_state.inputs_limitedc[f"birth_town_field{n}"], st.session_state.inputs_limitedc[f'birth_town_{n}'] = field_box_template("BIRTH TOWN", f"BIRTH TOWN", value=st.session_state.inputs_limitedc.get(f'birth_town_{n}',''))
        st.session_state.inputs_limitedc[f"birth_region_field_tax{n}"], st.session_state.inputs_limitedc[f'birth_region_{n}'] =field_box_template("BIRTH REGION", f"BIRTH REGION{' ' *n}",value=st.session_state.inputs_limitedc.get(f'birth_region_{n}','')) 
        st.session_state.inputs_limitedc[f"birth_district_field_tax{n}"], st.session_state.inputs_limitedc[f'birth_district_{n}'] = field_box_template("BIRTH DISTRICT", f"BIRTH DISTRICT{n*' '}",value=st.session_state.inputs_limitedc.get(f'birth_district_{n}',''))
        # st.session_state.inputs_limitedc[f"postal_zip_field{n}"], st.session_state.inputs_limitedc[f"postal_zip{n}"]= boxes("Postal/Zip code", "Postal/Zip code", find=st.session_state.inputs_limitedc.get(f"postal_zip{n}"))

            
        
    else:
        if form3:
            if dir:
                st.session_state.inputs_limitedc[f"title_field{n}"].fill_option(page, st.session_state.inputs_limitedc[f"title{pn}"], partner=False, new_x=-40 if st.session_state.inputs_limitedc[f"title{pn}"]==' Mrs ' or st.session_state.inputs_limitedc[f"title{pn}"]==' Miss ' else 0)
            elif add_dir:
                st.session_state.inputs_limitedc[f"title_field{n}"].fill_option(page, st.session_state.inputs_limitedc[f"title{pn}"], partner=False, new_x=-50 if st.session_state.inputs_limitedc[f"title{pn}"]==' Mrs ' else 0)
            elif add_sub:
                st.session_state.inputs_limitedc[f"title_field{n}"].fill_option(page, st.session_state.inputs_limitedc[f"title{pn}"], partner=False, ind=1 if st.session_state.inputs_limitedc[f"title{pn}"]==' Mrs ' else 0)
            elif sec:
                if st.session_state.inputs_limitedc[f"title{pn}"]==' Miss ':
                    st.session_state.inputs_limitedc[f"title_field{n}"].fill_option(page, 'Miss', partner=False, new_x=-40)
                elif st.session_state.inputs_limitedc[f"title{pn}"]==' Ms ':
                    st.session_state.inputs_limitedc[f"title_field{n}"].fill_option(page, 'Ms', partner=False)         
                elif st.session_state.inputs_limitedc[f"title{pn}"]==' Mrs ':
                    st.session_state.inputs_limitedc[f"title_field{n}"].fill_option(page, st.session_state.inputs_limitedc[f"title{pn}"], partner=False, new_x=-40)
                else:
                    st.session_state.inputs_limitedc[f"title_field{n}"].fill_option(page, st.session_state.inputs_limitedc[f"title{pn}"], partner=False)
            elif trust:
                if st.session_state.inputs_limitedc[f"title{pn}"]==' Ms ':
                    st.session_state.inputs_limitedc[f"title_field{n}"].fill_option(page, 'Ms', partner=False)
                else:
                    st.session_state.inputs_limitedc[f"title_field{n}"].fill_option(page, st.session_state.inputs_limitedc[f"title{pn}"], partner=False)
 
            else:
                st.session_state.inputs_limitedc[f"title_field{n}"].fill_option(page, st.session_state.inputs_limitedc[f"title{pn}"], partner=False)

            st.session_state.inputs_limitedc[f"first_name_field{n}"].fill_field(page, st.session_state.inputs_limitedc[f"first_name{pn}"].upper())
            st.session_state.inputs_limitedc[f"middle_name_field{n}"].fill_field(page, st.session_state.inputs_limitedc[f"middle_name{pn}"].upper())
            st.session_state.inputs_limitedc[f"last_name_field{n}"].fill_field(page, st.session_state.inputs_limitedc[f"last_name{pn}"].upper())
            st.session_state.inputs_limitedc[f"former_name_field{n}"].fill_field(page, st.session_state.inputs_limitedc[f"former_name{n}"].upper())
            st.session_state.inputs_limitedc[f"gender_field{n}"].fill_option(page, st.session_state.inputs_limitedc[f"gender{n}"], new_x=-48 if st.session_state.inputs_limitedc[f"gender{n}"]=='Female' else 0,partner=False)
            if dob:
                st.session_state.inputs_limitedc[f"dob_field{n}"].fill_field(page,st.session_state.inputs_limitedc[f"dob{n}"].strftime("%d%m%Y"), ind)
            if place_ob:
                st.session_state.inputs_limitedc[f"pob_field{n}"].fill_field(page, st.session_state.inputs_limitedc[f"birth_town_{n}"].upper(), ind)
            st.session_state.inputs_limitedc[f"nationality_field{n}"].fill_field(page, st.session_state.inputs_limitedc[f"nationality{n}"].upper())
            st.session_state.inputs_limitedc[f"occupation_field{n}"].fill_field(page, st.session_state.inputs_limitedc[f"occupation{n}"].upper())
            # st.session_state.inputs_limitedc[f"postal_zip_field{n}"].fill_field(page,f"postal_zip{n}")


            
def contact(n, fill=False, form3=False, page=0, ind=0):
    if not fill:
        st.session_state.inputs_limitedc[f"mobile_num_field{n}"], st.session_state.inputs_limitedc[f"mobile_num{n}"]= boxes("Mobile No 1*",label=f"Mobile No 1*{n*' '}", find=f"mobile_num{n}")
        st.session_state.inputs_limitedc[f"mobile_numb_field{n}"], st.session_state.inputs_limitedc[f"mobile_numb{n}"]= boxes("Mobile No 2",label=f"Mobile No 2{n*' '}", find=f"mobile_numb{n}")
        st.session_state.inputs_limitedc[f"fax_field{n}"], st.session_state.inputs_limitedc[f"fax{n}"]= boxes("Fax",label=f"Fax{n*' '}", find=f"fax{n}")
        st.session_state.inputs_limitedc[f"email_field{n}"], st.session_state.inputs_limitedc[f"email{n}"]=TextBox(boxes_per_row=34, search_text="Email Address", total_rows=1, x_offset=130, y_offset=5, row_height=8, box_width=8.5, control_x=0.7), st.text_input(f"Email Address*{n*' '}",max_chars=34, value=st.session_state.inputs_limitedc.get(f"email{n}", ''))
        

    else:
        st.session_state.inputs_limitedc[f"mobile_num_field{n}"].fill_field(page[0] if type(page)==list else page,st.session_state.inputs_limitedc[f"mobile_num{n}"].upper())
        st.session_state.inputs_limitedc[f"mobile_numb_field{n}"].fill_field(page[0] if type(page)==list else page,st.session_state.inputs_limitedc[f"mobile_numb{n}"].upper())
        st.session_state.inputs_limitedc[f"fax_field{n}"].fill_field(page[1] if type(page)==list else page,st.session_state.inputs_limitedc[f"fax{n}"].upper(), ind=ind)
        st.session_state.inputs_limitedc[f"email_field{n}"].fill_field(page[1] if type(page)==list else page,st.session_state.inputs_limitedc[f"email{n}"], ind=ind, fs=9)
    

def gh_tin(n, fill=False, page=0, ind=0):
    if not fill:
        st.session_state.inputs_limitedc[f"tin_field{n}"], st.session_state.inputs_limitedc[f"tin{n}"]= boxes("TIN*",label=f"TIN*{n*' '}", find=f"tin{n}", c_x=132, bpr=11)
        st.session_state.inputs_limitedc[f"gh_card_field{n}"], st.session_state.inputs_limitedc[f"gh_card{n}"]= boxes("Ghana Card(National Identity Card)*",label=f"Ghana Card(National Identity Card).Write ID numbers only Eg: GHA-XXXXXXXXX-X*{n*' '}",c_x=247, find=f"gh_card{n}", bpr=11)
        # st.session_state.inputs_limitedc[f"boidcountry{n}"]= st.text_input('ID Issuing Country/ State/Province',max_chars=35,  value=st.session_state.inputs_limitedc.get(f"boidcountry{n}", ''))
        
    else:
        st.session_state.inputs_limitedc[f"tin_field{n}"].fill_field(page, st.session_state.inputs_limitedc[f"tin{n}"].upper())
        st.session_state.inputs_limitedc[f"gh_card_field{n}"].fill_field(page, st.session_state.inputs_limitedc[f"gh_card{n}"].upper(), ind)


def body(n, pn='', fill=False, page=0, ind=0, gh=True, namerep=True, extra=False, trust=False):
    if not fill:
        st.session_state.inputs_limitedc[f"coporate_name_field{n}"]= boxes("Corporate Name*",label="", )
        st.session_state.inputs_limitedc[f"coporate_tin_field{n}"], st.session_state.inputs_limitedc[f"coporate_tin{n}"]= boxes("Corporate TIN*",label=f"Corporate TIN*", find=f"coporate_tin{n}")
        st.session_state.inputs_limitedc[f"coporate_digiadress_field{n}"], st.session_state.inputs_limitedc[f"coporate_digiadress{n}"]= boxes("Digital Address*",label=f"Digital Address*", find=f"coporate_digiadress{n}")
        st.session_state.inputs_limitedc[f"coporate_address_field{n}"], st.session_state.inputs_limitedc[f"coporate_address{n}"]= boxes("Corporate Address",label=f"Corporate AddressH/No. LMB*", find=f"coporate_address{n}", t_row=2)
        st.session_state.inputs_limitedc[f"coporate_pobox_field{n}"], st.session_state.inputs_limitedc[f"coporate_pobox{n}"]= boxes("P.O. Box/DTD/PMB*",label=f"P.O. Box/DTD/PMB*", find=f"coporate_pobox{n}")
        if namerep:
            st.session_state.inputs_limitedc[f"name_repre_field{n}"], st.session_state.inputs_limitedc[f"name_repre{n}"]= boxes("Name of Person",label=f"Name of Person Representing the Corporate Body*", find=f"name_repre{n}", c_y=4, t_row=3)
            st.session_state.inputs_limitedc[f"tinrep_field{n}"], st.session_state.inputs_limitedc[f"tinrep{n}"]= boxes("TIN of Representative*",label=f"TIN of Representative*", find=f"tinrep{n}", bpr=11)
            st.session_state.inputs_limitedc[f"gh_card_field{n}"], st.session_state.inputs_limitedc[f"gh_card{n}"]= boxes("Ghana Card(National Identity Card)*",label=f"Ghana Card(National Identity Card)*{n*' '}",c_x=247, find=f"gh_card{n}", bpr=11)


    else:
        if extra:
            st.session_state.inputs_limitedc[f"coporate_name_fieldx{n}"] = boxes("Corporate Name*", c_y=-17)
            st.session_state.inputs_limitedc[f"coporate_name_field{n}"].fill_field(page, st.session_state.inputs_limitedc[f"coporate_name{pn}"].upper(), ind)
        else:
            st.session_state.inputs_limitedc[f"coporate_name_field{n}"].fill_field(page, st.session_state.inputs_limitedc[f"coporate_name{pn}"].upper(), ind)
        st.session_state.inputs_limitedc[f"coporate_tin_field{n}"].fill_field(page, st.session_state.inputs_limitedc[f"coporate_tin{n}"].upper(), ind)
        if not trust:
            st.session_state.inputs_limitedc[f"coporate_digiadress_field{n}"].fill_field(page, st.session_state.inputs_limitedc[f"coporate_digiadress{n}"].upper(), ind)
        st.session_state.inputs_limitedc[f"coporate_address_field{n}"].fill_field(page, st.session_state.inputs_limitedc[f"coporate_address{n}"].upper())
        st.session_state.inputs_limitedc[f"coporate_pobox_field{n}"].fill_field(page, st.session_state.inputs_limitedc[f"coporate_pobox{n}"].upper(), ind)
        if namerep:
            st.session_state.inputs_limitedc[f"name_repre_field{n}"].fill_field(page, st.session_state.inputs_limitedc[f"name_repre{n}"].upper(), ind)
            st.session_state.inputs_limitedc[f"tinrep_field{n}"].fill_field(page, st.session_state.inputs_limitedc[f"tinrep{n}"].upper(), ind)
        if gh:
            st.session_state.inputs_limitedc[f"gh_card_field{n}"].fill_field(page, st.session_state.inputs_limitedc[f"gh_card{n}"].upper(), ind)

  


def payshare(i=1, address = "yes", fill=False, page=0, ind=0):
    if not fill:
        if address == "yes":
            st.session_state.inputs_limitedc[f"address_field{i}"]= boxes("Address*",label='') 
        else:
            st.session_state.inputs_limitedc[f"address_field{i}"]= boxes("Address*",label='') 
        # st.session_state.inputs_limitedc[f"shares{i}"]= 0
        # st.session_state.inputs_limitedc[f"payable{i}"]= 0
    
        st.session_state.inputs_limitedc[f"shares_field{i}"],  st.session_state.inputs_limitedc[f"shares{i}"]= boxes("No. of Shares ",label=''), st.number_input("No. of Shares to be Taken*", min_value=0, value=st.session_state.inputs_limitedc.get(f"shares{i}",0))
        st.session_state.inputs_limitedc[f"payable_field{i}"],  st.session_state.inputs_limitedc[f"payable{i}"]= boxes("Consideration Payable in Cash*",label=f"", c_x=190, bpr=14), st.number_input("Consideration Payable in Cash*", min_value=0, value=st.session_state.inputs_limitedc.get(f"payable{i}",0))
    else:
        if address == "yes":
            st.session_state.inputs_limitedc[f"address_field{i}"].fill_field(page, f'{st.session_state.inputs_limitedc[f"street_name{i}"]}, {st.session_state.inputs_limitedc[f"house_num{i}"]} {st.session_state.inputs_limitedc[f"house_address{i}"]}'.upper(), ind=ind) 
        st.session_state.inputs_limitedc[f"shares_field{i}"].fill_field(page, str(st.session_state.inputs_limitedc[f"shares{i}"])) 
        st.session_state.inputs_limitedc[f"payable_field{i}"].fill_field(page, str(st.session_state.inputs_limitedc[f"payable{i}"]))
    

def add_info(n,bo2=False,bo3=False,bo4=False):
    # purpose_of_ownership = ["Registration of a new company","Submission of Annual Returns","Company Update / Amendments","Other (Please specify)"]
    option_pep = ["Yes, they are a domestic Ghanaian PEP", "Yes, they are an international non-Ghanaian PEP", "No (skip to Part D)"]
    optionp_rel1 = ['None', 'In Person (skip to iii.)', 'Immediate Family of', 'Close Associate of']
    optionp_rel2 =['Head of State / Government', 'Senior Political Party Official', 'Government Official', 'Judicial Official'] 
    option_pep_stat  = ['Military Official', 'Executive of State-Owned Company', 'Important Political Party Officia']
   

    if bo2:
        #PART A - the company
        # st.markdown("<h6 style='text-align: center;'>Part A – About The company</h6>", unsafe_allow_html=True)

        st.session_state.inputs_limitedc[f"bopurpose_field{n}"] = PDFOptionField(control_x=26, control_y=5) 
        st.session_state.inputs_limitedc[f'boother_field{n}'] = field_plain_template(0, 'Other (Please specify)',40, 5,22, r_h=0,t_rows=1)
        st.session_state.inputs_limitedc[f'bocom_field{n}'] = field_plain_template(0,"Full legal name of Company", 40,-32,30, r_h=0,t_rows=1)
        st.session_state.inputs_limitedc[f'botin_field{n}']= field_plain_template(0,"TIN of Company (if any)",  20,0,30, r_h=0,t_rows=1)
        st.session_state.inputs_limitedc[f'borgd_field{n}'] = field_plain_template(0,"RGD number (if any):",20, 110,12, r_h=0,t_rows=1)
        st.session_state.inputs_limitedc[f'bocountry_field{n}'] = field_plain_template(0,"Country of incorporation:",40, -32, 22, r_h=0,t_rows=1)

    #    Part B – Beneficial Owners Particulars
        # st.markdown("<h6 style='text-align: center;'>Part B – Beneficial Owner Particulars</h6>", unsafe_allow_html=True)
        st.session_state.inputs_limitedc[f'firstname_field'] = field_plain_template(0, "First or given name:",35, -32,28, r_h=0,t_rows=1)
        st.session_state.inputs_limitedc[f'familyname_field'] = field_plain_template(0, "Family or surname:", 35, -32, 28, r_h=0, t_rows=1)
        st.session_state.inputs_limitedc[f'pname_field'] = field_plain_template(0, "Any previous name (e.g., maiden name):", 35, -32, 28, r_h=0, t_rows=1)
        # get_date_input(f"dob{n}", "Date of Birth*")
        st.session_state.inputs_limitedc[f'bodob_field'] = field_plain_template(0, "Date of Birth", 20, 20, 28, r_h=0, t_rows=1)
        st.session_state.inputs_limitedc[f'bopob_field'] = field_plain_template(0, "Place of Birth:", 35, -32, 22, r_h=0, t_rows=1)
        st.session_state.inputs_limitedc[f'bonation_field'] = field_plain_template(0, "Nationality:", 35, -32, 22, r_h=0, t_rows=1)
        st.session_state.inputs_limitedc[f'boaddress_field']= field_plain_template(0, "Residential Address", 35, -32, 41 , r_h=15, t_rows=3)
        st.session_state.inputs_limitedc[f'boservice_field'] = field_plain_template(0, "Service Address", 35, -32, 41, r_h=15, t_rows=3)
        st.session_state.inputs_limitedc[f'bodigi_field']= field_plain_template(0, "GPS):", 35, -32, 19, r_h=0, t_rows=1)
        st.session_state.inputs_limitedc[f'botaxnum_field'] = field_plain_template(0, "Tax Identification Number (TIN). (if applicable):", 20, 10, 27, r_h=0, t_rows=1)
        st.session_state.inputs_limitedc[f'bomobile_field']= field_plain_template(0, "Telephone/Mobile Number:", 20, 10, 22, r_h=0, t_rows=1)
        st.session_state.inputs_limitedc[f'boemail_field'] = field_plain_template(0, "Email address", 35, -32, 22, r_h=0, t_rows=1)
        st.session_state.inputs_limitedc[f'boidtype_field']= field_plain_template(0, "Primary ID Type (see instructions):", 30, -30, 30, r_h=0, t_rows=1)
        st.session_state.inputs_limitedc[f'boidnum_field'] = field_plain_template(0, "ID):", 35, -10, 22, r_h=0, t_rows=1)
        st.session_state.inputs_limitedc[f'boidcountry_field']= field_plain_template(0, "ID Issuing Country/ State/Province:", 35, -32, 28, r_h=0, t_rows=1)
        st.session_state.inputs_limitedc[f'bowork_field']= field_plain_template(0, "Place of Work and Position Held:", 30, -30, 28, r_h=0, t_rows=1)
        get_date_input(f"doregis{n}", "Date BO Became Registerable – This is the date on which the Natural Person became a Politically Exposed Persons (PEP)")
        st.session_state.inputs_limitedc[f"doregis_field"] = boxes("Date BO Became Registerable", c_x=115, c_y=8)
        
        # Part C – Politically Exposed Persons (PEP)
        st.markdown("<h6 style='text-align: center;'>Politically Exposed Persons (PEP)</h6>", unsafe_allow_html=True)
        st.session_state.inputs_limitedc[f"pep_field"],st.session_state.inputs_limitedc[f"pep{n}"] = PDFOptionField(control_x=19, control_y=5), st.selectbox("""(i) Is the individual named above a PEP, because of holding a position of importance or being a close relative or associate of a person holding a position of importance?""", option_pep, index=option_pep.index(st.session_state.inputs_limitedc.get(f"pep{n}", option_pep[0])))
        st.session_state.inputs_limitedc[f"con_to_holder_field"], st.session_state.inputs_limitedc[f"con_to_holder{n}"] = PDFOptionField(control_x=21, control_y=13), st.radio('(ii) Nature of Connection to office holder', optionp_rel1, horizontal=True, index=optionp_rel1.index(st.session_state.inputs_limitedc.get(f"con_to_holder{n}", optionp_rel1[0])))
        st.session_state.inputs_limitedc[f'pepfirstname_field'], st.session_state.inputs_limitedc[f'pepfirstname{n}'] = field_plain_template("First or given name of office holder", "First or given name of office holder:", 35, -32, 27, r_h=0, t_rows=1, value=st.session_state.inputs_limitedc.get(f"pepfirstname{n}", ''))
        st.session_state.inputs_limitedc[f'pepsurname_field'], st.session_state.inputs_limitedc[f'pepsurname_field{n}'] = field_plain_template("Family or surname of office holder:", "Family or surname of office holder:", 35, -32, 27, r_h=0, t_rows=1, value=st.session_state.inputs_limitedc.get(f"pepsurname_field{n}", ''))
        st.session_state.inputs_limitedc[f'pepprename_field'], st.session_state.inputs_limitedc[f'pepprename_field{n}'] = field_plain_template("Any previous name (e.g. maiden name) of office holder:", "holder:", 28, 25, 19, r_h=0, t_rows=1, value=st.session_state.inputs_limitedc.get(f"pepprename_field{n}", ''))
        get_date_input(f"holderdate{n}", "Date of Birth of office holder")
        st.session_state.inputs_limitedc[f"holderdate_field"] = field_plain_template(0, "Date of Birth of office holder", 20, 20, 27 )
        st.session_state.inputs_limitedc[f"pepexposed_field"], st.session_state.inputs_limitedc[f"pepexposed{n}"] =PDFOptionField(control_x=19, control_y=8), st.selectbox(f'Politically Exposed Persons means persons that have been entrusted in prominent public positions and their family members and close associates. Please select where applicable:{n}', optionp_rel2, index=optionp_rel2.index(st.session_state.inputs_limitedc.get(f"pepexposed{n}", optionp_rel2[0])))
        st.session_state.inputs_limitedc[f"pepstat_field"], st.session_state.inputs_limitedc[f"pepstat{n}"] = PDFOptionField(control_x=19, control_y=13), st.selectbox('(iii) Reason for PEP Status (See instructions)', option_pep_stat, index=option_pep_stat.index(st.session_state.inputs_limitedc.get(f"pepstat{n}", option_pep_stat[0])))
        st.session_state.inputs_limitedc[f'peprole_field'], st.session_state.inputs_limitedc[f'peprole_field{n}'] = field_plain_template("(iv) Role title of this office holder and office/department", "Role title of this", 55, 120,10, r_h=15, t_rows=3, value=st.session_state.inputs_limitedc.get(f"peprole_field{n}", ''))

        # Part D - Nature of Interest
        st.markdown("<h6 style='text-align: center;'>Nature of Interest</h6>", unsafe_allow_html=True)
        option_shareholder = ['Yes – Direct', 'Yes – Indirect']
        option_shareholder2 = ['No (skip to 3.)','Yes - Direct', 'Yes – Indirect']
        option_shareholder3 = ['No (skip to 5.)','Yes']
        # st.session_state.inputs_limitedc[f"sharehold{n}"] = 'Yes – Direct'
        st.session_state.inputs_limitedc[f"sharehold_field{n}"], st.session_state.inputs_limitedc[f"sharehold{n}"] = PDFOptionField(control_x=19, control_y=5), st.radio("""1\. Please select whether the Natural Person has a direct or indirect (via holding companies) shareholding in the company; no, yes (direct) or yes (indirect). If yes, please insert the effective percentage interest in the box below.""", option_shareholder, horizontal=True, index=option_shareholder.index(st.session_state.inputs_limitedc.get(f"sharehold{n}",option_shareholder[0])))
        st.session_state.inputs_limitedc[f'direct_field{n}'] = field_plain_template(0, "Direct:",15, 33,6, r_h=0,t_rows=1)
        st.session_state.inputs_limitedc[f'indirect_field{n}'] = field_plain_template(0, "Indirect:",15, 37,6, r_h=0,t_rows=1)
        # st.session_state.inputs_limitedc[f'direct_field{n}'], st.session_state.inputs_limitedc[f'direct{n}'] = field_plain_template("Direct", "Direct:",15, 33,6, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f"direct{n}",''))
        # st.session_state.inputs_limitedc[f'indirect_field{n}'], st.session_state.inputs_limitedc[f'indirect{n}'] = field_plain_template("Indirect", "Indirect:",15, 37,6, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f"indirect{n}",''))
       
        st.session_state.inputs_limitedc[f"voting_field{n}"], st.session_state.inputs_limitedc[f"voting{n}"] = PDFOptionField(control_x=19, control_y=9), st.radio("""2\. Please select whether the Natural Person direct or indirect (via holding companies) controls voting rights in the company; no, yes (direct) or yes (indirect). If yes, please insert the effective percentage voting rights in the box below, and also whether or not they have a right of veto. A right of veto exists if the Natural Person can block a decision of the board of the company.""", option_shareholder2, horizontal=True, index=option_shareholder2.index(st.session_state.inputs_limitedc.get(f"voting{n}",option_shareholder2[0])))
        st.session_state.inputs_limitedc[f'vrightheld_field{n}'], st.session_state.inputs_limitedc[f'vrightheld{n}'] = field_plain_template("% of Voting Rights Held", "% of Voting Rights Held:",12, -22,22, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f"vrightheld{n}",''))
        st.session_state.inputs_limitedc[f'voteright_field{n}'], st.session_state.inputs_limitedc[f'voteright{n}'] = PDFOptionField(control_x=11, control_y=4), st.radio('Right of Veto? (see instructions)', option_yesno, horizontal=True, index=option_yesno.index(st.session_state.inputs_limitedc.get(f"voteright{n}",option_yesno[0])))

        st.session_state.inputs_limitedc[f"apointright_field{n}"], st.session_state.inputs_limitedc[f"apointright{n}"] = PDFOptionField(control_x=19, control_y=9), st.radio("""3\. Please select whether the Natural Person has the right to appoint or remove a majority of the directors of the company. This might be the case even if they do not control voting rights as set out in Box 2 above, and they may have a specific separate right.""", option_yesno, horizontal=True, index=option_yesno.index(st.session_state.inputs_limitedc.get(f"apointright{n}",option_yesno[0])))
        st.session_state.inputs_limitedc[f"securities_field{n}"], st.session_state.inputs_limitedc[f"securities{n}"] = PDFOptionField(control_x=19, control_y=12), st.radio("""4\. Please select whether the Natural Person has any other form of securities in the company other than shares disclosed in Box 1 above. This could include share options or warrants. If yes, please provide a description.""", option_shareholder3, horizontal=True, index=option_shareholder3.index(st.session_state.inputs_limitedc.get(f"securities{n}",option_shareholder3[0])))
        st.session_state.inputs_limitedc[f'description_field1{n}'], st.session_state.inputs_limitedc[f'description1{n}'] = field_plain_template("Description", "Description:",45, 5,25, r_h=13,t_rows=2,value=st.session_state.inputs_limitedc.get(f"description1{n}",''))

        st.session_state.inputs_limitedc[f"control_field{n}"], st.session_state.inputs_limitedc[f"control{n}"] = PDFOptionField(control_x=19, control_y=5), st.radio("""5\. Please identify whether the Natural Person exercises control over the company in any other way not already disclosed in 1 to 4 above. If yes, please provide a description.""", option_yesno, horizontal=True, index=option_yesno.index(st.session_state.inputs_limitedc.get(f"control{n}",option_yesno[0])))
        st.session_state.inputs_limitedc[f'description_field2{n}'], st.session_state.inputs_limitedc[f'description2{n}'] = field_plain_template("Description ", "Description:",45, 5,25, r_h=13,t_rows=2,value=st.session_state.inputs_limitedc.get(f"description2{n}",''))



    elif bo3:
          #PART A - the company
        # st.markdown("<h6 style='text-align: center;'>Part A – About The company</h6>", unsafe_allow_html=True)
        st.session_state.inputs_limitedc[f"bopurpose_field{n}"] = PDFOptionField(control_x=26, control_y=5)
        st.session_state.inputs_limitedc[f'boother_field{n}'] = field_plain_template(0, 'Other (Please specify)',40, 5,22, r_h=0,t_rows=1)
        st.session_state.inputs_limitedc[f'bocom_field{n}']= field_plain_template(0,"Full legal name of Company", 40,-32,30, r_h=0,t_rows=1)
        st.session_state.inputs_limitedc[f'botin_field{n}']= field_plain_template(0,"TIN of Company (if any)",  20,0,30, r_h=0,t_rows=1)
        st.session_state.inputs_limitedc[f'borgd_field{n}'] = field_plain_template(0,"RGD number (if any):",20, 110,12, r_h=0,t_rows=1)
        st.session_state.inputs_limitedc[f'bocountry_field{n}'] = field_plain_template(0,"Country of incorporation:",38, -32, 22, r_h=0,t_rows=1)
    
    
     # Part B – Beneficial Owners Particulars
        # st.markdown("<h6 style='text-align: center;'>Part B – Beneficial Owner Particulars</h6>", unsafe_allow_html=True)
        st.session_state.inputs_limitedc[f'listedname_field{n}'] = field_plain_template(0, "Full legal name of Publicly Listed Company",70, -32,25, r_h=0,t_rows=1)
        st.session_state.inputs_limitedc[f'idnum_field{n}'], st.session_state.inputs_limitedc[f'idnum{n}'] = field_plain_template("International Securities Identifying Number (ISIN) (if any)", "any):",20, 30,15, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f"idnum{n}",''))
        st.session_state.inputs_limitedc[f'legalentity_field'], st.session_state.inputs_limitedc[f'legalentity{n}'] = field_plain_template("Legal Entity Identifier (If any)", "Legal Entity Identifier (If any)",35, -32,35, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f"legalentity{n}",''))
        st.session_state.inputs_limitedc[f'percent_field'], st.session_state.inputs_limitedc[f'percent{n}'] = field_plain_template("Percentage of shares listed on stock exchange(s)", "Percentage of shares listed on stock exchange(s):",55, -32,35, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f"percent{n}",''))
        
        # Part C - Stock Exchange Details        
        st.markdown("<h6 style='text-align: center;'>Part C – Stock Exchange Details</h6>", unsafe_allow_html=True)
        st.write('To delete an entire row, select the row and press the delete key. Select a maximum of 5 rows')
        user_id = f"benexx{n}"
        if user_id not in st.session_state.inputs_limitedc:
            st.session_state.inputs_limitedc[user_id] = {
                "table_data": {
                    "Name of Stock Exchange": [],
                    "Percentage of Shares Listed": [],
                    "Link to Web Address Pages on Stock Exchange": [],
                },
            }
        user_data = st.session_state.inputs_limitedc[user_id]  

        # Prepare data for the DataFrame
        if not user_data["table_data"]["Name of Stock Exchange"]:  #
            user_data["table_data"]["Name of Stock Exchange"].append("")
            user_data["table_data"]["Percentage of Shares Listed"].append("")
            user_data["table_data"]["Link to Web Address Pages on Stock Exchange"].append("")


        if len(user_data["table_data"]["Name of Stock Exchange"]) > 5:
            user_data["table_data"]["Name of Stock Exchange"] = user_data["table_data"]["Name of Stock Exchange"][:5]
            user_data["table_data"]["Percentage of Shares Listed"] = user_data["table_data"]["Percentage of Shares Listed"][:5]
            user_data["table_data"]["Link to Web Address Pages on Stock Exchange"] = user_data["table_data"]["Link to Web Address Pages on Stock Exchange"][:5]

        stock_exchange_df = pd.DataFrame(user_data["table_data"])


        edited_df = st.data_editor(
            stock_exchange_df,
            key=f"{user_id}_stock_exchange_table",
            num_rows="dynamic",  
        )

        user_data["table_data"]["Name of Stock Exchange"] = edited_df["Name of Stock Exchange"].tolist()
        user_data["table_data"]["Percentage of Shares Listed"] = edited_df["Percentage of Shares Listed"].tolist()
        user_data["table_data"]["Link to Web Address Pages on Stock Exchange"] = edited_df["Link to Web Address Pages on Stock Exchange"].tolist()

       
        # Part D - Nature of Interest
        st.markdown("<h6 style='text-align: center;'>Part D – Nature of Interest</h6>", unsafe_allow_html=True)
        option_shareholder = ['Yes – Direct', 'Yes – Indirect']
        option_shareholder2 = ['No (skip to 3.)','Yes - Direct', 'Yes – Indirect']
        option_shareholder3 = ['No (skip to 5.)','Yes']
        
        st.session_state.inputs_limitedc[f"sharehold_field{n}"], st.session_state.inputs_limitedc[f"sharehold{n}"] = PDFOptionField(control_x=19, control_y=5), st.radio("""1\. Please select whether the Publicly Listed Company has a direct or indirect (via holding companies) shareholding in the company; no, yes (direct) or yes (indirect). If yes, please insert the effective percentage interest in the box below.""", option_shareholder, horizontal=True, index=option_shareholder.index(st.session_state.inputs_limitedc.get(f"sharehold{n}",option_shareholder[0])))
        st.session_state.inputs_limitedc[f'direct_field{n}'] = field_plain_template(0, "Direct:",15, 33,6, r_h=0,t_rows=1)
        st.session_state.inputs_limitedc[f'indirect_field{n}'] = field_plain_template(0, "Indirect:",15, 37,6, r_h=0,t_rows=1)        
        # st.session_state.inputs_limitedc[f'direct_field{n}'], st.session_state.inputs_limitedc[f'direct{n}'] = field_plain_template("Direct", "Direct:",15, 33,6, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f"direct{n}",''))
        # st.session_state.inputs_limitedc[f'indirect_field{n}'], st.session_state.inputs_limitedc[f'indirect{n}'] = field_plain_template("Indirect", "Indirect:",15, 37,6, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f"indirect{n}",''))
       
        st.session_state.inputs_limitedc[f"voting_field{n}"], st.session_state.inputs_limitedc[f"voting{n}"] = PDFOptionField(control_x=19, control_y=9), st.radio("""2\. Please select whether the Publicly Listed Company direct or indirect (via holding companies) controls voting rights in the company; no, yes (direct) or yes (indirect). If yes, please insert the effective percentage voting rights in the box below, and whether or not they have a right of veto. A right of veto exists if the Publicly Listed Company can block a decision of the board of the company.""", option_shareholder2, horizontal=True, index=option_shareholder2.index(st.session_state.inputs_limitedc.get(f"voting{n}",option_shareholder2[0])))
        st.session_state.inputs_limitedc[f'vrightheld_field{n}'], st.session_state.inputs_limitedc[f'vrightheld{n}'] = field_plain_template("% of Voting Rights Held", "% of Voting Rights Held:",12, -22,35, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f"vrightheld{n}",''))
        st.session_state.inputs_limitedc[f'voteright_field{n}'], st.session_state.inputs_limitedc[f'voteright{n}'] = PDFOptionField(control_x=11, control_y=4), st.radio('Right of Veto? (see instructions)', option_yesno, horizontal=True, index=option_yesno.index(st.session_state.inputs_limitedc.get(f"voteright{n}",option_yesno[0])))

        st.session_state.inputs_limitedc[f"apointright_field{n}"], st.session_state.inputs_limitedc[f"apointright{n}"] = PDFOptionField(control_x=19, control_y=9), st.radio("""3\. Please select whether the Publicly Listed Company has the right to appoint or remove a majority of the directors of the company. This might be the case even if they do not control voting rights as set out in Box 2 above, and they may have a specific separate right.""", option_yesno, horizontal=True, index=option_yesno.index(st.session_state.inputs_limitedc.get(f"apointright{n}",option_yesno[0])))
        st.session_state.inputs_limitedc[f"securities_field{n}"], st.session_state.inputs_limitedc[f"securities{n}"] = PDFOptionField(control_x=19, control_y=12), st.radio("""4\. Please select whether the Publicly Listed Company has any other form of securities in the company other than shares disclosed in Box 1 above. This could include share options or warrants. If yes, please provide a description.""", option_shareholder3, horizontal=True, index=option_shareholder3.index(st.session_state.inputs_limitedc.get(f"securities{n}",option_shareholder3[0])))
        st.session_state.inputs_limitedc[f'description_field1{n}'], st.session_state.inputs_limitedc[f'description1{n}'] = field_plain_template("Description", "Description:",45, 5,25, r_h=13,t_rows=2,value=st.session_state.inputs_limitedc.get(f"description1{n}",''))

        st.session_state.inputs_limitedc[f"control_field{n}"], st.session_state.inputs_limitedc[f"control{n}"] = PDFOptionField(control_x=19, control_y=5), st.radio("""5\. Please identify whether the Publicly Listed Company exercises control over the company in any other way not already disclosed. If yes, please provide a description""", option_yesno, horizontal=True, index=option_yesno.index(st.session_state.inputs_limitedc.get(f"control{n}",option_yesno[0])))
        st.session_state.inputs_limitedc[f'description_field2{n}'], st.session_state.inputs_limitedc[f'description2{n}'] = field_plain_template("Description ", "Description:",45, 5,25, r_h=13,t_rows=2,value=st.session_state.inputs_limitedc.get(f"description2{n}",''))





    elif bo4:
           #PART A - the company
        # st.markdown("<h6 style='text-align: center;'>Part A – About The company</h6>", unsafe_allow_html=True)
        st.session_state.inputs_limitedc[f"bopurpose_field{n}"] = PDFOptionField(control_x=26, control_y=5)
        st.session_state.inputs_limitedc[f'boother_field{n}'] = field_plain_template(0, 'Other (Please specify)',40, 5,22, r_h=0,t_rows=1)
        st.session_state.inputs_limitedc[f'bocom_field{n}']= field_plain_template(0,"Full legal name of Company", 40,-32,30, r_h=0,t_rows=1)
        st.session_state.inputs_limitedc[f'botin_field{n}']= field_plain_template(0,"TIN of Company (if any)",  20,0,30, r_h=0,t_rows=1)
        st.session_state.inputs_limitedc[f'borgd_field{n}'] = field_plain_template(0,"RGD number (if any):",20, 97,12, r_h=0,t_rows=1)
        st.session_state.inputs_limitedc[f'bocountry_field{n}'] = field_plain_template(0,"Country of incorporation:",38, -32, 22, r_h=0,t_rows=1)
   
        # Part B – Beneficial Owners Particulars
        # st.markdown("<h6 style='text-align: center;'>Part B – Beneficial Owner Particulars</h6>", unsafe_allow_html=True)
        st.session_state.inputs_limitedc[f'governmentname_field{n}']= field_plain_template(0, "Name of government agency:",35, -32,29, r_h=15,t_rows=2)
        st.session_state.inputs_limitedc[f'boservice_field{n}'] = field_plain_template(0, "and: Postal/Zip code:",35, -32,27, r_h=15,t_rows=2)
        st.session_state.inputs_limitedc[f'boemail_field{n}'], st.session_state.inputs_limitedc[f'boemail{n}'] = field_plain_template("Email address", "Email address",35, -32,27, r_h=15,t_rows=2,value=st.session_state.inputs_limitedc.get(f"boemail{n}",''))
        st.session_state.inputs_limitedc[f'boidcountry_field{n}'], st.session_state.inputs_limitedc[f'boidcountry{n}'] = field_plain_template("Country of Incorporation (Please provide notarised copy of incorporation document)", "notarised copy of incorporation document)",35, -32,22, r_h=13,t_rows=2,value=st.session_state.inputs_limitedc.get(f"boidcountry{n}",''))
        st.session_state.inputs_limitedc[f'bonation_field{n}'], st.session_state.inputs_limitedc[f'bonation{n}'] = field_plain_template("Nationality", "Nationality:",35, -32,24, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f"bonation{n}",''))
        st.session_state.inputs_limitedc[f'oficialrepre_field'] = field_plain_template(0, "Government:",35, -32,22, r_h=0,t_rows=1)
        st.session_state.inputs_limitedc[f'currentrole_field'], st.session_state.inputs_limitedc[f'currentrole{n}'] = field_plain_template("Current Role", "Current Role:",35, -32,26, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f"currentrole{n}",''))
        st.session_state.inputs_limitedc[f'bomobile_field{n}'], st.session_state.inputs_limitedc[f'bomobile{n}'] = field_plain_template("Contact number", "Contact number:",35, -10,32, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f"bomobile{n}",''))
        

        st.markdown("<h6 style='text-align: center;'>Part D – Nature of Interest</h6>", unsafe_allow_html=True)
        option_shareholder = ['Yes – Direct', 'Yes – Indirect']
        option_shareholder2 = ['No (skip to 3.)','Yes - Direct', 'Yes – Indirect']
        option_shareholder3 = ['No (skip to 5.)','Yes']
        
        st.session_state.inputs_limitedc[f"sharehold_field{n}"], st.session_state.inputs_limitedc[f"sharehold{n}"] = PDFOptionField(control_x=19, control_y=5), st.radio("""1\. Please select whether the Government Owned Company has a direct or indirect (via holding companies) shareholding in the company; no, yes (direct) or yes (indirect). Please tick only one box. If yes, please insert the effective percentage interest in the box below.""", option_shareholder, horizontal=True, index=option_shareholder.index(st.session_state.inputs_limitedc.get(f"sharehold{n}",option_shareholder[0])))   
        st.session_state.inputs_limitedc[f'direct_field{n}'] = field_plain_template(0, "Direct:",15, 33,6, r_h=0,t_rows=1)
        st.session_state.inputs_limitedc[f'indirect_field{n}'] = field_plain_template(0, "Indirect:",15, 37,6, r_h=0,t_rows=1)
   
        # st.session_state.inputs_limitedc[f'direct_field{n}'], st.session_state.inputs_limitedc[f'direct{n}'] = field_plain_template("Direct", "Direct:",15, 33,6, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f"direct{n}",''))
        # st.session_state.inputs_limitedc[f'indirect_field{n}'], st.session_state.inputs_limitedc[f'indirect{n}'] = field_plain_template("Indirect", "Indirect:",15, 37,6, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f"indirect{n}",''))
       
        st.session_state.inputs_limitedc[f"voting_field{n}"], st.session_state.inputs_limitedc[f"voting{n}"] = PDFOptionField(control_x=19, control_y=9), st.radio("""2\. Please select whether the Government Owned Company direct or indirect (via holding companies) controls voting rights in the company; no, yes (direct) or yes (indirect). If yes, please insert the effective percentage voting rights in the box below, and also whether or not they have a right of veto. A right of veto exists if the Government Owned Company can block a decision of the board of the company.""", option_shareholder2, horizontal=True, index=option_shareholder2.index(st.session_state.inputs_limitedc.get(f"voting{n}",option_shareholder2[0])))
        st.session_state.inputs_limitedc[f'vrightheld_field{n}'], st.session_state.inputs_limitedc[f'vrightheld{n}'] = field_plain_template("% of Voting Rights Held", "% of Voting Rights Held:",12, -22,27, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f"vrightheld{n}",''))
        st.session_state.inputs_limitedc[f'voteright_field{n}'], st.session_state.inputs_limitedc[f'voteright{n}'] = PDFOptionField(control_x=11, control_y=4), st.radio('Right of Veto? (see instructions)', option_yesno, horizontal=True, index=option_yesno.index(st.session_state.inputs_limitedc.get(f"voteright{n}",option_yesno[0])))

        st.session_state.inputs_limitedc[f"apointright_field{n}"], st.session_state.inputs_limitedc[f"apointright{n}"] = PDFOptionField(control_x=19, control_y=9), st.radio("""3\. Please select whether the Government Owned Company has the right to appoint or remove a majority of the directors of the company. This might be the case even if they do not control voting rights as set out in Box 2 above, and they may have a specific separate right.""", option_yesno, horizontal=True, index=option_yesno.index(st.session_state.inputs_limitedc.get(f"apointright{n}",option_yesno[0])))
        st.session_state.inputs_limitedc[f"securities_field{n}"], st.session_state.inputs_limitedc[f"securities{n}"] = PDFOptionField(control_x=19, control_y=12), st.radio("""4\. Please select whether the Government Owned Company has any other form of securities in the company other than shares disclosed in Box 1 above. This could include share options or warrants. If yes, please provide a description.""", option_shareholder3, horizontal=True, index=option_shareholder3.index(st.session_state.inputs_limitedc.get(f"securities{n}",option_shareholder3[0])))
        st.session_state.inputs_limitedc[f'description_field1{n}'], st.session_state.inputs_limitedc[f'description1{n}'] = field_plain_template("Description", "Description:",45, 5,25, r_h=13,t_rows=2,value=st.session_state.inputs_limitedc.get(f"description1{n}",''))

        st.session_state.inputs_limitedc[f"control_field{n}"], st.session_state.inputs_limitedc[f"control{n}"] = PDFOptionField(control_x=19, control_y=5), st.radio("""5\. Please identify whether the Government Owned Company exercises control over the company in any other way not already disclosed. If yes, please provide a description.""", option_yesno, horizontal=True, index=option_yesno.index(st.session_state.inputs_limitedc.get(f"control{n}",option_yesno[0])))
        st.session_state.inputs_limitedc[f'description_field2{n}'], st.session_state.inputs_limitedc[f'description2{n}'] = field_plain_template("Description ", "Description:",45, 5,25, r_h=13,t_rows=2,value=st.session_state.inputs_limitedc.get(f"description2{n}",''))


       
 
    
def form3shares(i, fill=False, page=0, ind1=0, ind2=0):
    if not fill:
        st.session_state.inputs_limitedc[f"equityshares_field{i}"],  st.session_state.inputs_limitedc[f"equityshares{i}"]= boxes('Equity Shares*',label='', c_x=170, bpr=15), st.number_input(f"Equity Shares*{i*' '}",min_value=0, value=st.session_state.inputs_limitedc.get(f"equityshares{i}", 0))
        st.session_state.inputs_limitedc[f"preshares_field{i}"],  st.session_state.inputs_limitedc[f"preshares{i}"]= boxes("Preference Shares",label="", c_x=170, bpr=13), st.number_input(f"Preference Shares GHC{i*' '}", min_value=0, value=st.session_state.inputs_limitedc.get(f"preshares{i}", 0))
    else:
        st.session_state.inputs_limitedc[f"equityshares_field{i}"].fill_field(page, str(st.session_state.inputs_limitedc[f"equityshares{i}"]) if st.session_state.inputs_limitedc[f"equityshares{i}"] else '', ind1)
        st.session_state.inputs_limitedc[f"preshares_field{i}"].fill_field(page, str(st.session_state.inputs_limitedc[f"preshares{i}"]) if st.session_state.inputs_limitedc[f"preshares{i}"] else '', ind2)
   

def tax(i,pn=1, p=0, fill=False,l=[], label=''):
    if not fill:
        option_tax = ['Individual', 'Third Party']
        if p == 0:
            option_taxpayer, option_category = ["YES", "NO"], ["Self employed", "Employee", "Foreign mission employee", "Other"]
            options_postal_type = ["P. 0. BOX", "PMB", "DTD", "POSTAL NUMBER"]          

            st.session_state.inputs_limitedc[f'postal_address_taxfield{i}'], st.session_state.inputs_limitedc[f'postal_address_tax{i}'] = PDFOptionField(control_x=11, control_y=4), st.radio(f"IS THE RESIDENTIAL ADDRESS SAME AS POSTAL ADDRESS?", option_taxpayer, horizontal=True, index=option_taxpayer.index(st.session_state.inputs_limitedc.get(f"postal_address_tax{i}",option_taxpayer[0])))
            
            # st.session_state.inputs_limitedc[f"postal_type_taxfield{i}"],st.session_state.inputs_limitedc[f'postal_type_tax{i}'] = field_multi_options(options_postal_type, f"POSTAL TYPE (Select as applicable)", value=st.session_state.inputs_limitedc.get(f'postal_type_tax{i}',[]))
        
            st.session_state.inputs_limitedc[f"third_party_tax{i}"] = st.radio("Will the tax form be completed by the individual or a third party?",option_tax, horizontal=True, index = option_tax.index(st.session_state.inputs_limitedc.get(f"third_party_tax{i}",option_tax[0])))
            st.session_state.inputs_limitedc[f"tax_payer_field{i}"], st.session_state.inputs_limitedc[f"tax_payer_{i}"] = PDFOptionField(control_x=11, control_y=4), st.radio(f"ARE YOU A REGISTERED TAXPAYER?", option_taxpayer, horizontal=True, index=option_taxpayer.index(st.session_state.inputs_limitedc.get(f"tax_payer_{i}",option_taxpayer[0])))
            st.session_state.inputs_limitedc[f"category_field{i}"], st.session_state.inputs_limitedc[f"category_{i}"] = PDFOptionField(control_x=11, control_y=4), st.multiselect(f"CATEGORY TYPE (Select as applicable)", option_category, default=st.session_state.inputs_limitedc.get(f"category_{i}",[]))
            st.session_state.inputs_limitedc[f"self_employed_{i}"] = st.radio(f"Are you self-employed?", ["NO", "YES"], horizontal=True, index=["NO", "YES"].index(st.session_state.inputs_limitedc.get(f"self_employed_{i}",["NO", "YES"][0])))
            option_employee = ["NO", "YES"]  # fix repetitive yes or no, currently used because of the order
            st.session_state.inputs_limitedc[f'registered_field{i}'], st.session_state.inputs_limitedc[f'registered_{i}'] = PDFOptionField(control_x=11, control_y=4), st.radio(f"IF YES HAVE YOU REGISTERED YOUR BUSINESS NAME(S) WITH RGD?", option_employee, horizontal=True, index=option_employee.index(st.session_state.inputs_limitedc.get(f'registered_{i}',option_employee[0])))
          

        else:
            if "Other" in st.session_state.inputs_limitedc[f"category_{i}"]:
               st.session_state.inputs_limitedc[f"specify_field{i}"] = PDFTextFinder("If OTHER specify", max_chars_per_row=14, control_x=65, control_y=7)
               st.session_state.inputs_limitedc[f"specify_{i}"] = st.text_input(f"Please specify 'Other' selected among categories", max_chars=st.session_state.inputs_limitedc[f"specify_field{i}"].max_chars_per_row, value=st.session_state.inputs_limitedc.get(f"specify_{i}", ''))
            if "Employee" in st.session_state.inputs_limitedc[f"category_{i}"] or 'Foreign mission employee' in st.session_state.inputs_limitedc[f"category_{i}"]:
                st.session_state.inputs_limitedc[f"employer_field{i}"] = PDFTextFinder(f"Employer's Name", max_chars_per_row=32, control_x=70, control_y=7)
                st.session_state.inputs_limitedc[f"employer_{i}"] = st.text_input(f"Employer's Name:", max_chars=st.session_state.inputs_limitedc[f"employer_field{i}"].max_chars_per_row, value=st.session_state.inputs_limitedc.get(f"employer_{i}", ''))
      
            #SECTION 3: PERSONAL DETAILS 
            st.markdown("<h6 style='text-align: center;'> PERSONAL DETAILS</h6>", unsafe_allow_html=True)
            st.session_state.inputs_limitedc[f"title_field_tax{i}"] = PDFOptionField(control_x=11, control_y=4)
            st.session_state.inputs_limitedc[f"title_{i}"] = st.session_state.inputs_limitedc.get(f"title{pn}").strip()

            if st.session_state.inputs_limitedc[f"title{pn}"] == " Dr " or st.session_state.inputs_limitedc[f"title{pn}"] == " Miss ":
                res =  st.session_state.inputs_limitedc[f"title{pn}"]
                st.session_state.inputs_limitedc[f"title_{i}"] = "OTHER" 
                st.session_state.inputs_limitedc[f"specify_title_field_tax{i}"] = PDFTextFinder("SPECIFY", control_x=33, max_chars_per_row=22)
                st.session_state.inputs_limitedc[f"specify_title_{i}"] = res

            st.session_state.inputs_limitedc[f"first_name_field_tax{i}"] = field_box_template("FIRST NAME") 
            st.session_state.inputs_limitedc[f"middle_name_field_tax{i}"]= field_box_template("MIDDLE NAME(S)")
            st.session_state.inputs_limitedc[f"last_name_field_tax{i}"]= field_box_template("LAST NAME")
            st.session_state.inputs_limitedc[f"previous_name_field_tax{i}"] = field_box_template("PREVIOUS LAST NAME")
            st.session_state.inputs_limitedc[f"gender_field_tax{i}"] = field_option_template()
            st.session_state.inputs_limitedc[f"occupation_field_tax{i}"]= field_box_template("MAIN OCCUPATION", bpr=19, x_offset=74)
            st.session_state.inputs_limitedc[f"dob_field_tax{i}"]= field_box_template("DATE OF BIRTH")
            st.session_state.inputs_limitedc[f"nationality_field_tax{i}"] = field_box_template("NATIONALITY")
            # st.session_state.inputs[f"birth_country_field_tax{i}"], st.session_state.inputs[f'birth_country_{i}'] = field_box_template("BIRTH COUNTRY", f"BIRTH COUNTRY_{i}",  value=st.session_state.inputs.get(f'birth_country_{i}',''))
            # st.session_state.inputs[f"birth_region_field_tax{i}"], st.session_state.inputs[f'birth_region_{i}'] = field_box_template("BIRTH REGION", f"BIRTH REGION_{i}",value=st.session_state.inputs.get(f'birth_region_{i}',''))
            # st.session_state.inputs[f"birth_district_field_tax{i}"], st.session_state.inputs[f'birth_district_{i}'] = field_box_template("BIRTH DISTRICT", f"BIRTH DISTRICT{i}",value=st.session_state.inputs.get(f'birth_district_{i}',''))
           

            option_residents = ["YES", "NO"]
            st.session_state.inputs_limitedc[f"residents_field_tax{i}"],st.session_state.inputs_limitedc[f'residents_{i}'] = field_option_template(option_residents, f"RESIDENT (select one)", value= (st.session_state.inputs_limitedc.get(f'residents_{i}', "YES")))
            st.session_state.inputs_limitedc[f"security_field_tax{i}"],st.session_state.inputs_limitedc[f'security_{i}'] = field_box_template("SOCIAL SECURITY NUMBER", f"SOCIAL SECURITY NUMBER", bpr=13, x_offset=98, value=st.session_state.inputs_limitedc.get(f'security_{i}',''))
            options_info = ["IMPORTER", 'EXPORTER', 'TAX CONSULTANT', 'NOT APPLICABLE']
            st.session_state.inputs_limitedc[f"info_field{i}"],st.session_state.inputs_limitedc[f'info_{i}'] = field_multi_options(options_info, f'OTHER INFORMATION (Select applicable ones)', value=st.session_state.inputs_limitedc.get(f'info_{i}',[]))

            st.markdown("<h6 style='text-align: center;'>MOTHER'S INFORMATION</h6>", unsafe_allow_html=True)
            st.session_state.inputs_limitedc[f"mother_maiden_field{i}"],st.session_state.inputs_limitedc[f'mother_maiden_{i}'] = field_box_template("MAIDEN LAST NAME", f"MAIDEN LAST NAME", x_offset=84,value=st.session_state.inputs_limitedc.get(f'mother_maiden_{i}',''))
            st.session_state.inputs_limitedc[f"mother_first_field{i}"],st.session_state.inputs_limitedc[f'mother_first_{i}'] = field_box_template("FIRST NAME", f"FIRST NAME", x_offset=84, value=st.session_state.inputs_limitedc.get(f'mother_first_{i}',''))

            #SECTION 4: TAX REGISTRATION INFORMATION (Complete this section if you are a registered taxpayer)
            st.markdown("<h6 style='text-align: center;'>TAX REGISTRATION INFORMATION (Complete this section if you are a registered taxpayer)</h6>", unsafe_allow_html=True)

            st.session_state.inputs_limitedc[f"tax_office_field{i}"],st.session_state.inputs_limitedc[f'tax_office_{i}'] = field_box_template("CURRENT TAX OFFICE", f"CURRENT TAX OFFICE", value=st.session_state.inputs_limitedc.get(f'tax_office_{i}',''))
            st.session_state.inputs_limitedc[f"old_tin_field{i}"],st.session_state.inputs_limitedc[f'old_tin_{i}'] = field_box_template("OLD TIN NUMBER", f"OLD TIN NUMBER", bpr=10,  value=st.session_state.inputs_limitedc.get(f'old_tin_{i}',''))
            st.session_state.inputs_limitedc[f"tax_fee_field{i}"],st.session_state.inputs_limitedc[f'tax_fee_{i}'] = field_box_template("IRS TAX FILE #", f"IRS TAX FILE #", bpr=19, x_offset=53, value=st.session_state.inputs_limitedc.get(f'tax_fee_{i}',''))

            # SECTION 5: IDENTIFICATION INFORMATION/ check boxes
            st.markdown("<h6 style='text-align: center;'>IDENTIFICATION INFORMATION</h6>", unsafe_allow_html=True)

            options_id = ['National ID', "Voter's ID", "Driver's License (ID # is certificate of competence)", "Passport"]
            st.session_state.inputs_limitedc[f"id_type_field{i}"],st.session_state.inputs_limitedc[f'id_type_{i}'] = field_option_template(options_id, f"ID TYPE (tick one)", value= (st.session_state.inputs_limitedc.get(f'id_type_{i}', "National ID")))
            st.session_state.inputs_limitedc[f"id_num_field{i}"],st.session_state.inputs_limitedc[f'id_num_{i}'] = field_box_template("ID NUMBER", f"ID NUMBER", bpr=16,value=st.session_state.inputs_limitedc.get(f'id_num_{i}',''))

            st.session_state.inputs_limitedc[f"issue_date_field{i}"] = TextBox(10, "ISSUE DATE", x_offset=42, row_height=0, box_width=10, control_x=0.35, y_offset=3)
            get_date_input(f'issue_date_{i}', f"ISSUE DATE")
            st.session_state.inputs_limitedc[f"expiry_date_field{i}"] = TextBox(10, "EXPIRY DATE", x_offset=73, row_height=0, box_width=10, control_x=0.35, y_offset=3)
            get_date_input(f"expiry_d{i}", f"EXPIRY DATE")
            st.session_state.inputs_limitedc[f"country_of_issue_field{i}"],st.session_state.inputs_limitedc[f'country_of_issue_{i}'] = field_box_template("COUNTRY OF ISSUE", f"COUNTRY OF ISSUE", bpr=16, x_offset=67,value=st.session_state.inputs_limitedc.get(f'country_of_issue_{i}',''))
            st.session_state.inputs_limitedc[f"place_of_issue_field{i}"],st.session_state.inputs_limitedc[f'place_of_issue_{i}'] = field_box_template("PLACE OF ISSUE", f"PLACE OF ISSUE", bpr=25, x_offset=93,value=st.session_state.inputs_limitedc.get(f'place_of_issue_{i}',''))

            #SECTION 6: RESIDENTIAL ADDRESS
            st.session_state.inputs_limitedc[f"house_num_field_tax{i}"]= field_box_template("HOUSE NUMBER", bpr=8)
            st.session_state.inputs_limitedc[f"building_name_field_tax{i}"]= field_box_template("BUILDING NAME", bpr=24, x_offset=62)
            # st.session_state.inputs_limitedc[f"postal_field_tax{i}"],st.session_state.inputs_limitedc[f'postal_{i}'] = field_box_template("POSTAL CODE", f"Postal Code", value=st.session_state.inputs_limitedc.get(f'postal_{i}',''))
            st.session_state.inputs_limitedc[f"country_field_tax{i}"]= field_box_template("COUNTRY")
            st.session_state.inputs_limitedc[f"landmark_field_tax{i}"] = field_box_template("STREET NAME/PROMINENT LANDMARK", x_offset=135)
            st.session_state.inputs_limitedc[f"town_city_field_tax{i}"] = field_box_template("TOWN / CITY", bpr=25)
            st.session_state.inputs_limitedc[f"region_field_tax{i}"] = field_box_template("REGION")
            st.session_state.inputs_limitedc[f"district_field_tax{i}"] = field_box_template("DISTRICT")


            if st.session_state.inputs_limitedc[f'postal_address_tax{i}'] == "NO":
                st.markdown("<h6 style='text-align: center;'>POSTAL ADDRESS</h6>", unsafe_allow_html=True)
                st.session_state.inputs_limitedc[f"c_o_field_tax{i}"],st.session_state.inputs_limitedc[f'c_o_{i}'] = field_box_template("C/O", f"C/O", bpr=30, value=st.session_state.inputs_limitedc.get(f'c_o_{i}',''))
                options_postal_type = ["P. 0. BOX", "PMB", "DTD"]
                st.session_state.inputs_limitedc[f"postal_type_taxfield{i}"],st.session_state.inputs_limitedc[f'postal_type_tax{i}'] = field_multi_options(options_postal_type, f"POSTAL TYPE (select as applicable)", value=st.session_state.inputs_limitedc.get(f'postal_type_tax{i}',[]))
                st.session_state.inputs_limitedc[f"postal_num_taxfield{i}"],st.session_state.inputs_limitedc[f'postal_num_tax{i}'] = field_box_template("POSTAL NUMBER", f"POSTAL NUMBER - start with Prefix, followed by number", bpr=13, x_offset=65, value=st.session_state.inputs_limitedc.get(f'postal_num_tax{i}',''))     
                st.session_state.inputs_limitedc[f"box_region_field_tax{i}"],st.session_state.inputs_limitedc[f'box_region_{i}'] = field_box_template("BOX REGION", f"BOX REGION", value=st.session_state.inputs_limitedc.get(f'box_region_{i}',''))
                st.session_state.inputs_limitedc[f"box_town_field{i}"],st.session_state.inputs_limitedc[f'box_town_{i}'] = field_box_template("BOX TOWN", f"BOX TOWN", value=st.session_state.inputs_limitedc.get(f'box_town_{i}',''))
                st.session_state.inputs_limitedc[f"box_location_field{i}"],st.session_state.inputs_limitedc[f'box_location_{i}'] = field_box_template("BOX LOCATION/AREA", f"BOX LOCATION/AREA", value=st.session_state.inputs_limitedc.get(f'box_location_{i}',''))

                
            #SECTION 8: CONTACT METHOD Indicate purpose of contact within the thick outlined box provided (P - Personal; B - Business; H - Home)- work on this to ensure user gets the format

            st.markdown("<h6 style='text-align: center;'>CONTACT METHOD FOR TAX REGISTRATION</h6>", unsafe_allow_html=True)
            st.write('Indicate purpose of contact as Prefix (P - Personal; B - Business; H - Home) for all a under this section')
            option_contact = ['None', 'Personal', 'Home', 'Business']

            
            st.session_state.inputs_limitedc[f"pc{i}"] = st.radio(f'empty{i}', option_contact,label_visibility="hidden",  horizontal=True, index=option_contact.index(st.session_state.inputs_limitedc.get(f"pc{i}", option_contact[0])))
            st.session_state.inputs_limitedc[f"phone_num_taxfield{i}"], st.session_state.inputs_limitedc[f'phone_num_tax{i}'] = field_box_template("PHONE/LANDLINE NUMBER", f"PHONE/LANDLINE NUMBER",x_offset=93, bpr=10, value=st.session_state.inputs_limitedc.get(f'phone_num_tax{i}',''))

            
            st.session_state.inputs_limitedc[f"mc{i}"] = st.radio(f'empty.{i}', option_contact,label_visibility="hidden", horizontal=True, index=option_contact.index(st.session_state.inputs_limitedc.get(f"mc{i}", option_contact[1])))
            st.session_state.inputs_limitedc[f"mobile_num_taxfield{i}"], st.session_state.inputs_limitedc[f'mobile_num_tax{i}'] = field_box_template("MOBILE NUMBER",f"MOBILE NUMBER", bpr=10, x_offset=62, value=st.session_state.inputs_limitedc.get(f'mobile_num_tax{i}',st.session_state.inputs_limitedc.get(f"mobile_num{i}", "")))

            st.session_state.inputs_limitedc[f"fc{i}"] =st.radio(f'empty{i}..',option_contact,label_visibility="hidden", horizontal=True, index=option_contact.index(st.session_state.inputs_limitedc.get(f"fc{i}", option_contact[1])))
            st.session_state.inputs_limitedc[f"fax_num_taxfield{i}"], st.session_state.inputs_limitedc[f'fax_num_tax{i}'] = field_box_template("FAX NUMBER", f"FAX NUMBER", bpr=10, x_offset=93, value=st.session_state.inputs_limitedc.get(f'fax_num_tax{i}',st.session_state.inputs_limitedc.get(f"fax{i}",'')))


            st.session_state.inputs_limitedc[f"ec{i}"] =st.radio(f'empty{i}...',option_contact,label_visibility="hidden", horizontal=True, index=option_contact.index(st.session_state.inputs_limitedc.get(f"ec{i}", option_contact[1])))
            st.session_state.inputs_limitedc[f"email_taxfield{i}"], st.session_state.inputs_limitedc[f'email_tax{i}'] = field_box_template("E-MAIL",f"E-MAIL",x_offset=94, value = st.session_state.inputs_limitedc.get(f'email_tax{i}', st.session_state.inputs_limitedc.get(f"email{i}", "")))

            st.session_state.inputs_limitedc[f"wc{i}"] =st.radio(f'empty{i}....',option_contact,label_visibility="hidden", horizontal=True, index=option_contact.index(st.session_state.inputs_limitedc.get(f"wc{i}", option_contact[0])))
            st.session_state.inputs_limitedc[f"website_taxfield{i}"], st.session_state.inputs_limitedc[f'website_tax{i}'] = field_box_template("WEBSITE", f"WEBSITE",x_offset=94, value=st.session_state.inputs_limitedc.get(f'website_tax{i}',''))

            
            option_contact = ["MOBILE", "EMAIL", "LETTER"]
            st.session_state.inputs_limitedc[f"contact_taxfield{i}"], st.session_state.inputs_limitedc[f'contact_tax{i}'] = field_option_template(), st.radio(f"PREFERRED CONTACT METHOD (Select one)", option_contact, horizontal=True, index=option_contact.index(st.session_state.inputs_limitedc.get(f"contact_tax{i}", option_contact[0])))
            

                #SECTION 9: BUSINESS ( COMPLETE THIS SECTION IF YOU ARE SELF EMPLOYED)  
            # SECTION: BUSINESS
            if st.session_state.inputs_limitedc[f"self_employed_{i}"]  == "YES":
                st.markdown("<h6 style='text-align: center;'>BUSINESS</h6>", unsafe_allow_html=True)
                st.session_state.inputs_limitedc[f"business_nature_taxfield{i}"],st.session_state.inputs_limitedc[f'business_nature_tax{i}'] = field_plain_template( f"NATURE OF BUSINESS", "NATURE OF BUSINESS",maxi= 70, c_x=95, value=st.session_state.inputs_limitedc.get(f'business_nature_tax{i}',''))
                st.session_state.inputs_limitedc[f"annual_field{i}"],st.session_state.inputs_limitedc[f'annual_{i}'] = field_box_template("ANNUAL TURNOVER IN GH¢", f"ANNUAL TURNOVER IN GH¢", bpr=13, value=st.session_state.inputs_limitedc.get(f'annual_{i}',''))
                st.session_state.inputs_limitedc[f"num_employee_field{i}"],st.session_state.inputs_limitedc[f'num_employee_{i}'] = field_box_template("NO. OF EMPLOYEES", f"NO. OF EMPLOYEES", bpr=15, x_offset=73, value=st.session_state.inputs_limitedc.get(f'num_employee_{i}',''))
                if st.session_state.inputs_limitedc[f'registered_{i}'] == "YES":
                    st.session_state.inputs_limitedc[f"reg_buss_field{i}"],st.session_state.inputs_limitedc[f'reg_buss_{i}'] = field_plain_template(f"BUSINESS NAME", "BUSINESS NAME", maxi=57, c_x=-125,c_y=20, value=st.session_state.inputs_limitedc.get(f'reg_buss_{i}',''))
                    st.session_state.inputs_limitedc[f"reg_tin_field{i}"],st.session_state.inputs_limitedc[f'reg_tin_{i}'] = field_box_template("OLD TIN", f"OLD TIN", bpr=9, x_offset=-38, y_offset=17, value=st.session_state.inputs_limitedc.get(f'reg_tin_{i}',''))
                    st.session_state.inputs_limitedc[f"reg_rgd_field{i}"],st.session_state.inputs_limitedc[f'reg_rgd_{i}'] = field_box_template("RGD NUMBER", f"RGD NUMBER", bpr=8, x_offset=-18, y_offset=16, value=st.session_state.inputs_limitedc.get(f'reg_rgd_{i}',''))
              
            #     st.markdown("<h6 style='text-align: center;'>BUSINESS ADDRESS</h6>", unsafe_allow_html=True)
                st.session_state.inputs_limitedc[f"reg_house_field{i}"],st.session_state.inputs_limitedc[f'reg_house_{i}'] = field_box_template("HOUSE NUMBER", f"HOUSE NUMBER", bpr=9, value=st.session_state.inputs_limitedc.get(f'reg_house_{i}',''))
                st.session_state.inputs_limitedc[f"reg_build_field{i}"],st.session_state.inputs_limitedc[f'reg_build_{i}'] = field_box_template("BUILDING NAME", f"BUILDING NAME", bpr=22, x_offset=63, value=st.session_state.inputs_limitedc.get(f'reg_build_{i}',''))
                st.session_state.inputs_limitedc[f"reg_street_field{i}"],st.session_state.inputs_limitedc[f'reg_street_{i}'] = field_box_template("STREET NAME/PROMINENT LANDMARK", f"STREET NAME/PROMINENT LANDMARK", bpr=29, x_offset=135, value=st.session_state.inputs_limitedc.get(f'reg_street_{i}',''))
                st.session_state.inputs_limitedc[f"reg_town_field{i}"],st.session_state.inputs_limitedc[f'reg_town_{i}'] = field_box_template("TOWN / CITY", f"TOWN / CITY", bpr=36, value=st.session_state.inputs_limitedc.get(f'reg_town_{i}',''))
                st.session_state.inputs_limitedc[f"reg_location_field{i}"],st.session_state.inputs_limitedc[f'reg_location_{i}'] = field_box_template("LOCATION / AREA", f"LOCATION / AREA",value=st.session_state.inputs_limitedc.get(f'reg_location_{i}',''))
                st.session_state.inputs_limitedc[f"reg_postal_field_tax{i}"],st.session_state.inputs_limitedc[f'reg_postal_{i}'] = field_box_template("POSTAL CODE", f"POSTAL CODE", bpr=10,value=st.session_state.inputs_limitedc.get(f'reg_postal_{i}',''))
                st.session_state.inputs_limitedc[f"reg_country_field_tax{i}"],st.session_state.inputs_limitedc[f'reg_country_{i}'] = field_box_template("COUNTRY", f"COUNTRY", bpr=25,value=st.session_state.inputs_limitedc.get(f'reg_country_{i}',''))
                st.session_state.inputs_limitedc[f"reg_region_field_tax{i}"],st.session_state.inputs_limitedc[f'reg_region_{i}'] = field_box_template("REGION", f"REGION", bpr=36, value=st.session_state.inputs_limitedc.get(f'reg_region_{i}',''))
                st.session_state.inputs_limitedc[f"reg_district_field_tax{i}"],st.session_state.inputs_limitedc[f'reg_district_{i}'] = field_box_template("DISTRICT", f"DISTRICT", bpr=36, value=st.session_state.inputs_limitedc.get(f'reg_district_{i}',''))
     
            st.session_state.inputs_limitedc[f"declare_field_tax"] = PDFTextFinder("declare that the information", 35, control_x=-192)
            st.session_state.inputs_limitedc[f"declare_date_taxfield"] = TextBox(10, "DATE", x_offset=21, row_height=0, box_width=10, control_x=0.35, y_offset=3)
                # get_date_input(f'declare_date_tax', f"DATE_")

    else:
        pdf_file = 'backend/limited_company/data/Taxpayer-registration-form-individual.pdf'
        doc = fitz.open(pdf_file)
        page = doc[0]
        page1 = doc[1]
    
        st.session_state.inputs_limitedc[f"tax_payer_field{i}"].fill_option(page,st.session_state.inputs_limitedc[f"tax_payer_{i}"])
        for category_item in st.session_state.inputs_limitedc[f"category_{i}"]:
            st.session_state.inputs_limitedc[f"category_field{i}"].fill_option(page, category_item)

        if "Other" in st.session_state.inputs_limitedc[f"category_{i}"]:
            st.session_state.inputs_limitedc[f"specify_field{i}"].fill_field(page, st.session_state.inputs_limitedc[f"specify_{i}"].upper())


        if "Employee" in st.session_state.inputs_limitedc[f"category_{i}"] or 'Foreign mission employee' in st.session_state.inputs_limitedc[f"category_{i}"]:
            st.session_state.inputs_limitedc[f"employer_field{i}"].fill_field(page, st.session_state.inputs_limitedc[f"employer_{i}"].upper())

        # SECTION 3: PERSONAL DETAILS
        st.session_state.inputs_limitedc[f"title_field_tax{i}"].fill_option(page, st.session_state.inputs_limitedc[f"title_{i}"].strip().upper())
        if st.session_state.inputs_limitedc[f"title_{i}"] == "OTHER": 
            st.session_state.inputs_limitedc[f"title_field_tax{i}"].fill_option(page, "OTHER", ind=2)
            st.session_state.inputs_limitedc[f"specify_title_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f"specify_title_{i}"].upper(), 1)
        st.session_state.inputs_limitedc[f"first_name_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f'first_name{pn}'].upper(), fs=8)
        st.session_state.inputs_limitedc[f"middle_name_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f'middle_name{pn}'].upper(), fs=8)
        st.session_state.inputs_limitedc[f"last_name_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f'last_name{pn}'].upper(), fs=8)
        st.session_state.inputs_limitedc[f"gender_field_tax{i}"].fill_option(page, st.session_state.inputs_limitedc[f"gender{i}"].strip().upper())
        st.session_state.inputs_limitedc[f"occupation_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f"occupation{i}"].upper(), fs=8)
        st.session_state.inputs_limitedc[f"dob_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f"dob{i}"].strftime('%d%m%y'))
        st.session_state.inputs_limitedc[f"nationality_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f"nationality{i}"].upper(), fs=8)

        st.session_state.inputs_limitedc[f"previous_name_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f"former_name{i}"].upper(), fs=8)
                    
        st.session_state.inputs_limitedc[f"marital_field{i}"].fill_option(page, st.session_state.inputs_limitedc[f"marital_{i}"])

        st.session_state.inputs_limitedc[f"birth_town_field{i}"].fill_field(page, st.session_state.inputs_limitedc[f"birth_town_{i}"].upper(), fs=8)
        st.session_state.inputs_limitedc[f"birth_country_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f"birth_country_{i}"].upper(), fs=8)
        st.session_state.inputs_limitedc[f"birth_region_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f"birth_region_{i}"].upper(), fs=8)
        st.session_state.inputs_limitedc[f"birth_district_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f"birth_district_{i}"].upper(), fs=8)
        st.session_state.inputs_limitedc[f"residents_field_tax{i}"].fill_option(page, st.session_state.inputs_limitedc[f"residents_{i}"].upper(), 1)
        st.session_state.inputs_limitedc[f"security_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f"security_{i}"].upper(), fs=8)

        for info_item in st.session_state.inputs_limitedc[f"info_{i}"]:
            st.session_state.inputs_limitedc[f"info_field{i}"].fill_option(page, info_item)

        st.session_state.inputs_limitedc[f"mother_maiden_field{i}"].fill_field(page, st.session_state.inputs_limitedc[f"mother_maiden_{i}"].upper(), fs=8)
        st.session_state.inputs_limitedc[f"mother_first_field{i}"].fill_field(page, st.session_state.inputs_limitedc[f"mother_first_{i}"].upper(), 1, fs=8)

        # SECTION 4: TAX REGISTRATION INFORMATION
        st.session_state.inputs_limitedc[f"tax_office_field{i}"].fill_field(page, st.session_state.inputs_limitedc[f"tax_office_{i}"].upper(), fs=8)
        st.session_state.inputs_limitedc[f"old_tin_field{i}"].fill_field(page, st.session_state.inputs_limitedc[f"old_tin_{i}"].upper())
        st.session_state.inputs_limitedc[f"tax_fee_field{i}"].fill_field(page, st.session_state.inputs_limitedc[f"tax_fee_{i}"].upper(), fs=8)

        # SECTION 5: IDENTIFICATION INFORMATION
        st.session_state.inputs_limitedc[f"id_type_field{i}"].fill_option(page, st.session_state.inputs_limitedc[f"id_type_{i}"])
        st.session_state.inputs_limitedc[f"id_num_field{i}"].fill_field(page, st.session_state.inputs_limitedc[f"id_num_{i}"].upper(), fs=8)
        st.session_state.inputs_limitedc[f"issue_date_field{i}"].fill_field(page, st.session_state.inputs_limitedc[f"issue_date_{i}"].strftime("%d-%m-%Y"))
        st.session_state.inputs_limitedc[f"expiry_date_field{i}"].fill_field(page, st.session_state.inputs_limitedc[f"expiry_d{i}"].strftime("%d-%m-%Y"))
        st.session_state.inputs_limitedc[f"place_of_issue_field{i}"].fill_field(page, st.session_state.inputs_limitedc[f"place_of_issue_{i}"].upper(), fs=8)
        st.session_state.inputs_limitedc[f"country_of_issue_field{i}"].fill_field(page, st.session_state.inputs_limitedc[f"country_of_issue_{i}"].upper(), fs=8)
    
        # SECTION 6: RESIDENTIAL ADDRESS
        st.session_state.inputs_limitedc[f"house_num_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f"house_num{i}"].upper(), fs=8)
        st.session_state.inputs_limitedc[f"building_name_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f'house_address{i}'].upper(), fs=8)
        st.session_state.inputs_limitedc[f"landmark_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f"street_name{i}"].upper(), fs=8)
        st.session_state.inputs_limitedc[f"town_city_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f"city{i}"].upper(), fs=8)
        st.session_state.inputs_limitedc[f"location_area_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f"location_area_{i}"].upper(), fs=8)
        st.session_state.inputs_limitedc[f"postal_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f"postal_{i}"].upper(), fs=8)
        st.session_state.inputs_limitedc[f"country_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f"country{i}"].upper(), 1, fs=8)
        st.session_state.inputs_limitedc[f"region_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f"region{i}"].upper(), 1, fs=8)
        st.session_state.inputs_limitedc[f"district_field_tax{i}"].fill_field(page, st.session_state.inputs_limitedc[f"district{i}"].upper(), 1, fs=8)
       

        # SECTION 7: POSTAL ADDRESS
      
        if st.session_state.inputs_limitedc[f"postal_address_tax{i}"] == "YES":
            st.session_state.inputs_limitedc[f"postal_address_taxfield{i}"].fill_option(page1, "TICK IF SAME AS RESIDENTIAL ADDRESS")
        else:
            st.session_state.inputs_limitedc[f"c_o_field_tax{i}"].fill_field(page1, st.session_state.inputs_limitedc[f"c_o_{i}"])
            for item in st.session_state.inputs_limitedc[f'postal_type_tax{i}'] :
                st.session_state.inputs_limitedc[f"postal_type_taxfield{i}"].fill_option(page1, item)
            st.session_state.inputs_limitedc[f"postal_num_taxfield{i}"].fill_field(page1, st.session_state.inputs_limitedc[f"postal_num_tax{i}"].upper(), fs=8)
            st.session_state.inputs_limitedc[f"box_region_field_tax{i}"].fill_field(page1, st.session_state.inputs_limitedc[f"box_region_{i}"].upper(), fs=8)
            st.session_state.inputs_limitedc[f"box_town_field{i}"].fill_field(page1, st.session_state.inputs_limitedc[f"box_town_{i}"].upper(), fs=8)
            st.session_state.inputs_limitedc[f"box_location_field{i}"].fill_field(page1, st.session_state.inputs_limitedc[f"box_location_{i}"].upper(), fs=8)

        # SECTION 8: CONTACT METHOD
        if  st.session_state.inputs_limitedc[f"phone_num_tax{i}"]:
            st.session_state.inputs_limitedc[f"phone_num_taxfield{i}"].fill_field(page1, st.session_state.inputs_limitedc[f"pc{i}"][0] +' '+st.session_state.inputs_limitedc[f"phone_num_tax{i}"].upper(), fs=9)
        if st.session_state.inputs_limitedc[f"mobile_num_tax{i}"]:            
            st.session_state.inputs_limitedc[f"mobile_num_taxfield{i}"].fill_field(page1,st.session_state.inputs_limitedc[f"mc{i}"][0] +' '+ st.session_state.inputs_limitedc[f"mobile_num_tax{i}"].upper(), fs=9)
        if st.session_state.inputs_limitedc[f"fax_num_tax{i}"]:
            st.session_state.inputs_limitedc[f"fax_num_taxfield{i}"].fill_field(page1,st.session_state.inputs_limitedc[f"fc{i}"][0] +' '+ st.session_state.inputs_limitedc[f"fax_num_tax{i}"].upper(), fs=9)
        if st.session_state.inputs_limitedc[f"email_tax{i}"]:
            st.session_state.inputs_limitedc[f"email_taxfield{i}"].fill_field(page1,st.session_state.inputs_limitedc[f"ec{i}"][0] +' '+ st.session_state.inputs_limitedc[f"email_tax{i}"], fs=8)
        if st.session_state.inputs_limitedc[f"website_tax{i}"]:
            st.session_state.inputs_limitedc[f"website_taxfield{i}"].fill_field(page1,st.session_state.inputs_limitedc[f"wc{i}"][0] +' '+ st.session_state.inputs_limitedc[f"website_tax{i}"], fs=8)
        new = ["LETTER", "EMAIL"]
        st.session_state.inputs_limitedc[f"contact_taxfield{i}"].fill_option(page1, st.session_state.inputs_limitedc[f"contact_tax{i}"], 0 if st.session_state.inputs_limitedc[f"contact_tax{i}"] in new else 1)

        #SECTION 9: BUSINESS ( COMPLETE THIS SECTION IF YOU ARE SELF EMPLOYED)  
     
      
        if st.session_state.inputs_limitedc[f"self_employed_{i}"] == "YES":
            st.session_state.inputs_limitedc[f"business_nature_taxfield{i}"].fill_field(page1, st.session_state.inputs_limitedc[f"business_nature_tax{i}"].upper(), fs=8)
            st.session_state.inputs_limitedc[f"annual_field{i}"].fill_field(page1, st.session_state.inputs_limitedc[f"annual_{i}"].upper(), fs=9)
            st.session_state.inputs_limitedc[f"num_employee_field{i}"].fill_field(page1, st.session_state.inputs_limitedc[f"num_employee_{i}"].upper(), fs=9)
            
            if st.session_state.inputs_limitedc[f"registered_{i}"] == "YES":
                    st.session_state.inputs_limitedc[f"registered_field{i}"].fill_option(page1, st.session_state.inputs_limitedc[f"registered_{i}"])
                    st.session_state.inputs_limitedc[f"reg_buss_field{i}"].fill_field(page1, st.session_state.inputs_limitedc[f"reg_buss_{i}"].upper(), 1, fs=8)
                    st.session_state.inputs_limitedc[f"reg_tin_field{i}"].fill_field(page1, st.session_state.inputs_limitedc[f"reg_tin_{i}"])
                    st.session_state.inputs_limitedc[f"reg_rgd_field{i}"].fill_field(page1, st.session_state.inputs_limitedc[f'reg_rgd_{i}'])
            else:
                    st.session_state.inputs_limitedc[f"registered_field{i}"].fill_option(page1, st.session_state.inputs_limitedc[f"registered_{i}"], 2)
            st.session_state.inputs_limitedc[f"reg_house_field{i}"].fill_field(page1, st.session_state.inputs_limitedc[f"reg_house_{i}"].upper(), fs=8)
            st.session_state.inputs_limitedc[f"reg_build_field{i}"].fill_field(page1, st.session_state.inputs_limitedc[f"reg_build_{i}"].upper(), fs=8)
            st.session_state.inputs_limitedc[f"reg_street_field{i}"].fill_field(page1, st.session_state.inputs_limitedc[f"reg_street_{i}"].upper(), fs=8)
            st.session_state.inputs_limitedc[f"reg_town_field{i}"].fill_field(page1, st.session_state.inputs_limitedc[f"reg_town_{i}"].upper(), fs=8)
            st.session_state.inputs_limitedc[f"reg_location_field{i}"].fill_field(page1, st.session_state.inputs_limitedc[f"reg_location_{i}"].upper(), fs=8)
            st.session_state.inputs_limitedc[f"reg_postal_field_tax{i}"].fill_field(page1, st.session_state.inputs_limitedc[f"reg_postal_{i}"].upper(), fs=8)
            st.session_state.inputs_limitedc[f"reg_country_field_tax{i}"].fill_field(page1, st.session_state.inputs_limitedc[f"reg_country_{i}"].upper(), fs=8)
            st.session_state.inputs_limitedc[f"reg_region_field_tax{i}"].fill_field(page1, st.session_state.inputs_limitedc[f"reg_region_{i}"].upper(), 1, fs=8)
            st.session_state.inputs_limitedc[f"reg_district_field_tax{i}"].fill_field(page1, st.session_state.inputs_limitedc[f"reg_district_{i}"].upper(), fs=8)

        st.session_state.inputs_limitedc[f"declare_name{i}"] = f"{ st.session_state.inputs_limitedc[f'first_name{pn}']} { st.session_state.inputs_limitedc[f'middle_name{pn}']} {st.session_state.inputs_limitedc[f'last_name{pn}']}"
        st.session_state.inputs_limitedc[f"declare_date_tax"]=datetime.now().date()
        st.session_state.inputs_limitedc[f"declare_field_tax"].fill_field(page1, st.session_state.inputs_limitedc[f"declare_name{i}"].upper(), 1, fs=8)
        st.session_state.inputs_limitedc[f"declare_date_taxfield"].fill_field(page1, st.session_state.inputs_limitedc[f"declare_date_tax"].strftime("%d-%m-%Y"))

        if  st.session_state.inputs_limitedc[f"third_party_tax{i}"] == 'Third Party': 
            st.session_state.inputs_limitedc[f"third_party_field"].fill_field(page1, st.session_state.inputs_limitedc[f'third_party'].upper())
            st.session_state.inputs_limitedc[f"tp_date_field"].fill_field(page1, st.session_state.inputs_limitedc[f'tp_d'].strftime("%d-%m-%Y"), 1)
            st.session_state.inputs_limitedc[f"tp_tin_field"].fill_field(page1, st.session_state.inputs_limitedc[f"tp_tin"].upper())
            st.session_state.inputs_limitedc[f"tp_cell_field"].fill_field(page1, st.session_state.inputs_limitedc[f"tp_cell"].upper())
        # else:
           
        taxx = f"outputlc/taxform-{label}-{st.session_state.inputs_limitedc[f'first_name{pn}']} {st.session_state.inputs_limitedc[f'last_name{pn}']}.pdf"
        doc.save(taxx)
        doc.close()
        l.append(taxx)
        





 
      








def generate_form(page):
    if page==1:
        st.write("""Note the following:\n
    • Director/Secretary: Can hold multiple positions except for Auditor
    • Directors: Min 2, Max 4.
    • Secretary: Must have exactly 1 (either an individual or a body corporate).
    • Subscribers: Min 1, Max 4(either individuals or a body corporates).
    """)
        option_cop =["Corporate Body", "Individual"]
        st.session_state.inputs_limitedc["dir_num"] = st.number_input("How many directors are managing the company?", min_value=2,max_value=4, value=st.session_state.inputs_limitedc.get("dir_num", 2))
        st.session_state.inputs_limitedc["dirsub"] = st.number_input("How many of the directors are also shareholders (owners) of the company?", min_value=0,max_value=4, value=st.session_state.inputs_limitedc.get("dirsub", 0))
        st.session_state.inputs_limitedc["secretary_cop"] = st.radio("Is the Company Secretary a person or an organization?", option_cop, horizontal=True, index=option_cop.index(st.session_state.inputs_limitedc.get("secretary_cop",option_cop[0])))
        st.session_state.inputs_limitedc[f'secsubques'] = st.radio(f" Is the Company Secretary also a shareholder of the company?",['Yes', 'No'], horizontal=True, index=['Yes', 'No'].index(st.session_state.inputs_limitedc.get('secsubques', 'Yes')))
        st.session_state.inputs_limitedc["indsub"] = st.number_input("How many individuals own shares in the company but are not Directors or the Secretary?", min_value=0,max_value=4, value=st.session_state.inputs_limitedc.get("indsub", 0))
        st.session_state.inputs_limitedc["copsub"] = st.number_input("How many organizations own shares in the company but are not Directors or the Secretary?", min_value=0,max_value=4, value=st.session_state.inputs_limitedc.get("copsub", 0))
        st.write("In the absence of a stamp or a seal of  the company, the signature of two  directors and a Company Secretary are  needed for authentication purposes Reference to section 150 (1) (D)(ii ) of  Act 992")
        st.session_state.inputs_limitedc["authenticatexx"] = st.radio("Does the company use an official seal or stamp for documents?", option_yesno, horizontal=True, index=option_yesno.index(st.session_state.inputs_limitedc.get("authenticatexx",option_yesno[0])))
        options_revenue = ["Apply for BOP Later", "Already have a BOP"]
        st.session_state.inputs_limitedc["apply_bop_field"], st.session_state.inputs_limitedc["apply_bop"] = PDFOptionField(control_x=17, control_y=4), st.radio("Does the company already have a Business Operating Permit (BOP), or will it apply for one later?",options_revenue, horizontal=True, index = options_revenue.index(st.session_state.inputs_limitedc.get("apply_bop",options_revenue[0])))
        st.session_state.inputs_limitedc["illiterate"] = st.radio("Is there any Director, Secretary or Subscriber in the company who cannot read or write?",option_yesno, horizontal=True, index = option_yesno.index(st.session_state.inputs_limitedc.get("illiterate",option_yesno[0])))
        subs = 1 if st.session_state.inputs_limitedc[f'secsubques'] == 'Yes' else 0
        if st.session_state.inputs_limitedc["indsub"] +  st.session_state.inputs_limitedc["copsub"] + st.session_state.inputs_limitedc["dirsub"] + subs > 4:
            st.warning('Subscribers must sum up to four or less')
        if st.session_state.inputs_limitedc["dirsub"]> st.session_state.inputs_limitedc["dir_num"]:
            st.warning('Directors who are subscribers can\'t be more than the total number of directors')
        if st.session_state.inputs_limitedc["indsub"] +  st.session_state.inputs_limitedc["copsub"] + st.session_state.inputs_limitedc["dirsub"] + subs < 1:
            st.warning('The company must have at least one subscriber')
        if st.session_state.inputs_limitedc["secretary_cop"] =='Individual' :
            st.session_state.inputs_limitedc['sec_num'] =2
        else:
            st.session_state.inputs_limitedc['sec_num'] =1
        
    elif page==2:
        option_bene = ["Publicly Listed Company","Government"]
        option_subs = ['Yes', 'No']
        st.markdown(f"<h4 style='text-align: center;'>Information About Company Entities</h4>", unsafe_allow_html=True)
        option_title = [" Mr ", " Mrs ", " Miss ", " Ms ", " Dr "]
        ##############DIRECTOR
        st.markdown("### Directors")
        check =  st.session_state.inputs_limitedc["dirsub"]
        for i in range(1, st.session_state.inputs_limitedc["dir_num"]+1):
            st.session_state.inputs_limitedc[f"title{i}"] = st.radio(f"Choose title{i*' '}", option_title, horizontal=True, index=option_title.index(st.session_state.inputs_limitedc.get(f"title{i}",option_title[0])))
            st.session_state.inputs_limitedc[f"first_name{i}"]=st.text_input(f"First Name*{i*' '}", value=st.session_state.inputs_limitedc.get(f"first_name{i}",''), max_chars=17)
            st.session_state.inputs_limitedc[f"middle_name{i}"]=st.text_input(f"Middle Name{i*' '}", value=st.session_state.inputs_limitedc.get(f"middle_name{i}",''), max_chars=17) 
            st.session_state.inputs_limitedc[f"last_name{i}"]=st.text_input(f"Last Name*{i*' '}", value=st.session_state.inputs_limitedc.get(f"last_name{i}",''), max_chars=17)
            if check > 0:         
                st.session_state.inputs_limitedc[f'dirsub{i}'] = st.radio(f"Are the shares held on behalf of a minor?{i*' '}",option_subs, horizontal=True, index=option_subs.index(st.session_state.inputs_limitedc.get(f'dirsub{i}', option_subs[0])))
                check -= 1
            st.write('-'*20)
            

        st.markdown("### Secretary")
        #################SECRETARY
        if st.session_state.inputs_limitedc[f'secretary_cop'] == 'Individual':
            st.session_state.inputs_limitedc[f"titlex"] = st.radio(f"Choose title", option_title, horizontal=True, index=option_title.index(st.session_state.inputs_limitedc.get(f"title{i}",option_title[0])))
            st.session_state.inputs_limitedc[f"first_namex"]=st.text_input(f"First Name*", value=st.session_state.inputs_limitedc.get(f"first_namex",''), max_chars=17)
            st.session_state.inputs_limitedc[f"middle_namex"]=st.text_input(f"Middle Name", value=st.session_state.inputs_limitedc.get(f"middle_namex",''), max_chars=17) 
            st.session_state.inputs_limitedc[f"last_namex"]=st.text_input(f"Last Name*", value=st.session_state.inputs_limitedc.get(f"last_namex",''), max_chars=17)
            if st.session_state.inputs_limitedc[f'secsubques'] == 'Yes':
                st.session_state.inputs_limitedc[f'subtrustques'] = st.radio(f"Are the shares held on behalf of a minor?",['Yes', 'No'], horizontal=True, index=['Yes', 'No'].index(st.session_state.inputs_limitedc.get(f'subtrustques', 'Yes')))         
        else:
            st.session_state.inputs_limitedc[f"coporate_name_field"], st.session_state.inputs_limitedc[f"coporate_name"]= boxes("Corporate Name*",label=f"Enter name of Corporate Body*", find=f"coporate_name", t_row=2)
            if st.session_state.inputs_limitedc[f'secsubques'] == 'Yes':
                st.session_state.inputs_limitedc[f'subtrustques'] = st.radio(f"Are the shares held on behalf of a minor?",['Yes', 'No'], horizontal=True, index=['Yes', 'No'].index(st.session_state.inputs_limitedc.get(f'subtrustques', 'Yes')))
                st.session_state.inputs_limitedc[f"bene_type"] = st.radio(f"Type the Beneficial Owner falls under", option_bene,horizontal=True, index=option_bene.index(st.session_state.inputs_limitedc.get(f"bene_type", option_bene[0])))
        st.write('-'*20)

        st.markdown("### Auditor")
        ################AUDITOR
        st.session_state.inputs_limitedc["auditor_firm_name"]= st.text_input("Auditor's Firm Name*",max_chars=17*6, value=st.session_state.inputs_limitedc.get("auditor_firm_name", '')) 
        st.write('-'*20)
      
        #############ADDITIONAL SUBSCRIBERS 
        subs = 1 if st.session_state.inputs_limitedc[f'secsubques'] == 'Yes' else 0
        if st.session_state.inputs_limitedc["indsub"] +  st.session_state.inputs_limitedc["copsub"] + st.session_state.inputs_limitedc["dirsub"] + subs <= 4 and (st.session_state.inputs_limitedc["indsub"]!=0 or st.session_state.inputs_limitedc["copsub"]!=0):
            st.markdown("### Subscribers")
          
            for i in range(st.session_state.inputs_limitedc["dir_num"]+1,  st.session_state.inputs_limitedc["dir_num"]+st.session_state.inputs_limitedc["indsub"]+1):
                st.write(f"Individual")
                st.session_state.inputs_limitedc[f"title{i}"] = st.radio(f"Choose title{i*' '}", option_title, horizontal=True, index=option_title.index(st.session_state.inputs_limitedc.get(f"title{i}",option_title[0])))
                st.session_state.inputs_limitedc[f"first_name{i}"]=st.text_input(f"First Name*{i*' '}", value=st.session_state.inputs_limitedc.get(f"first_name{i}",''), max_chars=17)
                st.session_state.inputs_limitedc[f"middle_name{i}"]=st.text_input(f"Middle Name{i*' '}", value=st.session_state.inputs_limitedc.get(f"middle_name{i}",''), max_chars=17) 
                st.session_state.inputs_limitedc[f"last_name{i}"]=st.text_input(f"Last Name*{i*' '}", value=st.session_state.inputs_limitedc.get(f"last_name{i}",''), max_chars=17)               
                st.session_state.inputs_limitedc[f'subtrustques{i}'] = st.radio(f"Are the shares held on behalf of a minor?{i*' '}",['Yes', 'No'], horizontal=True, index=['Yes', 'No'].index(st.session_state.inputs_limitedc.get(f'subtrustques{i}', 'Yes')))
                st.write('-'*20)

            for i in range(st.session_state.inputs_limitedc["dir_num"]+st.session_state.inputs_limitedc["indsub"]+1, st.session_state.inputs_limitedc["dir_num"]+st.session_state.inputs_limitedc["indsub"]+st.session_state.inputs_limitedc["copsub"]+1):
                st.write("Corporate Body")
                st.session_state.inputs_limitedc[f"coporate_name_field{i}"], st.session_state.inputs_limitedc[f"coporate_name{i}"]= boxes("Corporate Name*",label=f"Enter name of Corporate Body*{i*' '}", find=f"coporate_name{i}", t_row=3)
                st.session_state.inputs_limitedc[f"bene_type{i}"] = st.radio(f"Type the Beneficial Owner falls under{' '*i}", option_bene,horizontal=True, index=option_bene.index(st.session_state.inputs_limitedc.get(f"bene_type{i}", option_bene[0])))
                st.session_state.inputs_limitedc[f'subtrustques{i}'] = st.radio(f"Are the shares held on behalf of a minor?{i*' '}",['Yes', 'No'], horizontal=True, index=['Yes', 'No'].index(st.session_state.inputs_limitedc.get(f'subtrustques{i}', 'Yes')))
                st.write('-'*20)
        if st.session_state.inputs_limitedc["indsub"] or  st.session_state.inputs_limitedc["copsub"] or st.session_state.inputs_limitedc["dirsub"]  or st.session_state.inputs_limitedc[f'secsubques']=='Yes' :
            st.write("""There are no natural persons, listed companies or government-owned companies that meet the definitions of a beneficial owner and
                    the applicable reporting threshold, AND there are no natural persons, publicly listed companies, or government-owned companies with
                    the right to exercise direct or indirect influence or control over the company as defined.""")
        st.session_state.inputs_limitedc[f"no_bene_field"], st.session_state.inputs_limitedc[f"no_bene"] = PDFOptionField(control_x=10, control_y=4), st.radio(f"No bene", ['True', 'False'],label_visibility="hidden" ,horizontal=True, index=['True', 'False'].index(st.session_state.inputs_limitedc.get(f"no_bene", ['True', 'False'][0])))

        

        st.markdown(f"<h6 style='text-align: center;'> The form must be signed by all subscribers in the presence of a witness, who shall attest to the signing. Enter the details of the witness below.</h4>", unsafe_allow_html=True)
        get_date_input("dob_witness", "Date*")
        st.session_state.inputs_limitedc["dob_witness_field"]= boxes("Date*")
        st.session_state.inputs_limitedc["fullname_witness_field"], st.session_state.inputs_limitedc["fullname_witness"]= boxes("Full Name*",label=f"Full Name*", find="fullname_witness", t_row=2)
        st.session_state.inputs_limitedc["adress_field"], st.session_state.inputs_limitedc["adress"]= boxes("Address*",label='Address*', find="adress", t_row=3)
        st.session_state.inputs_limitedc["occupation_witness_field"], st.session_state.inputs_limitedc["occupation_witness"]= boxes("Occupation*",label=f"Occupation*", find=f"occupation_witness")
        if st.session_state.inputs_limitedc["illiterate"] == "YES":
            st.markdown("<h6 style='text-align: center;'>Details of the individual that would assist with the reading and writing of the form to applicants who cannot read or write.</h6>", unsafe_allow_html=True)
            st.session_state.inputs_limitedc[f'illiterate_h_field'], st.session_state.inputs_limitedc[f'illiterate_h'] = field_plain_template("Full name of individual providing assistance", "resident of .", 26, -240,7, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f'illiterate_h',''))
            st.session_state.inputs_limitedc[f'illiterate_resident_field'], st.session_state.inputs_limitedc[f'illiterate_resident'] = field_plain_template("Resident:", "resident of .",16 , 55,7, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f'illiterate_resident',''))
            st.session_state.inputs_limitedc[f'illiterate_language_field'], st.session_state.inputs_limitedc[f'illiterate_language'] = field_plain_template("Language read in", "resident of .",45, -100,19, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f'illiterate_language',''))
            st.session_state.inputs_limitedc[f'illiterate_field'],  st.session_state.inputs_limitedc['illiterate_names'] = field_plain_template('List names of Director/Secretary/Subscriber/Trustee that cannot read or write, seperate names with comma.', "resident of .",57 ,-225,33, r_h=0,t_rows=1, value=st.session_state.inputs_limitedc.get('illiterate_names', ''))
                    
        # st.session_state.inputs_limitedc[f"third_party_tax{i}"] == 'Third Party':    
        st.markdown("<h6 style='text-align: center;'>THIRD PARTY COMPLETION FOR TAX FORM (Optional)</h6>", unsafe_allow_html=True)
        st.session_state.inputs_limitedc[f"third_party_field"], st.session_state.inputs_limitedc[f'third_party'] = field_plain_template("Full name of the third party submitting or completing the tax form application","THIRD PARTY COMPLETION OF FORM",27, -29,c_y=19, t_rows=1, r_h=0, value=st.session_state.inputs_limitedc.get(f'third_party',''))
        st.session_state.inputs_limitedc[f"tp_tin_field"],st.session_state.inputs_limitedc[f'tp_tin'] = field_box_template("CELL NUMBER", f"TIN", bpr=11, x_offset=-123, value=st.session_state.inputs_limitedc.get(f'tp_tin',''))
        st.session_state.inputs_limitedc[f"tp_cell_field"],st.session_state.inputs_limitedc[f'tp_cell'] = field_box_template("CELL NUMBER", f"CELL NUMBER", bpr=10, x_offset=52, value=st.session_state.inputs_limitedc.get(f'tp_cell',''))
        st.session_state.inputs_limitedc[f"tp_date_field"] = TextBox(10, "DATE", x_offset=21, row_height=0, box_width=10, control_x=0.35, y_offset=3)     
        get_date_input(f'tp_d', f"DATE:")
        
    elif page==3:
        st.markdown("### About the company")
    ####SECTION A
        option_constitution = ["Registered Constitution", "Standard Constitution"]
        purpose_of_ownership = ["Registration of a new company","Submission of Annual Returns","Company Update / Amendments","Other (Please specify)"]
        st.session_state.inputs_limitedc[f"bopurpose_field"], st.session_state.inputs_limitedc[f"bopurpose"] = field_option_template(purpose_of_ownership,label="Purpose of Beneficial Ownership Information Submission (Please select)", control_x=20, control_y=7, value=st.session_state.inputs_limitedc.get(f'bopurpose', purpose_of_ownership[0]))
        st.session_state.inputs_limitedc[f'boother_field'], st.session_state.inputs_limitedc[f'boother'] = field_plain_template("If Other (Please specify)", 'Other (Please specify)',40, 5,22, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f"boother",''))
        st.session_state.inputs_limitedc[f'botin_field'], st.session_state.inputs_limitedc[f'botin'] = field_plain_template('TIN of Company (if any)',"TIN of Company (if any):",  20,0,30, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f"botin",''))
        st.session_state.inputs_limitedc[f'borgd_field'], st.session_state.inputs_limitedc[f'borgd'] = field_plain_template('RGD number (if any)',"RGD number (if any):",20, 97,12, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f"borgd",''))
        st.session_state.inputs_limitedc[f'bocountry_field'], st.session_state.inputs_limitedc[f'bocountry'] = field_plain_template('Country of incorporation',"Country of incorporation:",38, -32, 22, r_h=0,t_rows=1,value=st.session_state.inputs_limitedc.get(f"bocountry",''))
        st.session_state.inputs_limitedc["constitution_field"],st.session_state.inputs_limitedc["constitution"] = field_option_template(option_constitution,"""Choose "Registered Constitution" if the company has its own Constitution. If not, choose "Standard Constitution" as in schedule 2 of Act 992.""",control_x=-132, control_y=6, value=(st.session_state.inputs_limitedc.get("constitution",option_constitution[0])))
        st.write("""Name should not be duplicated, similar, misleading or undesirable. The Registrar of Companies shall have the final approval regarding the name which is eventually submitted for registration.Section 21(2) of Act 992. A list of registered names can be found on our portal www.rgdeservices.com""")
        st.session_state.inputs_limitedc["company_name_field"], st.session_state.inputs_limitedc["company_name"]= boxes("Company Name*",label="Enter Company Name*", find="company_name", c_x=96, t_row=2, bpr=19, control=1.4)
        option_ending = ["LTD", "LIMITED COMPANY"]
        st.session_state.inputs_limitedc["ending_field"],st.session_state.inputs_limitedc["ending"] = field_option_template(option_ending,'Choose Applicable Ending*',control_x=-100, control_y=6, value=(st.session_state.inputs_limitedc.get("ending",option_ending[0])))
        st.write("Full name and TIN of the natural person or legal entity submitting documents to the Registrar of Companies")
        st.session_state.inputs_limitedc["presenter_field"], st.session_state.inputs_limitedc["presenter"]= boxes("Presented By*",label="Presented By*", find="presenter", c_x=95, t_row=2, bpr=19, control=1.4)
        st.session_state.inputs_limitedc["presenter_tin_field"], st.session_state.inputs_limitedc["presenter_tin"]= boxes("TIN*",label="TIN*",c_x=35.5, find="presenter_tin", bpr=11)
        
        st.session_state.inputs_limitedc[f"autoshares_field"],  st.session_state.inputs_limitedc[f"autoshares"]= boxes('Authorised Shares*',label=''), st.number_input("Authorised Shares*",min_value=0, value=st.session_state.inputs_limitedc.get('autoshares', 0))
        st.session_state.inputs_limitedc[f"statedcapi_field"],  st.session_state.inputs_limitedc[f"statedcapi"]= boxes("Stated Capital*",label="", c_x=170, bpr=15), st.number_input("Stated Capital* GHC",min_value=0, value=st.session_state.inputs_limitedc.get('statedcapi', 0))
        st.markdown("<h6 style='text-align: center;'>Number of Authorised Shares of Each Class.</h6>", unsafe_allow_html=True)
        st.write("Equity Shares and Preference Shares in this class must sum up to the Authorised Shares stated above")
        form3shares(1)
        st.markdown("<h6 style='text-align: center;'>Number of Issued Shares of Each Class</h6>", unsafe_allow_html=True)
        st.write("Equity Shares and Preference Shares in this class must sum up to the total Issued Shares stated below")
        st.session_state.inputs_limitedc[f"issuedshares"] = st.number_input("Enter total issued shares.",min_value=0, value=st.session_state.inputs_limitedc.get("issuedshares",0))
        form3shares(2)
        st.markdown("<h6 style='text-align: center;'>Amount Paid In Cash of Each Class</h6>", unsafe_allow_html=True)
        form3shares(3)   
        st.markdown("<h6 style='text-align: center;'>Amount Paid Otherwise than in Cash of Each Class</h6>", unsafe_allow_html=True)
        st.session_state.inputs_limitedc[f"equityshares_field4"],  st.session_state.inputs_limitedc[f"equityshares4"]= boxes('EquityShares',label="", c_x=170, bpr=15), st.number_input(f"Equity Shares GHC{4*' '}",min_value=0, value=st.session_state.inputs_limitedc.get(f"equityshares4", 0))
        st.session_state.inputs_limitedc[f"preshares_field4"],  st.session_state.inputs_limitedc[f"preshares4"]= boxes("Preference Shares",label="", c_x=170, bpr=13), st.number_input(f"Preference Shares GHC{4*' '}",min_value=0, value=st.session_state.inputs_limitedc.get(f"preshares4", 0))
        st.markdown("<h6 style='text-align: center;'>Amount Remaining to be Paid on Each Class</h6>", unsafe_allow_html=True)
        st.session_state.inputs_limitedc[f"equityunpaid_field"],  st.session_state.inputs_limitedc[f"equityunpaid"]= boxes('Equity Shares(Unpaid)',label="", c_x=170, bpr=15), st.number_input(f"Equity Shares(Unpaid) GHC",min_value=0, value=st.session_state.inputs_limitedc.get("equityunpaid", 0))
        st.session_state.inputs_limitedc[f"equitydue_field"],  st.session_state.inputs_limitedc[f"equitydue"]= boxes('Equity Shares (Due)',label="", c_x=170, bpr=15), st.number_input(f"Equity Shares (Due) GHC",min_value=0, value=st.session_state.inputs_limitedc.get(f"equitydue", 0))
        st.session_state.inputs_limitedc[f"preunpaid_field"],  st.session_state.inputs_limitedc[f"preunpaid"]= boxes("Preference Shares (Unpaid)",label="", c_x=170, bpr=15), st.number_input(f"Preference Shares (Unpaid) GHC",min_value=0, value=st.session_state.inputs_limitedc.get(f"preunpaid", 0))
        st.session_state.inputs_limitedc[f"predue_field"],  st.session_state.inputs_limitedc[f"predue"]= boxes("Preference Shares(Due)",label="", c_x=170, bpr=15), st.number_input(f"Preference Shares(Due) GHC",min_value=0, value=st.session_state.inputs_limitedc.get(f"predue", 0))                                                                                                                                                                           
        st.markdown(f"<h4 style='text-align: center;'>MSME Details</h4>", unsafe_allow_html=True)
        data = {
            "Enterprise Category": ["Micro", "Small", "Medium"],
            "Employment Size (Permanent)": ["1-5", "6-30", "31-100"],
            "Turnover": ["≤US$25,000", "US$25,001 - US$1,000,000", "US$1,000,001 - US$3,000,000"],
            "Assets": ["≤US$25,000", "US$25,001 - US$1,000,000", "US$1,000,001 - US$3,000,000"],
        }
        df = pd.DataFrame(data)
        st.table(df)
        st.write(
            """
            (An enterprise will be categorized as MSME based on employment size and any other variable.)
            All amounts in USD should be converted into Ghana cedis at the prevailing bank rate.
            """)
        st.session_state.inputs_limitedc["revenue_field"], st.session_state.inputs_limitedc["revenue"] = boxes("Revenue Envisaged*", "Revenue Envisaged*",find="revenue", bpr=17)
        st.session_state.inputs_limitedc["employees_envisaged_field"], st.session_state.inputs_limitedc["employees_envisaged"]= boxes("No. of Employees Envisaged*", "No. of Employees Envisaged*",find= "employees_envisaged")
        if st.session_state.inputs_limitedc["apply_bop"] == "Already have a BOP":
            st.markdown("<h6 style='text-align: center;'>Business Operating Permit (BOP) Request</h6>", unsafe_allow_html=True)
            st.session_state.inputs_limitedc["bop_ref_field"],st.session_state.inputs_limitedc["bop_ref"]= boxes("Provide BOP Reference No.", "Provide BOP Reference No.",find="bop_ref")
        st.session_state.inputs_limitedc["selected_sectors_field"], st.session_state.inputs_limitedc["selected_sectors"] = PDFOptionField(control_x=-76, control_y=5), st.multiselect("""Choose your sector(s) by selecting from the options below. If your sector is not listed, select "other" and write your sector in the space provided on the next page.*: (Choose up to 4 options:)""",list(isic_data.keys()), max_selections=4, default=st.session_state.inputs_limitedc.get("selected_sectors",[]))
        if st.session_state.inputs_limitedc[f"equityshares1"] +  st.session_state.inputs_limitedc[f"preshares1"] !=  st.session_state.inputs_limitedc[f"autoshares"]:
            st.warning("Equity Shares and Preference Shares in Authorised Shares class must sum up to the Authorised Shares stated.")
        if st.session_state.inputs_limitedc[f"equityshares2"] +  st.session_state.inputs_limitedc[f"preshares2"] !=  st.session_state.inputs_limitedc[f"issuedshares"]:
            st.warning("Equity Shares and Preference Shares in Number of Issued Shares class must sum up to the total Issued Shares stated.")
 
      
# # #############SECTION C Principal Business Activities
    elif page==4:
        st.markdown("### About the company")
        if "Others(Please Specify)" in  st.session_state.inputs_limitedc.get("selected_sectors", []):
                st.session_state.inputs_limitedc["other_field"],st.session_state.inputs_limitedc["other"] =field_plain_template("Please specify the sector of your business",'Others(Please Specify)', 20, 5, c_y=24.5, t_rows=3, value=st.session_state.inputs_limitedc.get("other", '')) 
        st.write("""ISIC or classification code is a standard classification for economic or business activities so that establishments could be classified based on the activity they carry out. A detailed list of ISIC or Classification Codes can be found on our website at www.orc.gov.gh""")
        for i, item in enumerate(st.session_state.inputs_limitedc["selected_sectors"], start=1):
                if item == "Others(Please Specify)":
                    st.session_state.inputs_limitedc[f'iso_other_field'], st.session_state.inputs_limitedc['iso_other']= boxes(f"ISIC code {i}",label="Enter ISIC code for Specified Sector", find='iso_other', c_x=96)
                else:
                    descriptions = list(isic_data[item].keys())
                    st.session_state.inputs_limitedc[f'iso_field{item}'], st.session_state.inputs_limitedc[f'iso_{item}']= boxes(f"ISIC code {i}", c_x=96), st.selectbox(f"Select a description for {item}", descriptions)
                    st.session_state.inputs_limitedc[f'isoxx{item}'] = st.text_input(f"If  'Others' please enter ISO code{i*' '}", max_chars=17, value = st.session_state.inputs_limitedc.get(f'isoxx{item}', ''))

        st.session_state.inputs_limitedc["describe_iso_field"],st.session_state.inputs_limitedc["describe_iso"] = field_plain_template(0, "If you cannot determine a code, please give a brief description",63,5,c_y=24.5,t_rows=3) , st.text_area("If you cannot determine a code, please give a brief description of the company's business activities below", max_chars=63*3, value=st.session_state.inputs_limitedc.get("describe_iso", ''))    
        ###########SECTION D
        st.write("Specialized institutions for example Banks, Insurance and Security companies are required to state their objects here. All other applicants who wish to indicate their objects can also state same in this column")
        st.session_state.inputs_limitedc["describe_buss_nature_field"],  st.session_state.inputs_limitedc["describe_buss_nature"] = field_plain_template(0,"Nature of Business of the Company",63,-180,24.5,t_rows=6), st.text_area('Nature of Business of the Company', max_chars=63*6, value=st.session_state.inputs_limitedc.get("describe_buss_nature", ''))     

        ################SECTION E

        st.markdown("<h6 style='text-align: center;'>Registered Office Address</h6>", unsafe_allow_html=True)
        address(1)
        ###############SECTION F Principal Place of Business 
        st.session_state.inputs_limitedc["same_address_field"],st.session_state.inputs_limitedc["same_address"] = PDFOptionField(control_x=10, control_y=10), st.radio("Is the Principal place of Business the same as the Registered Office Address?", ["YES", "NO"], horizontal=True, index=["YES", "NO"].index(st.session_state.inputs_limitedc.get("same_address",["YES", "NO"][0])))
        st.session_state.inputs_limitedc["other_address"] = st.radio("Are there multiple operational locations for the Company", option_yesno, horizontal=True, index=option_yesno.index(st.session_state.inputs_limitedc.get("other_address",option_yesno[0])))
        st.write("A Register of Members is a register that contains the names and addresses of members of an incorporated Company. It is required that every company keeps and maintains a Register of its Members at a location in the country.")
        st.session_state.inputs_limitedc["maintain_address"] = st.radio("Is the address at which Register of Members will be kept and maintained elsewhere than at the Registered Office", option_yesno,horizontal=True, index=option_yesno.index(st.session_state.inputs_limitedc.get("maintain_address",option_yesno[0])))

    elif page==5:
        st.markdown("### About the company")
        if st.session_state.inputs_limitedc["same_address"] =="NO":
            st.markdown("<h6 style='text-align: center;'>Principal Place of Business</h6>", unsafe_allow_html=True)
            address(2, p=2)
    #############SECTION G Other Place of Business
        if st.session_state.inputs_limitedc["other_address"] == "YES":
            st.markdown("<h6 style='text-align: center;'>Other Place of Business</h6>", unsafe_allow_html=True)
            st.write("Companies that have multiple operational locations must complete this section.")
            address(3, p=3)
        
    ###########SECTION H
        if st.session_state.inputs_limitedc["maintain_address"] == "YES":
            st.markdown("<h6 style='text-align: center;'>Address at which Register of Members will be kept and maintained</h6>", unsafe_allow_html=True)
            address(4, p=4)

        #######Postal Address
        st.markdown("<h6 style='text-align: center;'>Postal Address</h6>", unsafe_allow_html=True)
        st.write("""Please select either Post Office Box (P O BOX), Private Mail Bag (PMB) or Door to Door (DTD) and provide details as applicable.""")
        st.session_state.inputs_limitedc["c_o_field"], st.session_state.inputs_limitedc["c_o"] = boxes("C/O",label="C/O", find="c_o")
        options_g = ["P O BOX", "PMB", "DTD"]
        st.session_state.inputs_limitedc["type_field"],st.session_state.inputs_limitedc["type"] = PDFOptionField(control_x=258.5, control_y=10),st.radio("Choose Type of Postal Address:*", options_g, horizontal=True, index=options_g.index(st.session_state.inputs_limitedc.get("type",options_g[0])))
        st.session_state.inputs_limitedc["postal_number_field"],  st.session_state.inputs_limitedc["postal_number"] = boxes("Number*",label="Postal Number*", find="postal_number")
        st.session_state.inputs_limitedc["postal_town_field"],  st.session_state.inputs_limitedc["postal_town"] = boxes("Town*",label="Postal Town*", find="postal_town")
        st.session_state.inputs_limitedc["postal_region_field"],  st.session_state.inputs_limitedc["postal_region"] = boxes("Region*",label="Postal Region*", find="postal_region")
    
        ########I Contact of the Company
        st.markdown("<h6 style='text-align: center;'>Contact of the Company</h6>", unsafe_allow_html=True)
        st.write("""Applicants are to provide at least, one mobile phone number and an email address. This is to assist the Registrar of Companies to communicate to the company""")
        st.session_state.inputs_limitedc["phone_num_field"],  st.session_state.inputs_limitedc["phone_num"]= boxes("Phone No 1*",label="Phone No 1*", find="phone_num")
        st.session_state.inputs_limitedc["phone_num_field2"],  st.session_state.inputs_limitedc["phone_num2"]= boxes("Phone No 2",label="Phone No 2", find="phone_num2")
        contact(1)        
        st.session_state.inputs_limitedc["website_field"],  st.session_state.inputs_limitedc["website"]= TextBox(boxes_per_row=34, search_text="Email Address", total_rows=1, x_offset=130, y_offset=19, row_height=8, box_width=8.5, control_x=0.7), st.text_input(f"Website",max_chars=34, value=st.session_state.inputs_limitedc.get(f"website", ''))
    


#################################DIRECTOR#####################    
    elif 5 < page < 6+(2 * st.session_state.inputs_limitedc["dir_num"]):
            st.markdown("<h4 style='text-align: center;'>Particulars of Directors of the Company</h4>", unsafe_allow_html=True)
            n = st.session_state.inputs_limitedc["dir_num"]
            for i in  range(1, n+1):
                dir = 6 + (2 * (i - 1))
                if page == dir:
                    if st.session_state.inputs_limitedc.get(f'dirsub{i}')=='No':                      
                        st.markdown(f"<h4 style='text-align: center;'>{st.session_state.inputs_limitedc[f'first_name{i}']+ ' ' +st.session_state.inputs_limitedc[f'last_name{i}']} - A Director and a Subscriber</h4>", unsafe_allow_html=True)
                        st.write("""
                        A subscriber is somebody who agrees to become a member of the company by taking up shares at the inception of the company. 
                        The application for incorporation shall be made by a person:
                        a. Signing a duly completed application for incorporation form, or
                        b. Signing a duly completed application for incorporation to this form and the constitution of the proposed company
                        (where a registered constitution is preferred).""" ) 
                        payshare(page, address='yes')
                        add_info(page, bo2=True)
                        
                        
                    elif st.session_state.inputs_limitedc.get(f'dirsub{i}')=='Yes':
                        st.markdown(f"<h4 style='text-align: center;'>{st.session_state.inputs_limitedc[f'first_name{i}']+ ' ' + st.session_state.inputs_limitedc[f'last_name{i}']} - A Director, Subscriber and a Trustee</h4>", unsafe_allow_html=True)
                        st.write("""
                        A subscriber is somebody who agrees to become a member of the company by taking up shares at the inception of the company. 
                        The application for incorporation shall be made by a person:
                        a. Signing a duly completed application for incorporation form, or
                        b. Signing a duly completed application for incorporation to this form and the constitution of the proposed company
                        (where a registered constitution is preferred).""" ) 
                        st.write("That I/we hold the Share(s) and all dividends and interests accrued or to  accrue on trust for the Owner and I/we undertake to transfer and deal, in all  respects, and to pay the Share and any dividends, interest and other  benefits thereon and accretions thereto in such manner as the Owner shall  from time to time direct.")
                        payshare(page, address='yes')
                        st.session_state.inputs_limitedc[f"name_minor_field{page}"],  st.session_state.inputs_limitedc[f"name_minor{page}"]= boxes("Name (Minor)*",label=f"Name (Minor)*", find=f"name_minor{page}")
                        get_date_input(f"dob_minor{page}", "Date of Birth(Minor)*")
                        st.session_state.inputs_limitedc[f"dob_minor_field{page}"]= boxes("Date of Birth")
                        st.session_state.inputs_limitedc[f"id_minor_field{page}"]= boxes("Identification Type(ID)", find=f"id_minor{page}")
                        st.session_state.inputs_limitedc[f"ref_minor_field{page}"]= boxes("ID Reference Number", find=f"ref_minor{page}")
                        add_info(page, bo2=True)
                    else:
                        st.markdown(f"<h4 style='text-align: center;'>{st.session_state.inputs_limitedc[f'first_name{i}']+ ' ' + st.session_state.inputs_limitedc[f'last_name{i}']} - Director</h4>", unsafe_allow_html=True)
                    st.write("Directors should be at least 18 years Statutory Declaration & Consent Letter and above. Directors are to attach a statutory declaration and consent letter as stated in section 172 (2) of Act 992. If you select \"YES\" to any of the Statutory Declarations, provide details that qualifies you to be a director. Attach supporting documents. A Company shall have at least two directors of which one should be resident in Ghana. If there are more than two directors, additional directors’ forms shall be obtained from our website at www.orc.gov.gh")
                    consent(page)
                    personal(i,page, place_ob=True)
                    contact(page)
                    gh_tin(page)
                    st.markdown("<h6 style='text-align: center;'>Residential Address</h6>", unsafe_allow_html=True)
                    st.write("This address when provided will not appear on public record, unlike that of the Company. Applicants are to ensure that the digital address provided matches with the residential address provided.")
                    address(page, country="yes", p=1, split=True, tax=True)
                    st.markdown("<h6 style='text-align: center;'>Occupational Addres</h6>", unsafe_allow_html=True)
                    st.write("Provide your current workplace address.")
                    address(page+1, country="yes", p=2)
                    st.write("List the names of other Companies for which you serve as director, seperate names with comma.")
                    st.session_state.inputs_limitedc[f"particulars_field{page}"],  st.session_state.inputs_limitedc[f"particulars{page}"]= boxes("Particulars of other",label=f"Particulars of other Directorships{(page-4) * ' '}*", find=f"particulars{page}", t_row=5)
                    tax(page)
                    if st.session_state.inputs_limitedc.get((f"shares{page}")):
                        st.session_state.sharecheck[f'page: {page}'] = st.session_state.inputs_limitedc[(f"shares{page}")]
                    if st.session_state.inputs_limitedc.get(f"shares{page}", 0) >  st.session_state.inputs_limitedc[f"autoshares"]:
                        st.warning(f"Number of shares cannot be greater than the stated autorized share ({st.session_state.inputs_limitedc[f'autoshares']})")
                    elif st.session_state.inputs_limitedc.get((f"shares{page}")) and sum(list(st.session_state.sharecheck.values())) > st.session_state.inputs_limitedc[f"autoshares"]:
                        zz = list(st.session_state.sharecheck.values())
                        st.warning(f"The number of shares allocated must be less than or equal to the available remaining shares, which is {st.session_state.inputs_limitedc[f'autoshares'] - sum(zz[:len(zz)-1])}")


                elif page == dir+1:
                    if  st.session_state.inputs_limitedc.get(f'dirsub{i}')=='No':
                        st.markdown(f"<h4 style='text-align: center;'>{st.session_state.inputs_limitedc[f'first_name{i}']+ ' ' +st.session_state.inputs_limitedc[f'last_name{i}']} - A Director and a Subscriber</h4>", unsafe_allow_html=True)
                    elif  st.session_state.inputs_limitedc.get(f'dirsub{i}')=='Yes':
                        st.markdown(f"<h4 style='text-align: center;'>{st.session_state.inputs_limitedc[f'first_name{i}']+' '+ st.session_state.inputs_limitedc[f'last_name{i}']} - A Director, Subscriber and a Trustee</h4>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<h4 style='text-align: center;'>{st.session_state.inputs_limitedc[f'first_name{i}']+ ' ' + st.session_state.inputs_limitedc[f'last_name{i}']} - Director</h4>", unsafe_allow_html=True)
                    tax(page-1, pn=i, p=1)
                   
  


#############################SECRETARY#################
    elif 6 +(2 * st.session_state.inputs_limitedc["dir_num"]) <=page < 6 +(2 * st.session_state.inputs_limitedc["dir_num"]) +st.session_state.inputs_limitedc['sec_num']:
        options_secretary = ["Professional qualification","Tertiary level qualification","Company Secretary Trainee","Barrister or Solicitor in the Republic","Institute of Chartered Accountants","Under the supervision of a qualified Company Secretary","Institute of Chartered Secretaries and Administrators",
                    "By virtue of an academic qualification, member of a professional body, appears to the directors as capable of performing the functions of Secretary."]
        st.markdown(f"<h4 style='text-align: center;'>Particulars of Company Secretary</h4>", unsafe_allow_html=True) 
        if page == 6 +(2 * st.session_state.inputs_limitedc["dir_num"]):
            if st.session_state.inputs_limitedc["secretary_cop"] == "Individual" and st.session_state.inputs_limitedc[f'secsubques'] == 'Yes':
                st.markdown(f"<h4 style='text-align: center;'>{st.session_state.inputs_limitedc[f'first_namex']+' '+ st.session_state.inputs_limitedc[f'last_namex']} - Secretary</h4>", unsafe_allow_html=True)
                if  st.session_state.inputs_limitedc[f'subtrustques']=='Yes':
                    st.session_state.inputs_limitedc[f"name_minor_field{page}"],  st.session_state.inputs_limitedc[f"name_minor{page}"]= boxes("Name (Minor)*",label=f"Name (Minor)*", find=f"name_minor{page}")
                    get_date_input(f"dob_minor{page}", "Date of Birth(Minor)*")
                    st.session_state.inputs_limitedc[f"dob_minor_field{page}"]= boxes("Date of Birth")
                    st.session_state.inputs_limitedc[f"id_minor_field{page}"] = boxes("Identification Type(ID)")
                    st.session_state.inputs_limitedc[f"ref_minor_field{page}"]= boxes("ID Reference Number")
                st.markdown(f"Tick the applicable qualification(s) <br/>Attach Consent Letter Reference to Section 211 (1) and (3) of  Act 992", unsafe_allow_html=True)
                st.session_state.inputs_limitedc[f"qualification{page}"]= st.multiselect("Select all applicable qualification(s)", options_secretary, default=st.session_state.inputs_limitedc.get(f"qualification{page}", []))
                st.session_state.inputs_limitedc[f'consent_letter_field{page}'], st.session_state.inputs_limitedc[f'consent_letter{page}'] = PDFOptionField(control_x=-133, control_y=3), st.radio('Attached consent letter', option_yesno, horizontal=True, index=option_yesno.index(st.session_state.inputs_limitedc.get(f'consent_letter{page}', option_yesno[1])))
                personal('x', page)
                gh_tin(page)
                contact(page)
                st.markdown("<h6 style='text-align: center;'>Residential Address</h6>", unsafe_allow_html=True)
                st.write("""This address when provided will not  appear on public rec, ord, unlike that of  the Company. Applicants are to ensure that the  digital address provided matches with  the residential address provided. Provide your current workplace  address.""")
                address(page, country="yes", split=True, tax=True)
                st.write("""
                A subscriber is somebody who agrees to become a member of the company by taking up shares at the inception of the company. 
                The application for incorporation shall be made by a person:
                a. Signing a duly completed application for incorporation form, or
                b. Signing a duly completed application for incorporation to this form and the constitution of the proposed company
                (where a registered constitution is preferred).""" ) 
                payshare(page, address='yes')
                add_info(page, bo2=True)
                tax(page,pn='x') 
            elif st.session_state.inputs_limitedc["secretary_cop"] == "Individual": 
                st.markdown(f"Tick the applicable qualification(s) <br/>Attach Consent Letter Reference to Section 211 (1) and (3) of  Act 992", unsafe_allow_html=True)
                st.session_state.inputs_limitedc[f"qualification{page}"]= st.multiselect("Select all applicable qualification(s)", options_secretary, default=st.session_state.inputs_limitedc.get(f"qualification{page}", []))
                st.session_state.inputs_limitedc[f'consent_letter_field{page}'], st.session_state.inputs_limitedc[f'consent_letter{page}'] = PDFOptionField(control_x=-133, control_y=3), st.radio('Attached consent letter', option_yesno, horizontal=True, index=option_yesno.index(st.session_state.inputs_limitedc.get(f'consent_letter{page}', option_yesno[1])))
                personal('x', page)
                gh_tin(page)
                contact(page)
                st.markdown("<h6 style='text-align: center;'>Residential Address</h6>", unsafe_allow_html=True)
                st.write("""This address when provided will not  appear on public rec, ord, unlike that of  the Company. Applicants are to ensure that the  digital address provided matches with  the residential address provided. Provide your current workplace  address.""")
                address(page, country="yes", split=True, tax=True)
                tax(page, pn='x')     
            elif st.session_state.inputs_limitedc["secretary_cop"] == "Corporate Body":
                st.markdown(f"<h4 style='text-align: center;'>{st.session_state.inputs_limitedc[f'coporate_name']}</h4>", unsafe_allow_html=True)
                if st.session_state.inputs_limitedc[f'secsubques'] == 'Yes':
                    st.write("""
                    A subscriber is somebody who agrees to become a member of the company by taking up shares at the inception of the company. 
                    The application for incorporation shall be made by a person:
                    a. Signing a duly completed application for incorporation form, or
                    b. Signing a duly completed application for incorporation to this form and the constitution of the proposed company
                    (where a registered constitution is preferred).""" ) 
                    payshare(page, address='no')
                    if st.session_state.inputs_limitedc[f"bene_type"]=="Publicly Listed Company":
                        add_info(page, bo3=True)
                    else:
                        add_info(page, bo4=True)
                    if  st.session_state.inputs_limitedc[f'subtrustques']=='Yes':  
                        st.session_state.inputs_limitedc[f"name_minor_field{page}"],  st.session_state.inputs_limitedc[f"name_minor{page}"]= boxes("Name (Minor)*",label=f"Name (Minor)*", find=f"name_minor{page}")
                        get_date_input(f"dob_minor{page}", "Date of Birth(Minor)*")
                        st.session_state.inputs_limitedc[f"dob_minor_field{page}"]= boxes("Date of Birth")
                        st.session_state.inputs_limitedc[f"id_minor_field{page}"]= boxes("Identification Type(ID)")
                        st.session_state.inputs_limitedc[f"ref_minor_field{page}"]= boxes("ID Reference Number")
                st.write("""The Corporate Body must have as one  of its subscribers or operating officers  a person who qualifies to be a  Company Secretary. The Corporate Representative must  hold at least one of the qualification(s)  of secretary stated above Reference to section 211 (2) Act 992""")
                body(page)
            if st.session_state.inputs_limitedc.get((f"shares{page}")):
                st.session_state.sharecheck[f'page: {page}'] = st.session_state.inputs_limitedc[(f"shares{page}")]
            if st.session_state.inputs_limitedc.get(f"shares{page}", 0) >  st.session_state.inputs_limitedc[f"autoshares"]:
                st.warning(f"Number of shares cannot be greater than the stated autorized share ({st.session_state.inputs_limitedc[f'autoshares']})")
            elif st.session_state.inputs_limitedc.get((f"shares{page}")) and sum(list(st.session_state.sharecheck.values())) > st.session_state.inputs_limitedc[f"autoshares"]:
                zz = list(st.session_state.sharecheck.values())
                st.warning(f"The number of shares allocated must be less than or equal to the available remaining shares, which is {st.session_state.inputs_limitedc[f'autoshares'] - sum(zz[:len(zz)-1])}")
                       
        elif page == 7 +(2 * st.session_state.inputs_limitedc["dir_num"]):
            st.markdown(f"<h4 style='text-align: center;'>{st.session_state.inputs_limitedc[f'first_namex']+' '+ st.session_state.inputs_limitedc[f'last_namex']} - Secretary</h4>", unsafe_allow_html=True)
            tax(page-1, pn='x',p=1)
            


             
        
# #######################AUDITOR#######################
    elif page == 6 +(2 * st.session_state.inputs_limitedc["dir_num"]) + st.session_state.inputs_limitedc['sec_num']:
        st.markdown(f"<h4 style='text-align: center;'>Auditor of the Company</h4>", unsafe_allow_html=True)
        st.write("""A person shall be appointed an Auditor  of a private company if that person is  qualified and licensed in accordance  with the Chartered Accountants Act,  1963 (Act 170). See section 138 (1) and  (2) of Act 992. Applicant needs to attach an Auditor’s  consent letter to this application  before submission.  All Auditors shall hold office for a term  of not more than six years and are  eligible for appointment after a coolingoff period of not less than six years. Refer to section 139 (11) """)
        gh_tin(4)
        st.session_state.inputs_limitedc["auditor_firm_name_field"]= boxes("Auditor's Firm Name*",label="",t_row=6)
        st.session_state.inputs_limitedc["firm_address_field"],  st.session_state.inputs_limitedc["firm_address"]= boxes("Auditor's Firm Address* P.O.Box",label="Auditor's Firm Address* P.O.Box", find="firm_address", t_row=3)
        st.session_state.inputs_limitedc["firm_pmb_field"],  st.session_state.inputs_limitedc["firm_pmb"]= boxes("PMB/DTD*",label="PMB/DTD*", find="firm_pmb", t_row=2)
        address(page)
        st.session_state.inputs_limitedc["firm_moblie_field"],  st.session_state.inputs_limitedc["firm_moblie"]= boxes("Mobile No.*",label="Mobile No.*", find="firm_moblie")
        st.session_state.inputs_limitedc["office_num_field"],  st.session_state.inputs_limitedc["office_num"]= boxes("Office No.",label="Office No.", find="office_num")
       



# ##############################SUBSCRIBERS##########################  
   
    elif 7 +(2 * st.session_state.inputs_limitedc["dir_num"]) + st.session_state.inputs_limitedc['sec_num']<= page <  7 +(2 * st.session_state.inputs_limitedc["dir_num"]) + st.session_state.inputs_limitedc['sec_num'] +(2*st.session_state.inputs_limitedc["indsub"]):  
        n = st.session_state.inputs_limitedc["indsub"]
        for i in range(1, n + 1):
            sub = 7 +(2 * st.session_state.inputs_limitedc["dir_num"]) + st.session_state.inputs_limitedc['sec_num'] + (2 * (i - 1))
            v=st.session_state.inputs_limitedc["dir_num"]+i
            if page == sub:
                st.markdown(f"<h4 style='text-align: center;'>{st.session_state.inputs_limitedc[f'first_name{v}']+ ' '+st.session_state.inputs_limitedc[f'last_name{v}']} - Individual Subscriber</h4>", unsafe_allow_html=True)
                st.write("""
                A subscriber is somebody who agrees to become a member of the company by taking up shares at the inception of the company. 
                The application for incorporation shall be made by a person:
                a. Signing a duly completed application for incorporation form, or
                b. Signing a duly completed application for incorporation to this form and the constitution of the proposed company
                (where a registered constitution is preferred).  
                If there are more than two subscribers, additional subscriber forms shall be obtained from our website at www.orc.gov.gh.
                """)
                personal(v, page)
                gh_tin(page)
                address(page, split=True, tax=True, country='yes')
                contact(page)
                payshare(page, address='yes')
                add_info(page, bo2=True)
                if  st.session_state.inputs_limitedc[f'subtrustques{v}']:
                    st.write("That I/we hold the Share(s) and all dividends and interests accrued or to  accrue on trust for the Owner and I/we undertake to transfer and deal, in all  respects, and to pay the Share and any dividends, interest and other  benefits thereon and accretions thereto in such manner as the Owner shall  from time to time direct.")
                    st.session_state.inputs_limitedc[f"name_minor_field{page}"],  st.session_state.inputs_limitedc[f"name_minor{page}"]= boxes("Name (Minor)*",label=f"Name (Minor)*", find=f"name_minor{page}")
                    get_date_input(f"dob_minor{page}", "Date of Birth(Minor)*")
                    st.session_state.inputs_limitedc[f"dob_minor_field{page}"]= boxes("Date of Birth")
                    st.session_state.inputs_limitedc[f"id_minor_field{page}"]= boxes("Identification Type(ID)")
                    st.session_state.inputs_limitedc[f"ref_minor_field{page}"]= boxes("ID Reference Number")
                tax(page,pn=v)
                
               
            elif page == sub + 1:
                st.markdown(f"<h4 style='text-align: center;'>{st.session_state.inputs_limitedc[f'first_name{v}']+ ' '+st.session_state.inputs_limitedc[f'last_name{v}']} - Individual Subscriber</h4>", unsafe_allow_html=True)
                tax(page - 1,pn=v, p=1)
               
        if st.session_state.inputs_limitedc.get((f"shares{page}")):
            st.session_state.sharecheck[f'page: {page}'] = st.session_state.inputs_limitedc[(f"shares{page}")]
        if st.session_state.inputs_limitedc.get(f"shares{page}", 0) >  st.session_state.inputs_limitedc[f"autoshares"]:
            st.warning(f"Number of shares cannot be greater than the stated autorized share ({st.session_state.inputs_limitedc[f'autoshares']})")
        elif st.session_state.inputs_limitedc.get((f"shares{page}")) and sum(list(st.session_state.sharecheck.values())) > st.session_state.inputs_limitedc[f"autoshares"]:
            zz = list(st.session_state.sharecheck.values())
            st.warning(f"The number of shares allocated must be less than or equal to the available remaining shares, which is {st.session_state.inputs_limitedc[f'autoshares'] - sum(zz[:len(zz)-1])}")

    elif 7 +(2 * st.session_state.inputs_limitedc["dir_num"]) + st.session_state.inputs_limitedc['sec_num'] +(2*st.session_state.inputs_limitedc["indsub"]) <=page<7 +(2 * st.session_state.inputs_limitedc["dir_num"]) + st.session_state.inputs_limitedc['sec_num'] +(2*st.session_state.inputs_limitedc["indsub"])+(st.session_state.inputs_limitedc["copsub"]):
        n = st.session_state.inputs_limitedc["copsub"]
        for i in range(1, n+1):
            v=st.session_state.inputs_limitedc["dir_num"]+st.session_state.inputs_limitedc["indsub"]+i 
            sub_cop = 7 +(2 * st.session_state.inputs_limitedc["dir_num"]) + st.session_state.inputs_limitedc['sec_num'] +(2*st.session_state.inputs_limitedc["indsub"]) + (i-1)
            if page == sub_cop:
                st.markdown(f"<h4 style='text-align: center;'> {st.session_state.inputs_limitedc[f'coporate_name{v}']} - Corporate Body Subscriber</h4>", unsafe_allow_html=True)
                body(page)
                payshare(page, address="no")
                if st.session_state.inputs_limitedc[f"bene_type{v}"]=="Publicly Listed Company":
                    add_info(page, bo3=True)
                else:
                    add_info(page, bo4=True)
                if  st.session_state.inputs_limitedc[f'subtrustques{v}']:
                    st.write("That I/we hold the Share(s) and all dividends and interests accrued or to  accrue on trust for the Owner and I/we undertake to transfer and deal, in all  respects, and to pay the Share and any dividends, interest and other  benefits thereon and accretions thereto in such manner as the Owner shall  from time to time direct.")
                    st.session_state.inputs_limitedc[f"name_minor_field{page}"],  st.session_state.inputs_limitedc[f"name_minor{page}"]= boxes("Name (Minor)*",label=f"Name (Minor)*", find=f"name_minor{page}")
                    get_date_input(f"dob_minor{page}", "Date of Birth(Minor)*")
                    st.session_state.inputs_limitedc[f"dob_minor_field{page}"]= boxes("Date of Birth")
                    st.session_state.inputs_limitedc[f"id_minor_field{page}"]= boxes("Identification Type(ID)")
                    st.session_state.inputs_limitedc[f"ref_minor_field{page}"]= boxes("ID Reference Number")
                
        if st.session_state.inputs_limitedc.get((f"shares{page}")):
            st.session_state.sharecheck[f'page: {page}'] = st.session_state.inputs_limitedc[(f"shares{page}")]
        if st.session_state.inputs_limitedc.get(f"shares{page}", 0) >  st.session_state.inputs_limitedc[f"autoshares"]:
            st.warning(f"Number of shares cannot be greater than the stated autorized share ({st.session_state.inputs_limitedc[f'autoshares']})")          
        elif st.session_state.inputs_limitedc.get((f"shares{page}")) and sum(list(st.session_state.sharecheck.values())) > st.session_state.inputs_limitedc[f"autoshares"]:
            zz = list(st.session_state.sharecheck.values())
            st.warning(f"The number of shares allocated must be less than or equal to the available remaining shares, which is {st.session_state.inputs_limitedc[f'autoshares'] - sum(zz[:len(zz)-1])}")
# """State clearly the total amount of the 
# proposed Authorized Shares 
# and the Stated Capital
# All shares are of no par value
#  Also state all the relevant details 
# about the company shares
# The amount Paid in Cash of Each Class 
# and
#  Amount Remaining to be Paid on Each 
# Class must not exceed stated capital
# Equity Shares, previously known as 
# Ordinary shares"""


# """Amount Remaining to be Paid on Each 
# Class must be stated, if it is applicable 
# to the company"""








def fill_forms():
    all_files = []
    directors, secretary,subscribers,trustees,beneficiaries = [], [], [],[],[]

    #########################COVER
    pdf_cover = 'backend/limited_company/data/COVER NOTE Companies.pdf'
    doc_cover =  fitz.open(pdf_cover)
    cover1 = doc_cover[0]

    tin_gha_properties = {'boxes_per_row': 11,'total_rows': 1,'x_offset': 40,  'y_offset': 10}
    company_name_fieldcover = TextBox(boxes_per_row=24,total_rows=2,search_text="Company Name",  x_offset=8,y_offset=30)
    company_name_fieldcover.fill_field(cover1, st.session_state.inputs_limitedc['company_name'].upper())
    
    def cover(label,count='',lbl='', ind=0, controlx=100, maxi=55, cop=False, sec=False, v=0):
        if label=='SUBSCRIBER'and count==4:
            label = 'SUBSCRIBER '
        partner_key = f"{label}{count}(Name)"
        partner_key_field = PDFTextFinder(search_text=partner_key, max_chars_per_row=maxi, control_x=controlx)
        
        if cop:
            tin_nums=st.session_state.inputs_limitedc[f"tinrep{lbl}"]
            nm = st.session_state.inputs_limitedc[f"name_repre{lbl}"]
        elif sec:
            nm =st.session_state.inputs_limitedc['first_namex']+" "+st.session_state.inputs_limitedc["middle_namex"]+' '+st.session_state.inputs_limitedc["last_namex"]
            tin_nums= st.session_state.inputs_limitedc[f'tin{lbl}']
            
        elif v!=0:
            nm =st.session_state.inputs_limitedc[f'first_name{v}']+" "+st.session_state.inputs_limitedc[f"middle_name{v}"]+' '+st.session_state.inputs_limitedc[f"last_name{v}"]
            tin_nums= st.session_state.inputs_limitedc[f'tin{lbl}']
        else:
            nm =st.session_state.inputs_limitedc[f'first_name{count}']+" "+st.session_state.inputs_limitedc[f"middle_name{count}"]+' '+st.session_state.inputs_limitedc[f"last_name{count}"]
            tin_nums= st.session_state.inputs_limitedc[f'tin{lbl}']

        tin_num_field = TextBox( **tin_gha_properties, search_text="TIN")
        gha_num_field = TextBox(**tin_gha_properties, search_text="GHA")
        gha_nums = st.session_state.inputs_limitedc[f'gh_card{lbl}']

        partner_key_field.fill_field(cover1, nm.upper())
        tin_num_field.fill_field(cover1, tin_nums.upper(), ind)
        gha_num_field.fill_field(cover1, gha_nums.upper(), ind)
    

#############################################################

    st.session_state.inputs_limitedc[f'c_name_field'] = field_plain_template(0, "Company Name:", maxi=100,c_x=0,c_y=30, r_h=0,t_rows=1)
    st.session_state.inputs_limitedc[f'cdir_name_field'] = field_plain_template(0, "Proposed Company Name:", maxi=100,c_x=0,c_y=30, r_h=0,t_rows=1)
    
    st.session_state.inputs_limitedc[f'fullname_field']= field_plain_template(0, "Full Name:",maxi=100,c_x=0,c_y=30, r_h=0,t_rows=1)
    st.session_state.inputs_limitedc[f'formername_field'] = field_plain_template(0, "Former Name:",maxi=100,c_x=0,c_y=30, r_h=0,t_rows=1)
    st.session_state.inputs_limitedc[f'pbox_field'] = field_plain_template(0, "P. O. Box Number",maxi=100,c_x=0,c_y=30, r_h=0,t_rows=1)
    st.session_state.inputs_limitedc[f'resaddre_field'] = field_plain_template(0, "Residential Address",maxi=60,c_x=0,c_y=30, r_h=0,t_rows=1)
    st.session_state.inputs_limitedc[f'con_field'] = field_plain_template(0, "Contact Number",maxi=100,c_x=0,c_y=30, r_h=0,t_rows=1)
    st.session_state.inputs_limitedc[f'dirdate_field'] = field_plain_template(0, "Date",maxi=100,c_x=50, r_h=0,t_rows=1)

    st.session_state.inputs_limitedc[f'fullname1_field']= field_plain_template(0, "Full Name",maxi=41,c_x=95, r_h=0,t_rows=1)
    st.session_state.inputs_limitedc[f'fullname2_field']= field_plain_template(0, "Full Name",maxi=41,c_x=75, r_h=0,t_rows=1)
    st.session_state.inputs_limitedc[f'numbx_field'] = field_plain_template(0, "Number",maxi=20,c_x=60, r_h=0,t_rows=1)
    st.session_state.inputs_limitedc[f'landmark_field'] = field_plain_template(0, "(Landmark):",maxi=60,c_x=75, r_h=0,t_rows=1)
    st.session_state.inputs_limitedc[f'street'] = field_plain_template(0, "(Street Name):",maxi=60,c_x=135, r_h=0,t_rows=1)
    st.session_state.inputs_limitedc[f'town'] = field_plain_template(0, "(Town & City):",maxi=60,c_x=110, r_h=0,t_rows=1)

        



######################FORMB
    pdf_file = 'backend/limited_company/data/Form 3.pdf'
    doc = fitz.open(pdf_file)
    page1 = doc[0]
    page2 = doc[1]
    page3 = doc[2]
    page4 = doc[3]
    page5 = doc[4]
    page6 = doc[5]
    page7 = doc[6]
    page8 = doc[7]
    page9 = doc[8]
    page10 = doc[9]
    page11 = doc[10]
    page12 = doc[11]



    
    st.session_state.inputs_limitedc["apply_bop_field"].fill_option(page12,  st.session_state.inputs_limitedc["apply_bop"])
    st.session_state.inputs_limitedc["revenue_field"].fill_field(page12, st.session_state.inputs_limitedc["revenue"].upper()) 
    st.session_state.inputs_limitedc["employees_envisaged_field"].fill_field(page12, st.session_state.inputs_limitedc["employees_envisaged"].upper()) 
    if st.session_state.inputs_limitedc["apply_bop"] == "Already have a BOP":
        st.session_state.inputs_limitedc["bop_ref_field"].fill_field(page12, st.session_state.inputs_limitedc["bop_ref"].upper()) 
    st.session_state.inputs_limitedc["dob_witness_field"].fill_field(page11, st.session_state.inputs_limitedc["dob_witness"].strftime("%d%m%Y")) 
    st.session_state.inputs_limitedc["fullname_witness_field"].fill_field(page11, st.session_state.inputs_limitedc["fullname_witness"].upper()) 
    st.session_state.inputs_limitedc["adress_field"].fill_field(page11, st.session_state.inputs_limitedc["adress"].upper()) 
    st.session_state.inputs_limitedc["occupation_witness_field"].fill_field(page11, st.session_state.inputs_limitedc["occupation_witness"].upper()) 

####SECTION A
    st.session_state.inputs_limitedc["constitution_field"].fill_option(page1, st.session_state.inputs_limitedc["constitution"].upper())
    st.session_state.inputs_limitedc["company_name_field"].fill_field(page1, st.session_state.inputs_limitedc['company_name'].upper())
    st.session_state.inputs_limitedc["ending_field"].fill_option(page1,st.session_state.inputs_limitedc["ending"].upper(), new_x=(-32 if st.session_state.inputs_limitedc["ending"]=='LTD' else 0))
    st.session_state.inputs_limitedc["presenter_field"].fill_field(page1, st.session_state.inputs_limitedc['presenter'].upper())
    st.session_state.inputs_limitedc["presenter_tin_field"].fill_field(page1, st.session_state.inputs_limitedc['presenter_tin'].upper())

    st.session_state.inputs_limitedc[f"autoshares_field"].fill_field(page7, str(st.session_state.inputs_limitedc[f"autoshares"]))
    st.session_state.inputs_limitedc[f"statedcapi_field"].fill_field(page7, str(st.session_state.inputs_limitedc[f"statedcapi"]))
    form3shares(1, fill=True, page=page7, ind1=0, ind2=3)
    form3shares(2, fill=True, page=page7, ind1=2)
    form3shares(3, fill=True, page=page7, ind1=1, ind2=2)
    st.session_state.inputs_limitedc[f"equityshares_field4"].fill_field(page7, str(st.session_state.inputs_limitedc[f"equityshares4"]) if st.session_state.inputs_limitedc[f"equityshares4"] else '')
    st.session_state.inputs_limitedc[f"preshares_field4"].fill_field(page7, str(st.session_state.inputs_limitedc[f"preshares4"]) if st.session_state.inputs_limitedc[f"preshares4"] else '',1)
    st.session_state.inputs_limitedc[f"equityunpaid_field"].fill_field(page7, str(st.session_state.inputs_limitedc[f"equityunpaid"]) if st.session_state.inputs_limitedc[f"equityunpaid"] else '')
    st.session_state.inputs_limitedc[f"equitydue_field"].fill_field(page7, str(st.session_state.inputs_limitedc[f"equitydue"]) if st.session_state.inputs_limitedc[f"equitydue"] else '')
    st.session_state.inputs_limitedc[f"preunpaid_field"].fill_field(page8, str(st.session_state.inputs_limitedc[f"preunpaid"]) if st.session_state.inputs_limitedc[f"preunpaid"] else '')
    st.session_state.inputs_limitedc[f"predue_field"].fill_field(page8, str(st.session_state.inputs_limitedc[f"predue"]) if st.session_state.inputs_limitedc[f"predue"] else '')
                                                                                                                                                                        

# #############SECTION C Principal Business Activities
    for item in st.session_state.inputs_limitedc["selected_sectors"]:  
        col2 = ['Security', 'Estate/Housing', 'Insurance']
        col3  = ["Media", "Shipping & Port", "Hospitality", "Health Care" ,"Securities/Brokers", "Banking and Finance", "Sanitation"]        
        col4 = ["Transport/Aerospace","Fashion/Beautification", "Refinery of Minerals", "Others(Please Specify)"]
        if item == "Others(Please Specify)":
            st.session_state.inputs_limitedc['other_field'].fill_field(page1,st.session_state.inputs_limitedc['other'].upper())
            st.session_state.inputs_limitedc['iso_other_field'].fill_field(page1, st.session_state.inputs_limitedc['iso_other'].upper())
            st.session_state.inputs_limitedc['selected_sectors_fieldz'] = PDFOptionField(control_x=-132, control_y=5)
            st.session_state.inputs_limitedc['selected_sectors_fieldz'].fill_option(page1, item)

        else:
            if item == "Commerce/Trading":
                st.session_state.inputs_limitedc['selected_sectors_fieldx'] = PDFOptionField(control_x=-95, control_y=20)
                st.session_state.inputs_limitedc['selected_sectors_fieldx'].fill_option(page1,"Securities/Brokers")
            
            elif item in col2:
                st.session_state.inputs_limitedc['selected_sectors_field'].fill_option(page1, item, ind=1)
            elif item in col3:
                st.session_state.inputs_limitedc['selected_sectors_fieldx'] = PDFOptionField(control_x=-95, control_y=5)
                st.session_state.inputs_limitedc['selected_sectors_fieldx'].fill_option(page1,item)
            elif item in col4:
                st.session_state.inputs_limitedc['selected_sectors_fieldxx'] = PDFOptionField(control_x=-132, control_y=5)
                st.session_state.inputs_limitedc['selected_sectors_fieldxx'].fill_option(page1, item)           
            else:
                st.session_state.inputs_limitedc['selected_sectors_field'].fill_option(page1, item, ind=1 if item=="Legal" else 0)
            if isic_data[item][st.session_state.inputs_limitedc[f'iso_{item}']]:
                st.session_state.inputs_limitedc[f'iso_field{item}'].fill_field(page1, isic_data[item][st.session_state.inputs_limitedc[f'iso_{item}']])
            else:
                st.session_state.inputs_limitedc[f'iso_field{item}'].fill_field(page1, st.session_state.inputs_limitedc[f'isoxx{item}'])

        
    st.session_state.inputs_limitedc['describe_iso_field'].fill_field(page1, st.session_state.inputs_limitedc['describe_iso'].upper())

        
    ###########SECTION D
    st.session_state.inputs_limitedc["describe_buss_nature_field"].fill_field(page1, st.session_state.inputs_limitedc['describe_buss_nature'].upper())   
#     ################SECTION E
    address(1, fill=True, form3=True, page=page2)
    ###############SECTION F Principal Place of Business
    if st.session_state.inputs_limitedc["same_address"] =="YES":
        st.session_state.inputs_limitedc["same_address_field"] = PDFOptionField(control_x=-232,control_y=6)
        st.session_state.inputs_limitedc["same_address_field"].fill_option(page2, st.session_state.inputs_limitedc["same_address"])

    if st.session_state.inputs_limitedc["same_address"] =="NO":
        address(2, fill=True,form3=True,page=page2)
#############SECTION G Other Place of Business
    if st.session_state.inputs_limitedc["other_address"] == "YES":
        address(3, fill=True,form3=True,page=page2)    
# # ###########SECTION H
    if st.session_state.inputs_limitedc["maintain_address"] == "YES":
        address(4, fill=True,form3=True,page=page2,ind=1)    

# #     #######Postal Address
    st.session_state.inputs_limitedc["c_o_field"].fill_field(page2, st.session_state.inputs_limitedc["c_o"].upper())
    if st.session_state.inputs_limitedc["type"]=="DTD":
        st.session_state.inputs_limitedc["type_field"] = PDFOptionField(control_x=155)

    st.session_state.inputs_limitedc["type_field"].fill_option(page2, st.session_state.inputs_limitedc["type"], ind=1)#fix
    st.session_state.inputs_limitedc["postal_number_field"].fill_field(page2, st.session_state.inputs_limitedc["postal_number"].upper())
    st.session_state.inputs_limitedc["postal_town_field"].fill_field(page2, st.session_state.inputs_limitedc["postal_town"].upper())
    st.session_state.inputs_limitedc["postal_region_field"].fill_field(page2, st.session_state.inputs_limitedc["postal_region"].upper(),ind=3)
    
    # ########I Contact of the Company
    st.session_state.inputs_limitedc["phone_num_field"].fill_field(page2, st.session_state.inputs_limitedc["phone_num"].upper())
    st.session_state.inputs_limitedc["phone_num_field2"].fill_field(page2, st.session_state.inputs_limitedc["postal_town"].upper())
    st.session_state.inputs_limitedc["website_field"].fill_field(page3, st.session_state.inputs_limitedc["website"], fs=9)
    contact(1, form3=True, fill=True, page=[page2, page3])  
##############################################################################################################
    
    # if st.session_state.inputs_limitedc["indsub"] or  st.session_state.inputs_limitedc["copsub"] or st.session_state.inputs_limitedc["dirsub"] or  st.session_state.inputs_limitedc[f'secsubques']=='Yes' : 
    bene_file = 'backend/limited_company/data/BO1 Overarching BO Form.pdf'
    doc_mbene = fitz.open(bene_file)
    mbene1 = doc_mbene[0]

    st.session_state.inputs_limitedc[f'bocom_field'] = field_plain_template(0,"Full legal name of Company", 40,-32,30, r_h=0,t_rows=1)
    st.session_state.inputs_limitedc[f"typeofco"] = PDFOptionField(control_x=20, control_y=5)
    st.session_state.inputs_limitedc[f"bopurpose_field"].fill_option(mbene1, st.session_state.inputs_limitedc[f"bopurpose"])
    st.session_state.inputs_limitedc[f'boother_field'].fill_field(mbene1, st.session_state.inputs_limitedc[f'boother'].upper())
    st.session_state.inputs_limitedc[f'bocom_field'].fill_field(mbene1, st.session_state.inputs_limitedc[f'company_name'].upper())
    st.session_state.inputs_limitedc[f'botin_field'].fill_field(mbene1, st.session_state.inputs_limitedc[f'botin'].upper())
    st.session_state.inputs_limitedc[f'borgd_field'].fill_field(mbene1, st.session_state.inputs_limitedc[f'borgd'].upper())
    st.session_state.inputs_limitedc[f'bocountry_field'].fill_field(mbene1, st.session_state.inputs_limitedc[f'bocountry'].upper())
    st.session_state.inputs_limitedc[f"typeofco"].fill_option(mbene1, 'Company Limited by Shares')
    if st.session_state.inputs_limitedc[f"no_bene"] == 'True':
        st.session_state.inputs_limitedc[f"no_bene_field"].fill_option(mbene1, 'There are no natural persons,')
    


    def first_sub_field(n, lb):               
        st.session_state.inputs_limitedc[f"title_field{n}"].fill_option(page8,st.session_state.inputs_limitedc[f"title{lb}"],ind =1 if st.session_state.inputs_limitedc[f"title{lb}"]==" Miss "  else 0, new_x=-32 if st.session_state.inputs_limitedc[f"title{lb}"]==" Mrs " or st.session_state.inputs_limitedc[f"title{lb}"]==" Miss " else 0)
        st.session_state.inputs_limitedc[f"first_name_field{n}"].fill_field(page8, st.session_state.inputs_limitedc[f"first_name{lb}"].upper(), 0)
        st.session_state.inputs_limitedc[f"middle_name_field{n}"].fill_field(page8, st.session_state.inputs_limitedc[f"middle_name{lb}"].upper(), 0)
        st.session_state.inputs_limitedc[f"last_name_field{n}"].fill_field(page8, st.session_state.inputs_limitedc[f"last_name{lb}"].upper(), 0)
        st.session_state.inputs_limitedc[f"former_name_field{n}"].fill_field(page8, st.session_state.inputs_limitedc[f"former_name{n}"].upper(), 0)
        st.session_state.inputs_limitedc[f"gender_field{n}"].fill_option(page8,  st.session_state.inputs_limitedc[f"gender{n}"], 0, new_x=-48 if st.session_state.inputs_limitedc[f"gender{n}"]=='Female' else 0,partner=False)
        st.session_state.inputs_limitedc[f"dob_field{n}"].fill_field(page8,st.session_state.inputs_limitedc[f"dob{n}"].strftime("%d%m%Y"), 1)
        st.session_state.inputs_limitedc[f"pob_field{n}"].fill_field(page8, st.session_state.inputs_limitedc[f'birth_town_{n}'].upper(), 1)
        st.session_state.inputs_limitedc[f"nationality_field{n}"].fill_field(page8, st.session_state.inputs_limitedc[f"nationality{n}"].upper(), 0)
        st.session_state.inputs_limitedc[f"occupation_field{n}"].fill_field(page8, st.session_state.inputs_limitedc[f"occupation{n}"].upper(), 0)
        st.session_state.inputs_limitedc[f"tin_field{n}"].fill_field(page8, st.session_state.inputs_limitedc[f"tin{n}"].upper(), 0)
        st.session_state.inputs_limitedc[f"gh_card_field{n}"].fill_field(page8, st.session_state.inputs_limitedc[f"gh_card{n}"].upper(),1)
        st.session_state.inputs_limitedc[f"digital_address_field{n}"].fill_field(page8,st.session_state.inputs_limitedc[f"digital_address{n}"].upper(),0)
        st.session_state.inputs_limitedc[f"address_field{n}"].fill_field(page8, f'{st.session_state.inputs_limitedc[f"street_name{n}"]}, {st.session_state.inputs_limitedc[f"house_num{n}"]} {st.session_state.inputs_limitedc[f"house_address{n}"]}'.upper(), 1) 
        st.session_state.inputs_limitedc[f"shares_field{n}"].fill_field(page8, str(st.session_state.inputs_limitedc[f"shares{n}"]), 0) 
        st.session_state.inputs_limitedc[f"payable_field{n}"].fill_field(page8, str(st.session_state.inputs_limitedc[f"payable{n}"]), 1)

    def second_sub_field(n, i):
        st.session_state.inputs_limitedc[f"title_field{n}"].fill_option(page8,st.session_state.inputs_limitedc[f"title{i}"], ind =0 if st.session_state.inputs_limitedc[f"title{i}"]==" Miss "  else 1, new_x=-32 if st.session_state.inputs_limitedc[f"title{i}"]==" Mrs " or st.session_state.inputs_limitedc[f"title{i}"]==" Miss " else 0)
        st.session_state.inputs_limitedc[f"first_name_field{n}"].fill_field(page8, st.session_state.inputs_limitedc[f"first_name{i}"].upper(), ind=1 )
        st.session_state.inputs_limitedc[f"middle_name_field{n}"].fill_field(page8, st.session_state.inputs_limitedc[f"middle_name{i}"].upper(), ind=1 )
        st.session_state.inputs_limitedc[f"last_name_field{n}"].fill_field(page8, st.session_state.inputs_limitedc[f"last_name{i}"].upper(), ind=1 )
        st.session_state.inputs_limitedc[f"former_name_field{n}"].fill_field(page8, st.session_state.inputs_limitedc[f"former_name{n}"].upper(), ind=1 )
        st.session_state.inputs_limitedc[f"gender_field{n}"].fill_option(page8,st.session_state.inputs_limitedc[f"gender{n}"], ind=1,new_x=-48 if st.session_state.inputs_limitedc[f"gender{n}"]=='Female' else 0, partner=False)
        st.session_state.inputs_limitedc[f"dob_field{n}"].fill_field(page8,st.session_state.inputs_limitedc[f"dob{n}"].strftime("%d%m%Y"),ind=0 )
        st.session_state.inputs_limitedc[f"pob_field{n}"].fill_field(page8,st.session_state.inputs_limitedc[f'birth_town_{n}'].upper(), ind=0 )
        st.session_state.inputs_limitedc[f"nationality_field{n}"].fill_field(page8, st.session_state.inputs_limitedc[f"nationality{n}"].upper(), ind=1 )
        st.session_state.inputs_limitedc[f"occupation_field{n}"].fill_field(page8, st.session_state.inputs_limitedc[f"occupation{n}"].upper(), ind=1 )
        st.session_state.inputs_limitedc[f"tin_field{n}"].fill_field(page8, st.session_state.inputs_limitedc[f"tin{n}"].upper(), ind=1 )
        st.session_state.inputs_limitedc[f"gh_card_field{n}"].fill_field(page8, st.session_state.inputs_limitedc[f"gh_card{n}"].upper(), ind=0 )
        st.session_state.inputs_limitedc[f"digital_address_field{n}"].fill_field(page8,st.session_state.inputs_limitedc[f"digital_address{n}"].upper(), ind=1)
        st.session_state.inputs_limitedc[f"address_field{n}"].fill_field(page8, f'{st.session_state.inputs_limitedc[f"street_name{n}"]}, {st.session_state.inputs_limitedc[f"house_num{n}"]} {st.session_state.inputs_limitedc[f"house_address{n}"]}'.upper(), ind=2 ) 
        st.session_state.inputs_limitedc[f"shares_field{n}"].fill_field(page8, str(st.session_state.inputs_limitedc[f"shares{n}"]), ind=1 ) 
        st.session_state.inputs_limitedc[f"payable_field{n}"].fill_field(page8, str(st.session_state.inputs_limitedc[f"payable{n}"]), ind=0)
    def first_cop_sub(p, x):
        i = 6 + (2*st.session_state.inputs_limitedc['dir_num'])
        body(p,pn=x, fill=True, page=page9, gh=False)
        payshare(p, fill=True, page=page9, address='no')
        st.session_state.inputs_limitedc["authtin_field"] = boxes("TIN", c_x=35)
        if st.session_state.inputs_limitedc["secretary_cop"] == "Individual":
            sec = st.session_state.inputs_limitedc[f"first_namex"]+' '+   st.session_state.inputs_limitedc[f"middle_namex"] + ' ' + st.session_state.inputs_limitedc[f"last_namex"]
            tin = st.session_state.inputs_limitedc[f"tin{i}"]
        else:
            sec=st.session_state.inputs_limitedc[f"name_repre{i}"]
            tin = st.session_state.inputs_limitedc[f"tinrep{i}"]
        if st.session_state.inputs_limitedc["authenticatexx"]=='YES':
            st.session_state.inputs_limitedc["authtin_field"].fill_field(page9, st.session_state.inputs_limitedc["tin6"].upper(),5)
            st.session_state.inputs_limitedc["gh_card_field6"].fill_field(page9, st.session_state.inputs_limitedc["gh_card6"].upper())
            st.session_state.inputs_limitedc["auth_field"]=boxes("Name")
            name1 = st.session_state.inputs_limitedc["first_name6"]+' '+   st.session_state.inputs_limitedc["middle_name6"] + ' ' + st.session_state.inputs_limitedc["last_name6"]
            st.session_state.inputs_limitedc["auth_field"].fill_field(page9, name1.upper(),0)

            st.session_state.inputs_limitedc["authtin_field"].fill_field(page9, tin.upper(),7)
            st.session_state.inputs_limitedc[f"gh_card_field{i}"].fill_field(page9, st.session_state.inputs_limitedc[f"gh_card{i}"].upper(),1)
            st.session_state.inputs_limitedc["auth_field"]=boxes("Name")
            st.session_state.inputs_limitedc["auth_field"].fill_field(page9, sec.upper(),5)

        else:   
            st.session_state.inputs_limitedc["authtin_field"].fill_field(page9, st.session_state.inputs_limitedc["tin6"].upper(),6)
            st.session_state.inputs_limitedc["gh_card_field6"].fill_field(page9, st.session_state.inputs_limitedc["gh_card6"].upper(),2)
            st.session_state.inputs_limitedc["auth_field"]=boxes("Name")
            name1 = st.session_state.inputs_limitedc["first_name1"]+' '+   st.session_state.inputs_limitedc["middle_name1"] + ' ' + st.session_state.inputs_limitedc["last_name1"]
            st.session_state.inputs_limitedc["auth_field"].fill_field(page9, name1.upper(),2)


            st.session_state.inputs_limitedc["authtin_field"].fill_field(page9, st.session_state.inputs_limitedc["tin8"].upper(),2)
            st.session_state.inputs_limitedc["gh_card_field8"].fill_field(page9, st.session_state.inputs_limitedc["gh_card8"].upper(),3)
            auth_field=boxes("Name")
            name2 = st.session_state.inputs_limitedc["first_name2"]+' '+   st.session_state.inputs_limitedc["middle_name2"] + ' ' + st.session_state.inputs_limitedc["last_name2"]
            auth_field.fill_field(page9, name2.upper(),1 )

            
            st.session_state.inputs_limitedc["authtin_field"].fill_field(page9, tin.upper(),1)
            st.session_state.inputs_limitedc[f"gh_card_field{i}"].fill_field(page9, st.session_state.inputs_limitedc[f"gh_card{i}"].upper(),4)
            st.session_state.inputs_limitedc["auth_field"]=boxes("Name")
            st.session_state.inputs_limitedc["auth_field"].fill_field(page10, sec.upper())
            
    def add_subs(n , i):
        pdf_file = 'backend/limited_company/data/Additional-SUBSCRIBER-Form-Individuals.pdf'
        doc_sub = fitz.open(pdf_file)
        sub1 = doc_sub[0]
        st.session_state.inputs_limitedc["company_name_fielddir"]= boxes("Company Name*", c_x=96, bpr=25, t_row=2, control=1.4)
        st.session_state.inputs_limitedc["company_name_fielddir"].fill_field(sub1, st.session_state.inputs_limitedc['company_name'].upper())
        personal(i, n, fill=True, form3=True, page=sub1, add_sub=1)
        payshare(n, fill=True, page=sub1, address='yes', ind=1)
        gh_tin(n,fill=True,page=sub1)
        st.session_state.inputs_limitedc[f"digital_address_field{n}"].fill_field(sub1,st.session_state.inputs_limitedc[f"digital_address{n}"].upper())  
        additional_sub =  f"outputlc/Additional-Individual-SubscriberForm-{st.session_state.inputs_limitedc[f'first_name{i}']}.pdf"
        doc_sub.save(additional_sub)
        doc_sub.close()
        subscribers.append(additional_sub) 
    def add_cop_subs(val, x):
        i = 6 + (2*st.session_state.inputs_limitedc['dir_num'])
        pdf_file = 'backend/limited_company/data/Additional-In-Case-the-Subscriber-is-a-Body-Corporate-Form.pdf'
        doc_sub_cop = fitz.open(pdf_file)
        sub_cop1=doc_sub_cop[0]
        sub_cop2=doc_sub_cop[1]
        body(val,pn=x,  fill=True, page=sub_cop1, gh=False, extra=True)
        payshare(val, fill=True, page=sub_cop1, address='no')
        st.session_state.inputs_limitedc["authtin_field"] = boxes("TIN", c_x=35)
        if st.session_state.inputs_limitedc["secretary_cop"] == "Individual":
            sec = st.session_state.inputs_limitedc[f"first_namex"]+' '+   st.session_state.inputs_limitedc[f"middle_namex"] + ' ' + st.session_state.inputs_limitedc[f"last_namex"]
            tin = st.session_state.inputs_limitedc[f"tin{i}"]
        else:
            sec=st.session_state.inputs_limitedc[f"name_repre{i}"]
            tin = st.session_state.inputs_limitedc[f"tinrep{i}"]

        if st.session_state.inputs_limitedc["authenticatexx"]=='YES':
            st.session_state.inputs_limitedc["authtin_field"].fill_field(sub_cop1, st.session_state.inputs_limitedc["tin6"].upper())
            st.session_state.inputs_limitedc["gh_card_field6"].fill_field(sub_cop1, st.session_state.inputs_limitedc["gh_card6"].upper())
            st.session_state.inputs_limitedc["auth_field"]=boxes("Name")
            name1 = st.session_state.inputs_limitedc["first_name1"]+' '+   st.session_state.inputs_limitedc["middle_name1"] + ' ' + st.session_state.inputs_limitedc["last_name1"]
            st.session_state.inputs_limitedc["auth_field"].fill_field(sub_cop1, name1.upper())

            st.session_state.inputs_limitedc["authtin_field"].fill_field(sub_cop1, tin.upper())
            st.session_state.inputs_limitedc[f"gh_card_field{i}"].fill_field(page9, st.session_state.inputs_limitedc[f"gh_card{i}"].upper())
            st.session_state.inputs_limitedc["auth_field"]=boxes("Name")
            st.session_state.inputs_limitedc["auth_field"].fill_field(sub_cop1, sec.upper())

        else:   
            st.session_state.inputs_limitedc["authtin_field"].fill_field(sub_cop2, st.session_state.inputs_limitedc["tin6"].upper())
            st.session_state.inputs_limitedc["gh_card_field6"].fill_field(sub_cop2, st.session_state.inputs_limitedc["gh_card6"].upper())
            st.session_state.inputs_limitedc["auth_field"]=boxes("Name")
            name1 = st.session_state.inputs_limitedc["first_name1"]+' '+   st.session_state.inputs_limitedc["middle_name1"] + ' ' + st.session_state.inputs_limitedc["last_name1"]
            st.session_state.inputs_limitedc["auth_field"].fill_field(sub_cop2, name1.upper())

            st.session_state.inputs_limitedc["authtin_field"].fill_field(sub_cop2, st.session_state.inputs_limitedc["tin8"].upper())
            st.session_state.inputs_limitedc["gh_card_field8"].fill_field(sub_cop2, st.session_state.inputs_limitedc["gh_card8"].upper())
            auth_field=boxes("Name")
            name2 = st.session_state.inputs_limitedc["first_name2"]+' '+   st.session_state.inputs_limitedc["middle_name2"] + ' ' + st.session_state.inputs_limitedc["last_name2"]
            auth_field.fill_field(sub_cop2, name2.upper())
    
            st.session_state.inputs_limitedc["authtin_field"].fill_field(sub_cop2, tin.upper())
            st.session_state.inputs_limitedc[f"gh_card_field{i}"].fill_field(sub_cop2, st.session_state.inputs_limitedc[f"gh_card{i}"].upper())
            st.session_state.inputs_limitedc["auth_field"]=boxes("Name")
            st.session_state.inputs_limitedc["auth_field"].fill_field(sub_cop2, sec.upper())

        subcop = f"outputlc/Additional-Subscriber-Body-Corporate-{st.session_state.inputs_limitedc[f'coporate_name{x}']}.pdf"
        doc_sub_cop.save(subcop)
        doc_sub_cop.close()
        subscribers.append(subcop) 
    bo1_name = 64
    bo1_type = 30 
    start=0
    def bo1(n, item, x):
        if  item == "bo2":  
            nonlocal start, bo1_name, bo1_type
            if start <=15:
                name = f"{st.session_state.inputs_limitedc[f'first_name{x}']} {st.session_state.inputs_limitedc[f'middle_name{x}']} {st.session_state.inputs_limitedc[f'last_name{x}']}"
                st.session_state.inputs_limitedc[f'name_bo1_field'] = field_plain_template(0,"Name of Beneficial Owner", 40,-1,bo1_name, r_h=0,t_rows=1)
                st.session_state.inputs_limitedc[f"name_bo1_field"].fill_field(mbene1, name.upper())
                st.session_state.inputs_limitedc[f"natural_bo1_field"] = PDFOptionField(control_x=-27, control_y=bo1_type)
                st.session_state.inputs_limitedc[f"natural_bo1_field"].fill_option(mbene1, 'Natural Person')
                bo1_name +=14
                bo1_type +=14
                start +=1   
        elif item == "bo3":  
            if start <=15:
                st.session_state.inputs_limitedc[f'name_bo1_field'] = field_plain_template(0,"Name of Beneficial Owner", 40,-1,bo1_name, r_h=0,t_rows=1)
                st.session_state.inputs_limitedc[f"name_bo1_field"].fill_field(mbene1, st.session_state.inputs_limitedc[f'coporate_name{x}'].upper())
                st.session_state.inputs_limitedc[f"public_bo1_field"] = PDFOptionField(control_x=-27, control_y=bo1_type)
                st.session_state.inputs_limitedc[f"public_bo1_field"].fill_option(mbene1, 'Publicly Listed Company')
                bo1_name +=14
                bo1_type +=14
                start +=1

        elif item == "bo4":  
            if start <=15:
                st.session_state.inputs_limitedc[f'name_bo1_field'] = field_plain_template(0,"Name of Beneficial Owner", 40,-1,bo1_name, r_h=0,t_rows=1)
                st.session_state.inputs_limitedc[f"name_bo1_field"].fill_field(mbene1, st.session_state.inputs_limitedc[f'coporate_name{x}'].upper())
                st.session_state.inputs_limitedc[f"gov_bo1_field"] = PDFOptionField(control_x=-20, control_y=bo1_type)
                st.session_state.inputs_limitedc[f"gov_bo1_field"].fill_option(mbene1, 'Government')
                bo1_name +=14
                bo1_type +=14
                start +=1
    def bo2(n, i):
        bene_file = 'backend/limited_company/data/BO2 Natural Person BO Form.pdf'
        doc_bene = fitz.open(bene_file)
        bene1 = doc_bene[0]
        bene2 = doc_bene[1]   
        st.session_state.inputs_limitedc[f"bopurpose_field{n}"].fill_option(bene1, st.session_state.inputs_limitedc[f"bopurpose"])
        st.session_state.inputs_limitedc[f'boother_field{n}'].fill_field(bene1, st.session_state.inputs_limitedc[f'boother'].upper())
        st.session_state.inputs_limitedc[f'bocom_field{n}'].fill_field(bene1, st.session_state.inputs_limitedc[f'company_name'].upper())
        st.session_state.inputs_limitedc[f'botin_field{n}'].fill_field(bene1, st.session_state.inputs_limitedc[f'botin'].upper())
        st.session_state.inputs_limitedc[f'borgd_field{n}'].fill_field(bene1, st.session_state.inputs_limitedc[f'borgd'].upper())
        st.session_state.inputs_limitedc[f'bocountry_field{n}'].fill_field(bene1, st.session_state.inputs_limitedc[f'bocountry'].upper())

    # #    Part B – Beneficial Owners Particulars
        st.session_state.inputs_limitedc[f'firstname_field'].fill_field(bene1, st.session_state.inputs_limitedc[f'first_name{i}'].upper())
        st.session_state.inputs_limitedc[f'familyname_field'].fill_field(bene1, st.session_state.inputs_limitedc[f'last_name{i}'].upper())
        st.session_state.inputs_limitedc[f'pname_field'].fill_field(bene1, st.session_state.inputs_limitedc[f'former_name{n}'].upper())
        st.session_state.inputs_limitedc[f'bodob_field'].fill_field(bene1, st.session_state.inputs_limitedc[f"dob{n}"].strftime('%d-%m-%y'))
        st.session_state.inputs_limitedc[f'bopob_field'].fill_field(bene1, st.session_state.inputs_limitedc[f'birth_town_{n}'].upper())
        st.session_state.inputs_limitedc[f'bonation_field'].fill_field(bene1, st.session_state.inputs_limitedc[f'nationality{n}'].upper())
        st.session_state.inputs_limitedc[f'boaddress_field'].fill_field(bene1, f'{st.session_state.inputs_limitedc[f"street_name{n}"]}, {st.session_state.inputs_limitedc[f"city{n}"]}, {st.session_state.inputs_limitedc[f"country{n}"]} {st.session_state.inputs_limitedc[f"postal_{n}"]}'.upper())
        st.session_state.inputs_limitedc[f'boservice_field'].fill_field(bene1, f'{st.session_state.inputs_limitedc[f"street_name1"]}, {st.session_state.inputs_limitedc[f"city1"]}, {st.session_state.inputs_limitedc["type"]} - {st.session_state.inputs_limitedc["postal_number"]}'.upper())
        st.session_state.inputs_limitedc[f'bodigi_field'].fill_field(bene1, st.session_state.inputs_limitedc[f'digital_address{n}'].upper())
        st.session_state.inputs_limitedc[f'botaxnum_field'].fill_field(bene1, st.session_state.inputs_limitedc[f'tin{n}'].upper())
        st.session_state.inputs_limitedc[f'bomobile_field'].fill_field(bene1, st.session_state.inputs_limitedc[f'mobile_num{n}'].upper())
        st.session_state.inputs_limitedc[f'boemail_field'].fill_field(bene1, st.session_state.inputs_limitedc[f'email{n}'].upper())
        st.session_state.inputs_limitedc[f'boidtype_field'].fill_field(bene1, 'National ID'.upper())
        st.session_state.inputs_limitedc[f'boidnum_field'].fill_field(bene1, st.session_state.inputs_limitedc[f'gh_card{n}'].upper())
        st.session_state.inputs_limitedc[f'boidcountry_field'].fill_field(bene1, 'Ghana'.upper())
        st.session_state.inputs_limitedc[f'doregis_field'].fill_field(bene1, st.session_state.inputs_limitedc[f'doregis{n}'].strftime('%d/%m/%y'))
        if n <= (2*st.session_state.inputs_limitedc['dir_num']):
            st.session_state.inputs_limitedc[f'bowork_field'].fill_field(bene1, f"{st.session_state.inputs_limitedc[f'city{n+1}']}, {st.session_state.inputs_limitedc[f'occupation{n}']}".upper())
        else:
            st.session_state.inputs_limitedc[f'bowork_field'].fill_field(bene1, f"{st.session_state.inputs_limitedc[f'city{n}']}, {st.session_state.inputs_limitedc[f'occupation{n}']}".upper())
        # Part C – Politically Exposed Persons (PEP)
        st.session_state.inputs_limitedc[f'pep_field'].fill_option(bene1, st.session_state.inputs_limitedc[f'pep{n}']) 
        st.session_state.inputs_limitedc[f'con_to_holder_field'].fill_option(bene1, st.session_state.inputs_limitedc[f'con_to_holder{n}'])  
        st.session_state.inputs_limitedc[f'pepfirstname_field'].fill_field(bene1, st.session_state.inputs_limitedc[f'pepfirstname{n}'].upper())  
        st.session_state.inputs_limitedc[f'pepsurname_field'].fill_field(bene1, st.session_state.inputs_limitedc[f'pepsurname_field{n}'].upper())  
        st.session_state.inputs_limitedc[f'pepprename_field'].fill_field(bene1, st.session_state.inputs_limitedc[f'pepprename_field{n}'].upper(), ind=2) 
        st.session_state.inputs_limitedc[f'holderdate_field'].fill_field(bene1, st.session_state.inputs_limitedc[f'holderdate{n}'].strftime('%d-%m-%Y')) 
        st.session_state.inputs_limitedc[f'pepexposed_field'].fill_option(bene1, st.session_state.inputs_limitedc[f'pepexposed{n}'])  
        st.session_state.inputs_limitedc[f'pepstat_field'].fill_option(bene2, st.session_state.inputs_limitedc[f'pepstat{n}']) 
        st.session_state.inputs_limitedc[f'peprole_field'].fill_field(bene2, st.session_state.inputs_limitedc[f'peprole_field{n}'].upper())  

        # Part D - Nature of Interest
        st.session_state.inputs_limitedc[f'sharehold_field{n}'].fill_option(bene2, st.session_state.inputs_limitedc[f'sharehold{n}'].upper())
        value = f'{round((st.session_state.inputs_limitedc[f"shares{n}"]/ st.session_state.inputs_limitedc[f"autoshares"])*100, 2)}%' if st.session_state.inputs_limitedc[f"autoshares"] else 0
        if st.session_state.inputs_limitedc[f"sharehold{n}"] == 'Yes – Direct':
            st.session_state.inputs_limitedc[f'direct_field{n}'].fill_field(bene2, str(value))
        elif st.session_state.inputs_limitedc[f"sharehold{n}"] == 'Yes – Indirect':
            st.session_state.inputs_limitedc[f'indirect_field{n}'].fill_field(bene2, str(value))

        # st.session_state.inputs_limitedc[f'direct_field{n}'].fill_field(bene2, st.session_state.inputs_limitedc[f'direct{n}'].upper())
        # st.session_state.inputs_limitedc[f'indirect_field{n}'].fill_field(bene2, st.session_state.inputs_limitedc[f'indirect{n}'].upper())

        st.session_state.inputs_limitedc[f'voting_field{n}'].fill_option(bene2, st.session_state.inputs_limitedc[f'voting{n}'].upper(), 3 if st.session_state.inputs_limitedc[f'voting{n}']=='Yes – Indirect' else 0)
        st.session_state.inputs_limitedc[f'vrightheld_field{n}'].fill_field(bene2, st.session_state.inputs_limitedc[f'vrightheld{n}'].upper())
        st.session_state.inputs_limitedc[f'voteright_field{n}'].fill_option(bene2, st.session_state.inputs_limitedc[f'voteright{n}'].upper(), 4 if st.session_state.inputs_limitedc[f'voteright{n}']=='YES' else 2)

        st.session_state.inputs_limitedc[f'apointright_field{n}'].fill_option(bene2, st.session_state.inputs_limitedc[f'apointright{n}'].upper(),5)
        st.session_state.inputs_limitedc[f'securities_field{n}'].fill_option(bene2, st.session_state.inputs_limitedc[f'securities{n}'].upper(), 6 if st.session_state.inputs_limitedc[f'securities{n}']=='Yes' else 0)
        st.session_state.inputs_limitedc[f'description_field1{n}'].fill_field(bene2, st.session_state.inputs_limitedc[f'description1{n}'].upper())

        st.session_state.inputs_limitedc[f'control_field{n}'].fill_option(bene2, st.session_state.inputs_limitedc[f'control{n}'], 7 if st.session_state.inputs_limitedc[f'control{n}']=='YES' else 6)
        st.session_state.inputs_limitedc[f'description_field1{n}'].fill_field(bene2, st.session_state.inputs_limitedc[f'description2{n}'].upper(), 1)
    
        bene = f"outputlc/Beneficiary(Individual) - {st.session_state.inputs_limitedc[f'first_name{i}'] + st.session_state.inputs_limitedc[f'last_name{i}']}.pdf"
        doc_bene.save(bene)
        doc_bene.close()
        beneficiaries.append(bene)

    def bo3(n, x):
        benex_file = 'backend/limited_company/data/BO3 Listed Company BO Form.pdf'
        doc_benex = fitz.open(benex_file)
        benex1 = doc_benex[0]
        benex2 = doc_benex[1]   
        st.session_state.inputs_limitedc[f"bopurpose_field{n}"].fill_option(benex1,st.session_state.inputs_limitedc[f"bopurpose"])
        st.session_state.inputs_limitedc[f'boother_field{n}'].fill_field(benex1,st.session_state.inputs_limitedc[f'boother'].upper())
        st.session_state.inputs_limitedc[f'bocom_field{n}'].fill_field(benex1,st.session_state.inputs_limitedc[f'company_name'].upper())
        st.session_state.inputs_limitedc[f'botin_field{n}'].fill_field(benex1,st.session_state.inputs_limitedc[f'botin'].upper())
        st.session_state.inputs_limitedc[f'borgd_field{n}'].fill_field(benex1,st.session_state.inputs_limitedc[f'borgd'].upper())
        st.session_state.inputs_limitedc[f'bocountry_field{n}'].fill_field(benex1,st.session_state.inputs_limitedc[f'bocountry'].upper())

        st.session_state.inputs_limitedc[f'listedname_field{n}'].fill_field(benex1,st.session_state.inputs_limitedc[f"coporate_name{x}"].upper())
        st.session_state.inputs_limitedc[f'idnum_field{n}'].fill_field(benex1,st.session_state.inputs_limitedc[f'idnum{n}'].upper(),2)
        st.session_state.inputs_limitedc[f'legalentity_field'].fill_field(benex1,st.session_state.inputs_limitedc[f'legalentity{n}'].upper())
        st.session_state.inputs_limitedc[f'percent_field'].fill_field(benex1,st.session_state.inputs_limitedc[f'percent{n}'].upper())

        user_id = f"benexx{n}"
        user_data = st.session_state.inputs_limitedc[user_id] 
        incre = 50
        for idx in range(len(user_data["table_data"]["Name of Stock Exchange"])):
            st.session_state.inputs_limitedc[f"name_field_{idx}"] = field_plain_template(0, 'Name of Stock Exchange', 25, 20, incre, t_rows=1)
            st.session_state.inputs_limitedc[f"name_field_{idx}"].fill_field(benex1, user_data["table_data"]["Name of Stock Exchange"][idx].upper())
            st.session_state.inputs_limitedc[f"percentage_field_{idx}"] = field_plain_template(0, 'Percentage of Shares',15, 5, incre, t_rows=1)
            st.session_state.inputs_limitedc[f"percentage_field_{idx}"].fill_field(benex1, user_data["table_data"]["Percentage of Shares Listed"][idx].upper(), 1)
            st.session_state.inputs_limitedc[f"link_field_{idx}"] = field_plain_template(0, 'Link to web address pages on stock exchange', 30, 5, incre, t_rows=1)
            st.session_state.inputs_limitedc[f"link_field_{idx}"].fill_field(benex1, user_data["table_data"]["Link to Web Address Pages on Stock Exchange"][idx].upper())
            incre += 15

        st.session_state.inputs_limitedc[f'sharehold_field{n}'].fill_option(benex1, st.session_state.inputs_limitedc[f'sharehold{n}'].upper())
        value = f'{round((st.session_state.inputs_limitedc[f"shares{n}"]/ st.session_state.inputs_limitedc[f"autoshares"])*100, 2)}%' if st.session_state.inputs_limitedc[f"autoshares"] else 0
        if st.session_state.inputs_limitedc[f"sharehold{n}"] == 'Yes – Direct':
            st.session_state.inputs_limitedc[f'direct_field{n}'].fill_field(benex1, str(value))
        elif st.session_state.inputs_limitedc[f"sharehold{n}"] == 'Yes – Indirect':
            st.session_state.inputs_limitedc[f'indirect_field{n}'].fill_field(benex1, str(value))

        # st.session_state.inputs_limitedc[f'direct_field{n}'].fill_field(benex1, st.session_state.inputs_limitedc[f'direct{n}'].upper())
        # st.session_state.inputs_limitedc[f'indirect_field{n}'].fill_field(benex1, st.session_state.inputs_limitedc[f'indirect{n}'].upper())

        st.session_state.inputs_limitedc[f'voting_field{n}'].fill_option(benex1, st.session_state.inputs_limitedc[f'voting{n}'].upper(), 3 if st.session_state.inputs_limitedc[f'voting{n}']=='Yes – Indirect' else 0)
        st.session_state.inputs_limitedc[f'vrightheld_field{n}'].fill_field(benex1, st.session_state.inputs_limitedc[f'vrightheld{n}'].upper())
        st.session_state.inputs_limitedc[f'voteright_field{n}'].fill_option(benex1, st.session_state.inputs_limitedc[f'voteright{n}'].upper(), 4 if st.session_state.inputs_limitedc[f'voteright{n}']=='YES' else 2)

        st.session_state.inputs_limitedc[f'apointright_field{n}'].fill_option(benex1, st.session_state.inputs_limitedc[f'apointright{n}'].upper(), 3 if st.session_state.inputs_limitedc[f'apointright{n}']=='NO' else 5)
        st.session_state.inputs_limitedc[f'securities_field{n}'].fill_option(benex1, st.session_state.inputs_limitedc[f'securities{n}'].upper(), 6 if st.session_state.inputs_limitedc[f'securities{n}']=='Yes' else 0)
        st.session_state.inputs_limitedc[f'description_field1{n}'].fill_field(benex1, st.session_state.inputs_limitedc[f'description1{n}'].upper())

        st.session_state.inputs_limitedc[f'control_field{n}'].fill_option(benex1, st.session_state.inputs_limitedc[f'control{n}'], 7 if st.session_state.inputs_limitedc[f'control{n}']=='YES' else 6)
        st.session_state.inputs_limitedc[f'description_field1{n}'].fill_field(benex2, st.session_state.inputs_limitedc[f'description2{n}'].upper())

        bene = f"outputlc/Beneficiary(Publicly Listed Company) - {st.session_state.inputs_limitedc[f'coporate_name{x}']}.pdf"
        doc_benex.save(bene)
        doc_benex.close()
        beneficiaries.append(bene)

    def bo4(n, x):
        bene_file = 'backend/limited_company/data/BO4 Government BO Form.pdf'
        doc_benexx = fitz.open(bene_file)
        benexx1 = doc_benexx[0]
        benexx2 = doc_benexx[1]  

        st.session_state.inputs_limitedc[f"bopurpose_field{n}"].fill_option(benexx1, st.session_state.inputs_limitedc[f"bopurpose"])
        st.session_state.inputs_limitedc[f'boother_field{n}'].fill_field(benexx1, st.session_state.inputs_limitedc[f'boother'].upper())
        st.session_state.inputs_limitedc[f'bocom_field{n}'].fill_field(benexx1, st.session_state.inputs_limitedc[f'company_name'].upper())
        st.session_state.inputs_limitedc[f'botin_field{n}'].fill_field(benexx1, st.session_state.inputs_limitedc[f'botin'].upper())
        st.session_state.inputs_limitedc[f'borgd_field{n}'].fill_field(benexx1, st.session_state.inputs_limitedc[f'borgd'].upper())
        st.session_state.inputs_limitedc[f'bocountry_field{n}'].fill_field(benexx1, st.session_state.inputs_limitedc[f'bocountry'].upper())

        # Part B – Beneficial Owners Particulars
        st.session_state.inputs_limitedc[f'governmentname_field{n}'].fill_field(benexx1, st.session_state.inputs_limitedc[f"coporate_name{x}"].upper())
        st.session_state.inputs_limitedc[f'boservice_field{n}'].fill_field(benexx1, f'{st.session_state.inputs_limitedc[f"coporate_address{n}"]}, {st.session_state.inputs_limitedc[f"coporate_pobox{n}"]}'.upper())
        st.session_state.inputs_limitedc[f'boemail_field{n}'].fill_field(benexx1, st.session_state.inputs_limitedc[f'boemail{n}'].upper())
        st.session_state.inputs_limitedc[f'boidcountry_field{n}'].fill_field(benexx1, st.session_state.inputs_limitedc[f'boidcountry{n}'].upper())
        st.session_state.inputs_limitedc[f'bonation_field{n}'].fill_field(benexx1, st.session_state.inputs_limitedc[f'bonation{n}'].upper())
        st.session_state.inputs_limitedc[f'oficialrepre_field'].fill_field(benexx1, st.session_state.inputs_limitedc[f"name_repre{n}"].upper())
        st.session_state.inputs_limitedc[f'currentrole_field'].fill_field(benexx1, st.session_state.inputs_limitedc[f'currentrole{n}'].upper())
        st.session_state.inputs_limitedc[f'bomobile_field{n}'].fill_field(benexx1, st.session_state.inputs_limitedc[f'bomobile{n}'].upper())

        st.session_state.inputs_limitedc[f'sharehold_field{n}'].fill_option(benexx1, st.session_state.inputs_limitedc[f'sharehold{n}'].upper())
        value = f'{round((st.session_state.inputs_limitedc[f"shares{n}"]/ st.session_state.inputs_limitedc[f"autoshares"])*100, 2)}%' if st.session_state.inputs_limitedc[f"autoshares"] else 0
        if st.session_state.inputs_limitedc[f"sharehold{n}"] == 'Yes – Direct':
            st.session_state.inputs_limitedc[f'direct_field{n}'].fill_field(benexx1, str(value))
        elif st.session_state.inputs_limitedc[f"sharehold{n}"] == 'Yes – Indirect':
            st.session_state.inputs_limitedc[f'indirect_field{n}'].fill_field(benexx1, str(value))
        # st.session_state.inputs_limitedc[f'direct_field{n}'].fill_field(benexx1, st.session_state.inputs_limitedc[f'direct{n}'].upper())
        # st.session_state.inputs_limitedc[f'indirect_field{n}'].fill_field(benexx1, st.session_state.inputs_limitedc[f'indirect{n}'].upper())
    
    
    
    
        st.session_state.inputs_limitedc[f'voting_field{n}'].fill_option(benexx1, st.session_state.inputs_limitedc[f'voting{n}'].upper(), 3 if st.session_state.inputs_limitedc[f'voting{n}']=='Yes – Indirect' else 0)
        st.session_state.inputs_limitedc[f'vrightheld_field{n}'].fill_field(benexx1, st.session_state.inputs_limitedc[f'vrightheld{n}'].upper())
        st.session_state.inputs_limitedc[f'voteright_field{n}'].fill_option(benexx1, st.session_state.inputs_limitedc[f'voteright{n}'].upper(), 4 if st.session_state.inputs_limitedc[f'voteright{n}']=='YES' else 3)
        st.session_state.inputs_limitedc[f'apointright_field{n}'].fill_option(benexx1, st.session_state.inputs_limitedc[f'apointright{n}'].upper(), 4 if st.session_state.inputs_limitedc[f'apointright{n}']=='NO' else 5)
        st.session_state.inputs_limitedc[f'securities_field{n}'].fill_option(benexx1, st.session_state.inputs_limitedc[f'securities{n}'].upper(), 6 if st.session_state.inputs_limitedc[f'securities{n}']=='Yes' else 0)
        st.session_state.inputs_limitedc[f'description_field1{n}'].fill_field(benexx1, st.session_state.inputs_limitedc[f'description1{n}'].upper())
        st.session_state.inputs_limitedc[f'control_field{n}'].fill_option(benexx1, st.session_state.inputs_limitedc[f'control{n}'], 7 if st.session_state.inputs_limitedc[f'control{n}']=='YES' else 7)
        st.session_state.inputs_limitedc[f'description_field1{n}'].fill_field(benexx1, st.session_state.inputs_limitedc[f'description2{n}'].upper(),1)
        bene = f"outputlc/Beneficiary(Government) - {st.session_state.inputs_limitedc[f'coporate_name{x}']}.pdf"
        doc_benexx.save(bene)
        doc_benexx.close()
        beneficiaries.append(bene)
                
    
    def trusteeform3(i, numtrust):
        st.session_state.inputs_limitedc[f"tin_field{numtrust}"].fill_field(page10, st.session_state.inputs_limitedc[f"tin{numtrust}"].upper(),1)
        st.session_state.inputs_limitedc[f"gh_card_field{numtrust}"].fill_field(page10, st.session_state.inputs_limitedc[f"gh_card{numtrust}"].upper())
        personal(i, numtrust, fill=True, page=page10, form3=True, place_ob=False, dob=False, trust=True)
        payshare(numtrust,address='yes', fill=True, page=page10)
        st.session_state.inputs_limitedc[f"digital_address_field{numtrust}"].fill_field(page10, st.session_state.inputs_limitedc[f"digital_address{numtrust}"].upper())
        st.session_state.inputs_limitedc[f"name_minor_field{numtrust}"].fill_field(page10,st.session_state.inputs_limitedc[f"name_minor{numtrust}"].upper())
        st.session_state.inputs_limitedc[f"dob_minor_field{numtrust}"].fill_field(page10,st.session_state.inputs_limitedc[f"dob_minor{numtrust}"].strftime("%d%m%Y"))
        st.session_state.inputs_limitedc[f"id_minor_field{numtrust}"].fill_field(page10,'National ID'.upper())
        st.session_state.inputs_limitedc[f"ref_minor_field{numtrust}"].fill_field(page10,st.session_state.inputs_limitedc[f"gh_card{numtrust}"].upper())

    def trustee_cop(n,x):
        i = 6 +(2 * st.session_state.inputs_limitedc["dir_num"])
        body(n,pn=x,  fill=True, page=page10, namerep=False, gh=False, trust=True)
        payshare(n,address='no', fill=True, page=page11)
        st.session_state.inputs_limitedc["authtin_field"] = boxes("TIN", c_x=35)
        if st.session_state.inputs_limitedc["secretary_cop"] == "Individual":
            sec = st.session_state.inputs_limitedc[f"first_namex"]+' '+   st.session_state.inputs_limitedc[f"middle_namex"] + ' ' + st.session_state.inputs_limitedc[f"last_namex"]
            tin = st.session_state.inputs_limitedc[f"tin{i}"]
        else:
            sec=st.session_state.inputs_limitedc[f"name_repre{i}"]
            tin = st.session_state.inputs_limitedc[f"tinrep{i}"]

        if st.session_state.inputs_limitedc["authenticatexx"]=='YES':
            st.session_state.inputs_limitedc["authtin_field"].fill_field(page10, st.session_state.inputs_limitedc["tin6"].upper())
            st.session_state.inputs_limitedc["gh_card_field6"].fill_field(page10, st.session_state.inputs_limitedc["gh_card6"].upper(), 1)
            st.session_state.inputs_limitedc["auth_field"]=boxes("Name*")
            name1 = st.session_state.inputs_limitedc["first_name1"]+' '+   st.session_state.inputs_limitedc["middle_name1"] + ' ' + st.session_state.inputs_limitedc["last_name1"]
            st.session_state.inputs_limitedc["auth_field"].fill_field(page10, name1.upper(), 1)

            st.session_state.inputs_limitedc["authtin_field"].fill_field(page11, tin.upper())
            st.session_state.inputs_limitedc[f"gh_card_field{i}"].fill_field(page11, st.session_state.inputs_limitedc[f"gh_card{i}"].upper(),2)
            st.session_state.inputs_limitedc["auth_field"]=boxes("Name")
            st.session_state.inputs_limitedc["auth_field"].fill_field(page11, sec.upper(),1)
        
        else:   
            st.session_state.inputs_limitedc["authtin_field"].fill_field(page11, st.session_state.inputs_limitedc["tin6"].upper(),1)
            st.session_state.inputs_limitedc["gh_card_field6"].fill_field(page11, st.session_state.inputs_limitedc["gh_card6"].upper(), 3)
            st.session_state.inputs_limitedc["auth_field"]=boxes("Name")
            name1 = st.session_state.inputs_limitedc["first_name1"]+' '+   st.session_state.inputs_limitedc["middle_name1"] + ' ' + st.session_state.inputs_limitedc["last_name1"]
            st.session_state.inputs_limitedc["auth_field"].fill_field(page11, name1.upper(),5)

            st.session_state.inputs_limitedc["authtin_field"].fill_field(page11, st.session_state.inputs_limitedc["tin8"].upper(),ind=3)
            st.session_state.inputs_limitedc["gh_card_field8"].fill_field(page11, st.session_state.inputs_limitedc["gh_card8"].upper())
            auth_field=boxes("Name")
            name2 = st.session_state.inputs_limitedc["first_name2"]+' '+   st.session_state.inputs_limitedc["middle_name2"] + ' ' + st.session_state.inputs_limitedc["last_name2"]
            auth_field.fill_field(page11, name2.upper())

            st.session_state.inputs_limitedc["authtin_field"].fill_field(page11, tin.upper(),2)
            st.session_state.inputs_limitedc[f"gh_card_field{i}"].fill_field(page11, st.session_state.inputs_limitedc[f"gh_card{i}"].upper(),1)
            st.session_state.inputs_limitedc["auth_field"]=boxes("Name")
            st.session_state.inputs_limitedc["auth_field"].fill_field(page11, sec.upper(),2)

        st.session_state.inputs_limitedc[f"name_minor_field{n}"].fill_field(page11, st.session_state.inputs_limitedc[f"name_minor{n}"].upper())
        st.session_state.inputs_limitedc[f"dob_minor_field{n}"].fill_field(page11,st.session_state.inputs_limitedc[f"dob_minor{n}"].strftime("%d%m%Y"))
        st.session_state.inputs_limitedc[f"id_minor_field{n}"].fill_field(page11, "National ID".upper())
        st.session_state.inputs_limitedc[f"ref_minor_field{n}"].fill_field(page11, st.session_state.inputs_limitedc[f"gh_card{n}"].upper())
        
            
    
    def add_trustee(t, x):
        i = 6 +(2 * st.session_state.inputs_limitedc["dir_num"])
        pdf_file = 'backend/limited_company/data/Additional Shares In Trust for Minor(s).pdf'
        doc_trust = fitz.open(pdf_file)
        trust1 = doc_trust[0]
        trust2 = doc_trust[1]
        st.session_state.inputs_limitedc["company_name_field"].fill_field(trust1, st.session_state.inputs_limitedc['company_name'].upper())
        st.session_state.inputs_limitedc[f"tin_field{t}"].fill_field(trust1, st.session_state.inputs_limitedc[f"tin{t}"].upper())
        st.session_state.inputs_limitedc[f"gh_card_field{t}"].fill_field(trust1, st.session_state.inputs_limitedc[f"gh_card{t}"].upper())
        personal(x, t, fill=True, page=trust1, form3=True, place_ob=False, dob=False)
        payshare(t, fill=True, page=trust1, ind=1)
        st.session_state.inputs_limitedc[f"digital_address_field{t}"].fill_field(trust1,st.session_state.inputs_limitedc[f"digital_address{t}"].upper())
        st.session_state.inputs_limitedc[f"name_minor_field{t}"].fill_field(trust1,st.session_state.inputs_limitedc[f"name_minor{t}"].upper())
        st.session_state.inputs_limitedc[f"dob_minor_field{t}"].fill_field(trust1,st.session_state.inputs_limitedc[f"dob_minor{t}"].strftime("%d%m%Y"))
        trustee_minor = f"outputlc/Additional Trustees(Minor)-{st.session_state.inputs_limitedc[f'first_name{x}']}.pdf"
        doc_trust.save(trustee_minor)
        doc_trust.close()
        trustees.append(trustee_minor)            

    def add_cop_trustee(tc, m):
        i = 6 +(2 * st.session_state.inputs_limitedc["dir_num"])
        pdf_file = 'backend/limited_company/data/Additional Shares In Trust for Minor(s).pdf'
        doc_trust = fitz.open(pdf_file)
        trust1 = doc_trust[0]
        trust2 = doc_trust[1]   
        st.session_state.inputs_limitedc["company_name_field"].fill_field(trust1, st.session_state.inputs_limitedc['company_name'].upper())
        body(tc, fill=True, page=trust1, namerep=False, gh=False, trust=True)
        payshare(tc,address='no', fill=True, page=trust2)
        
        if st.session_state.inputs_limitedc["secretary_cop"] == "Individual":
            sec = st.session_state.inputs_limitedc[f"first_namex"]+' '+   st.session_state.inputs_limitedc[f"middle_namex"] + ' ' + st.session_state.inputs_limitedc[f"last_namex"]
            tin = st.session_state.inputs_limitedc[f"tin{i}"]
        else:
            sec=st.session_state.inputs_limitedc[f"name_repre{i}"]
            tin=st.session_state.inputs_limitedc[f"tinrep{i}"]

        st.session_state.inputs_limitedc["authtin_field"] = boxes("TIN", c_x=35)
        if st.session_state.inputs_limitedc["authenticatexx"]=='YES':
            st.session_state.inputs_limitedc["authtin_field"].fill_field(trust2, st.session_state.inputs_limitedc["tin6"].upper(),0)
            st.session_state.inputs_limitedc["gh_card_field6"].fill_field(trust2, st.session_state.inputs_limitedc["gh_card6"].upper(),2)
            st.session_state.inputs_limitedc["auth_field"]=boxes("Name")
            name1 = st.session_state.inputs_limitedc["first_name1"]+' '+   st.session_state.inputs_limitedc["middle_name1"] + ' ' + st.session_state.inputs_limitedc["last_name1"]
            st.session_state.inputs_limitedc["auth_field"].fill_field(trust2, name1.upper(), 3)

            st.session_state.inputs_limitedc["authtin_field"].fill_field(trust2, tin.upper(),3)
            st.session_state.inputs_limitedc[f"gh_card_field{i}"].fill_field(trust2, st.session_state.inputs_limitedc[f"gh_card{i}"].upper(),3)
            st.session_state.inputs_limitedc["auth_field"]=boxes("Name")
            st.session_state.inputs_limitedc["auth_field"].fill_field(trust2, sec.upper(),0)


        else:   
            st.session_state.inputs_limitedc["authtin_field"].fill_field(trust2, st.session_state.inputs_limitedc["tin6"].upper(),4)
            st.session_state.inputs_limitedc["gh_card_field6"].fill_field(trust2, st.session_state.inputs_limitedc["gh_card6"].upper(),4)
            st.session_state.inputs_limitedc["auth_field"]=boxes("Name")
            name1 = st.session_state.inputs_limitedc["first_name1"]+' '+   st.session_state.inputs_limitedc["middle_name1"] + ' ' + st.session_state.inputs_limitedc["last_name1"]
            st.session_state.inputs_limitedc["auth_field"].fill_field(trust2, name1.upper(),1)


            st.session_state.inputs_limitedc["authtin_field"].fill_field(trust2, st.session_state.inputs_limitedc["tin8"].upper(),2)
            st.session_state.inputs_limitedc["gh_card_field8"].fill_field(trust2, st.session_state.inputs_limitedc["gh_card8"].upper(),0)
            auth_field=boxes("Name")
            name2 = st.session_state.inputs_limitedc["first_name2"]+' '+   st.session_state.inputs_limitedc["middle_name2"] + ' ' + st.session_state.inputs_limitedc["last_name2"]
            auth_field.fill_field(trust2, name2.upper(),4)

            
            st.session_state.inputs_limitedc["authtin_field"].fill_field(trust2, tin.upper(),1)
            st.session_state.inputs_limitedc[f"gh_card_field{i}"].fill_field(trust2, st.session_state.inputs_limitedc[f"gh_card{i}"].upper(),1)
            st.session_state.inputs_limitedc["auth_field"]=boxes("Name")
            st.session_state.inputs_limitedc["auth_field"].fill_field(trust2, sec.upper(),5)

        st.session_state.inputs_limitedc[f"name_minor_field{tc}"].fill_field(trust2, st.session_state.inputs_limitedc[f"name_minor{tc}"].upper())
        st.session_state.inputs_limitedc[f"dob_minor_field{tc}"].fill_field(trust2,st.session_state.inputs_limitedc[f"dob_minor{tc}"].strftime("%d%m%Y"))

        trustee_minor = f"outputlc/Additional Trustees(Minor)-{st.session_state.inputs_limitedc[f'coporate_name{m}']}.pdf"
        doc_trust.save(trustee_minor)
        doc_trust.close()
        trustees.append(trustee_minor)
        


    st.session_state.inputs_limitedc['first_sub_field'] = False
    st.session_state.inputs_limitedc['second_sub_field'] = False
    st.session_state.inputs_limitedc['first_sub_cop_field'] = False
    st.session_state.inputs_limitedc['subcount'] = 0
    st.session_state.inputs_limitedc['trusteeform3'] = False
    st.session_state.inputs_limitedc['trusteecopform3']=False
        

        #############DIRECTORS
    try: 
        c = 1
        ind = 0
        for i in range(6, 6+(2 * st.session_state.inputs_limitedc["dir_num"])):
            if not i%2:
                if st.session_state.inputs_limitedc.get(f'dirsub{c}')=='No' or  st.session_state.inputs_limitedc.get(f'dirsub{c}')=='Yes': 
                    st.session_state.inputs_limitedc['subcount'] += 1
                    cover('SUBSCRIBER',count=st.session_state.inputs_limitedc['subcount'], lbl=i, ind=3+st.session_state.inputs_limitedc['subcount'] , maxi=55, controlx=125)
                    bo2(i, c)
                    bo1(i, 'bo2',c)
                    if st.session_state.inputs_limitedc['first_sub_field'] == False:
                        first_sub_field(i, c)
                        st.session_state.inputs_limitedc['first_sub_field']=True
                    elif st.session_state.inputs_limitedc['second_sub_field']==False:
                        second_sub_field(i, c)
                        st.session_state.inputs_limitedc['second_sub_field']=True
                    else:
                        add_subs(i, c)
                if  st.session_state.inputs_limitedc.get(f'dirsub{c}')=='Yes': 
                    if st.session_state.inputs_limitedc['trusteeform3'] == False:
                        trusteeform3(c, i)
                        st.session_state.inputs_limitedc['trusteeform3'] = True
                    else:
                        add_trustee(i, c)

                tax(i,pn=c, fill=True, l=directors, label='Director')
                cover('DIRECTOR', count=c, lbl=i, ind=ind)
                

                pdf_dirA = 'backend/limited_company/data/FORM 26 (A) Consent to Act as A Director.pdf'
                doc_dirA =  fitz.open(pdf_dirA)
                dirA1 = doc_dirA[0]

                
                pdf_dirB = 'backend/limited_company/data/Form 26 (C) Statutory Declaration Director.pdf'
                doc_dirB =  fitz.open(pdf_dirB)
                dirB1 = doc_dirB[0]

                fullname = st.session_state.inputs_limitedc[f"first_name{c}"]+' '+   st.session_state.inputs_limitedc[f"middle_name{c}"] + ' ' + st.session_state.inputs_limitedc[f"last_name{c}"]
                resaddr = f'{st.session_state.inputs_limitedc[f"digital_address{i}"]} {st.session_state.inputs_limitedc[f"house_address{i}"]} {st.session_state.inputs_limitedc[f"house_num{i}"]}'
                st.session_state.inputs_limitedc[f'cdir_name_field'].fill_field(dirA1, st.session_state.inputs_limitedc['company_name'].upper(), fs=14)
                st.session_state.inputs_limitedc[f'fullname_field'].fill_field(dirA1, fullname.upper(), fs=14)
                st.session_state.inputs_limitedc[f'formername_field'].fill_field(dirA1, st.session_state.inputs_limitedc[f"former_name{i}"].upper(), fs=14)
                st.session_state.inputs_limitedc[f'pbox_field'].fill_field(dirA1, st.session_state.inputs_limitedc[f'postal_number'].upper() if st.session_state.inputs_limitedc[f'type']=='P O Box' else '', fs=14)
                st.session_state.inputs_limitedc[f'resaddre_field'].fill_field(dirA1, resaddr.upper(), fs=14)
                st.session_state.inputs_limitedc[f'con_field'].fill_field(dirA1, st.session_state.inputs_limitedc[f"mobile_num{i}"].upper(), fs=14)
                st.session_state.inputs_limitedc[f'dirdate_field'].fill_field(dirA1, datetime.now().date().strftime("%d-%m-%Y"), fs=14)

                st.session_state.inputs_limitedc[f'fullname1_field'].fill_field(dirB1, fullname.upper(), fs=11)
                st.session_state.inputs_limitedc[f'fullname2_field'].fill_field(dirB1, fullname.upper(), fs=10, ind=1)
                st.session_state.inputs_limitedc[f'numbx_field'].fill_field(dirB1, st.session_state.inputs_limitedc[f'house_num{i}'].upper(), fs=12)
                st.session_state.inputs_limitedc[f'landmark_field'].fill_field(dirB1, st.session_state.inputs_limitedc[f'house_address{i}'].upper(), fs=10)
                st.session_state.inputs_limitedc[f'street'].fill_field(dirB1, st.session_state.inputs_limitedc[f'street_name{i}'].upper(), fs=10)
                st.session_state.inputs_limitedc[f'town'].fill_field(dirB1, st.session_state.inputs_limitedc[f'city{i}'].upper(), fs=10)
                                             
                               
                if i == 6 :
                    page = page3
                    st.session_state.inputs_limitedc[f"consent_fieldi{i}"].fill_option(page, st.session_state.inputs_limitedc[f"consenti{i}"],ind=5 if st.session_state.inputs_limitedc[f"consenti{i}"] == "NO" else 1)
                    st.session_state.inputs_limitedc[f"consent_fieldii{i}"].fill_option(page, st.session_state.inputs_limitedc[f"consentii{i}"],ind=2 if st.session_state.inputs_limitedc[f"consentii{i}"] == "NO" else 3)
                    st.session_state.inputs_limitedc[f"consent_fieldiii{i}"].fill_option(page, st.session_state.inputs_limitedc[f"consentii{i}"],ind=4 if st.session_state.inputs_limitedc[f"consenti{i}"] == "NO" else 0)
                    personal(c,i, page=page, fill=True,form3=True, place_ob=True, dir=True)
                    contact(i, fill=True, form3=True, page=page, ind=1 if i==6 else 0)
                    gh_tin(i, fill=True, page=page, ind=0)
                    house_address = st.session_state.inputs_limitedc[f"house_num{i}"] +  st.session_state.inputs_limitedc[f"house_address{i}"]
                    st.session_state.inputs_limitedc[f"house_address_field{i}"].fill_field(page, house_address.upper(), 1)             
                    st.session_state.inputs_limitedc[f"country_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"country{i}"].upper())
                    st.session_state.inputs_limitedc[f"digital_address_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"digital_address{i}"].upper())            
                    st.session_state.inputs_limitedc[f"street_name_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"street_name{i}"].upper(), 1)
                    st.session_state.inputs_limitedc[f"city_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"city{i}"].upper(),1)
                    st.session_state.inputs_limitedc[f"district_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"district{i}"].upper(),1)
                    st.session_state.inputs_limitedc[f"region_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"region{i}"].upper())
                    st.session_state.inputs_limitedc[f"particulars_field{i}"].fill_field(page4, st.session_state.inputs_limitedc[f"particulars{i}"].upper())
                    i+=1
                    st.session_state.inputs_limitedc[f"house_address_field{i}"].fill_field(page,  st.session_state.inputs_limitedc[f"house_address{i}"].upper())             
                    st.session_state.inputs_limitedc[f"country_field{i}"].fill_field(page4,st.session_state.inputs_limitedc[f"country{i}"].upper(),0)
                    st.session_state.inputs_limitedc[f"digital_address_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"digital_address{i}"].upper(),1)            
                    st.session_state.inputs_limitedc[f"street_name_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"street_name{i}"].upper(), 0)
                    st.session_state.inputs_limitedc[f"city_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"city{i}"].upper(),0)
                    st.session_state.inputs_limitedc[f"district_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"district{i}"].upper(),0)
                    st.session_state.inputs_limitedc[f"region_field{i}"].fill_field(page4,st.session_state.inputs_limitedc[f"region{i}"].upper())

                
                if i ==8:
                        page = page4
                        st.session_state.inputs_limitedc[f"consent_fieldi{i}"].fill_option(page, st.session_state.inputs_limitedc[f"consenti{i}"],ind=1 if st.session_state.inputs_limitedc[f"consenti{i}"] == "NO" else 0)
                        st.session_state.inputs_limitedc[f"consent_fieldii{i}"].fill_option(page, st.session_state.inputs_limitedc[f"consentii{i}"],ind=4 if st.session_state.inputs_limitedc[f"consentii{i}"] == "NO" else 2)
                        st.session_state.inputs_limitedc[f"consent_fieldiii{i}"].fill_option(page, st.session_state.inputs_limitedc[f"consentiii{i}"],ind=2 if st.session_state.inputs_limitedc[f"consenti{i}"] == "NO" else 1)
                        personal(c,i, page=page, fill=True,form3=True, place_ob=True, dir=True)
                        contact(i, fill=True, form3=True, page=page, ind=1 if i==6 else 0)
                        gh_tin(i, fill=True, page=page, ind=0)
                        house_address = st.session_state.inputs_limitedc[f"house_num{i}"] +  st.session_state.inputs_limitedc[f"house_address{i}"]
                        st.session_state.inputs_limitedc[f"house_address_field{i}"].fill_field(page, house_address.upper())             
                        st.session_state.inputs_limitedc[f"country_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"country{i}"].upper(), 1)
                        st.session_state.inputs_limitedc[f"digital_address_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"digital_address{i}"].upper(), 1)            
                        st.session_state.inputs_limitedc[f"street_name_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"street_name{i}"].upper())
                        st.session_state.inputs_limitedc[f"city_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"city{i}"].upper())
                        st.session_state.inputs_limitedc[f"district_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"district{i}"].upper())
                        st.session_state.inputs_limitedc[f"region_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"region{i}"].upper(), 1)
                        st.session_state.inputs_limitedc[f"particulars_field{i}"].fill_field(page5, st.session_state.inputs_limitedc[f"particulars{i}"].upper())      
                        i+=1
                        page = page5
                        st.session_state.inputs_limitedc[f"house_address_field{i}"].fill_field(page,  st.session_state.inputs_limitedc[f"house_address{i}"].upper())             
                        st.session_state.inputs_limitedc[f"country_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"country{i}"].upper(),0)
                        st.session_state.inputs_limitedc[f"digital_address_field{i}"].fill_field(page4,st.session_state.inputs_limitedc[f"digital_address{i}"].upper(),0)            
                        st.session_state.inputs_limitedc[f"street_name_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"street_name{i}"].upper(), 1)
                        st.session_state.inputs_limitedc[f"city_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"city{i}"].upper(),1)
                        st.session_state.inputs_limitedc[f"district_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"district{i}"].upper(),1)
                        st.session_state.inputs_limitedc[f"region_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"region{i}"].upper(),1)

        
                if i == 10:
                    add_dir = 'backend/limited_company/data/Company-By-Shares-Additional-Director-Form.pdf'
                    dir_doc = fitz.open(add_dir)
                    dir1 = dir_doc[0]
                    dir2 = dir_doc[1]  
                    dir3 = dir_doc[2]  
                    
               
                    page = dir1
                    st.session_state.inputs_limitedc["company_name_fielddir"]= boxes("Company Name*", c_x=96, bpr=25, t_row=2, control=1.4)
                    st.session_state.inputs_limitedc["company_name_fielddir"].fill_field(page, st.session_state.inputs_limitedc['company_name'].upper())
                    st.session_state.inputs_limitedc[f"consent_fieldi{i}"].fill_option(page, st.session_state.inputs_limitedc[f"consenti{i}"],ind=6 if st.session_state.inputs_limitedc[f"consenti{i}"] == "NO" else 3)
                    st.session_state.inputs_limitedc[f"consent_fieldii{i}"].fill_option(page, st.session_state.inputs_limitedc[f"consentii{i}"],ind=2 if st.session_state.inputs_limitedc[f"consentii{i}"] == "NO" else 1)
                    st.session_state.inputs_limitedc[f"consent_fieldiii{i}"].fill_option(page, st.session_state.inputs_limitedc[f"consentiii{i}"],ind=4 if st.session_state.inputs_limitedc[f"consentiii{i}"] == "NO" else 2)
                    personal(c,i, page=page, fill=True,form3=True, place_ob=True, add_dir=True)
                    contact(i, fill=True, form3=True, page=page)
                    gh_tin(i, fill=True, page=page, ind=0)
                    house_address = st.session_state.inputs_limitedc[f"house_num{i}"] +  st.session_state.inputs_limitedc[f"house_address{i}"]
                    st.session_state.inputs_limitedc[f"house_address_field{i}"].fill_field(page, house_address.upper())             
                    st.session_state.inputs_limitedc[f"country_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"country{i}"].upper())
                    st.session_state.inputs_limitedc[f"digital_address_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"digital_address{i}"].upper(), 1)            
                    st.session_state.inputs_limitedc[f"street_name_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"street_name{i}"].upper())
                    st.session_state.inputs_limitedc[f"city_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"city{i}"].upper())
                    st.session_state.inputs_limitedc[f"district_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"district{i}"].upper())
                    st.session_state.inputs_limitedc[f"region_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"region{i}"].upper())
                    st.session_state.inputs_limitedc[f"particulars_field{i}"].fill_field(dir2, st.session_state.inputs_limitedc[f"particulars{i}"].upper())      
                    i+=1
                    page = dir2
                    st.session_state.inputs_limitedc[f"house_address_field{i}"].fill_field(page,  st.session_state.inputs_limitedc[f"house_address{i}"].upper())             
                    st.session_state.inputs_limitedc[f"country_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"country{i}"].upper())
                    st.session_state.inputs_limitedc[f"digital_address_field{i}"].fill_field(dir1,st.session_state.inputs_limitedc[f"digital_address{i}"].upper())            
                    st.session_state.inputs_limitedc[f"street_name_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"street_name{i}"].upper())
                    st.session_state.inputs_limitedc[f"city_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"city{i}"].upper())
                    st.session_state.inputs_limitedc[f"district_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"district{i}"].upper())
                    st.session_state.inputs_limitedc[f"region_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"region{i}"].upper())

                    if st.session_state.inputs_limitedc["dir_num"] == 4:
                        i+=1
                        page = dir2
                        st.session_state.inputs_limitedc[f"consent_fieldi{i}"].fill_option(page, st.session_state.inputs_limitedc[f"consenti{i}"], ind=3 if st.session_state.inputs_limitedc[f"consenti{i}"]=='NO' else 0)
                        st.session_state.inputs_limitedc[f"consent_fieldii{i}"].fill_option(page, st.session_state.inputs_limitedc[f"consentii{i}"], ind=4 if st.session_state.inputs_limitedc[f"consentii{i}"]=='NO' else 1)
                        st.session_state.inputs_limitedc[f"consent_fieldiii{i}"].fill_option(page, st.session_state.inputs_limitedc[f"consentiii{i}"], ind=5 if st.session_state.inputs_limitedc[f"consentiii{i}"]=='NO'else 2)
                        personal(c,i, page=page, fill=True,form3=True, place_ob=True, dir=True)
                        contact(i, fill=True, form3=True, page=page)
                        gh_tin(i, fill=True, page=page, ind=0)
                        house_address = st.session_state.inputs_limitedc[f"house_num{i}"] +  st.session_state.inputs_limitedc[f"house_address{i}"]
                        st.session_state.inputs_limitedc[f"house_address_field{i}"].fill_field(page, house_address.upper(), 1)             
                        st.session_state.inputs_limitedc[f"country_field{i}"].fill_field(dir3,st.session_state.inputs_limitedc[f"country{i}"].upper())
                        st.session_state.inputs_limitedc[f"digital_address_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"digital_address{i}"].upper())            
                        st.session_state.inputs_limitedc[f"street_name_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"street_name{i}"].upper(),1)
                        st.session_state.inputs_limitedc[f"city_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"city{i}"].upper(),1)
                        st.session_state.inputs_limitedc[f"district_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"district{i}"].upper(),1)
                        st.session_state.inputs_limitedc[f"region_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"region{i}"].upper(), 1)
                        st.session_state.inputs_limitedc[f"particulars_field{i}"].fill_field(dir3, st.session_state.inputs_limitedc[f"particulars{i}"].upper())      
                        i+=1
                        page = dir3
                        st.session_state.inputs_limitedc[f"house_address_field{i}"].fill_field(page,  st.session_state.inputs_limitedc[f"house_address{i}"].upper())             
                        st.session_state.inputs_limitedc[f"country_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"country{i}"].upper(),1)
                        st.session_state.inputs_limitedc[f"digital_address_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"digital_address{i}"].upper())            
                        st.session_state.inputs_limitedc[f"street_name_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"street_name{i}"].upper())
                        st.session_state.inputs_limitedc[f"city_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"city{i}"].upper())
                        st.session_state.inputs_limitedc[f"district_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"district{i}"].upper())
                        st.session_state.inputs_limitedc[f"region_field{i}"].fill_field(page,st.session_state.inputs_limitedc[f"region{i}"].upper())
                   
                    director = f"outputlc/AdditionalDirectorForm.pdf"
                    dir_doc.save(director)
                    dir_doc.close()
                    directors.append(director)
                
               
                directordeclare = f"outputlc/CONSENT-{fullname}.pdf"
                doc_dirA.save(directordeclare)
                doc_dirA.close()
                directors.append(directordeclare)

                directorstat = f"outputlc/STATUTORY DECLARATIONS-{fullname}.pdf"
                doc_dirB.save(directorstat)
                doc_dirB.close()
                directors.append(directorstat)
                c += 1  
                ind += 1         
    except Exception as e:
        print(e)
    
##############################SECRETARY#######################################
    try:        
        i = 6 +(2 * st.session_state.inputs_limitedc["dir_num"])
        if st.session_state.inputs_limitedc["secretary_cop"] == "Individual":
            cover('SECRETARY/REP. OF CORPORATE SECRETARY ', lbl=i, ind=8, maxi=40, controlx=275, sec=True)
            pdf_sec = 'backend/limited_company/data/Form 26(B) Consent to Act as A Secretary.pdf'
            doc_sec =  fitz.open(pdf_sec)
            secA1 = doc_sec[0]

            fullname = st.session_state.inputs_limitedc[f"first_namex"]+' '+   st.session_state.inputs_limitedc[f"middle_namex"] + ' ' + st.session_state.inputs_limitedc[f"last_namex"]
            resaddr = f'{st.session_state.inputs_limitedc[f"digital_address{i}"]} {st.session_state.inputs_limitedc[f"house_address{i}"]} {st.session_state.inputs_limitedc[f"house_num{i}"]}'
            qual = ','.join(st.session_state.inputs_limitedc[f"qualification{i}"])

            st.session_state.inputs_limitedc[f'mbil_field'] = field_plain_template(0, "Mobile Number:",maxi=100,c_x=100, r_h=0,t_rows=1)
            st.session_state.inputs_limitedc[f'qual_consent_field'] = field_plain_template(0, "My qualification under Section 211(3) of Act 992 is",maxi=55,c_x=0,c_y=33, r_h=27,t_rows=3)
            st.session_state.inputs_limitedc[f'c_name_field'].fill_field(secA1, st.session_state.inputs_limitedc['company_name'].upper(), fs=14)
            st.session_state.inputs_limitedc[f'fullname_field'].fill_field(secA1, fullname.upper(), fs=14)
            st.session_state.inputs_limitedc[f'formername_field'].fill_field(secA1, st.session_state.inputs_limitedc[f"former_name{i}"].upper(), fs=14)
            st.session_state.inputs_limitedc[f'pbox_field'].fill_field(secA1,  st.session_state.inputs_limitedc[f'postal_number'].upper() if st.session_state.inputs_limitedc[f'type']=='P O Box' else '', fs=14)
            st.session_state.inputs_limitedc[f'resaddre_field'].fill_field(secA1, resaddr.upper(), fs=14)
            st.session_state.inputs_limitedc[f'mbil_field'].fill_field(secA1, st.session_state.inputs_limitedc[f"mobile_num{i}"].upper(), fs=14)
            st.session_state.inputs_limitedc[f'qual_consent_field'].fill_field(secA1, qual.upper(), fs=14)
            st.session_state.inputs_limitedc[f'dirdate_field'].fill_field(secA1, datetime.now().date().strftime("%d-%m-%Y"), fs=14)
            if st.session_state.inputs_limitedc[f'secsubques'] == 'Yes':
                st.session_state.inputs_limitedc['subcount'] += 1
                cover('SUBSCRIBER',count=st.session_state.inputs_limitedc['subcount'], lbl=i, ind=3+st.session_state.inputs_limitedc['subcount'] , maxi=55, controlx=125, sec=True)
                c+=1
                bo2(i, 'x')
                bo1(i, 'bo2', 'x')
                if st.session_state.inputs_limitedc['first_sub_field'] == False:
                    first_sub_field(i, 'x')
                    st.session_state.inputs_limitedc['first_sub_field']=True
                elif st.session_state.inputs_limitedc['second_sub_field']==False:
                    second_sub_field(i, 'x')
                    st.session_state.inputs_limitedc['second_sub_field']=True
                else:
                    add_subs(i, 'x')
            if  st.session_state.inputs_limitedc[f'subtrustques']=='Yes':        
                if st.session_state.inputs_limitedc['trusteeform3'] == False:
                    trusteeform3('x', i)
                    st.session_state.inputs_limitedc['trusteeform3'] = True
                else:
                    add_trustee(i, 'x')


            if st.session_state.inputs_limitedc[f"qualification{i}"]:
                for item in st.session_state.inputs_limitedc[f"qualification{i}"]:
                    st.session_state.inputs_limitedc[f"qualification_field{item}"] = PDFOptionField(control_x=-372, control_y=5)
                    if "By virtue of an academic qualification" in item:
                        st.session_state.inputs_limitedc[f"qualification_field{item}"].fill_option(page5, "By virtue of an academic qualification")
                    else:
                        st.session_state.inputs_limitedc[f"qualification_field{item}"].fill_option(page5, f"{item}")
            if st.session_state.inputs_limitedc[f'consent_letter{i}'] =='YES':
                st.session_state.inputs_limitedc[f'consent_letter_field{i}'].fill_option(page5, 'Consent Letter*')
            personal('x', i, fill=True, form3=True, page=page5, sec=True)
            gh_tin(i, fill=True, page=page5)
            contact(i, fill=True, form3=True, page=page5)
            address(i, split=True, fill=True, form3=True, page=page5)
            st.session_state.inputs_limitedc[f"country_field{i}"].fill_field(page6,st.session_state.inputs_limitedc[f"country{i}"].upper())
            tax(i, pn='x', fill=True, l=secretary, label='Secretary')

            secdeclare = f"outputlc/CONSENT-{fullname}.pdf"
            doc_sec.save(secdeclare)
            doc_sec.close()
            secretary.append(secdeclare)
        
        ##########################SECRETARY CORPORATE########################
        else:    
            cover('SECRETARY/REP. OF CORPORATE SECRETARY ', lbl=i, ind=8, maxi=40, controlx=275, cop=True)
            body(i, fill=True, page=page6)
            if st.session_state.inputs_limitedc[f'secsubques'] == 'Yes':
                st.session_state.inputs_limitedc['subcount'] += 1
                cover('SUBSCRIBER',count=st.session_state.inputs_limitedc['subcount'], lbl=i, ind=3+st.session_state.inputs_limitedc['subcount'] , maxi=55, controlx=125, cop=True)
                c+=1
                if st.session_state.inputs_limitedc[f"bene_type"]=="Publicly Listed Company":
                    bo3(i, '')
                    bo1(i, 'bo3', '')
                else:
                    bo4(i, '')
                    bo1(i, 'bo4', '')
                if st.session_state.inputs_limitedc['first_sub_cop_field'] == False:
                    first_cop_sub(i, '')
                    st.session_state.inputs_limitedc['first_sub_cop_field'] =True
                else:
                   add_cop_subs(i, '')
            if  st.session_state.inputs_limitedc.get(f'subtrustques')=='Yes':        
                if st.session_state.inputs_limitedc['trusteecopform3'] == False:
                    trustee_cop(i, '')
                    st.session_state.inputs_limitedc['trusteecopform3'] = True
                else:
                    add_cop_trustee(i, '')
            st.session_state.inputs_limitedc["authtin_field"] = boxes("TIN", c_x=35)
            if st.session_state.inputs_limitedc["secretary_cop"] == "Individual":
                sec = st.session_state.inputs_limitedc[f"first_namex"]+' '+   st.session_state.inputs_limitedc[f"middle_namex"] + ' ' + st.session_state.inputs_limitedc[f"last_namex"]
                tin = st.session_state.inputs_limitedc[f"tin{i}"]
            else:
                sec=st.session_state.inputs_limitedc[f"name_repre{i}"]
                tin=st.session_state.inputs_limitedc[f"tinrep{i}"]

            if st.session_state.inputs_limitedc["authenticatexx"]=='YES':
                st.session_state.inputs_limitedc["authtin_field"].fill_field(page6, st.session_state.inputs_limitedc["tin6"].upper(),ind=4)
                st.session_state.inputs_limitedc["gh_card_field6"].fill_field(page6, st.session_state.inputs_limitedc["gh_card6"].upper(), 1)
                st.session_state.inputs_limitedc["auth_field"]=boxes("Name")
                name1 = st.session_state.inputs_limitedc["first_name1"]+' '+   st.session_state.inputs_limitedc["middle_name1"] + ' ' + st.session_state.inputs_limitedc["last_name1"]
                st.session_state.inputs_limitedc["auth_field"].fill_field(page6, name1.upper(), ind=2)

                st.session_state.inputs_limitedc["authtin_field"].fill_field(page6, tin.upper(),3)
                st.session_state.inputs_limitedc[f"gh_card_field{i}"].fill_field(page6, st.session_state.inputs_limitedc[f"gh_card{i}"].upper(), 2)
                st.session_state.inputs_limitedc["auth_field"]=boxes("Name")
                st.session_state.inputs_limitedc["auth_field"].fill_field(page6, sec.upper(), 3)
    
            else:   
                st.session_state.inputs_limitedc["authtin_field"].fill_field(page6, st.session_state.inputs_limitedc["tin6"].upper(),ind=0)
                st.session_state.inputs_limitedc["gh_card_field6"].fill_field(page6, st.session_state.inputs_limitedc["gh_card6"].upper(), 3)
                st.session_state.inputs_limitedc["auth_field"]=boxes("Name")
                name1 = st.session_state.inputs_limitedc["first_name1"]+' '+   st.session_state.inputs_limitedc["middle_name1"] + ' ' + st.session_state.inputs_limitedc["last_name1"]
                st.session_state.inputs_limitedc["auth_field"].fill_field(page6, name1.upper())

                st.session_state.inputs_limitedc["authtin_field"].fill_field(page6, st.session_state.inputs_limitedc["tin8"].upper(),ind=1)
                st.session_state.inputs_limitedc["gh_card_field8"].fill_field(page6, st.session_state.inputs_limitedc["gh_card8"].upper(), 4)
                auth_field=boxes("Name", c_y=-2)
                name2 = st.session_state.inputs_limitedc["first_name2"]+' '+   st.session_state.inputs_limitedc["middle_name2"] + ' ' + st.session_state.inputs_limitedc["last_name2"]
                auth_field.fill_field(page6, name2.upper(), ind=5, )
            
                st.session_state.inputs_limitedc["authtin_field"].fill_field(page7, tin.upper(),1)
                st.session_state.inputs_limitedc[f"gh_card_field{i}"].fill_field(page7, st.session_state.inputs_limitedc[f"gh_card{i}"].upper())
                st.session_state.inputs_limitedc["auth_field"]=boxes("Name")
                st.session_state.inputs_limitedc["auth_field"].fill_field(page7, sec.upper())

    ######################AUDITOR##################################
        gh_tin(4,  fill=True, page=page7, ind=1)
        st.session_state.inputs_limitedc["auditor_firm_name_field"].fill_field(page7,st.session_state.inputs_limitedc["auditor_firm_name"].upper())
        st.session_state.inputs_limitedc["firm_address_field"].fill_field(page7, st.session_state.inputs_limitedc["firm_address"].upper())
        st.session_state.inputs_limitedc["firm_pmb_field"].fill_field(page7, st.session_state.inputs_limitedc["firm_pmb"].upper())
        address(6 +(2 * st.session_state.inputs_limitedc["dir_num"]) + st.session_state.inputs_limitedc['sec_num'], fill=True, form3=True, page=page7, ind1=0)
        st.session_state.inputs_limitedc["firm_moblie_field"].fill_field(page7, st.session_state.inputs_limitedc["firm_moblie"])
        st.session_state.inputs_limitedc["office_num_field"].fill_field(page7, st.session_state.inputs_limitedc["office_num"].upper())
    except Exception as e:
        print(e)
        
     

# ###################SUBSCRIBERS  
    try:
        v=st.session_state.inputs_limitedc["dir_num"]+1    
        m = 7 +(2 * st.session_state.inputs_limitedc["dir_num"]) + st.session_state.inputs_limitedc['sec_num']
        while m < 7 +(2 * st.session_state.inputs_limitedc["dir_num"]) + st.session_state.inputs_limitedc['sec_num'] +(2*st.session_state.inputs_limitedc["indsub"]):
            st.session_state.inputs_limitedc['subcount'] += 1
            cover('SUBSCRIBER',count=st.session_state.inputs_limitedc['subcount'], lbl=m, ind=3+st.session_state.inputs_limitedc['subcount'] , maxi=55, controlx=125, v=v)
            tax(m, pn=v, fill=True, l=subscribers, label='Subscriber')
            bo2(m, v)
            bo1(m, 'bo2', v)
            if st.session_state.inputs_limitedc['first_sub_field'] == False:
                first_sub_field(m, v)
                st.session_state.inputs_limitedc['first_sub_field']=True
            elif st.session_state.inputs_limitedc['second_sub_field']==False:
                second_sub_field(m, v)
                st.session_state.inputs_limitedc['second_sub_field']=True
            else:
                add_subs(m, v)
            if  st.session_state.inputs_limitedc[f'subtrustques{v}']=='Yes':        
                if st.session_state.inputs_limitedc['trusteeform3'] == False:
                    trusteeform3(v, m)
                    st.session_state.inputs_limitedc['trusteeform3'] = True
                else:
                    add_trustee(m, v)
            m +=2
            v+=1
        

        for i in range(7 +(2 * st.session_state.inputs_limitedc["dir_num"]) + st.session_state.inputs_limitedc['sec_num'] +(2*st.session_state.inputs_limitedc["indsub"]), 7 +(2 * st.session_state.inputs_limitedc["dir_num"]) + st.session_state.inputs_limitedc['sec_num'] +(2*st.session_state.inputs_limitedc["indsub"])+(st.session_state.inputs_limitedc["copsub"])):
            st.session_state.inputs_limitedc['subcount'] += 1
            cover('SUBSCRIBER',count=st.session_state.inputs_limitedc['subcount'], lbl=i, ind=3+st.session_state.inputs_limitedc['subcount'] , maxi=55, controlx=125, cop=True)
            if st.session_state.inputs_limitedc[f"bene_type{v}"]=="Publicly Listed Company":
                bo3(i, v)
                bo1(i, 'bo3', v)
            else:
                bo4(i, v)
                bo1(i, 'bo4',v)
            if st.session_state.inputs_limitedc['first_sub_cop_field'] == False:
                first_cop_sub(i, v)
                st.session_state.inputs_limitedc['first_sub_cop_field'] =True
            else:
                add_cop_subs(i, v)
            if  st.session_state.inputs_limitedc.get(f'subtrustques')=='Yes':        
                if st.session_state.inputs_limitedc['trusteecopform3'] == False:
                    trustee_cop(i, v)
                    st.session_state.inputs_limitedc['trusteecopform3'] = True
                else:
                    add_cop_trustee(i, v)       
            v+=1
                            
        bene = f"outputlc/Beneficiary(BO1).pdf"
        doc_mbene.save(bene)
        doc_mbene.close()
        beneficiaries.append(bene)    
                
        coverp = "outputlc/CoverForm.pdf"
        doc_cover.save(coverp)
        doc_cover.close()  
     
        form3 = "outputlc/form3.pdf"
        doc.save(form3)
        doc.close()
       
        all_files.append(coverp)
        all_files.append(form3)
    except Exception as e:
        print(e)
    try:
        all_files.append(directors) 
        all_files.append(secretary)
        all_files.append(subscribers) 
        all_files.append(trustees) 
        all_files.append(beneficiaries) 
    except Exception as e:
        print(e)
     
    # print(all_fi
    return all_files