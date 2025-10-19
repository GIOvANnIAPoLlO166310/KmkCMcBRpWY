# 代码生成时间: 2025-10-20 02:09:23
# inventory_forecast.py
"""
A Celery task for inventory forecasting using a simple model.
"""

import os
from celery import Celery
from celery.utils.log import get_task_logger
import logging
from datetime import datetime, timedelta
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Set up the Celery app
os.environ.setdefault('CELERY_BROKER_URL', 'amqp://guest:guest@localhost//')
app = Celery('tasks', broker='amqp://guest:guest@localhost//')
app.conf.update(task_serializer='json',
                accept_content=['json'],
                result_serializer='json',
                timezone='UTC',
                enable_utc=True)

# Get the logger
logger = get_task_logger(__name__)

class InventoryForecast:
    """
    A class for inventory forecasting.
    """
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path
        self.model = LinearRegression()

    def load_data(self):
        """
        Load inventory data from a CSV file.
        """
        try:
            data = pd.read_csv(self.data_file_path)
            return data
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            raise

    def preprocess_data(self, data):
        """
        Preprocess the data for forecasting.
        """
        try:
            # Convert the dates to datetime objects
            data['date'] = pd.to_datetime(data['date'])
            # Create a new column for the day of the week
            data['day_of_week'] = data['date'].dt.day_name()
            # Drop any rows with missing values
            data = data.dropna()
            return data
        except Exception as e:
            logger.error(f"Failed to preprocess data: {e}")
            raise

    def fit_model(self, data):
        """
        Fit the linear regression model to the data.
        """
        try:
            # Prepare the features and target
            X = data[['day_of_week', 'previous_day_sales']]
            y = data['sales']
            # Fit the model
            self.model.fit(X, y)
            return self.model
        except Exception as e:
            logger.error(f"Failed to fit model: {e}")
            raise

    def predict(self, data, model):
        """
        Predict sales for the next period.
        """
        try:
            # Preprocess the input data for prediction
            data['date'] = pd.to_datetime(data['date'])
            data['day_of_week'] = data['date'].dt.day_name()
            data = data.dropna()
            # Prepare the features for prediction
            X = data[['day_of_week', 'previous_day_sales']]
            # Make the prediction
            prediction = model.predict(X)
            return prediction
        except Exception as e:
            logger.error(f"Failed to make prediction: {e}")
            raise

    @staticmethod
    def add_days(date, days):
        """
        Add days to a given date.
        """
        return date + timedelta(days=days)

# Define the Celery task
@app.task
def forecast_inventory(data_file_path, days=7):
    """
    A Celery task that forecasts inventory for the next 'days' days.
    """
    forecast = InventoryForecast(data_file_path)
    data = forecast.load_data()
    data = forecast.preprocess_data(data)
    model = forecast.fit_model(data)
    # Prediction for the next 'days' days
    today = datetime.now().date()
    predictions = []
    for i in range(days):
        # Prepare input data for prediction
        next_day = InventoryForecast.add_days(today, i + 1)
        next_day_sales = data[data['date'].dt.date == today].iloc[0]['sales']
        # Assign the next day's data as a dictionary
        next_day_data = {
            'date': next_day,
            'previous_day_sales': next_day_sales
        }
        # Make the prediction
        prediction = forecast.predict(pd.DataFrame([next_day_data]), model)
        predictions.append((next_day, prediction[0]))
    return predictions
