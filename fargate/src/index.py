"""
Entry point for forecasting requests
"""

import json

from src.forecast_models.exponential_smoothing_model import ExponentialSmoothingModel
from src.forecast_models.fb_prophet_model import FbProphetModel

def model(model_name):
    """
    Figure out which model to use
    Returns the FbProphetModel if 'prophet'
    is the model name given, otherwise defaults to
    ExponentialSmoothingModel
    """
    if model_name == 'prophet':
        return FbProphetModel
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
        prediction = model(model_name)(time_series, aggregation).magic()
        return prediction.to_json(orient='records', date_format='iso')
    except Exception as e: # pylint: disable=broad-except
        return '{"message":"Unknown error ocurred"}'
