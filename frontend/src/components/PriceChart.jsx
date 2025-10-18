import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const PriceChart = ({ priceHistory, isLoading }) => {
  if (isLoading) {
    return (
      <div className="w-full max-w-2xl mx-auto p-6 bg-white rounded-xl shadow-lg">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded mb-4"></div>
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (!priceHistory || priceHistory.length === 0) {
    return (
      <div className="w-full max-w-2xl mx-auto p-6 bg-white rounded-xl shadow-lg text-center">
        <div className="text-gray-500 mb-4">
          <div className="text-6xl mb-2">📈</div>
          <h3 className="text-xl font-semibold mb-2">No Price History</h3>
          <p className="text-sm">Price history will appear here after scanning a card</p>
        </div>
      </div>
    );
  }

  // Format data for the chart
  const chartData = priceHistory.map((entry, index) => ({
    date: new Date(entry.date).toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric' 
    }),
    price: parseFloat(entry.price),
    fullDate: entry.date
  }));

  // Calculate price change
  const firstPrice = chartData[0]?.price || 0;
  const lastPrice = chartData[chartData.length - 1]?.price || 0;
  const priceChange = lastPrice - firstPrice;
  const priceChangePercent = firstPrice > 0 ? ((priceChange / firstPrice) * 100) : 0;

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium">{`Date: ${label}`}</p>
          <p className="text-green-600 font-semibold">
            {`Price: $${payload[0].value.toFixed(2)}`}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-6 bg-white rounded-xl shadow-lg">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-center mb-2 text-gray-800">
          📈 Price History
        </h2>
        
        {/* Price Change Summary */}
        <div className="flex justify-center items-center gap-4 mb-4">
          <div className="text-center">
            <p className="text-sm text-gray-600">Current Price</p>
            <p className="text-xl font-bold text-gray-900">
              ${lastPrice.toFixed(2)}
            </p>
          </div>
          
          <div className="text-center">
            <p className="text-sm text-gray-600">Change</p>
            <p className={`text-lg font-semibold ${
              priceChange >= 0 ? 'text-green-600' : 'text-red-600'
            }`}>
              {priceChange >= 0 ? '+' : ''}${priceChange.toFixed(2)}
            </p>
          </div>
          
          <div className="text-center">
            <p className="text-sm text-gray-600">Change %</p>
            <p className={`text-lg font-semibold ${
              priceChangePercent >= 0 ? 'text-green-600' : 'text-red-600'
            }`}>
              {priceChangePercent >= 0 ? '+' : ''}{priceChangePercent.toFixed(1)}%
            </p>
          </div>
        </div>
      </div>

      {/* Chart */}
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis 
              dataKey="date" 
              stroke="#6b7280"
              fontSize={12}
            />
            <YAxis 
              stroke="#6b7280"
              fontSize={12}
              tickFormatter={(value) => `$${value.toFixed(0)}`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Line 
              type="monotone" 
              dataKey="price" 
              stroke="#10b981" 
              strokeWidth={2}
              dot={{ fill: '#10b981', strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6, stroke: '#10b981', strokeWidth: 2 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Chart Info */}
      <div className="mt-4 text-center">
        <p className="text-xs text-gray-500">
          Showing {chartData.length} data points
        </p>
        <p className="text-xs text-gray-500">
          Data range: {chartData[0]?.fullDate} to {chartData[chartData.length - 1]?.fullDate}
        </p>
      </div>
    </div>
  );
};

export default PriceChart;
