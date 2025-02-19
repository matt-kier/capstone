#
from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Root route
@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Sustainability Power Dashboard API"

# Endpoint to calculate gas usage metrics
@app.route('/api/gas-usage', methods=['GET'])
def gas_usage():
    try:
        # Load gas usage data from CSV file
        gas_data = pd.read_csv('gas_data.csv')
        
        # Calculate total gas usage
        total_gas_usage = gas_data['Usage/CCF'].sum()
        
        # Calculate average daily gas usage
        num_days = len(gas_data)
        daily_avg_gas = total_gas_usage / num_days if num_days else 0
        
        # Calculate CO₂ emissions
        total_emissions_kg = total_gas_usage * 0.0545  # Conversion factor for natural gas
        total_emissions_ton = total_emissions_kg / 1000  # Convert to metric tons

        # Return results as JSON
        return jsonify({
            "total_gas_usage": total_gas_usage,
            "daily_avg_gas": daily_avg_gas,
            "total_emissions_kg": total_emissions_kg,
            "total_emissions_ton": total_emissions_ton
        })
    
    except FileNotFoundError:
        return jsonify({"error": "gas_data.csv file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
