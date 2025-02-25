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

if __name__ == '__main__':
    app.run(debug=True)
