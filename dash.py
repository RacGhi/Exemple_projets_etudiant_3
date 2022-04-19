import streamlit as st
import yfinance as yf
import datetime
import matplotlib.pyplot as plt
from st_btn_select import st_btn_select
import pandas as pd
import numpy as np


# commentaire
start_date =  datetime.date(2000, 1, 1)
end_date =  datetime.date.today()



# Page setting
st.set_page_config(layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Row A
a1, a2, a3, a4 = st.columns(4)

with a1:
    st.image('./Tableau de bord.png')

SP500 = yf.Ticker('^GSPC') # Get ticker data
SP500_DATA = SP500.history(period='1d', interval = "1m")
SP500_DATA2 = SP500.history(period='5d')
r_sp500 = (SP500_DATA.Close[-1] - SP500_DATA2.Close[-1])/SP500_DATA2.Close[-1]
a2.metric("S&P 500", f"{SP500_DATA.Close[-1] :,.0f}", f"{100*r_sp500:.2f} %")



nasdaq = yf.Ticker('^IXIC') # Get ticker data
nasdaq_DATA = nasdaq.history(period='5d', interval = "1m")
nasdaq_DATA2 = nasdaq.history(period='5d', start=start_date, end=end_date)
r_nasdaq = (nasdaq_DATA2.Close[-1] - nasdaq_DATA2.Close[-2])/nasdaq_DATA2.Close[-2]
a3.metric("NASDAQ Composite", f"{nasdaq_DATA.Close[-1] :,.0f}", f"{100*r_nasdaq:.2f} %")

SP_TSX = yf.Ticker('^GSPTSE') # Get ticker data
SP_TSX_DATA = SP_TSX.history(period='5d', interval = "1m")
SP_TSX_DATA2 = SP_TSX.history(period='5d', start=start_date, end=end_date)
r_sp_tsx = (SP_TSX_DATA2.Close[-1] - SP_TSX_DATA2.Close[-2])/SP_TSX_DATA2.Close[-2]
a4.metric("S&P/TSX", f"{SP_TSX_DATA.Close[-1] :,.0f}", f"{100*r_sp_tsx:.2f} %")

# Row B
b1, b2, b3, b4 = st.columns(4)

cad_usd = yf.Ticker('CADUSD=X') # Get ticker data
cad_usd_DATA = cad_usd.history(period='5d', interval = "1m")
cad_usd_DATA2 = cad_usd.history(period='5d', start=start_date, end=end_date)
r_cad_usd = (cad_usd_DATA2.Close[-1] - cad_usd_DATA2.Close[-2])/cad_usd_DATA2.Close[-2]
b1.metric("CAD/USD", f"{cad_usd_DATA.Close[-1] :.3f}", f"{100*r_cad_usd :.2f} %")

wti = yf.Ticker('CL=F') # Get ticker data
wti_DATA = wti.history(period='5d', interval = "1m")
wti_DATA2 = wti.history(period='5d', start=start_date, end=end_date)
diff_wti = wti_DATA.Close[-1] - wti_DATA2.Close[-1]
r_wti = diff_wti/wti_DATA2.Close[-1]
b2.metric("Pétrole", f"{wti_DATA.Close[-1] :.2f}", f"{diff_wti:.2} ({100*r_wti :.2f}%)")

us10y = yf.Ticker('^TNX') # Get ticker data
us10y_DATA = us10y.history(period='1d', start=start_date, end=end_date)
diff_us10y = us10y_DATA.Close[-1] - us10y_DATA.Close[-2]
r_us10y = diff_us10y/us10y_DATA.Close[-2]
b3.metric("Taux US 10 ans", f"{us10y_DATA.Close[-1] :.3f}", f"{diff_us10y:.2} ({100*r_us10y :.2f}%)")

volatilité = yf.Ticker('^VIX') # Get ticker data
volatilité_DATA = volatilité.history(period='5d', interval = "1m")
volatilité_DATA2 = volatilité.history(period='1d', start=start_date, end=end_date)
diff_volatilité = volatilité_DATA2.Close[-1] - volatilité_DATA2.Close[-2]
r_volatilité = diff_volatilité/volatilité_DATA2.Close[-2]
b4.metric("Volatilité", f"{volatilité_DATA.Close[-1] :.2f}", f"{diff_volatilité:.2} ({100*r_volatilité :.2f}%)")






# Retrieving tickers data
ticker_list = ['AMZN', 'MSFT', 'WMT','SHOP.TO', 'TD.TO', 'SAP.TO', 'DOL.TO']
tickerSymbol = st.sidebar.selectbox('Choisir une entreprise :', ticker_list) # Select ticker symbol
tickerData = yf.Ticker(tickerSymbol) # Get ticker data
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) #get the historical prices for this ticker


entreprise = tickerData.info["shortName"]
recommandation = tickerData.info["recommendationKey"]
target = tickerData.info["targetMeanPrice"]
CB = tickerData.info["forwardPE"]

st.write('______')

st.write(f"### Information financière sur {entreprise.title()}")


c1, c2, c3, c4 = st.columns(4)

diff_tickerDf = tickerDf.Close[-1] - tickerDf.Close[-2]
r_tickerDf = diff_tickerDf/tickerDf.Close[-2]
c1.metric(f"{tickerSymbol}", f"{tickerDf.Close[-1] :.2f}", f"{diff_tickerDf:.3} ({100*r_tickerDf :.2f}%)")


c2.metric("Recommandation ", recommandation.title() )

c3.metric("Prix cible ", target )

c4.metric("C/B",  f'{CB:.2f}' )

st.markdown('##')

selection = st_btn_select(('5 jours', '1 mois', '6 mois', '1 an', '3 ans', '5 ans', '10 ans'))

fig, ax = plt.subplots(figsize = (8, 4), dpi = 400)
plt.style.use('ggplot')
ax.set_facecolor('#C5C9C7')

if selection == '5 jours':
    ax.plot(tickerDf.Close[-5:-1])  
elif selection == '1 mois':
    ax.plot(tickerDf.Close[-30:-1])   
elif selection == '6 mois':
    ax.plot(tickerDf.Close[-180:-1])
elif selection == '1 an':
    ax.plot(tickerDf.Close[-252:-1])
elif selection == '3 ans':
    ax.plot(tickerDf.Close[-3*252:-1])
elif selection == '5 ans':
    ax.plot(tickerDf.Close[-5*252:-1])
elif selection == '10 ans':
    ax.plot(tickerDf.Close[-10*252:-1])

fig.autofmt_xdate(rotation=45)
st.pyplot(fig)

   



string_logo = '<img src=%s>' % tickerData.info['logo_url']
st.markdown(string_logo, unsafe_allow_html=True)
tickerData.info["longBusinessSummary"]  

st.write("_______")

st.write("### Détenteurs institutionnels majeurs :")

tickerData.institutional_holders


st.write("_______")


st.write('Sentiment:', run_sentiment_analysis(txt))
