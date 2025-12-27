#!/usr/bin/env python3
"""
Comparative analysis of solar radiation on opposite valley slopes.
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
    
    # Calculate hourly radiation
    rad_a = solar_model.calculate_daily_radiation(latitude, day_of_year, slope_a, aspect_a)
    rad_b = solar_model.calculate_daily_radiation(latitude, day_of_year, slope_b, aspect_b)
    
    # Total daily radiation (sum of hourly values, units: W·h/m²)
    total_a = sum(rad_a)
    total_b = sum(rad_b)
    
    # Percentage difference relative to south-facing slope
    if total_a != 0:
        diff_percent = (total_b - total_a) / total_a * 100.0
    else:
        diff_percent = 0.0
    
    print("=== Valley Slope Radiation Comparison ===")
    print(f"Latitude: {latitude}°")
    print(f"Day of year: {day_of_year} (summer solstice)")
    print(f"Slope angle: {slope_a}°")
    print()
    print("South-facing slope (aspect 180°):")
    print(f"  Total daily incoming shortwave radiation: {total_a:.1f} W·h/m²")
    print("North-facing slope (aspect 0°):")
    print(f"  Total daily incoming shortwave radiation: {total_b:.1f} W·h/m²")
    print()
    print(f"Difference (North - South): {total_b - total_a:.1f} W·h/m²")
    print(f"Relative difference: {diff_percent:.1f}%")
    print("(Positive means north-facing receives more)")
    
    # Optional: print hourly values
    # print("\nHourly radiation (W/m²):")
    # for h in range(24):
    #     print(f"Hour {h:2d}: South {rad_a[h]:6.1f} | North {rad_b[h]:6.1f}")

if __name__ == "__main__":
    main()