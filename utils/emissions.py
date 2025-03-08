#

class CO2Estimator:
    """Class to estimate CO2 emissions for a trip based on distance and congestion levels."""

    AVERAGE_EMISSION_PER_KM = 0.12  # kg CO₂ per km for an average car

    def estimate_emissions(self, distance_km, congestion_level):
        """
        Estimate CO₂ emissions based on:
        - Distance traveled (in km)
        - Congestion level (time spent in traffic, in minutes)
        """
        if distance_km is None or distance_km <= 0:
            return 0.0

        congestion_factor = 1 + (congestion_level / 30)  
        emissions = distance_km * self.AVERAGE_EMISSION_PER_KM * congestion_factor
        return emissions
