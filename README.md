# Pokémon Card Price Finder

A full-stack web application that allows users to scan Pokémon cards using their camera or upload images, then automatically identifies the card and fetches its current market price and historical data.

## 🚀 Features

- **📸 Card Capture**: Upload images or use camera to capture Pokémon cards
- **🔍 Smart Recognition**: OCR technology extracts card names from images
- **💰 Real-time Prices**: Get current market prices from Pokémon TCG API
- **📈 Price History**: View historical price trends with interactive charts
- **📱 Mobile Responsive**: Optimized for mobile devices
- **🤖 ML Integration**: Optional machine learning model for card recognition

## 🏗️ Project Structure

```
pokemon-card-price-finder/
├── frontend/                    # React frontend application
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── CardCapture.jsx      # Image capture component
│   │   │   ├── CardInfoDisplay.jsx  # Card information display
│   │   │   └── PriceChart.jsx       # Price history chart
│   │   ├── pages/
│   │   │   └── HomePage.jsx         # Main page component
│   │   ├── App.jsx                  # Root component
│   │   ├── index.jsx                # Entry point
│   │   └── styles.css               # Global styles
│   ├── package.json
│   └── tailwind.config.js
├── backend/                     # FastAPI backend application
│   ├── app/
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── routes/
│   │   │   └── card_scan.py        # Card scanning endpoints
│   │   ├── services/
│   │   │   ├── ocr_service.py      # OCR text extraction
│   │   │   └── price_service.py    # Price data fetching
│   │   └── models/
│   │       └── card_model.py        # ML model integration
│   ├── requirements.txt
│   └── .env
├── ml_model/                   # Machine learning model (optional)
│   ├── data/
│   │   └── images/               # Training images by class
│   ├── model/                    # Saved model files
│   └── train.py                  # Model training script
└── README.md
```

## 🛠️ Technology Stack

### Frontend

- **React 18** - UI framework
- **TailwindCSS** - Styling
- **Recharts** - Data visualization
- **JavaScript/JSX** - Programming language

### Backend

- **FastAPI** - Web framework
- **Python 3.8+** - Programming language
- **Pytesseract** - OCR text extraction
- **Pillow** - Image processing
- **aiohttp** - Async HTTP client

### Machine Learning (Optional)

- **TensorFlow** - Deep learning framework
- **scikit-learn** - Machine learning utilities
- **OpenCV** - Computer vision

## 📋 Prerequisites

- Node.js 16+ and npm
- Python 3.8+
- Tesseract OCR
- Pokémon TCG API key (optional)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd pokemon-card-price-finder
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file with your API keys

# Run the backend server
python app/main.py
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000`

### 4. Optional: ML Model Setup

```bash
# Navigate to ml_model directory
cd ml_model

# Create data directory structure
mkdir -p data/images/{Pikachu,Charizard,Blastoise,Venusaur}

# Add training images to respective class folders
# Run training script
python train.py
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Pokémon TCG API Configuration
POKEMON_TCG_API_KEY=your_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# OCR Configuration
TESSERACT_CMD=/usr/bin/tesseract

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Tesseract OCR Installation

**Windows:**

1. Download Tesseract from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install and add to PATH
3. Update `TESSERACT_CMD` in `.env`

**macOS:**

```bash
brew install tesseract
```

**Linux:**

```bash
sudo apt-get install tesseract-ocr
```

## 📱 Usage

1. **Open the application** in your web browser
2. **Capture a card** by either:
   - Uploading an image file
   - Using your device's camera
3. **Wait for processing** - the app will extract the card name using OCR
4. **View results** - see card information, current price, and historical data
5. **Explore price trends** - interact with the price history chart

## 🔌 API Endpoints

### POST `/api/card/scan`

Scan a Pokémon card image and return card information.

**Request:**

- `multipart/form-data` with `image` field

**Response:**

```json
{
  "card_name": "Pikachu",
  "set_name": "Base Set",
  "rarity": "Common",
  "image_url": "https://images.pokemontcg.io/base1/58_hires.png",
  "card_number": "58",
  "hp": "40",
  "types": ["Lightning"],
  "latest_market_price": 2.50,
  "price_history": [...]
}
```

### GET `/api/card/search/{card_name}`

Search for a card by name.

**Response:**
Same as scan endpoint.

## 🚀 Deployment

### Frontend Deployment (Vercel/Netlify)

1. **Build the frontend:**

```bash
cd frontend
npm run build
```

2. **Deploy to Vercel:**

```bash
npx vercel --prod
```

3. **Deploy to Netlify:**
   - Connect your repository
   - Set build command: `npm run build`
   - Set publish directory: `build`

### Backend Deployment (Render/Heroku)

1. **Prepare for deployment:**

```bash
cd backend
pip freeze > requirements.txt
```

2. **Deploy to Render:**

   - Connect your repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `python app/main.py`

3. **Deploy to Heroku:**

```bash
# Install Heroku CLI
heroku create your-app-name
git push heroku main
```

### Environment Variables for Production

Set these environment variables in your deployment platform:

- `POKEMON_TCG_API_KEY`
- `CORS_ORIGINS` (your frontend URL)
- `TESSERACT_CMD` (if using OCR)

## 🧪 Testing

### Backend Testing

```bash
cd backend
python -m pytest tests/
```

### Frontend Testing

```bash
cd frontend
npm test
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Pokémon TCG API](https://pokemontcg.io/) for card data
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for text extraction
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [React](https://reactjs.org/) for the frontend framework

## 🐛 Troubleshooting

### Common Issues

**OCR not working:**

- Ensure Tesseract is installed and in PATH
- Check image quality and lighting
- Verify file permissions

**API errors:**

- Check your Pokémon TCG API key
- Verify network connectivity
- Check CORS settings

**Frontend not connecting to backend:**

- Ensure backend is running on port 8000
- Check proxy settings in package.json
- Verify CORS configuration

### Getting Help

- Check the [Issues](https://github.com/your-repo/issues) page
- Create a new issue with detailed error information
- Include logs and system information

## 📊 Performance Tips

- Use high-quality images for better OCR accuracy
- Implement image compression for faster uploads
- Cache API responses to reduce external calls
- Use CDN for static assets in production

---

**Happy Pokémon card hunting! 🎴✨**
