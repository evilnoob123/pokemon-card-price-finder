import React from 'react';

function App() {
  return (
    <div style={{ 
      padding: '20px', 
      fontFamily: 'Arial, sans-serif',
      backgroundColor: '#f5f5f5',
      minHeight: '100vh'
    }}>
      <div style={{
        maxWidth: '800px',
        margin: '0 auto',
        backgroundColor: 'white',
        padding: '40px',
        borderRadius: '10px',
        boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
      }}>
        <h1 style={{ 
          color: '#333', 
          textAlign: 'center',
          fontSize: '2.5rem',
          marginBottom: '20px'
        }}>
          🎴 Pokémon Card Price Finder
        </h1>
        
        <p style={{ 
          textAlign: 'center', 
          color: '#666',
          fontSize: '1.2rem',
          marginBottom: '30px'
        }}>
          Testing deployment - If you can see this, the app is working!
        </p>
        
        <div style={{ 
          backgroundColor: '#e8f4fd', 
          padding: '30px', 
          borderRadius: '8px',
          margin: '20px 0',
          textAlign: 'center',
          border: '2px solid #007bff'
        }}>
          <h2 style={{ color: '#007bff', marginBottom: '20px' }}>Backend Status</h2>
          <p style={{ marginBottom: '20px' }}>
            Backend URL: <strong>https://pokemoncardpricefinder.onrender.com</strong>
          </p>
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
              padding: '15px 30px',
              borderRadius: '5px',
              cursor: 'pointer',
              fontSize: '1.1rem',
              fontWeight: 'bold'
            }}
          >
            Test Backend Connection
          </button>
        </div>

        <div style={{
          marginTop: '30px',
          padding: '20px',
          backgroundColor: '#f8f9fa',
          borderRadius: '5px',
          border: '1px solid #dee2e6'
        }}>
          <h3 style={{ color: '#495057', marginBottom: '15px' }}>Deployment Info:</h3>
          <ul style={{ color: '#6c757d', lineHeight: '1.6' }}>
            <li>✅ Frontend deployed to Vercel</li>
            <li>✅ Backend deployed to Render</li>
            <li>✅ CORS configured</li>
            <li>✅ React app working</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default App;