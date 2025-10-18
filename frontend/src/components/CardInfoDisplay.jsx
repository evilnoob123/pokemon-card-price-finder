import React from 'react';

const CardInfoDisplay = ({ cardData, isLoading, showConfirmation, onConfirm, onRetry, onNewScan, retryCount, isPSAMode }) => {
  if (isLoading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded mb-4"></div>
          <div className="h-4 bg-gray-200 rounded mb-2"></div>
          <div className="h-4 bg-gray-200 rounded mb-2"></div>
          <div className="h-4 bg-gray-200 rounded mb-4"></div>
          <div className="h-48 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (!cardData) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 text-center">
        <div className="text-gray-400 mb-4">
          <div className="text-5xl mb-3">🎴</div>
          <h3 className="text-lg font-semibold mb-2 text-gray-600">No Card Data</h3>
          <p className="text-sm text-gray-500">Scan a Pokémon card to see its information and price</p>
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
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="text-center mb-6">
        <h2 className="text-xl font-bold text-gray-900 mb-2">
          {isPSAMode ? '🏆 PSA Graded Card' : '🎴 Card Information'}
        </h2>
        <div className="flex items-center justify-center gap-2 text-sm text-gray-600">
          <div className="w-2 h-2 bg-green-500 rounded-full"></div>
          <span>{isPSAMode ? 'PSA Verified Data' : 'Verified Data'}</span>
        </div>
      </div>

      {/* Card Image */}
      {cardData.image_url && (
        <div className="mb-6">
          <img
            src={cardData.image_url}
            alt={cardData.card_name || 'Pokémon card'}
            className="w-full h-48 object-contain rounded-lg border border-gray-200 bg-gray-50"
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
        </div>
      )}

      {/* Card Details Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {/* Card Name */}
        <div className="md:col-span-2">
          <label className="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
            Card Name
          </label>
          <p className="text-lg font-bold text-gray-900">
            {cardData.card_name || 'Unknown'}
          </p>
        </div>

        {/* Set Name */}
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
            Set
          </label>
          <p className="text-sm font-medium text-gray-900">
            {cardData.set_name || 'Unknown'}
          </p>
        </div>

        {/* Rarity */}
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
            Rarity
          </label>
          <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${getRarityColor(cardData.rarity)}`}>
            {cardData.rarity || 'Unknown'}
          </span>
        </div>

        {/* Card Number */}
        {cardData.card_number && (
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
              Card Number
            </label>
            <p className="text-sm font-medium text-gray-900">
              #{cardData.card_number}
            </p>
          </div>
        )}

        {/* HP */}
        {cardData.hp && (
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
              HP
            </label>
            <p className="text-sm font-medium text-gray-900">
              {cardData.hp}
            </p>
          </div>
        )}

        {/* PSA Specific Fields */}
        {isPSAMode && (
          <>
            {/* PSA Grade */}
            {cardData.psa_grade && (
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
                  PSA Grade
                </label>
                <span className="inline-block px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm font-bold">
                  {cardData.psa_grade}
                </span>
              </div>
            )}

            {/* PSA Certificate Number */}
            {cardData.psa_cert_number && (
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
                  Certificate #
                </label>
                <p className="text-sm font-medium text-gray-900">
                  {cardData.psa_cert_number}
                </p>
              </div>
            )}

            {/* Certification Date */}
            {cardData.certification_date && (
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
                  Certified Date
                </label>
                <p className="text-sm font-medium text-gray-900">
                  {cardData.certification_date}
                </p>
              </div>
            )}

            {/* Card Condition */}
            {cardData.card_condition && (
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
                  Condition
                </label>
                <p className="text-sm font-medium text-gray-900">
                  {cardData.card_condition}
                </p>
              </div>
            )}

            {/* Year */}
            {cardData.year && (
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
                  Year
                </label>
                <p className="text-sm font-medium text-gray-900">
                  {cardData.year}
                </p>
              </div>
            )}

            {/* Total Population */}
            {cardData.total_population && (
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
                  Total Population
                </label>
                <p className="text-sm font-medium text-gray-900">
                  {cardData.total_population.toLocaleString()}
                </p>
              </div>
            )}

            {/* Population Higher */}
            {cardData.population_higher && (
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">
                  Higher Grades
                </label>
                <p className="text-sm font-medium text-gray-900">
                  {cardData.population_higher.toLocaleString()}
                </p>
              </div>
            )}
          </>
        )}
      </div>

      {/* Price Section */}
      <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg p-4 mb-6">
        <div className="text-center">
          <label className="block text-xs font-medium text-gray-500 mb-2 uppercase tracking-wide">
            Latest Market Price
          </label>
          <div className="flex items-center justify-center gap-2">
            <span className="text-3xl font-bold text-green-600">
              {formatPrice(cardData.latest_market_price)}
            </span>
            {cardData.latest_market_price && (
              <span className="text-sm text-gray-500 font-medium">
                USD
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Types */}
      {cardData.types && cardData.types.length > 0 && (
        <div className="mb-6">
          <label className="block text-xs font-medium text-gray-500 mb-2 uppercase tracking-wide">
            Types
          </label>
          <div className="flex flex-wrap gap-2">
            {cardData.types.map((type, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
              >
                {type}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Last Updated */}
      <div className="pt-4 border-t border-gray-200">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>Last updated: {new Date().toLocaleString()}</span>
          <div className="flex items-center gap-1">
            <div className="w-1.5 h-1.5 bg-green-500 rounded-full"></div>
            <span>Live Data</span>
          </div>
        </div>
      </div>

      {/* Confirmation Dialog */}
      {showConfirmation && (
        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="text-center">
            <div className="text-blue-600 text-2xl mb-2">🤔</div>
            <h3 className="text-lg font-semibold text-blue-900 mb-2">
              Is this the correct card?
            </h3>
            <p className="text-sm text-blue-700 mb-4">
              We found: <strong>{cardData.card_name}</strong> from {cardData.set_name}
              {retryCount > 0 && (
                <span className="block mt-1 text-xs text-blue-600">
                  (Attempt {retryCount + 1})
                </span>
              )}
            </p>
            
            <div className="flex gap-3 justify-center">
              <button
                onClick={onConfirm}
                className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors font-medium text-sm flex items-center gap-2"
              >
                ✅ Yes, this is correct
              </button>
              
              <button
                onClick={onRetry}
                className="bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600 transition-colors font-medium text-sm flex items-center gap-2"
              >
                🔄 Try different card
              </button>
              
              <button
                onClick={onNewScan}
                className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600 transition-colors font-medium text-sm flex items-center gap-2"
              >
                📷 Scan new image
              </button>
            </div>
            
            <p className="text-xs text-blue-600 mt-3">
              If this isn't the right card, we'll try to find the next closest match
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default CardInfoDisplay;