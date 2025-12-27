"""
Solar radiation model for sloped surfaces.
Simplified clear-sky model for hourly radiation.
"""

import math

def calculate_daily_radiation(latitude, day_of_year, slope_deg, aspect_deg):
    """
    Calculate incoming shortwave solar radiation (W/m²) for each hour of the day.

    Parameters
    ----------
    latitude : float
        Latitude in decimal degrees (positive north).
    day_of_year : int
        Day of year (1-365).
    slope_deg : float
        Slope inclination angle in degrees from horizontal (0 = flat, 90 = vertical).
    aspect_deg : float
        Aspect (compass direction) in degrees clockwise from north (0 = North, 90 = East, 180 = South).

    Returns
    -------
    list
        List of 24 hourly radiation values (W/m²) for hours 0-23.
        Hours with no sun (night or behind slope) return 0.
    """
    # Convert angles to radians
    lat = math.radians(latitude)
    slope = math.radians(slope_deg)
    # Convert aspect from N=0 clockwise to surface azimuth gamma measured from south, positive west.
    # North (0°) => gamma = 180° (i.e., surface faces south) in south‑referenced system.
    # Formula: gamma = (aspect_deg - 180) degrees, then convert to radians.
    gamma = math.radians(aspect_deg - 180.0)
    
    # Solar declination (radians) using simple Cooper (1969) formula
    declination = 23.45 * math.sin(math.radians(360.0 / 365.0 * (284 + day_of_year)))
    delta = math.radians(declination)
    
    # Extraterrestrial solar constant (W/m²)
    I0 = 1367.0
    # Correction for Earth‑Sun distance
    day_angle = 2.0 * math.pi * (day_of_year - 1) / 365.0
    I0_corr = I0 * (1.0 + 0.033 * math.cos(day_angle))
    
    # Clear‑sky transmittance (simplified)
    tau = 0.7
    
    hourly_rad = []
    for hour in range(24):
        # Solar hour angle (radians). Solar noon at 12:00.
        # Hour 0 corresponds to midnight, but we compute for the middle of the hour.
        hour_decimal = hour + 0.5
        omega = math.radians(15.0 * (hour_decimal - 12.0))
        
        # Solar altitude (radians)
        sin_alpha = math.sin(lat) * math.sin(delta) + math.cos(lat) * math.cos(delta) * math.cos(omega)
        if sin_alpha <= 0:
            # Sun below horizon
            hourly_rad.append(0.0)
            continue
        alpha = math.asin(sin_alpha)
        
        # Cosine of solar zenith angle
        cos_theta_z = math.sin(alpha)  # same as sin_alpha
        
        # Incidence angle on tilted surface (theta)
        # Duffie & Beckman formula (Eq. 1.6.2)
        cos_theta = (math.sin(delta) * math.sin(lat) * math.cos(slope)
                     - math.sin(delta) * math.cos(lat) * math.sin(slope) * math.cos(gamma)
                     + math.cos(delta) * math.cos(lat) * math.cos(slope) * math.cos(omega)
                     + math.cos(delta) * math.sin(lat) * math.sin(slope) * math.cos(gamma) * math.cos(omega)
                     + math.cos(delta) * math.sin(slope) * math.sin(gamma) * math.sin(omega))
        
        if cos_theta <= 0:
            # Sun behind the slope
            hourly_rad.append(0.0)
            continue
        
        # Clear‑sky horizontal irradiance (GHI) using simple beam component only
        # (ignore diffuse for simplicity)
        GHI = I0_corr * cos_theta_z * tau
        
        # Irradiance on tilted surface (beam component only)
        # Assuming isotropic sky, beam radiation = GHI * cos_theta / cos_theta_z
        # Avoid division by zero (cos_theta_z is zero only at sunrise/sunset, where sin_alpha ~0)
        if cos_theta_z > 1e-10:
            tilted_irrad = GHI * cos_theta / cos_theta_z
        else:
            tilted_irrad = 0.0
        
        hourly_rad.append(tilted_irrad)
    
    return hourly_rad


if __name__ == "__main__":
    # Example usage
    lat = 48.0  # Freiburg area
    doy = 172   # summer solstice
    slope = 30.0
    aspect = 180.0  # south-facing
    
    rad = calculate_daily_radiation(lat, doy, slope, aspect)
    print("Hourly radiation (W/m²) for south-facing slope:")
    for h, val in enumerate(rad):
        print(f"Hour {h:2d}: {val:6.1f}")
    print(f"Total daily: {sum(rad):.1f} W·h/m² (hourly sum)")
    # Note: units are W/m² at each hour; summing gives W·h/m² over 24h.