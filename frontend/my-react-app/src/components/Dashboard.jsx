import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const Dashboard = () => {
  const [gasData, setGasData] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/api/gas-usage')
      .then((response) => response.json())
      .then((data) => {
        // Transform the data into the format required by Recharts
        const transformedData = data.map((item) => ({
          date: item.date,
          total_gas_usage: item.total_gas_usage,
          daily_avg_gas: item.daily_avg_gas,
          total_emissions_ton: item.total_emissions_ton,
        }));
        setGasData(transformedData);
      })
      .catch((error) => console.error('Error fetching gas usage data:', error));
  }, []);

  return (
    <div className="dashboard">
      <h1>Energy Monitoring Dashboard</h1>
      <section>
        <h2>Gas Usage</h2>
        <LineChart width={600} height={300} data={gasData}>
          <CartesianGrid stroke="#f5f5f5" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="total_gas_usage" stroke="#ff7300" />
          <Line type="monotone" dataKey="daily_avg_gas" stroke="#387908" />
          <Line type="monotone" dataKey="total_emissions_ton" stroke="#8884d8" />
        </LineChart>
      </section>
    </div>
  );
};

export default Dashboard;
