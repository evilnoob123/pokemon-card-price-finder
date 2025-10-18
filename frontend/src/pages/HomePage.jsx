import React, { useState } from 'react';
import CardCapture from '../components/CardCapture';
import CardInfoDisplay from '../components/CardInfoDisplay';
import PriceChart from '../components/PriceChart';

const HomePage = () => {
  const [cardData, setCardData] = useState(null);
  const [priceHistory, setPriceHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageCapture = async (imageFile) => {
    setIsLoading(true);
    setError(null);
    setCardData(null);
    setPriceHistory([]);

    try {
      const formData = new FormData();
      formData.append('image', imageFile);

      const apiUrl = process.env.REACT_APP_API_URL || 'https://pokemoncardpricefinder.onrender.com';
      const response = await fetch(`${apiUrl}/api/card/scan`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      if (result.error) {
        throw new Error(result.error);
      }

      setCardData(result);
      
      // Generate mock price history for demonstration
      if (result.card_name) {
        const mockPriceHistory = generateMockPriceHistory(result.latest_market_price);
        setPriceHistory(mockPriceHistory);
      }
    } catch (err) {
      console.error('Error scanning card:', err);
      setError(err.message || 'Failed to scan card');
    } finally {
      setIsLoading(false);
    }
  };

  // Generate mock price history for demonstration
  const generateMockPriceHistory = (currentPrice) => {
    if (!currentPrice) return [];
    
    const history = [];
    const basePrice = parseFloat(currentPrice);
    const days = 30;
    
    for (let i = days; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      
      // Generate realistic price fluctuations
      const variation = (Math.random() - 0.5) * 0.2; // ±10% variation
      const price = basePrice * (1 + variation);
      
      history.push({
        date: date.toISOString().split('T')[0],
        price: Math.max(0.01, price).toFixed(2)
      });
    }
    
    return history;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-center">
            <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-2">
              🎴 Pokémon Card Price Finder
            </h1>
          </div>
          <p className="text-center text-gray-600 mt-2">
            Scan your Pokémon cards to find their current market value
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Card Capture */}
          <div className="space-y-8">
            <CardCapture 
              onImageCapture={handleImageCapture}
              isLoading={isLoading}
            />
            
            {/* Error Display */}
            {error && (
              <div className="w-full max-w-md mx-auto p-4 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex items-center gap-2">
                  <span className="text-red-500 text-xl">⚠️</span>
                  <div>
                    <h3 className="font-semibold text-red-800">Scan Error</h3>
                    <p className="text-red-700 text-sm">{error}</p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Right Column - Card Info and Price Chart */}
          <div className="space-y-8">
            <CardInfoDisplay 
              cardData={cardData}
              isLoading={isLoading}
            />
            
            <PriceChart 
              priceHistory={priceHistory}
              isLoading={isLoading}
            />
          </div>
        </div>

        {/* Features Section */}
        <div className="mt-16 bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-center mb-8 text-gray-800">
            🚀 Features
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-4xl mb-4">📸</div>
              <h3 className="text-lg font-semibold mb-2">Easy Capture</h3>
              <p className="text-gray-600 text-sm">
                Upload images or use your camera to capture Pokémon cards
              </p>
            </div>
            <div className="text-center">
              <div className="text-4xl mb-4">🔍</div>
              <h3 className="text-lg font-semibold mb-2">Smart Recognition</h3>
              <p className="text-gray-600 text-sm">
                Advanced OCR technology identifies card names and details
              </p>
            </div>
            <div className="text-center">
              <div className="text-4xl mb-4">💰</div>
              <h3 className="text-lg font-semibold mb-2">Real-time Prices</h3>
              <p className="text-gray-600 text-sm">
                Get current market prices and historical price trends
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-gray-300">
            Pokémon Card Price Finder - Built with React, FastAPI, and ❤️
          </p>
          <p className="text-gray-400 text-sm mt-2">
            Data provided by Pokémon TCG API
          </p>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;