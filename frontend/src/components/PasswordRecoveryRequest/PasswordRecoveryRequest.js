import React, { useState } from 'react';
import axios from 'axios';

const PasswordRecoveryRequest = () => {
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        axios.post('/api/auth/recovery/', { email })
            .then(response => {
                setMessage('Check your email for the password reset link.');
            })
            .catch(error => {
                setMessage('Error sending password reset email.');
            });
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

    const labelStyle = {
        marginBottom: '8px',
        fontSize: '14px',
        color: '#333',
    };

    const inputStyle = {
        marginBottom: '12px',
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
        color: message.includes('Check your email') ? 'green' : 'red',
        textAlign: 'center',
    };

    return (
        <form onSubmit={handleSubmit} style={formStyle}>
            <label htmlFor="email" style={labelStyle}>Email:</label>
            <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                style={inputStyle}
                required
            />
            <button type="submit" style={buttonStyle}>Send Reset Email</button>
            {message && <div style={messageStyle}>{message}</div>}
        </form>
    );
};

export default PasswordRecoveryRequest;
