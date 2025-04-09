from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Root route
@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Sustainability Power Dashboard API"

# Endpoint to calculate gas usage metrics
@app.route('/api/gas-usage', methods=['GET'])
def gas_usage():
    try:
        gas_data = pd.read_csv('gas_data.csv')
        gas_data['Month'] = pd.to_datetime(gas_data['Month'], format='%m/%d/%Y')
        
        # Calculate days in month for accurate daily averages
        gas_data['days_in_month'] = gas_data['Month'].dt.daysinmonth
        
        transformed_data = []
        for _, row in gas_data.iterrows():
            data_point = {
                "date": row['Month'].strftime('%Y-%m-%d'),
                "total_gas_usage": row['Usage/CCF'],
                "daily_avg_gas": row['Usage/CCF'] / row['days_in_month'],
                "total_emissions_ton": row['Usage/CCF'] * 0.0545 / 1000  # 0.0545 kg/CCF → metric tons
            }
            transformed_data.append(data_point)
            
        return jsonify(transformed_data)

    except FileNotFoundError:
        return jsonify({"error": "gas_data.csv file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to calculate energy baseline metrics
@app.route('/api/energy-baseline', methods=['GET'])
def energy_baseline():
    try:
        energy_data = pd.read_csv('energy_data.csv')
        energy_data['Month'] = pd.to_datetime(energy_data['Month'], format='%b-%y')
        
        # Calculate actual days in month
        energy_data['days_in_month'] = energy_data['Month'].dt.daysinmonth
        energy_data['Daily_kWh'] = energy_data['Usage/kWh'] / energy_data['days_in_month']
        
        transformed_data = []
        for _, row in energy_data.iterrows():
            data_point = {
                "date": row['Month'].strftime('%Y-%m-%d'),
                "total_kwh": row['Usage/kWh'],
                "daily_avg_kwh": row['Daily_kWh'],
            }
            transformed_data.append(data_point)
            
        daily_avg = energy_data['Daily_kWh'].mean()
        total_30_day_usage = daily_avg * 30  # Projected 30-day usage from average

        return jsonify({
            "daily_avg": daily_avg,
            "total_30_day_usage": total_30_day_usage,
            "data": transformed_data
        })

    except FileNotFoundError:
        return jsonify({"error": "energy_data.csv file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# EUI endpoint remains unchanged per user request

if __name__ == '__main__':
    app.run(debug=True)
