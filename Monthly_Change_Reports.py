# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 14:34:26 2024

@author: PLedin
"""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px

###############################################################################
#Function Definitions
###############################################################################
def convertDateToDisplay(date):
    switcher = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December",
    }
    
    return switcher.get(date[4:], "**Bad Month**") + "-" + date[:4]

def convertDateToSystem(date):
    switcher = {
        "January":  "01",
        "February": "02",
        "March":    "03",
        "April":    "04",
        "May":      "05",
        "June":     "06",
        "July":     "07",
        "August":   "08",
        "September":"09",
        "October":  "10",
        "November": "11",
        "December": "12",
    }
    
    return date[len(date)-4:len(date)] + switcher.get(date[:len(date)-5], "**Bad Month**")

def get_report_periods():
    periods = pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/MonthlyReportPeriods.csv')
    
    retVal = list()
    index = 0
    for x in periods:
        retVal.insert(index, periods[x])
        index += 1
    
    return (retVal)

def getMergersTable(month):
    return pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/merged_cus_' + convertDateToSystem(month) + '.csv', dtype={
    'NIMBLE_CUNA_ID': 'string',
    'NAME': 'string',
    'State': 'string',
    'Assets': 'int64',
    'Members': 'int64',
    'Employees': 'int64',
    'SURVIVOR_ID': 'string',
    'Status Chg Date': 'string'
    }))

def getPendingTable(month):
    return pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/pending_cus_' + convertDateToSystem(month) + '.csv', dtype={
    'NIMBLE_CUNA_ID': 'string',
    'NAME': 'string',
    'State': 'string',
    'Assets': 'int64',
    'Members': 'int64',
    'Employees': 'int64'
    }))

def getLiquidationsTable(month):
    return pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/liquidated_cus_' + convertDateToSystem(month) + '.csv', dtype={
    'NIMBLE_CUNA_ID': 'string',
    'NAME': 'string',
    'State': 'string',
    'Assets': 'int64',
    'Members': 'int64',
    'Employees': 'int64'
    }))

def getNameChgsTable(month):
    return pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/name_chgs_' + convertDateToSystem(month) + '.csv', dtype={
    'NIMBLE_CUNA_ID': 'string',
    'Old Name': 'string',
    'State': 'string',
    'New Name': 'string'
    }))

def getCEOChgsTable(month):
    return pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/ceo_chgs_' + convertDateToSystem(month) + '.csv', dtype={
    'NIMBLE_CUNA_ID': 'string',
    'Old Name': 'string',
    'State': 'string',
    'New Name': 'string'
    }))

def getAddressChgsTable(month, addressType):
    if (addressType == 'mailing'):
        df_address_chgs = pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/mailing_address_chgs_' + convertDateToSystem(month) + '.csv', dtype={
                                                'NIMBLE_CUNA_ID': 'string',
                                                'Old Name': 'string',
                                                'State': 'string',
                                                'New Name': 'string'
                                                }))
    else:
        df_address_chgs = pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/street_address_chgs_' + convertDateToSystem(month) + '.csv', dtype={
                                                'NIMBLE_CUNA_ID': 'string',
                                                'Old Name': 'string',
                                                'State': 'string',
                                                'New Name': 'string'
                                                }))
    return df_address_chgs

def getAFLChgsTables(month, aflChgType, aflType):
    if (aflChgType == 'REAFL'):
        df_afl_chgs = pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/reafl_chgs_' + aflType + '_' + convertDateToSystem(month) + '.csv', dtype={
                                            'NIMBLE_CUNA_ID': 'string',
                                            'Old Name': 'string',
                                            'State': 'string',
                                            'New Name': 'string'
                                            }))
    elif (aflChgType == 'DISAFL'):
        df_afl_chgs = pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/disafl_chgs_' + aflType + '_' + convertDateToSystem(month) + '.csv', dtype={
                                             'NIMBLE_CUNA_ID': 'string',
                                             'Old Name': 'string',
                                             'State': 'string',
                                             'New Name': 'string'
                                             }))
    return df_afl_chgs

def getCharterChgsTable(month):
    return pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/charter_chgs_' + convertDateToSystem(month) + '.csv', dtype={
    'NIMBLE_CUNA_ID': 'string',
    'Name': 'string',
    'Old Charter': 'string',
    'Old Charter Type': 'string',
    'New Charter': 'string',
    'New Charter Type': 'string',
    }))

def getPreviousSystemMonth(month):
    system_month = int(convertDateToSystem(month)[4:])
    prev_system_year = convertDateToSystem(month)[:4]
    
    prev_system_month = system_month - 1
    if(prev_system_month == 0):
        prev_system_month = 12
        prev_system_year = str(int(prev_system_year) - 1)
           
    return (prev_system_year + str(prev_system_month).rjust(2, '0'))

def get_report_periods_for_display():
    periods = pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/MonthlyReportPeriods.csv')    
    retVal = list()

    index = 0
    for x in periods:
        retVal.insert(index, periods[x])
        index += 1
        
    df_retVal = pd.DataFrame(retVal[0])
        
    for i in range(len(df_retVal)):
        period = df_retVal.loc[i, "period"]
        df_retVal.loc[df_retVal['period'] == period, 'report_periods_formatted'] = convertDateToDisplay(str(period))

    return df_retVal
    
def format_currency(amount):
    return '${:,.2f}'.format(amount)


###############################################################################
#Start building Streamlit App
###############################################################################
report_periods = get_report_periods_for_display()

st.set_page_config(
    page_title="America's Credit Unions",
    layout="wide",
    initial_sidebar_state="expanded")
alt.themes.enable("dark") 

column_configuration = {
    "State": st.column_config.TextColumn(
        "State", max_chars=50
    ),
    "Affiliated CUs": st.column_config.NumberColumn(
        "Affiliated CUs",
        min_value=0,
        max_value=10000,
    ),
    "Non Affiliated CUs": st.column_config.NumberColumn(
        "Non Affiliated CUs",
        min_value=0,
        max_value=10000,
    ),
    "State Chartered": st.column_config.NumberColumn(
        "State Chartered",
        min_value=0,
        max_value=10000,
    ),
    "Fed Chartered": st.column_config.NumberColumn(
        "Fed Chartered",
        min_value=0,
        max_value=10000,
    ),
    "Total CUs": st.column_config.NumberColumn(
        "Total CUs",
        min_value=0,
        max_value=10000,
    ),
    "Affiliated Memberships": st.column_config.NumberColumn(
        "Affiliated Memberships",
        min_value=0,
        max_value=10000,
    ),
    "Affiliated Assets": st.column_config.NumberColumn(
        "Affiliated Assets",
        min_value=0,
        max_value=10000,
    ),
    "Total Assets": st.column_config.NumberColumn(
        "Total Assets",
        min_value=0,
        max_value=10000,
    ),
    "% CUs Affiliated": st.column_config.NumberColumn(
        "% CUs Affiliated",
        min_value=0,
        max_value=10000,
        format="%.1f"
    ),
    "% Memberships Affiliated": st.column_config.NumberColumn(
        "% Memberships Affiliated",
        min_value=0,
        max_value=10000,
        format="%.1f"
    ),
    "% Assets Affiliated": st.column_config.NumberColumn(
        "% Assets Affiliated",
        min_value=0,
        max_value=10000,
        format="%.1f"
    ),
}
     
with st.sidebar:
    st.title('America\'s Credit Unions - Monthly Change Reports')
    
    report_type = ['Status','Affiliation', 'Name', 'Address', 'Miscellaneous', 'New']
    selected_report_type = st.selectbox('Report Type', report_type)
    
    month = report_periods['report_periods_formatted']
    selected_month = st.selectbox('Month', month)
    
df_mergers = getMergersTable(selected_month)
df_pending = getPendingTable(selected_month)
df_liquidated = getLiquidationsTable(selected_month)
df_name_chgs = getNameChgsTable(selected_month)
df_mailing_address_chgs = getAddressChgsTable(selected_month, 'mailing')
df_street_address_chgs = getAddressChgsTable(selected_month, 'street')
df_ceo_chgs = getCEOChgsTable(selected_month)
df_charter_chgs = getCharterChgsTable(selected_month)

col = st.columns((1.5, 6.5), gap='medium')
with col[0]:          
    st.markdown('#### Summary')

with col[1]:
    st.markdown('#### Details')

    if (selected_report_type == 'Affiliation'):
        st.markdown('#### Affiliation Changes')
        
        affiliation_type = ['Legacy CUNA','Legacy NAFCU', 'Either / At least 1 Legacy Org']
        selected_affiliation_type = st.selectbox('Affiliation Type', affiliation_type)
        
        if (selected_affiliation_type == 'Legacy CUNA'):
            df_reafl_chgs = getAFLChgsTables(selected_month, 'REAFL', 'cuna')
            df_disafl_chgs = getAFLChgsTables(selected_month, 'DISAFL', 'cuna')
        elif (selected_affiliation_type == 'Legacy NAFCU'):
            df_reafl_chgs = getAFLChgsTables(selected_month, 'REAFL', 'nafcu')
            df_disafl_chgs = getAFLChgsTables(selected_month, 'DISAFL', 'nafcu')
        else:
            df_reafl_chgs = getAFLChgsTables(selected_month, 'REAFL', 'either')
            df_disafl_chgs = getAFLChgsTables(selected_month, 'DISAFL', 'either')
            
        st.markdown('#### Reaffiliations - ' + selected_affiliation_type)
        st.dataframe(data = df_reafl_chgs, 
                     column_config=column_configuration,
                     use_container_width = True, 
                     hide_index = True,
                     )
        
        st.markdown('#### Disaffiliations - ' + selected_affiliation_type)
        st.dataframe(data = df_disafl_chgs, 
                     column_config=column_configuration,
                     use_container_width = True, 
                     hide_index = True,
                     )

    elif (selected_report_type == 'Name'):
        st.markdown('#### Name Changes')
        st.dataframe(data = df_name_chgs, 
                     column_config=column_configuration,
                     use_container_width = True, 
                     hide_index = True,
                     )
    elif (selected_report_type == 'Address'):
        st.markdown('#### Mailing Address Changes')
        st.dataframe(data = df_mailing_address_chgs, 
                     column_config=column_configuration,
                     use_container_width = True, 
                     hide_index = True,
                     )
        st.markdown('#### Street Address Changes')
        st.dataframe(data = df_street_address_chgs, 
                     column_config=column_configuration,
                     use_container_width = True, 
                     hide_index = True,
                     )
    elif (selected_report_type == 'Miscellaneous'):
        st.markdown('#### Manager Changes')
        st.dataframe(data = df_ceo_chgs, 
                     column_config=column_configuration,
                     use_container_width = True, 
                     hide_index = True,
                     )
        st.markdown('#### Charter Changes')
        st.dataframe(data = df_charter_chgs, 
                     column_config=column_configuration,
                     use_container_width = True, 
                     hide_index = True,
                     )
    else:
        st.markdown('#### Merged Credit Unions')
        st.dataframe(data = df_mergers, 
                     column_config=column_configuration,
                     use_container_width = True, 
                     hide_index = True,
                     )
    
        st.markdown('#### Pending Merger/Liquidation Credit Unions')
        st.dataframe(data = df_pending, 
                     column_config=column_configuration,
                     use_container_width = True, 
                     hide_index = True,
                     )
    
        st.markdown('#### Liquidated Credit Unions')
        st.dataframe(data = df_liquidated, 
                     column_config=column_configuration,
                     use_container_width = True, 
                     hide_index = True,
                     )

    
