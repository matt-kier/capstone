import React, { useState, useEffect } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const months = [
  'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
];

const Dashboard = () => {
  const [gasData, setGasData] = useState([]);
  const [energyData, setEnergyData] = useState([]);
  const [gasMultiplier, setGasMultiplier] = useState(1);
  const [energyMultiplier, setEnergyMultiplier] = useState(1);
  const [selectedMonths, setSelectedMonths] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/api/gas-usage')
      .then((res) => res.json())
      .then((data) => setGasData(data))
      .catch((err) => console.error('Gas error:', err));

    fetch('http://localhost:5000/api/energy-baseline')
      .then((res) => res.json())
      .then((data) => setEnergyData(data.data))
      .catch((err) => console.error('Energy error:', err));
  }, []);

  const isMonthSelected = (date) => {
    const month = new Date(date).getMonth();
    return selectedMonths.includes(month);
  };

  const getAverage = (data, key) =>
    data.reduce((sum, item) => sum + item[key], 0) / data.length;

  const gasAverage = getAverage(gasData, 'total_gas_usage') || 0;
  const energyAverage = getAverage(energyData, 'total_kwh') || 0;

  const adjustedGasData = gasData.map((item) => {
    const adjustedValue = isMonthSelected(item.date)
      ? item.total_gas_usage * gasMultiplier
      : item.total_gas_usage;
    const color =
      adjustedValue > gasAverage
        ? `rgba(255, 0, 0, ${Math.min((adjustedValue - gasAverage) / gasAverage, 1)})`
        : `rgba(0, 200, 0, ${Math.min((gasAverage - adjustedValue) / gasAverage, 1)})`;
    return {
      ...item,
      total_gas_usage: adjustedValue,
      daily_avg_gas: isMonthSelected(item.date) ? item.daily_avg_gas * gasMultiplier : item.daily_avg_gas,
      total_emissions_ton: isMonthSelected(item.date) ? item.total_emissions_ton * gasMultiplier : item.total_emissions_ton,
      avg_usage: gasAverage,
      strokeColor: color,
    };
  });

  const adjustedEnergyData = energyData.map((item) => {
    const adjustedValue = isMonthSelected(item.date)
      ? item.total_kwh * energyMultiplier
      : item.total_kwh;
    const color =
      adjustedValue > energyAverage
        ? `rgba(255, 0, 0, ${Math.min((adjustedValue - energyAverage) / energyAverage, 1)})`
        : `rgba(0, 200, 0, ${Math.min((energyAverage - adjustedValue) / energyAverage, 1)})`;
    return {
      ...item,
      total_kwh: adjustedValue,
      daily_avg_kwh: isMonthSelected(item.date) ? item.daily_avg_kwh * energyMultiplier : item.daily_avg_kwh,
      avg_usage: energyAverage,
      strokeColor: color,
    };
  });

  const handleMonthSelect = (e) => {
    const value = parseInt(e.target.value);
    setSelectedMonths((prev) =>
      prev.includes(value) ? prev.filter((m) => m !== value) : [...prev, value]
    );
  };

  return (
    <div className="dashboard">
      {/* Logo at the top left */}
      <div className="logo-container">
        <img src="/pied.png" alt="Piedmont Hospital Logo" className="logo" />
      </div>

      <h1 className="dashboard-title">Energy Monitoring Dashboard</h1>

      <div className="dashboard-container">
        <div className="month-selector">
          <h3>Select Months to Adjust:</h3>
          <div className="month-grid">
            {months.map((m, i) => (
              <label key={i}>
                <input
                  type="checkbox"
                  value={i}
                  checked={selectedMonths.includes(i)}
                  onChange={handleMonthSelect}
                />
                {m}
              </label>
            ))}
          </div>
        </div>

        <div className="graph-section">
          {/* Gas and Energy Graphs Section */}
          <section className="card">
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
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={adjustedGasData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="total_gas_usage"
                  stroke="#ff7300"
                  strokeWidth={2}
                />
                <Line type="monotone" dataKey="daily_avg_gas" stroke="#387908" />
                <Line type="monotone" dataKey="total_emissions_ton" stroke="#8884d8" />
                <Line
                  type="monotone"
                  dataKey="avg_usage"
                  stroke="#00bcd4"
                  strokeDasharray="5 5"
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </section>

          <section className="card">
            <h2>Electricity Usage</h2>
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
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={adjustedEnergyData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="total_kwh"
                  stroke="#ff4081"
                  strokeWidth={2}
                />
                <Line type="monotone" dataKey="daily_avg_kwh" stroke="#82ca9d" />
                <Line
                  type="monotone"
                  dataKey="avg_usage"
                  stroke="#00bcd4"
                  strokeDasharray="5 5"
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </section>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
