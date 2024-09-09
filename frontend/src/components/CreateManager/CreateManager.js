import React, { useState } from 'react';
import axios from 'axios';

const CreateManager = () => {
    const [managerData, setManagerData] = useState({ email: '', username: '', password: '' });
    const [message, setMessage] = useState('');

    const handleChange = (e) => {
        setManagerData({ ...managerData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            await axios.post('api/users/create_manager/', managerData);
            setMessage('Manager created successfully.');
        } catch (error) {
            setMessage('Failed to create manager.');
        }
    };

    // Минимальная стилизация
    const formStyle = {
        display: 'flex',
        flexDirection: 'column',
        maxWidth: '300px',
        margin: '0 auto',
        padding: '20px',
        border: '1px solid #ccc',
        borderRadius: '8px',
        backgroundColor: '#f9f9f9',
    };

    const inputStyle = {
        marginBottom: '10px',
        padding: '8px',
        fontSize: '14px',
        borderRadius: '4px',
        border: '1px solid #ccc',
    };

    const buttonStyle = {
        padding: '10px',
        fontSize: '14px',
        backgroundColor: '#4CAF50',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
    };

    const messageStyle = {
        marginTop: '10px',
        fontSize: '14px',
        color: message.includes('successfully') ? 'green' : 'red',
        textAlign: 'center',
    };

    return (
        <div>
            <form onSubmit={handleSubmit} style={formStyle}>
                <input
                    type="email"
                    name="email"
                    value={managerData.email}
                    onChange={handleChange}
                    placeholder="Email"
                    style={inputStyle}
                    required
                />
                <input
                    type="text"
                    name="username"
                    value={managerData.username}
                    onChange={handleChange}
                    placeholder="Username"
                    style={inputStyle}
                    required
                />
                <input
                    type="password"
                    name="password"
                    value={managerData.password}
                    onChange={handleChange}
                    placeholder="Password"
                    style={inputStyle}
                    required
                />
                <button type="submit" style={buttonStyle}>Create Manager</button>
            </form>
            {message && <div style={messageStyle}>{message}</div>}
        </div>
    );
};

export default CreateManager;
