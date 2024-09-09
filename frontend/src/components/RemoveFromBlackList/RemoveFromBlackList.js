import React, { useState } from 'react';
import axios from 'axios';

const RemoveFromBlacklist = () => {
    const [userId, setUserId] = useState('');
    const [message, setMessage] = useState('');

    const handleRemove = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.delete('api/users/blacklist/manage/', { data: { user_id: userId } });
            setMessage('User removed from blacklist successfully');
        } catch (error) {
            setMessage('Error removing user from blacklist');
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
        <div>
            <form onSubmit={handleRemove} style={formStyle}>
                <input
                    type="text"
                    value={userId}
                    onChange={(e) => setUserId(e.target.value)}
                    placeholder="User ID"
                    style={inputStyle}
                    required
                />
                <button type="submit" style={buttonStyle}>Remove from Blacklist</button>
            </form>
            <p style={messageStyle}>{message}</p>
        </div>
    );
};

export default RemoveFromBlacklist;
