from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

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
        # Load gas usage data from CSV file
        gas_data = pd.read_csv('gas_data.csv')

        # Convert 'Month' to datetime
        gas_data['Month'] = pd.to_datetime(gas_data['Month'], format='%m/%d/%Y')

        # Initialize an empty list to store the transformed data
        transformed_data = []

        # Iterate over each row in the DataFrame
        for index, row in gas_data.iterrows():
            # Create a dictionary for each data point
            data_point = {
                "date": row['Month'].strftime('%Y-%m-%d'),
                "total_gas_usage": row['Usage/CCF'],
                "daily_avg_gas": row['Usage/CCF'],  # Assuming daily average is the same as monthly usage
                "total_emissions_ton": row['Usage/CCF'] * 0.0545 / 1000  # Conversion factor for natural gas
            }
            # Append the data point to the list
            transformed_data.append(data_point)

        # Return the transformed data as JSON
        return jsonify(transformed_data)

    except FileNotFoundError:
        return jsonify({"error": "gas_data.csv file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to calculate energy baseline metrics
@app.route('/api/energy-baseline', methods=['GET'])
def energy_baseline():
    try:
        # Load energy data from CSV file
        energy_data = pd.read_csv('energy_data.csv')

        # Convert 'Month' to datetime with the correct format
        energy_data['Month'] = pd.to_datetime(energy_data['Month'], format='%b-%y')

        # Assuming 'Usage/kWh' is the total energy for the month, and we'll calculate daily average using a standard 30 days
        energy_data['Daily_kWh'] = energy_data['Usage/kWh'] / 30  # You can replace 30 with actual billing days if available
        daily_avg = energy_data['Daily_kWh'].mean()

        # Calculate total 30-day energy consumption
        total_30_day_usage = daily_avg * 30

        # Create a list to store transformed data
        transformed_data = []

        # Iterate over each row to transform data
        for _, row in energy_data.iterrows():
            data_point = {
                "date": row['Month'].strftime('%Y-%m-%d'),
                "total_kwh": row['Usage/kWh'],
                "daily_avg_kwh": row['Daily_kWh'],
            }
            transformed_data.append(data_point)

        # Create a dictionary with calculated values and transformed data
        energy_baseline_results = {
            "daily_avg": daily_avg,
            "total_30_day_usage": total_30_day_usage,
            "data": transformed_data
        }

        # Return results as JSON
        return jsonify(energy_baseline_results)

    except FileNotFoundError:
        return jsonify({"error": "energy_data.csv file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to calculate Energy Use Intensity (EUI)
@app.route('/api/eui', methods=['GET'])
def calculate_eui():
    try:
        # Load electricity usage data from CSV file
        electric_data = pd.read_csv('electric_data.csv')

        # Ensure 'Usage' column exists
        if 'Usage' not in electric_data.columns:
            return jsonify({"error": "'Usage' column not found in CSV file"}), 400

        # Calculate total annual energy consumption in kWh (using 'Usage' column)
        total_energy_kwh = electric_data['Usage'].sum()

        # Convert total energy to kBtu (1 kWh = 3.412 kBtu)
        total_energy_kbtu = total_energy_kwh * 3.412

        # Define the building area in square feet
        building_area_sqft = 10000  # Example area; replace with actual value

        # Calculate EUI in kBtu per square foot per year
        eui = total_energy_kbtu / building_area_sqft

        # Return the EUI result as JSON
        return jsonify({
            "total_energy_kwh": total_energy_kwh,
            "total_energy_kbtu": total_energy_kbtu,
            "building_area_sqft": building_area_sqft,
            "eui_kbtu_per_sqft_per_year": eui
        })

    except FileNotFoundError:
        return jsonify({"error": "electric_data.csv file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
