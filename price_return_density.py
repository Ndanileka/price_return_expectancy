import yfinance as yf
import pandas as pd
import altair as alt


#Create dataset
mtn = yf.Ticker('SLM.JO').history(period='3y').reset_index()
mtn['1_day_change'] = mtn['Close'].pct_change()
mtn['Date'] = mtn['Date'].dt.tz_localize(None)
for days in range(1, 21):
    column_name = days
    mtn[column_name] = mtn['Close'].pct_change(periods=days)

price_returns  = mtn.iloc[20:].reset_index(drop=True).iloc[:,8:]

price_returns_tn = price_returns.melt(value_vars=[days for days in range(1, 21)], 
               var_name='Days', value_name='PercentChange')

price_returns_1_to_11 = price_returns_tn[price_returns_tn['Days'].isin(range(1, 11))]
price_returns_11_to_21 = price_returns_tn[price_returns_tn['Days'].isin(range(11, 21))]

print(price_returns_1_to_11.describe(),price_returns_11_to_21.describe())
#Char 3



#chart 1
price_returns_1_to_11_chart = alt.Chart(price_returns_1_to_11, width=100).transform_density(
    'PercentChange',
    as_=['PercentChange', 'density'],
    groupby=['Days']
).mark_area(orient='horizontal').encode(
    alt.X('density:Q')
        .stack('center')
        .impute(None)
        .title(None)
        .axis(labels=False, values=[0], grid=False, ticks=True),
    alt.Y('PercentChange:Q',axis=alt.Axis(format='%')),
    alt.Color('Days:N'),
    alt.Column('Days:N')
        .spacing(0)
        .header(titleOrient='bottom', labelOrient='bottom', labelPadding=0)
)


#chart 2
price_returns_11_to_21_chart = alt.Chart(price_returns_11_to_21, width=100).transform_density(
    'PercentChange',
    as_=['PercentChange', 'density'],
    groupby=['Days']
).mark_area(orient='horizontal').encode(
    alt.X('density:Q')
        .stack('center')
        .impute(None)
        .title(None)
        .axis(labels=False, values=[0], grid=False, ticks=True),
    alt.Y('PercentChange:Q',axis=alt.Axis(format='%')),
    alt.Color('Days:N'),
    alt.Column('Days:N')
        .spacing(0)
        .header(titleOrient='bottom', labelOrient='bottom', labelPadding=0)
)


price_expentancy = alt.vconcat(price_returns_1_to_11_chart , price_returns_11_to_21_chart).configure_view(
    stroke=None
)
price_expentancy.save('price_expentancy.html')