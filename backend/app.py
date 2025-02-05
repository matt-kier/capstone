from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Root route
@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Sustainability Power Dashboard API"

# Endpoint to calculate energy baseline metrics
@app.route('/api/energy-baseline', methods=['GET'])
def energy_baseline():
    try:
        # Load CSV file with energy data
        energy_data = pd.read_csv('energy_data.csv')
        
        # Calculate peak and off-peak energy usage averages
        peak_avg = energy_data[energy_data['time'] == 'peak']['kWh'].mean()
        off_peak_avg = energy_data[energy_data['time'] == 'off-peak']['kWh'].mean()
        
        # Calculate average daily consumption
        daily_avg = (peak_avg + off_peak_avg) / 2
        
        # Calculate weekday and weekend energy consumption totals
        weekday_total = daily_avg * 20  # 20 weekdays in a month
        weekend_total = energy_data[energy_data['time'] == 'weekend']['kWh'].mean() * 8  # 8 weekend days
        
        # Calculate total 30-day energy consumption
        total_30_day_usage = weekday_total + weekend_total

        # Create a dictionary with calculated values
        energy_baseline_results = {
            "peak_avg": peak_avg,
            "off_peak_avg": off_peak_avg,
            "daily_avg": daily_avg,
            "total_30_day_usage": total_30_day_usage
        }

        # Return results as JSON
        return jsonify(energy_baseline_results)
    
    except FileNotFoundError:
        return jsonify({"error": "energy_data.csv file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to calculate gas usage metrics
@app.route('/api/gas-usage', methods=['GET'])
def gas_usage():
    try:
        # Load gas usage data from CSV file
        gas_data = pd.read_csv('gas_data.csv')
        
        # Calculate weekday and weekend gas usage
        weekday_avg_gas = gas_data[gas_data['day_type'] == 'weekday']['CFH'].mean()
        weekend_avg_gas = gas_data[gas_data['day_type'] == 'weekend']['CFH'].mean()
        
        # Total gas usage for the month
        weekday_gas_total = weekday_avg_gas * 20 * 24  # 20 weekdays, 24 hours each day
        weekend_gas_total = weekend_avg_gas * 8 * 24   # 8 weekend days, 24 hours each day
        total_gas_usage = weekday_gas_total + weekend_gas_total
        
        # Calculate CO₂ emissions
        total_emissions_kg = total_gas_usage * 0.0545  # Conversion factor for natural gas
        total_emissions_ton = total_emissions_kg / 1000  # Convert to metric tons

        # Return results as JSON
        return jsonify({
            "weekday_avg_gas": weekday_avg_gas,
            "weekend_avg_gas": weekend_avg_gas,
            "total_gas_usage": total_gas_usage,
            "total_emissions_kg": total_emissions_kg,
            "total_emissions_ton": total_emissions_ton
        })
    
    except FileNotFoundError:
        return jsonify({"error": "gas_data.csv file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to calculate Water and Energy Use Intensity (WUI and EUI)
@app.route('/api/intensity-metrics', methods=['GET'])
def intensity_metrics():
    try:
        # Load energy and water usage data
        energy_data = pd.read_csv('energy_data.csv')
        water_data = pd.read_csv('water_data.csv')
        
        # Building area (in square feet)
        building_area = 10000  # Example area value
        
        # Calculate total energy and water usage
        total_energy = energy_data['kWh'].sum()
        total_water = water_data['gallons'].sum()
        
        # Calculate Energy Use Intensity (EUI) and Water Use Intensity (WUI)
        eui = total_energy / building_area
        wui = total_water / building_area

        # Return intensity metrics as JSON
        return jsonify({
            "total_energy": total_energy,
            "total_water": total_water,
            "eui": eui,
            "wui": wui
        })
    
    except FileNotFoundError:
        return jsonify({"error": "Required CSV file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


