def get_recommendation(
    stock_flow,
    filler_flow,
    steam_pressure,
    machine_speed,
    moisture,
    ash,
    caliper
):

    recommendations = []

    # Stock Flow
    if stock_flow < 115:
        recommendations.append({
            "Recommendation": "Increase Stock Flow",
            "Reason": "Stock Flow is below the recommended operating range, which may reduce Basis Weight.",
            "Source": "Engineering Rule Base"
        })

    elif stock_flow > 125:
        recommendations.append({
            "Recommendation": "Reduce Stock Flow",
            "Reason": "High Stock Flow may increase Basis Weight beyond specification.",
            "Source": "Engineering Rule Base"
        })

    # Filler Flow
    if filler_flow < 20:
        recommendations.append({
            "Recommendation": "Increase Filler Flow",
            "Reason": "Low Filler Flow may reduce Ash content.",
            "Source": "Engineering Rule Base"
        })

    elif filler_flow > 24:
        recommendations.append({
            "Recommendation": "Reduce Filler Flow",
            "Reason": "High Filler Flow may increase Ash content.",
            "Source": "Engineering Rule Base"
        })

    # Steam Pressure
    if steam_pressure < 6.2:
        recommendations.append({
            "Recommendation": "Increase Steam Pressure",
            "Reason": "Steam Pressure is too low for effective paper drying.",
            "Source": "Engineering Rule Base"
        })

    elif steam_pressure > 6.8:
        recommendations.append({
            "Recommendation": "Reduce Steam Pressure",
            "Reason": "Excessive Steam Pressure may over-dry the paper.",
            "Source": "Engineering Rule Base"
        })

    # Machine Speed
    if machine_speed < 650:
        recommendations.append({
            "Recommendation": "Increase Machine Speed",
            "Reason": "Machine Speed is lower than the recommended range.",
            "Source": "Historical Process Data"
        })

    elif machine_speed > 760:
        recommendations.append({
            "Recommendation": "Reduce Machine Speed",
            "Reason": "High Machine Speed may reduce paper thickness (Caliper).",
            "Source": "Historical Process Data"
        })

    # Moisture
    if moisture > 5.8:
        recommendations.append({
            "Recommendation": "Reduce Moisture",
            "Reason": "High Moisture indicates insufficient drying.",
            "Source": "Historical Process Data"
        })

    elif moisture < 5.2:
        recommendations.append({
            "Recommendation": "Increase Moisture",
            "Reason": "Very low Moisture may produce brittle paper.",
            "Source": "Historical Process Data"
        })

    # Ash
    if ash > 10.5:
        recommendations.append({
            "Recommendation": "Reduce Filler Flow",
            "Reason": "High Ash content may affect paper quality.",
            "Source": "Historical Process Data"
        })

    elif ash < 9.5:
        recommendations.append({
            "Recommendation": "Increase Filler Flow",
            "Reason": "Low Ash content may indicate insufficient filler.",
            "Source": "Historical Process Data"
        })

    # Caliper
    if caliper < 0.090:
        recommendations.append({
            "Recommendation": "Reduce Machine Speed or Increase Stock Flow",
            "Reason": "Paper thickness (Caliper) is below the desired range.",
            "Source": "Historical Process Data"
        })

    elif caliper > 0.100:
        recommendations.append({
            "Recommendation": "Increase Machine Speed or Reduce Stock Flow",
            "Reason": "Paper thickness (Caliper) is above the desired range.",
            "Source": "Historical Process Data"
        })

    # Overall Recommendation
    if len(recommendations) == 0:
        recommendations.append({
            "Recommendation": "No Action Required",
            "Reason": "All process parameters are within the recommended operating range.",
            "Source": "Historical Process Data + Engineering Rule Base"
        })

    return recommendations