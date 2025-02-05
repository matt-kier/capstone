// Import necessary libraries and components
import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';

// Function to fetch data from API
const fetchData = async (endpoint) => {
    const response = await fetch(endpoint);
    return await response.json();
};

// Main Dashboard component
const Dashboard = () => {
    // React state variables to store API data
    const [energyData, setEnergyData] = useState({});
    const [gasData, setGasData] = useState({});
    const [intensityMetrics, setIntensityMetrics] = useState({});

    // Fetch data from Flask API on component mount
    useEffect(() => {
        // Fetch energy baseline data
        fetchData('/api/energy-baseline').then(data => setEnergyData(data));
        
        // Fetch gas usage data
        fetchData('/api/gas-usage').then(data => setGasData(data));
        
        // Fetch intensity metrics data
        fetchData('/api/intensity-metrics').then(data => setIntensityMetrics(data));
    }, []);

    // Render charts using Chart.js for each data metric

    return (
        <div className="dashboard">
            <h1>Energy Monitoring Dashboard</h1>

            <section>
                <h2>Energy Baseline</h2>
                <p>30-Day Energy Consumption: {energyData.total_30_day_usage} kWh</p>
            </section>

            <section>
                <h2>Gas Usage</h2>
                <p>Total Monthly Gas Usage: {gasData.total_gas_usage} CFH</p>
                <p>CO₂ Emissions: {gasData.total_emissions_ton} metric tons</p>
            </section>

            <section>
                <h2>Intensity Metrics</h2>
                <p>Energy Use Intensity (EUI): {intensityMetrics.eui} kBtu/ft²</p>
                <p>Water Use Intensity (WUI): {intensityMetrics.wui} gal/ft²</p>
            </section>
        </div>
    );
};

// Export the Dashboard component
export default Dashboard;
