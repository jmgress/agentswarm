import React, { useState } from 'react';

interface AgentFormProps {
  onAgentCreated: () => void;
}

const AgentForm: React.FC<AgentFormProps> = ({ onAgentCreated }) => {
  const [name, setName] = useState('');
  const [type, setType] = useState('');
  const [description, setDescription] = useState('');
  const [endpoint, setEndpoint] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const agentData = {
      name,
      type,
      description,
      mcp_connection: {
        endpoint,
      },
    };

    try {
      const response = await fetch('http://localhost:8000/agents', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(agentData),
      });

      if (response.ok) {
        // Reset form
        setName('');
        setType('');
        setDescription('');
        setEndpoint('');
        onAgentCreated();
        alert('Agent created successfully!');
      } else {
        alert('Failed to create agent.');
      }
    } catch (error) {
      console.error('Error creating agent:', error);
      alert('Error creating agent.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="agent-form">
      <h2>Create New Agent</h2>
      <div className="form-group">
        <label>Name:</label>
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
      </div>
      <div className="form-group">
        <label>Type:</label>
        <input type="text" value={type} onChange={(e) => setType(e.target.value)} required />
      </div>
      <div className="form-group">
        <label>Description:</label>
        <textarea value={description} onChange={(e) => setDescription(e.target.value)} required />
      </div>
      <div className="form-group">
        <label>MCP Endpoint:</label>
        <input type="text" value={endpoint} onChange={(e) => setEndpoint(e.target.value)} required />
      </div>
      <button type="submit">Create Agent</button>
    </form>
  );
};

export default AgentForm;
