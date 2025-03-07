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
                # Split petrol pumps and their coordinates
                petrol_pumps = route['petrolpump'].split(', ') if 'petrolpump' in route else []
                petrol_coords = route['petrolpump_coordinates'].split('; ') if 'petrolpump_coordinates' in route else []
                petrol_pump_info = {pump.strip(): coord.strip() for pump, coord in zip(petrol_pumps, petrol_coords)}

                # Split hotels and their coordinates
                hotels = route['hotels'].split(', ') if 'hotels' in route else []
                hotel_coords = route['hotel_coordinates'].split('; ') if 'hotel_coordinates' in route else []
                hotel_info = {hotel.strip(): coord.strip() for hotel, coord in zip(hotels, hotel_coords)}

                # Build route information dictionary
                route_info = {
                    'road_name': route['road_name'],
                  
'road_cls': str(route['route_cls']),

                    'distance_km': float(route['distance_km']) if route['distance_km'] else 0.0,
                    'predicted_time_min': self.processor.calculate_predicted_time(route),
                    'future_time_min': self.processor.calculate_future_time(route, hours_later=2),
                    'complexity_score': route['complexity_score'],
                    'recommendation': 'Good within 15 min' if self.processor.calculate_predicted_time(route) <= 15 else 'Not ideal now',
                    'future_recommendation': f"After 2 hours: {self.processor.calculate_future_time(route, hours_later=2)} min",
                    'image_url': route.get('image_url', 'https://via.placeholder.com/150'),
                    'petrol_pumps': petrol_pump_info,
                    'hotels': hotel_info,
                    
                }

                route_options.append(route_info)

            # Sort routes by future time and mark the best route
            if route_options:
                best_future_route = min(route_options, key=lambda x: x['future_time_min'])
                best_future_route['future_recommendation'] += " (Best option after 2 hours)"

            logger.info(f"Generated {len(route_options)} route options for {start_point} to {destination}")
            return route_options

        except Exception as e:
            logger.error(f"Error predicting routes: {e}")
            raise