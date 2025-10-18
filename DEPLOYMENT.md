# 🚀 Vercel Deployment Guide for Pokémon Card Price Finder

This guide will help you deploy your Pokémon Card Price Finder to Vercel so others can use it from their browsers.

## 📋 Prerequisites

- GitHub account
- Vercel account (free at [vercel.com](https://vercel.com))
- Backend deployment service (Render/Railway/Heroku)

## 🎯 Deployment Strategy

Since your app has both frontend and backend components, we'll use a two-part deployment:

1. **Frontend** → Vercel (for the React app)
2. **Backend** → Render/Railway (for the FastAPI server)

## 🚀 Step 1: Deploy Backend First

### Option A: Deploy to Render (Recommended)

1. **Push your code to GitHub:**

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/pokemon-card-price-finder.git
   git push -u origin main
   ```

2. **Go to [Render.com](https://render.com) and sign up**

3. **Create a new Web Service:**

   - Connect your GitHub repository
   - Choose the `pokemon-card-price-finder/backend` directory
   - Set these settings:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python app/main.py`
     - **Environment:** Python 3

4. **Add Environment Variables in Render:**

   ```
   POKEMON_TCG_API_KEY=your_api_key_here
   CORS_ORIGINS=https://your-frontend-url.vercel.app
   ```

5. **Deploy!** Render will give you a URL like `https://your-app.onrender.com`

### Option B: Deploy to Railway

1. **Go to [Railway.app](https://railway.app) and sign up**

2. **Create a new project from GitHub**

3. **Select the backend folder**

4. **Add environment variables:**
   ```
   POKEMON_TCG_API_KEY=your_api_key_here
   CORS_ORIGINS=https://your-frontend-url.vercel.app
   ```

## 🎨 Step 2: Deploy Frontend to Vercel

### Method 1: Vercel CLI (Recommended)

1. **Install Vercel CLI:**

   ```bash
   npm install -g vercel
   ```

2. **Navigate to frontend directory:**

   ```bash
   cd pokemon-card-price-finder/frontend
   ```

3. **Login to Vercel:**

   ```bash
   vercel login
   ```

4. **Deploy:**

   ```bash
   vercel
   ```

5. **Set environment variable:**

   ```bash
   vercel env add REACT_APP_API_URL
   # Enter your backend URL (e.g., https://your-app.onrender.com)
   ```

6. **Redeploy with environment variable:**
   ```bash
   vercel --prod
   ```

### Method 2: Vercel Dashboard

1. **Go to [vercel.com](https://vercel.com) and sign up**

2. **Click "New Project"**

3. **Import your GitHub repository**

4. **Configure the project:**

   - **Framework Preset:** Create React App
   - **Root Directory:** `pokemon-card-price-finder/frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `build`

5. **Add Environment Variable:**

   - **Name:** `REACT_APP_API_URL`
   - **Value:** Your backend URL (e.g., `https://your-app.onrender.com`)

6. **Deploy!**

## 🔧 Step 3: Update CORS Settings

After deploying both frontend and backend:

1. **Get your Vercel frontend URL** (e.g., `https://pokemon-card-finder.vercel.app`)

2. **Update your backend CORS settings:**
   - Go to your Render/Railway dashboard
   - Update the `CORS_ORIGINS` environment variable to include your Vercel URL
   - Redeploy the backend

## 🎉 Step 4: Test Your Deployment

1. **Visit your Vercel URL**
2. **Try uploading a Pokémon card image**
3. **Check that it connects to your backend**

## 🛠️ Troubleshooting

### Common Issues:

**CORS Errors:**

- Make sure `CORS_ORIGINS` includes your Vercel URL
- Check that your backend is running

**API Connection Issues:**

- Verify `REACT_APP_API_URL` is set correctly
- Check backend logs for errors

**Build Failures:**

- Make sure all dependencies are in `package.json`
- Check that TailwindCSS is properly configured

### Debug Steps:

1. **Check Vercel deployment logs:**

   ```bash
   vercel logs
   ```

2. **Check backend logs in Render/Railway dashboard**

3. **Test API endpoint directly:**
   ```bash
   curl -X POST https://your-backend-url.com/api/card/scan
   ```

## 📱 Mobile Testing

Test your deployed app on mobile devices:

- The app should work on both iOS and Android browsers
- Camera functionality should work on mobile devices
- Make sure the UI is responsive

## 🔄 Continuous Deployment

Once set up, your app will automatically redeploy when you push changes to GitHub:

1. **Push changes to GitHub**
2. **Vercel automatically rebuilds and deploys frontend**
3. **Render/Railway automatically rebuilds and deploys backend**

## 💡 Pro Tips

1. **Use custom domains:** You can add custom domains in Vercel settings
2. **Monitor performance:** Use Vercel Analytics to track usage
3. **Set up monitoring:** Use services like UptimeRobot to monitor your backend
4. **Backup your data:** Consider using a database service for persistent data

## 🎯 Final Result

After completing these steps, you'll have:

- ✅ Frontend deployed at `https://your-app.vercel.app`
- ✅ Backend deployed at `https://your-backend.onrender.com`
- ✅ Full-stack Pokémon Card Price Finder accessible worldwide
- ✅ Mobile-responsive design working on all devices

Your Pokémon Card Price Finder will be live and accessible to anyone with an internet connection! 🎴✨
