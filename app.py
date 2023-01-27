import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import random
import streamlit.components.v1 as components
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

##
conn=sqlite3.connect('oikotie.db')

sql='''select Sijainti, Kaupunginosa, Kerros, Asuinpinta_ala, Huoneita, Kunto, Parveke, Velaton_hinta, Neliohinta, Rahoitusvastike, Hoitovastike, Yhtiovastike, Rakennuksen_tyyppi, Rakennusvuosi,
Energialuokka, Tontin_omistus, Kerroksia, Hissi, Asumistyyppi, Asunnossa_sauna, pvm, Hoitovastike_m2
from oikotie_asunnot'''

def filter_dataframe(df: pd.DataFrame, keys, checkbox, modification_container, right) -> pd.DataFrame:
    modify = checkbox##st.checkbox("Add filters", key=keys[0])

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    ##modification_container = st.container()

    with modification_container:


        
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns, key=keys[1])
        for column in to_filter_columns:
            ##left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if column=="Kerros":
                opts=list(df[column].unique())
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    options=opts,
                    default=opts,
                    key=keys[13]
                )
                df = df[df[column].isin(user_cat_input)]


            elif column=="Huoneita":
                opts=list(df[column].unique())
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    options=opts,
                    default=opts,
                    key=keys[14]
                )
                df = df[df[column].isin(user_cat_input)]


            elif column=="Rakennuksen_tyyppi":
                opts=list(df[column].unique())
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    options=opts,
                    default=opts,
                    key=keys[15]
                )
                df = df[df[column].isin(user_cat_input)]


            elif column=="Hissi":
                opts=list(df[column].unique())
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    options=opts,
                    default=opts,
                    key=keys[16]
                )
                df = df[df[column].isin(user_cat_input)]



            elif column=="Tontin_omistus":
                opts=list(df[column].unique())
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    options=opts,
                    default=opts,
                    key=keys[17]
                )
                df = df[df[column].isin(user_cat_input)]


            elif column=="Asunnossa_sauna":
                opts=list(df[column].unique())
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    options=opts,
                    default=opts,
                    key=keys[18]
                )
                df = df[df[column].isin(user_cat_input)]

            elif column=="Asumistyyppi":
                opts=list(df[column].unique())
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    options=opts,
                    default=opts,
                    key=keys[19]
                )
                df = df[df[column].isin(user_cat_input)]           
            
            elif column=="Kunto":
                opts=list(df[column].unique())
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    options=opts,
                    default=opts,
                    key=keys[20]
                )
                df = df[df[column].isin(user_cat_input)]           
            
            elif column=="Parveke":
                opts=list(df[column].unique())
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    options=opts,
                    default=opts,
                    key=keys[21]
                )
                df = df[df[column].isin(user_cat_input)]

            elif column=="Asuinpinta_ala":
                
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                    key=keys[22]
                    ##on_change=
                )
                print(user_num_input)
                df = df[df[column].between(*user_num_input)]


            elif column=="Myyntihinta":
                
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                    key=keys[3]
                    ##on_change=
                )
                print(user_num_input)
                df = df[df[column].between(*user_num_input)]


            elif column=="Neliohinta":
                
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                    key=keys[4]
                    ##on_change=
                )
                print(user_num_input)
                df = df[df[column].between(*user_num_input)]


            elif column=="Velaton_hinta":
                
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                    key=keys[5]
                    ##on_change=
                )
                print(user_num_input)
                df = df[df[column].between(*user_num_input)]


            elif column=="Rahoitusvastike":
                
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                    key=keys[6]
                    ##on_change=
                )
                print(user_num_input)
                df = df[df[column].between(*user_num_input)]


            elif column=="Hoitovastike":
                
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                    key=keys[7]
                    ##on_change=
                )
                print(user_num_input)
                df = df[df[column].between(*user_num_input)]


            elif column=="Yhtiovastike":
                
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                    key=keys[8]
                    ##on_change=
                )
                print(user_num_input)
                df = df[df[column].between(*user_num_input)]


            elif column=="Hoitovastike_m2":
                
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                    key=keys[9]
                    ##on_change=
                )
                print(user_num_input)
                df = df[df[column].between(*user_num_input)]


            elif column=="Rakennusvuosi":
                
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                    key=keys[10]
                    ##on_change=
                )
                print(user_num_input)
                df = df[df[column].between(*user_num_input)]

            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ), key=keys[4]
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]

            elif column=="Kaupunginosa":
                user_text_input = right.text_input(
                    f"Substring or regex in {column}", key=keys[11]
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

            elif column=="Sijainti":
                user_text_input = right.text_input(
                    f"Substring or regex in {column}", key=keys[12]
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]
    
    return df


##Anna mahdollisuus exportata csv
keys_1=[i for i in range(1,30)]
keys_2=[i for i in range(31,60)]


df=pd.read_sql(sql, conn, parse_dates=["pvm"])
date=df.iloc[2]['pvm']

st.set_page_config(layout="wide")
st.title("Explore statistics for apartments for sale in Helsinki")
st.subheader(f'Last update date: {date}')
col1, col2= st.columns(2)
checkbox1 = col1.checkbox("Add filters for dataset 1")
checkbox2 = col2.checkbox("Add filters for dataset 2")
modification_container1 = col1.container()
modification_container2 = col2.container()


df_1=filter_dataframe(df, keys_1, checkbox1, modification_container1, col1)
df_2=filter_dataframe(df, keys_2, checkbox2, modification_container2, col2)

df_1_descr= df_1.replace(np.inf, np.nan).describe().reset_index()
df_2_descr=df_2.replace(np.inf, np.nan).describe().reset_index()

##df_2=df_2.describe().reset_index().iloc[1]
df_joined=pd.concat([df_1_descr.iloc[1].rename('filter1'), df_2_descr.iloc[1].rename('filter2')], axis=1).iloc[1:]

metrics=df_joined.to_dict()
prices=(round(metrics['filter1']['Velaton_hinta'],0),round(metrics['filter2']['Velaton_hinta'],0))
m2_prices=(round(metrics['filter1']['Neliohinta'],1), round(metrics['filter2']['Neliohinta'],1))
hoitovastike_m2=(round(metrics['filter1']['Hoitovastike_m2'],1), round(metrics['filter2']['Hoitovastike_m2'],1))


col1.metric(label='Velaton hinta', value=prices[0], delta=prices[0]-prices[1], delta_color="inverse")
col2.metric(label='Velaton hinta', value=prices[1], delta=prices[1]-prices[0], delta_color="inverse")
col1.metric(label='Neliohinta', value=m2_prices[0], delta=m2_prices[0]-m2_prices[1], delta_color="inverse")
col2.metric(label='Neliohinta', value=m2_prices[1], delta=m2_prices[1]-m2_prices[0], delta_color="inverse")
col1.metric(label='Hoitovastike/m2', value=hoitovastike_m2[0], delta=hoitovastike_m2[0]-hoitovastike_m2[1], delta_color="inverse")
col2.metric(label='Hoitovastike/m2', value=hoitovastike_m2[1], delta=hoitovastike_m2[1]-hoitovastike_m2[0], delta_color="inverse")

col1.dataframe(df_1_descr)
col2.dataframe(df_2_descr)