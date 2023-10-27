import yfinance as yf
import pandas as pd
import altair as alt



ticker = ['ABG.JO','ABG.JO','APN.JO','ANH.JO','BTI.JO']
n_days = 21

#Create dataset
stacked_n_days_price_returns = pd.DataFrame()
for i in ticker:
    price_data = yf.download(i[0],period='10y').reset_index()

    #price_data_sample = price_data.sample(n=100+n_days-1,random_state=42)
    #print(price_data_sample)

    #Calculate percentage change for each n_day.
    for days in range(0, n_days):
        column_name = days
        price_data[column_name] = price_data['Close'].pct_change(periods=days)

    price_data_sample = price_data.iloc[n_days-1:].sample(n=100,random_state=42)
    print(price_data_sample)

    n_days_price_returns  = price_data_sample.reset_index(drop=True).iloc[:,8:].melt(
    value_vars=[days for days in range(1, 21)], 
    var_name='days', value_name='percent_change')
    print(n_days_price_returns)
    print(n_days_price_returns[n_days_price_returns['days'].isin([1])].describe())

    stacked_n_days_price_returns = pd.concat([stacked_n_days_price_returns, n_days_price_returns], ignore_index=True)
    
stacked_n_days_price_returns_1 = stacked_n_days_price_returns[stacked_n_days_price_returns['days'].isin(range(1, 11))]
stacked_n_days_price_returns_2 = stacked_n_days_price_returns[stacked_n_days_price_returns['days'].isin(range(11, 21))] 



print(stacked_n_days_price_returns_1.describe(),stacked_n_days_price_returns_2.describe())


#chart 1
price_returns_1_to_11_chart = alt.Chart(stacked_n_days_price_returns_1, width=100).transform_density(
    'percent_change',
    as_=['percent_change', 'density'],
    groupby=['days']
).mark_area(orient='horizontal').encode(
    alt.X('density:Q')
        .stack('center')
        .impute(None)
        .title(None)
        .axis(labels=False, values=[0], grid=False, ticks=True),
    alt.Y('percent_change:Q',axis=alt.Axis(format='%')),
    alt.Color('days:N'),
    alt.Column('days:N')
        .spacing(0)
        .header(titleOrient='bottom', labelOrient='bottom', labelPadding=0)
)


#chart 2
price_returns_11_to_21_chart = alt.Chart(stacked_n_days_price_returns_2, width=100).transform_density(
    'percent_change',
    as_=['percent_change', 'density'],
    groupby=['days']
).mark_area(orient='horizontal').encode(
    alt.X('density:Q')
        .stack('center')
        .impute(None)
        .title(None)
        .axis(labels=False, values=[0], grid=False, ticks=True),
    alt.Y('percent_change:Q',axis=alt.Axis(format='%')),
    alt.Color('days:N'),
    alt.Column('days:N')
        .spacing(0)
        .header(titleOrient='bottom', labelOrient='bottom', labelPadding=0)
)


price_expentancy = alt.vconcat(price_returns_1_to_11_chart , price_returns_11_to_21_chart).configure_view(
    stroke=None
)
price_expentancy.save('price_expentancy.html')