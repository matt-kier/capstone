import React, { useState, useEffect } from 'react';

const Dashboard = () => {
    const [gasData, setGasData] = useState({});

    useEffect(() => {
        fetch('/api/gas-usage')
            .then(response => response.json())
            .then(data => setGasData(data))
            .catch(error => console.error('Error fetching gas usage data:', error));
    }, []);

    return (
        <div className="dashboard">
            <h1>Energy Monitoring Dashboard</h1>

            <section>
                <h2>Gas Usage</h2>
                <p>Total Gas Usage: {gasData.total_gas_usage_CCF} CCF</p>
                <p>Average Gas Usage: {gasData.avg_gas_usage_CCF} CCF</p>
                <p>CO₂ Emissions: {gasData.total_emissions_ton} metric tons</p>
            </section>
        </div>
    );
};

export default Dashboard;
