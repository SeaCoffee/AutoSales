import React, { useState } from 'react';
import axios from 'axios';


const AddToBlacklist = () => {
    const [userId, setUserId] = useState('');
    const [reason, setReason] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post('api/users/blacklist/manage/', { user_id: userId, reason: reason });
            setMessage('User has been successfully added to the blacklist.');
        } catch (error) {
            setMessage('Failed to add user to blacklist.');
        }
    };

    // Минимальная стилизация
    const formStyle = {
        display: 'flex',
        flexDirection: 'column',
        maxWidth: '400px',
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
        textAlign: 'center',
    };

    return (
        <div>
            <h1>Add User to Blacklist</h1>
            <form onSubmit={handleSubmit} style={formStyle}>
                <label style={labelStyle}>
                    User ID:
                    <input
                        type="text"
                        value={userId}
                        onChange={(e) => setUserId(e.target.value)}
                        style={inputStyle}
                        required
                    />
                </label>
                <label style={labelStyle}>
                    Reason for Blacklisting:
                    <input
                        type="text"
                        value={reason}
                        onChange={(e) => setReason(e.target.value)}
                        style={inputStyle}
                        required
                    />
                </label>
                <button type="submit" style={buttonStyle}>Add to Blacklist</button>
            </form>
            <p style={messageStyle}>{message}</p>
        </div>
    );
};

export default AddToBlacklist;
