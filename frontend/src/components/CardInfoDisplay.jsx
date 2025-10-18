import React from 'react';

const CardInfoDisplay = ({ cardData, isLoading }) => {
  if (isLoading) {
    return (
      <div className="w-full max-w-md mx-auto p-6 bg-white rounded-xl shadow-lg">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded mb-4"></div>
          <div className="h-4 bg-gray-200 rounded mb-2"></div>
          <div className="h-4 bg-gray-200 rounded mb-2"></div>
          <div className="h-4 bg-gray-200 rounded mb-4"></div>
          <div className="h-32 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (!cardData) {
    return (
      <div className="w-full max-w-md mx-auto p-6 bg-white rounded-xl shadow-lg text-center">
        <div className="text-gray-500 mb-4">
          <div className="text-6xl mb-2">🎴</div>
          <h3 className="text-xl font-semibold mb-2">No Card Data</h3>
          <p className="text-sm">Scan a Pokémon card to see its information and price</p>
        </div>
      </div>
    );
  }

  const formatPrice = (price) => {
    if (!price) return 'N/A';
    return `$${parseFloat(price).toFixed(2)}`;
  };

  const getRarityColor = (rarity) => {
    const rarityColors = {
      'Common': 'bg-gray-100 text-gray-800',
      'Uncommon': 'bg-green-100 text-green-800',
      'Rare': 'bg-blue-100 text-blue-800',
      'Rare Holo': 'bg-purple-100 text-purple-800',
      'Rare Ultra': 'bg-yellow-100 text-yellow-800',
      'Rare Secret': 'bg-red-100 text-red-800',
      'Promo': 'bg-pink-100 text-pink-800'
    };
    return rarityColors[rarity] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="w-full max-w-md mx-auto p-6 bg-white rounded-xl shadow-lg">
      <h2 className="text-2xl font-bold text-center mb-6 text-gray-800">
        🎴 Card Information
      </h2>

      {/* Card Image */}
      {cardData.image_url && (
        <div className="mb-6">
          <img
            src={cardData.image_url}
            alt={cardData.card_name || 'Pokémon card'}
            className="w-full h-64 object-contain rounded-lg border-2 border-gray-200 bg-gray-50"
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
        </div>
      )}

      {/* Card Details */}
      <div className="space-y-4">
        {/* Card Name */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Card Name
          </label>
          <p className="text-lg font-semibold text-gray-900">
            {cardData.card_name || 'Unknown'}
          </p>
        </div>

        {/* Set Name */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Set
          </label>
          <p className="text-gray-900">
            {cardData.set_name || 'Unknown'}
          </p>
        </div>

        {/* Rarity */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Rarity
          </label>
          <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getRarityColor(cardData.rarity)}`}>
            {cardData.rarity || 'Unknown'}
          </span>
        </div>

        {/* Latest Price */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Latest Market Price
          </label>
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold text-green-600">
              {formatPrice(cardData.latest_market_price)}
            </span>
            {cardData.latest_market_price && (
              <span className="text-sm text-gray-500">
                USD
              </span>
            )}
          </div>
        </div>

        {/* Additional Info */}
        {cardData.card_number && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Card Number
            </label>
            <p className="text-gray-900">
              {cardData.card_number}
            </p>
          </div>
        )}

        {cardData.hp && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              HP
            </label>
            <p className="text-gray-900">
              {cardData.hp}
            </p>
          </div>
        )}

        {cardData.types && cardData.types.length > 0 && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Types
            </label>
            <div className="flex flex-wrap gap-2">
              {cardData.types.map((type, index) => (
                <span
                  key={index}
                  className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm"
                >
                  {type}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Last Updated */}
      <div className="mt-6 pt-4 border-t border-gray-200">
        <p className="text-xs text-gray-500 text-center">
          Last updated: {new Date().toLocaleString()}
        </p>
      </div>
    </div>
  );
};

export default CardInfoDisplay;