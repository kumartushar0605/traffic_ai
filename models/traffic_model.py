# # models/traffic_model.py
# from utils.data_processing import DataProcessor

# class TrafficModel:
#     def __init__(self, data_path):
#         self.processor = DataProcessor(data_path)

#     def predict_routes(self, start_point, destination):
#         """Predict and return multiple route options with current and future times."""
#         routes = self.processor.get_routes(start_point, destination)
#         if routes.empty:
#             return None
        
#         route_options = []
#         for _, route in routes.iterrows():
#             predicted_time = self.processor.calculate_predicted_time(route)
#             future_time = self.processor.calculate_future_time(route, hours_later=2)
#             route_info = {
#                 'road_name': route['road_name'],
#                 'distance_km': route['distance_km'],
#                 'predicted_time_min': predicted_time,
#                 'future_time_min': future_time,
#                 'complexity_score': route['complexity_score'],
#                 'recommendation': 'Good within 15 min' if predicted_time <= 15 else 'Not ideal now',
#                 'future_recommendation': f"After 2 hours: {future_time} min",
#                 'image_url': route['image_url'] if 'image_url' in route else 'https://via.placeholder.com/150'  # Placeholder if missing
#             }
#             route_options.append(route_info)
        
#         # Sort by future time to recommend the best route after 2 hours
#         best_future_route = min(route_options, key=lambda x: x['future_time_min'])
#         best_future_route['future_recommendation'] += " (Best option after 2 hours)"
        
#         return route_options

#     def display_routes(self, route_options):
#         """Display route options in a formatted manner."""
#         if not route_options:
#             print("No routes found for the given start point and destination.")
#             return
        
#         print("\nAvailable Routes:")
#         print("-" * 70)
#         for i, route in enumerate(route_options, 1):
#             print(f"Route {i}: {route['road_name']}")
#             print(f"  Distance: {route['distance_km']} km")
#             print(f"  Predicted Travel Time (Now): {route['predicted_time_min']} min")
#             print(f"  Complexity Score: {route['complexity_score']} (0-1)")
#             print(f"  Recommendation: {route['recommendation']}")
#             print(f"  Future Prediction: {route['future_recommendation']}")
#             print(f"  Image: {route['image_url']}")
#             print("-" * 70)


# models/traffic_model.py
from utils.data_processing import DataProcessor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrafficModel:
    def __init__(self, data_path):
        logger.info(f"Initializing TrafficModel with data from {data_path}")
        self.processor = DataProcessor(data_path)

    def predict_routes(self, start_point, destination):
        """Predict and return multiple route options with current and future times."""
        try:
            routes = self.processor.get_routes(start_point, destination)
            if routes.empty:
                logger.warning(f"No routes found for {start_point} to {destination}")
                return None
            
            route_options = []
            for _, route in routes.iterrows():
                predicted_time = self.processor.calculate_predicted_time(route)
                future_time = self.processor.calculate_future_time(route, hours_later=2)
                route_info = {
                    'road_name': route['road_name'],
                    'distance_km': float(route['distance_km']),
                    'predicted_time_min': predicted_time,
                    'future_time_min': future_time,
                    'complexity_score': float(route['complexity_score']),
                    'recommendation': 'Good within 15 min' if predicted_time <= 15 else 'Not ideal now',
                    'future_recommendation': f"After 2 hours: {future_time} min",
                    'image_url': route['image_url'] if 'image_url' in route else 'https://via.placeholder.com/150'
                }
                route_options.append(route_info)
            
            # Sort by future time and mark the best route
            best_future_route = min(route_options, key=lambda x: x['future_time_min'])
            best_future_route['future_recommendation'] += " (Best option after 2 hours)"
            
            logger.info(f"Generated {len(route_options)} route options for {start_point} to {destination}")
            return route_options
        
        except Exception as e:
            logger.error(f"Error predicting routes: {e}")
            raise