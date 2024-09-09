import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';


const PasswordReset = () => {
    const { token } = useParams();
    const navigate = useNavigate();

    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        axios.post(`/api/auth/recovery/${token}`, { password })
            .then(response => {
                setMessage('Password has been reset successfully.');
                setTimeout(() => {
                    navigate('/login');
                }, 3000);
            })
            .catch(error => {
                setMessage('Failed to reset password.');
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
        color: message.includes('successfully') ? 'green' : 'red',
        textAlign: 'center',
    };

    return (
        <form onSubmit={handleSubmit} style={formStyle}>
            <label htmlFor="password" style={labelStyle}>New Password:</label>
            <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={inputStyle}
                required
            />
            <button type="submit" style={buttonStyle}>Reset Password</button>
            {message && <div style={messageStyle}>{message}</div>}
        </form>
    );
};

export default PasswordReset;
