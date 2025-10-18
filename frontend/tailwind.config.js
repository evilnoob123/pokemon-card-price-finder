/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'pokemon-blue': '#3B82F6',
        'pokemon-red': '#EF4444',
        'pokemon-yellow': '#F59E0B',
        'pokemon-green': '#10B981',
      },
      fontFamily: {
        'pokemon': ['Pokemon', 'Arial', 'sans-serif'],
      },
      animation: {
        'bounce-slow': 'bounce 2s infinite',
        'pulse-slow': 'pulse 3s infinite',
      }
    },
  },
  plugins: [],
}
