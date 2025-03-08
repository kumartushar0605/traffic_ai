from utils.data_processing import DataProcessor
from utils.emissions import CO2Estimator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_time(minutes):
    """Convert time in minutes to hours and minutes format, with minutes in decimal (1 decimal place)."""
    hours = minutes // 60
    mins = (minutes % 60) / 60  # Convert remaining minutes to decimal
    return f"{hours + round(mins, 1)} hrs" if hours > 0 else f"{round(mins * 60, 1)} min"


class TrafficModel:
    def __init__(self, data_path):
        logger.info(f"Initializing TrafficModel with data from {data_path}")
        self.processor = DataProcessor(data_path)
        self.co2_estimator = CO2Estimator()

    def predict_routes(self, start_point, destination):
        """Predict and return multiple route options with current and future times, comparing CO2 emissions."""
        try:
            routes = self.processor.get_routes(start_point, destination)
            if routes.empty:
                logger.warning(f"No routes found for {start_point} to {destination}")
                return None

            route_options = []
            for _, route in routes.iterrows():
                petrol_pumps = route['petrolpump'].split(', ') if 'petrolpump' in route else []
                petrol_coords = route['petrolpump_coordinates'].split('; ') if 'petrolpump_coordinates' in route else []
                petrol_pump_info = {pump.strip(): coord.strip() for pump, coord in zip(petrol_pumps, petrol_coords)}

                hotels = route['hotels'].split(', ') if 'hotels' in route else []
                hotel_coords = route['hotel_coordinates'].split('; ') if 'hotel_coordinates' in route else []
                hotel_info = {hotel.strip(): coord.strip() for hotel, coord in zip(hotels, hotel_coords)}

                predicted_time = self.processor.calculate_predicted_time(route)
                future_time = self.processor.calculate_future_time(route, hours_later=2)
                co2_emissions = self.co2_estimator.estimate_emissions(route['distance_km'], route['recent_congestion_min'])

                route_info = {
                    'road_name': route['road_name'],
                    'road_cls': str(route['route_cls']),
                    'distance_km': float(route['distance_km']) if route['distance_km'] else 0.0,
                    'predicted_time': convert_time(predicted_time),
                    'future_time': convert_time(future_time),
                    'complexity_score': route['complexity_score'],
                    'recommendation': 'Good within 15 min' if predicted_time <= 15 else 'Not ideal now',
                    'future_recommendation': f"After 2 hours: {convert_time(future_time)}",
                    'co2_emissions_kg': round(co2_emissions, 2),
                    'no_of_tolls': str(route['no_of_tolls']),
                    'cost_of_each_tolls': str(route['cost_of_each_tolls']),
                    'sum_of_cost_of_each_tolls': str(route['sum_of_cost_of_each_tolls']),
                    'image_url': route.get('image_url', 'https://via.placeholder.com/150'),
                    'petrol_pumps': petrol_pump_info,
                    'hotels': hotel_info,
                }

                route_options.append(route_info)

            if route_options:
                # Find route with minimum CO2 emissions
                best_co2_route = min(route_options, key=lambda x: x['co2_emissions_kg'])
                best_future_route = min(route_options, key=lambda x: x['future_time'])

                # Add CO2 comparison message to each route
                for route in route_options:
                    if route['co2_emissions_kg'] == best_co2_route['co2_emissions_kg']:
                        route['environmental_impact'] = "This route has the least CO2 emissions, making it the most environmentally friendly option."
                    else:
                        diff = route['co2_emissions_kg'] - best_co2_route['co2_emissions_kg']
                        route['environmental_impact'] = f"This route emits {round(diff, 2)} kg more CO2 than the most eco-friendly option."

                # Update best future route recommendation
                best_future_route['future_recommendation'] += " (Best option after 2 hours)"

            logger.info(f"Generated {len(route_options)} route options for {start_point} to {destination}")
            return route_options

        except Exception as e:
            logger.error(f"Error predicting routes: {e}")
            raise
