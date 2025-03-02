# # utils/data_processing.py
# import pandas as pd

# class DataProcessor:
#     def __init__(self, data_path):
#         try:
#             self.data = pd.read_csv(data_path)
#             print("CSV loaded successfully. Columns found:", self.data.columns.tolist())
#         except FileNotFoundError:
#             print(f"Error: Could not find file at {data_path}")
#             raise
#         except Exception as e:
#             print(f"Error loading CSV: {e}")
#             raise

#     def get_routes(self, start_point, destination):
#         """Filter routes based on start point and destination."""
#         if 'start_point' not in self.data.columns or 'destination' not in self.data.columns:
#             raise KeyError(f"Required columns 'start_point' or 'destination' not found in data. Available columns: {self.data.columns.tolist()}")
#         routes = self.data[(self.data['start_point'] == start_point) & 
#                            (self.data['destination'] == destination)]
#         return routes

#     def calculate_predicted_time(self, route):
#         """Predict travel time using a weighted combination of historical, recent, and live data."""
#         predicted_time = (0.5 * route['live_update_time_min'] + 
#                           0.3 * route['historical_avg_time_min'] + 
#                           0.2 * route['recent_congestion_min'])
#         return round(predicted_time, 2)

#     def calculate_future_time(self, route, hours_later=2):
#         """Simulate future travel time by reducing congestion (e.g., after 2 hours)."""
#         # Assume congestion reduces by 50% after 2 hours
#         future_congestion = max(0, route['recent_congestion_min'] * 0.5)
#         future_live_time = max(route['historical_avg_time_min'] * 0.9, route['live_update_time_min'] - future_congestion)
#         future_time = (0.5 * future_live_time + 
#                        0.3 * route['historical_avg_time_min'] + 
#                        0.2 * future_congestion)
#         return round(future_time, 2)


# utils/data_processing.py
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, data_path):
        try:
            self.data = pd.read_csv(data_path)
            logger.info(f"CSV loaded successfully from {data_path}. Columns: {self.data.columns.tolist()}")
        except FileNotFoundError:
            logger.error(f"Could not find file at {data_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            raise

    def get_routes(self, start_point, destination):
        """Filter routes based on start point and destination."""
        try:
            if 'start_point' not in self.data.columns or 'destination' not in self.data.columns:
                raise KeyError(f"Required columns missing. Available: {self.data.columns.tolist()}")
            routes = self.data[(self.data['start_point'] == start_point) & 
                              (self.data['destination'] == destination)]
            return routes
        except Exception as e:
            logger.error(f"Error filtering routes: {e}")
            raise

    def calculate_predicted_time(self, route):
        """Predict travel time using weighted combination."""
        try:
            predicted_time = (0.5 * route['live_update_time_min'] + 
                            0.3 * route['historical_avg_time_min'] + 
                            0.2 * route['recent_congestion_min'])
            return round(predicted_time, 2)
        except Exception as e:
            logger.error(f"Error calculating predicted time: {e}")
            raise

    def calculate_future_time(self, route, hours_later=2):
        """Simulate future travel time."""
        try:
            future_congestion = max(0, route['recent_congestion_min'] * 0.5)
            future_live_time = max(route['historical_avg_time_min'] * 0.9, 
                                 route['live_update_time_min'] - future_congestion)
            future_time = (0.5 * future_live_time + 
                          0.3 * route['historical_avg_time_min'] + 
                          0.2 * future_congestion)
            return round(future_time, 2)
        except Exception as e:
            logger.error(f"Error calculating future time: {e}")
            raise