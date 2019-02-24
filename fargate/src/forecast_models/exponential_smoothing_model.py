"""
Exponential smoothing model
Utilizes Holt-Winters model under the hood
"""

import pandas as pd

from statsmodels.tsa.holtwinters import ExponentialSmoothing


class ExponentialSmoothingModel:
    def __init__(self, json_data, aggregation):
        self.json_data = json_data
        self.aggregation = aggregation
        self.data_frame = pd.DataFrame(json_data)

    def magic(self):
        train = self.data_frame.loc[:, 'quantity']
        model = ExponentialSmoothing(
            train, seasonal='mul', seasonal_periods=self.seasonal_period()).fit()
        prediction = model.predict(
            start=train.index[0], end=self.prediction_end_index())
        predicted_df = self.prediction_dataframe()
        predicted_df['quantity'] = prediction
        predicted_df['date'] = predicted_df['date'].dt.strftime('%Y-%m-%d')
        return predicted_df

    def seasonal_period(self):
        if self.aggregation == 'month':
            return 12
        elif self.aggregation == 'week':
            return 365 / 7
        else:
            return 365

    def prediction_end_index(self):
        return len(self.data_frame.index) + self.seasonal_period()

    def prediction_dataframe(self):
        date_range = pd.date_range(
            self.data_frame['date'][0], periods=self.prediction_end_index())
        return pd.DataFrame(date_range, columns=['date'])
