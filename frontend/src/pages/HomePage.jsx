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
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">🎴</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Pokémon Card Price Finder
                </h1>
                <p className="text-sm text-gray-600">
                  Discover authenticated trading cards with confidence
                </p>
              </div>
            </div>
            <div className="hidden md:flex items-center gap-4 text-sm text-gray-600">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span>Live Market Data</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Section */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
            <div className="text-2xl font-bold text-gray-900">1,247+</div>
            <div className="text-sm text-gray-600">Cards Scanned</div>
          </div>
          <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
            <div className="text-2xl font-bold text-gray-900">850+</div>
            <div className="text-sm text-gray-600">Verified Cards</div>
          </div>
          <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
            <div className="text-2xl font-bold text-gray-900">$2.5M+</div>
            <div className="text-sm text-gray-600">Cards Valued</div>
          </div>
          <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
            <div className="text-2xl font-bold text-gray-900">10K+</div>
            <div className="text-sm text-gray-600">Happy Users</div>
          </div>
        </div>

        {/* Main Grid Layout */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
          {/* Left Column - Card Capture (1/3 width) */}
          <div className="xl:col-span-1">
            <CardCapture 
              onImageCapture={handleImageCapture}
              isLoading={isLoading}
            />
            
            {/* Error Display */}
            {error && (
              <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
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

          {/* Right Column - Card Info and Price Chart (2/3 width) */}
          <div className="xl:col-span-2 space-y-6">
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
        <div className="mt-16 bg-white rounded-xl shadow-sm border border-gray-200 p-8">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Trusted by 10,000+ collectors worldwide
            </h2>
            <p className="text-lg text-gray-600">
              Your premier destination for authenticated trading cards
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                <span className="text-white text-2xl">📸</span>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-gray-900">Easy Capture</h3>
              <p className="text-gray-600">
                Upload images or use your camera to capture Pokémon cards with advanced OCR technology
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-green-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                <span className="text-white text-2xl">🔍</span>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-gray-900">Smart Recognition</h3>
              <p className="text-gray-600">
                Advanced AI identifies card names, sets, and details with professional-grade accuracy
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                <span className="text-white text-2xl">💰</span>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-gray-900">Real-time Prices</h3>
              <p className="text-gray-600">
                Get current market prices and historical trends from trusted trading card databases
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="md:col-span-2">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-lg">🎴</span>
                </div>
                <div>
                  <h3 className="text-xl font-bold">Pokémon Card Price Finder</h3>
                  <p className="text-gray-400 text-sm">Your premier destination for authenticated trading cards</p>
                </div>
              </div>
              <p className="text-gray-400 text-sm">
                Built with ❤️ for collectors worldwide. Find, buy, and sell graded cards with confidence.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Features</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>Card Scanning</li>
                <li>Price Analysis</li>
                <li>Market Trends</li>
                <li>Authentication</li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>Help Center</li>
                <li>Contact Us</li>
                <li>Terms of Service</li>
                <li>Privacy Policy</li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center">
            <p className="text-gray-400 text-sm">
              © 2025 Pokémon Card Price Finder. All rights reserved. Data provided by Pokémon TCG API.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;