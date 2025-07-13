import React, { useEffect, useState } from 'react';

function App() {
  const [status, setStatus] = useState('');

  useEffect(() => {
    fetch('http://localhost:8000/health')
      .then((res) => res.json())
      .then((data) => setStatus(data.status))
      .catch((err) => setStatus('error'));
  }, []);

  return (
    <div>
      <h1>Agent Swarm Frontend</h1>
      <p>Backend status: {status}</p>
    </div>
  );
}

export default App;
