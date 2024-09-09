import React, { useState } from 'react';
import axios from 'axios';

const DeleteAccount = () => {
    const [message, setMessage] = useState('');

    const handleDelete = async () => {
        try {
            const response = await axios.delete('/api/users/delete-account/');
            setMessage('Your account has been deleted successfully.');
        } catch (error) {
            setMessage('Failed to delete your account.');
        }
    };

    // Минимальная стилизация
    const containerStyle = {
        maxWidth: '300px',
        margin: '0 auto',
        padding: '20px',
        textAlign: 'center',
    };

    const buttonStyle = {
        padding: '10px 20px',
        fontSize: '14px',
        backgroundColor: '#FF6347',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
    };

    const messageStyle = {
        marginTop: '10px',
        fontSize: '14px',
        color: message.includes('successfully') ? 'green' : 'red',
    };

    return (
        <div style={containerStyle}>
            <button onClick={handleDelete} style={buttonStyle}>Delete My Account</button>
            <p style={messageStyle}>{message}</p>
        </div>
    );
};

export default DeleteAccount;
