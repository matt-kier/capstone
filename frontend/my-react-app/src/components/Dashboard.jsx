import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
  const [gasData, setGasData] = useState([]);
  const [energyData, setEnergyData] = useState([]);
  const [gasMultiplier, setGasMultiplier] = useState(1);
  const [energyMultiplier, setEnergyMultiplier] = useState(1);

  useEffect(() => {
    // Fetch gas usage data
    fetch('http://localhost:5000/api/gas-usage')
      .then((response) => response.json())
      .then((data) => setGasData(data))
      .catch((error) => console.error('Error fetching gas usage data:', error));

    // Fetch energy baseline data
    fetch('http://localhost:5000/api/energy-baseline')
      .then((response) => response.json())
      .then((data) => setEnergyData(data.data))
      .catch((error) => console.error('Error fetching energy baseline data:', error));
  }, []);

  // Adjust data based on slider values
  const adjustedGasData = gasData.map((item) => ({
    ...item,
    total_gas_usage: item.total_gas_usage * gasMultiplier,
    daily_avg_gas: item.daily_avg_gas * gasMultiplier,
    total_emissions_ton: item.total_emissions_ton * gasMultiplier,
  }));

  const adjustedEnergyData = energyData.map((item) => ({
    ...item,
    total_kwh: item.total_kwh * energyMultiplier,
    daily_avg_kwh: item.daily_avg_kwh * energyMultiplier,
  }));

  return (
    <div className="dashboard">
      <h1>Energy Monitoring Dashboard</h1>

      {/* Gas Usage Section */}
      <section>
        <h2>Gas Usage</h2>
        <label>
          Adjust Gas Usage:
          <input
            type="range"
            min="0.5"
            max="1.5"
            step="0.01"
            value={gasMultiplier}
            onChange={(e) => setGasMultiplier(parseFloat(e.target.value))}
          />
          {gasMultiplier.toFixed(2)}
        </label>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={adjustedGasData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="total_gas_usage" stroke="#ff7300" />
            <Line type="monotone" dataKey="daily_avg_gas" stroke="#387908" />
            <Line type="monotone" dataKey="total_emissions_ton" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      </section>

      {/* Energy Baseline Section */}
      <section>
        <h2>Energy Baseline</h2>
        <label>
          Adjust Energy Usage:
          <input
            type="range"
            min="0.5"
            max="1.5"
            step="0.01"
            value={energyMultiplier}
            onChange={(e) => setEnergyMultiplier(parseFloat(e.target.value))}
          />
          {energyMultiplier.toFixed(2)}
        </label>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={adjustedEnergyData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="total_kwh" stroke="#8884d8" />
            <Line type="monotone" dataKey="daily_avg_kwh" stroke="#82ca9d" />
          </LineChart>
        </ResponsiveContainer>
      </section>
    </div>
  );
};

export default Dashboard;
