"""
TSA using FB Prohpet
"""

import pandas as pd
from fbprophet import Prophet
from scipy.stats import boxcox
from scipy.special import inv_boxcox
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

class FbProphetModel:
    def __init__(self, json_data):
        self.json_data = json_data
        self.data_frame = pd.DataFrame(json_data)

    def magic(self):
        self.data_frame['ds'] = self.data_frame['date']
        self.data_frame.set_index('date')
        self.data_frame['y'], lam = boxcox(self.data_frame['quantity'])
        train = Prophet(seasonality_mode='multiplicative')
        train.fit(self.data_frame)
        future = train.make_future_dataframe(periods=365, include_history=True)
        forecast = train.predict(future)
        forecast['date'] = pd.to_datetime(forecast['ds'], format='%Y-%m-%d')
        forecast[['yhat','yhat_upper','yhat_lower']] = forecast[['yhat','yhat_upper','yhat_lower']].apply(lambda x: inv_boxcox(x, lam))
        forecast[['quantity', 'quantity_upper', 'quantity_lower']] = forecast[['yhat', 'yhat_upper', 'yhat_lower']]
        return forecast[['date', 'quantity', 'quantity_upper', 'quantity_lower']]
