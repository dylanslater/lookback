import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

## libraries to bring in models
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.regression.linear_model import OLSResults

## streamlit run lookback_app.py
def load_linearmodel(filename):
    model = OLSResults.load(filename)
    return model

## this is what model looks like:
#mod = ols(formula="fg ~ salemonth + sex + genetic_code + program_code + avgage + adg + avgplacewgt + \
#                        liv + earlymort + gradedperc + cullperc + total_eout + callb + \
#                        stockingdensity + percentfines", data=sliced_df)

def main():
    fin_fc = load_linearmodel("fin_fc.pkl")
    page = st.sidebar.selectbox("Choose a page", ["HomePage", "Lookback Models"])

    out_yhat = None
        
    if page == "Homepage":
        st.header("Welcome to the SHP Analytics App.")
        st.write("Please select a page on the left to interact with currently developed models.")
        st.write(df)
    elif page == "Lookback Models":
        st.title("Lookback Models")

        tab1, tab2, tab3 = st.tabs(["FG", "ADG", "Livability"])
        with tab1:
            animaltype = st.radio("Choose Animal Type",('FIN', 'NUR', 'WTF'))
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            if animaltype == 'FIN':
                col1, col2, col3 = st.columns(3)
                ## initialize variables
                d = {'salemonth': ['April'], 'sex': ['MIX'], 'genetic_code': ['1STD'], \
                     'program_code': ['1STD'], 'avgage': [115.0], 'liv': [93.32], \
                     'adg': [1.98], 'avgplacewgt': [55.52], 'earlymort': [2.05], \
                     'gradedperc': [54.32], 'cullperc': [3.15], 'total_eout': [3.155], \
                     'callb': [1617], 'stockingdensity': [101.7], 'percentfines': [40.34]}
                test = pd.DataFrame(data=d)
                ## set fc prediction to default
                if out_yhat == None:
                    out_yhat = fin_fc.predict(test)
                ## adjust any widgets now
                with col1:
                    test['avgplacewgt'][0] = st.number_input('Avg Place Weight',min_value=35.0,max_value=70.0,value=test['avgplacewgt'][0],step=0.01)
                    test['adg'][0] = st.number_input('True ADG',min_value=1.45,max_value=2.5,value=test['adg'][0],step=0.01)
                    test['cullperc'][0] = st.number_input("Cull %",min_value=0.50,max_value=15.0,value=test['cullperc'][0],step=0.01)
                    test['stockingdensity'][0] = st.number_input("Stocking Density",min_value=75.0,max_value=125.0,value=test['stockingdensity'][0],step=0.01)
                with col2:
                    test['avgage'][0] = st.number_input("Average Age",min_value=95.0,max_value=150.0,value=test['avgage'][0],step=0.01)
                    test['gradedperc'][0] = st.number_input("Graded %",min_value=0.00,max_value=75.0,value=test['gradedperc'][0],step=0.01)
                    test['total_eout'][0] = st.number_input("Total E-Outs",min_value=0.00,max_value=75.0,value=test['total_eout'][0],step=0.01)
                with col3:
                    test['liv'][0] = st.number_input("Livability",min_value=75.0,max_value=100.0,value=test['liv'][0],step=0.01)
                    test['earlymort'][0] = st.number_input("Early Mortality",min_value=0.0,max_value=10.0,value=test['earlymort'][0],step=0.01)
                    test['callb'][0] = st.number_input("Calories",min_value=1500,max_value=1675,value=test['callb'][0],step=1)
                    test['percentfines'][0] = st.number_input("Fine Percent",min_value=30.0,max_value=60.0,value=test['percentfines'][0],step=0.01)
                
                ## now show updated prediction
                out_yhat = fin_fc.predict(test)
                col1.metric('FeedConversion: ',out_yhat)
            
        
        
if __name__ == "__main__":
    main()
   