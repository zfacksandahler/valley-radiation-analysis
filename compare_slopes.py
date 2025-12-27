#!/usr/bin/env python3
"""
Comparative analysis of solar radiation on opposite valley slopes.
Includes net shortwave radiation after accounting for albedo.
"""

import solar_model

def main():
    # Parameters for south-western Germany (Freiburg area)
    latitude = 48.0
    
    # Summer solstice (approx. day 172)
    day_of_year = 172
    
    # Slope A: South-facing (aspect 180° from North)
    slope_a = 30.0
    aspect_a = 180.0
    
    # Slope B: North-facing (aspect 0° from North)
    slope_b = 30.0
    aspect_b = 0.0
    
    # Forest canopy albedo (reflectivity)
    albedo = 0.15
    
    # Calculate hourly incoming radiation
    rad_a = solar_model.calculate_daily_radiation(latitude, day_of_year, slope_a, aspect_a)
    rad_b = solar_model.calculate_daily_radiation(latitude, day_of_year, slope_b, aspect_b)
    
    # Net shortwave radiation = incoming * (1 - albedo)
    net_a = [r * (1.0 - albedo) for r in rad_a]
    net_b = [r * (1.0 - albedo) for r in rad_b]
    
    # Total daily incoming radiation (sum of hourly values, units: W·h/m²)
    total_a = sum(rad_a)
    total_b = sum(rad_b)
    
    # Total daily net shortwave radiation
    total_net_a = sum(net_a)
    total_net_b = sum(net_b)
    
    # Percentage differences relative to south-facing slope
    if total_a != 0:
        diff_percent_incoming = (total_b - total_a) / total_a * 100.0
    else:
        diff_percent_incoming = 0.0
    
    if total_net_a != 0:
        diff_percent_net = (total_net_b - total_net_a) / total_net_a * 100.0
    else:
        diff_percent_net = 0.0
    
    print("=== Valley Slope Radiation Comparison ===")
    print(f"Latitude: {latitude}°")
    print(f"Day of year: {day_of_year} (summer solstice)")
    print(f"Slope angle: {slope_a}°")
    print(f"Canopy albedo: {albedo}")
    print()
    print("South-facing slope (aspect 180°):")
    print(f"  Total daily incoming shortwave radiation: {total_a:.1f} W·h/m²")
    print(f"  Total daily net shortwave radiation: {total_net_a:.1f} W·h/m²")
    print()
    print("North-facing slope (aspect 0°):")
    print(f"  Total daily incoming shortwave radiation: {total_b:.1f} W·h/m²")
    print(f"  Total daily net shortwave radiation: {total_net_b:.1f} W·h/m²")
    print()
    print("--- Incoming radiation differences ---")
    print(f"Difference (North - South): {total_b - total_a:.1f} W·h/m²")
    print(f"Relative difference: {diff_percent_incoming:.1f}%")
    print()
    print("--- Net shortwave radiation differences ---")
    print(f"Difference (North - South): {total_net_b - total_net_a:.1f} W·h/m²")
    print(f"Relative difference: {diff_percent_net:.1f}%")
    print()
    print("(Positive values indicate north-facing receives more)")

if __name__ == "__main__":
    main()