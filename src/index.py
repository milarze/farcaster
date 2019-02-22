"""
Entry point for forecasting requests
"""

import json

from src.forecast_models.exponential_smoothing_model import ExponentialSmoothingModel


def handler(jsonstring):
    """
    Accepts a JSON string payload
    Returns a JSON string with forecast predictions
    """
    try:
      payload = json.loads(jsonstring)
      time_series = payload['time_series']
      aggregation = payload['aggregation']
      prediction = ExponentialSmoothingModel(time_series, aggregation).magic()
      return prediction.to_json(orient='records', date_format='None')
    except Exception as e:
      print(str(e))
      return "\{\"message\":\"Unknown error ocurred\"\}"
