import React from 'react';
import './styles.css';

function App() {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ color: '#333', textAlign: 'center' }}>
        🎴 Pokémon Card Price Finder
      </h1>
      <p style={{ textAlign: 'center', color: '#666' }}>
        Testing deployment - If you can see this, the app is working!
      </p>
      <div style={{ 
        backgroundColor: '#f0f0f0', 
        padding: '20px', 
        borderRadius: '8px',
        margin: '20px auto',
        maxWidth: '400px',
        textAlign: 'center'
      }}>
        <h2>Backend Status</h2>
        <p>Backend URL: https://pokemoncardpricefinder.onrender.com</p>
        <button 
          onClick={() => {
            fetch('https://pokemoncardpricefinder.onrender.com/health')
              .then(res => res.json())
              .then(data => alert('Backend Status: ' + JSON.stringify(data)))
              .catch(err => alert('Backend Error: ' + err.message));
          }}
          style={{
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            padding: '10px 20px',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Test Backend Connection
        </button>
      </div>
    </div>
  );
}

export default App;