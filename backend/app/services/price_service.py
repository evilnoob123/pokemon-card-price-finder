import aiohttp
import asyncio
import logging
import os
from typing import Optional, Dict, Any
import json

logger = logging.getLogger(__name__)

class PriceService:
    def __init__(self):
        """Initialize price service with Pokémon TCG API configuration."""
        self.api_key = os.getenv('POKEMON_TCG_API_KEY', '')
        self.base_url = 'https://api.pokemontcg.io/v2'
        self.headers = {
            'X-Api-Key': self.api_key
        } if self.api_key else {}
        
        logger.info(f"Price service initialized with API key: {'Yes' if self.api_key else 'No'}")
    
    async def get_card_info(self, card_name: str) -> Optional[Dict[str, Any]]:
        """
        Get Pokémon card information and current market price.
        
        Args:
            card_name: Name of the Pokémon card
            
        Returns:
            Dictionary with card information and price data
        """
        try:
            # Search for the card
            card_data = await self._search_card(card_name)
            
            if not card_data:
                return None
            
            # Get price information
            price_data = await self._get_card_price(card_data.get('id'))
            
            # Combine card data with price information
            result = {
                'card_name': card_data.get('name'),
                'set_name': card_data.get('set', {}).get('name'),
                'rarity': card_data.get('rarity'),
                'image_url': card_data.get('images', {}).get('large'),
                'card_number': card_data.get('number'),
                'hp': card_data.get('hp'),
                'types': card_data.get('types', []),
                'latest_market_price': price_data.get('latest_price') if price_data else None,
                'price_history': price_data.get('price_history', []) if price_data else []
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting card info for {card_name}: {e}")
            return None
    
    async def _search_card(self, card_name: str) -> Optional[Dict[str, Any]]:
        """
        Search for a card by name using Pokémon TCG API.
        
        Args:
            card_name: Name of the card to search for
            
        Returns:
            Card data dictionary or None
        """
        try:
            # Clean card name for search
            search_name = self._clean_card_name(card_name)
            
            async with aiohttp.ClientSession() as session:
                # Try exact match first
                url = f"{self.base_url}/cards"
                params = {
                    'q': f'name:"{search_name}"',
                    'pageSize': 1
                }
                
                async with session.get(url, params=params, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        cards = data.get('data', [])
                        
                        if cards:
                            logger.info(f"Found exact match for: {search_name}")
                            return cards[0]
                
                # Try fuzzy search if exact match fails
                params = {
                    'q': f'name:{search_name}',
                    'pageSize': 5
                }
                
                async with session.get(url, params=params, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        cards = data.get('data', [])
                        
                        if cards:
                            # Find the best match
                            best_match = self._find_best_match(cards, search_name)
                            if best_match:
                                logger.info(f"Found fuzzy match for: {search_name}")
                                return best_match
                
                logger.warning(f"No card found for: {search_name}")
                return None
                
        except Exception as e:
            logger.error(f"Error searching for card {card_name}: {e}")
            return None
    
    def _clean_card_name(self, card_name: str) -> str:
        """
        Clean card name for API search.
        
        Args:
            card_name: Raw card name
            
        Returns:
            Cleaned card name
        """
        # Remove common suffixes and clean up
        cleaned = card_name.strip()
        
        # Remove common card suffixes
        suffixes_to_remove = [
            ' V', ' VMAX', ' VSTAR', ' EX', ' GX', ' BREAK',
            ' Prime', ' LV.X', ' SP', ' LEGEND', ' LEGENDARY'
        ]
        
        for suffix in suffixes_to_remove:
            if cleaned.endswith(suffix):
                cleaned = cleaned[:-len(suffix)]
                break
        
        return cleaned
    
    def _find_best_match(self, cards: list, search_name: str) -> Optional[Dict[str, Any]]:
        """
        Find the best matching card from search results.
        
        Args:
            cards: List of card dictionaries
            search_name: Original search name
            
        Returns:
            Best matching card or None
        """
        if not cards:
            return None
        
        # Simple scoring based on name similarity
        best_card = None
        best_score = 0
        
        for card in cards:
            card_name = card.get('name', '').lower()
            search_lower = search_name.lower()
            
            # Calculate similarity score
            score = 0
            
            # Exact match gets highest score
            if card_name == search_lower:
                score = 100
            # Partial match gets medium score
            elif search_lower in card_name or card_name in search_lower:
                score = 50
            # Word overlap gets lower score
            else:
                search_words = set(search_lower.split())
                card_words = set(card_name.split())
                overlap = len(search_words.intersection(card_words))
                score = overlap * 10
            
            if score > best_score:
                best_score = score
                best_card = card
        
        return best_card if best_score > 20 else None
    
    async def _get_card_price(self, card_id: str) -> Optional[Dict[str, Any]]:
        """
        Get current market price for a card.
        
        Args:
            card_id: Pokémon TCG API card ID
            
        Returns:
            Price data dictionary or None
        """
        try:
            # For demo purposes, we'll simulate price data
            # In a real implementation, you would integrate with price APIs like:
            # - TCGPlayer API
            # - eBay API
            # - CardMarket API
            
            if not card_id:
                return None
            
            # Simulate price data
            import random
            base_price = random.uniform(0.50, 50.00)
            
            price_data = {
                'latest_price': round(base_price, 2),
                'price_history': self._generate_mock_price_history(base_price)
            }
            
            logger.info(f"Generated price data for card {card_id}: ${price_data['latest_price']}")
            return price_data
            
        except Exception as e:
            logger.error(f"Error getting price for card {card_id}: {e}")
            return None
    
    def _generate_mock_price_history(self, base_price: float) -> list:
        """
        Generate mock price history for demonstration.
        
        Args:
            base_price: Base price to generate history around
            
        Returns:
            List of price history entries
        """
        import random
        from datetime import datetime, timedelta
        
        history = []
        current_price = base_price
        
        for i in range(30):  # 30 days of history
            date = datetime.now() - timedelta(days=30-i)
            
            # Generate realistic price movement
            change_percent = random.uniform(-0.1, 0.1)  # ±10% daily change
            current_price *= (1 + change_percent)
            
            history.append({
                'date': date.strftime('%Y-%m-%d'),
                'price': round(max(0.01, current_price), 2)
            })
        
        return history
    
    async def get_card_sets(self) -> list:
        """
        Get list of all Pokémon card sets.
        
        Returns:
            List of card sets
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/sets"
                
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('data', [])
                    
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting card sets: {e}")
            return []
