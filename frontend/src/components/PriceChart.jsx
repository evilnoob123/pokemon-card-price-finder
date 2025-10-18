import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const PriceChart = ({ priceHistory, isLoading, isPSAMode }) => {
  if (isLoading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded mb-4"></div>
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (!priceHistory || priceHistory.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 text-center">
        <div className="text-gray-400 mb-4">
          <div className="text-5xl mb-3">📈</div>
          <h3 className="text-lg font-semibold mb-2 text-gray-600">No Price History</h3>
          <p className="text-sm text-gray-500">Price history will appear here after scanning a card</p>
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
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="text-center mb-6">
        <h2 className="text-xl font-bold text-gray-900 mb-2">
          {isPSAMode ? '🏆 PSA Sales History' : '📈 Price History'}
        </h2>
        <div className="flex items-center justify-center gap-2 text-sm text-gray-600">
          <div className="w-2 h-2 bg-green-500 rounded-full"></div>
          <span>{isPSAMode ? 'PSA Sales Data' : 'Live Market Data'}</span>
        </div>
      </div>
      
      {/* Price Change Summary */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <p className="text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">Current Price</p>
          <p className="text-lg font-bold text-gray-900">
            ${lastPrice.toFixed(2)}
          </p>
        </div>
        
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <p className="text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">Change</p>
          <p className={`text-lg font-bold ${
            priceChange >= 0 ? 'text-green-600' : 'text-red-600'
          }`}>
            {priceChange >= 0 ? '+' : ''}${priceChange.toFixed(2)}
          </p>
        </div>
        
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <p className="text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">Change %</p>
          <p className={`text-lg font-bold ${
            priceChangePercent >= 0 ? 'text-green-600' : 'text-red-600'
          }`}>
            {priceChangePercent >= 0 ? '+' : ''}{priceChangePercent.toFixed(1)}%
          </p>
        </div>
      </div>

      {/* Chart */}
      <div className="h-64 mb-4">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
            <XAxis 
              dataKey="date" 
              stroke="#9ca3af"
              fontSize={11}
              tickLine={false}
              axisLine={false}
            />
            <YAxis 
              stroke="#9ca3af"
              fontSize={11}
              tickFormatter={(value) => `$${value.toFixed(0)}`}
              tickLine={false}
              axisLine={false}
            />
            <Tooltip content={<CustomTooltip />} />
            <Line 
              type="monotone" 
              dataKey="price" 
              stroke="#10b981" 
              strokeWidth={3}
              dot={{ fill: '#10b981', strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6, stroke: '#10b981', strokeWidth: 2, fill: '#fff' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Chart Info */}
      <div className="pt-4 border-t border-gray-200">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>Showing {chartData.length} data points</span>
          <div className="flex items-center gap-1">
            <div className="w-1.5 h-1.5 bg-green-500 rounded-full"></div>
            <span>Live Data</span>
          </div>
        </div>
        <p className="text-xs text-gray-500 mt-1">
          Data range: {chartData[0]?.fullDate} to {chartData[chartData.length - 1]?.fullDate}
        </p>
      </div>
    </div>
  );
};

export default PriceChart;