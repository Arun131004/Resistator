from django.shortcuts import render
from django.http import JsonResponse

def resistor_home(request):
    return render(request, "resistor/index.html")

def calculate_resistance(request):
    color_codes = {
        "black": 0, "brown": 1, "red": 2, "orange": 3, "yellow": 4,
        "green": 5, "blue": 6, "violet": 7, "gray": 8, "white": 9
    }
    
    multipliers = {
        "black": 1, "brown": 10, "red": 100, "orange": 1_000, "yellow": 10_000,
        "green": 100_000, "blue": 1_000_000, "violet": 10_000_000,
        "gold": 0.1, "silver": 0.01
    }
    
    tolerance_values = {
        "brown": "±1%", "red": "±2%", "green": "±0.5%", "blue": "±0.25%",
        "violet": "±0.1%", "gray": "±0.05%", "gold": "±5%", "silver": "±10%"
    }
    
    if request.method == "GET":
        try:
            bands = int(request.GET.get("bands", 4))
            band1 = request.GET.get("band1", "").lower()
            band2 = request.GET.get("band2", "").lower()
            band3 = request.GET.get("band3", "").lower()
            multiplier = request.GET.get("multiplier", "").lower()
            tolerance = request.GET.get("tolerance", "").lower()

            # Validate Inputs
            if band1 not in color_codes or band2 not in color_codes or multiplier not in multipliers:
                return JsonResponse({"error": "Invalid color selection"}, status=400)
            if bands >= 5 and band3 not in color_codes:
                return JsonResponse({"error": "Invalid third band color"}, status=400)
            if tolerance and tolerance not in tolerance_values:
                return JsonResponse({"error": "Invalid tolerance color"}, status=400)

            # Compute Resistance
            resistance_value = (color_codes[band1] * 10 + color_codes[band2])

            if bands >= 5:  # For 5-band and 6-band resistors
                resistance_value = resistance_value * 10 + color_codes[band3]

            resistance_value *= multipliers[multiplier]
            
            return JsonResponse({"resistance": f"{resistance_value} Ω", "tolerance": tolerance_values.get(tolerance, "")})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
