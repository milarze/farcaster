"""
Entry point for forecasting requests
"""

import json

from src.forecast_models.exponential_smoothing_model import ExponentialSmoothingModel
from src.forecast_models.fb_prophet_model import FbProphetModel

def model(model_name):
    if model_name is 'prophet':
        return FbProphetModel
    else:
        return ExponentialSmoothingModel

def handler(jsonstring, model_name):
    """
    Accepts a JSON string payload
    Returns a JSON string with forecast predictions
    """
    try:
        payload = json.loads(jsonstring)
        time_series = payload['time_series']
        aggregation = payload['aggregation']
        prediction = model(model_name)(time_series).magic()
        return prediction.to_json(orient='records', date_format='iso')
    except Exception as error: # pylint: disable=broad-except
        return '{"message":"Unknown error ocurred"}'
