import React, { useState } from 'react';
import axios from 'axios';

const UpgradeAccount = () => {
    const [accountType, setAccountType] = useState('premium');
    const [message, setMessage] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.put('/api/users/upgrade_account/', { account_type: accountType });
            setMessage('Account upgraded successfully.');
        } catch (error) {
            setMessage(`Failed to upgrade account: ${error.response.data.detail}`);
        }
    };

    // Стилизация
    const containerStyle = {
        maxWidth: '400px',
        margin: '0 auto',
        padding: '20px',
        border: '1px solid #ccc',
        borderRadius: '8px',
        backgroundColor: '#f9f9f9',
        textAlign: 'center',
    };

    const formStyle = {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    };

    const selectStyle = {
        marginBottom: '10px',
        padding: '8px',
        fontSize: '16px',
        borderRadius: '4px',
        border: '1px solid #ccc',
    };

    const buttonStyle = {
        padding: '10px',
        fontSize: '16px',
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
    };

    return (
        <div style={containerStyle}>
            <form onSubmit={handleSubmit} style={formStyle}>
                <select value={accountType} onChange={(e) => setAccountType(e.target.value)} style={selectStyle}>
                    <option value="premium">Premium</option>
                </select>
                <button type="submit" style={buttonStyle}>Upgrade Account</button>
            </form>
            {message && <p style={messageStyle}>{message}</p>}
        </div>
    );
};

export default UpgradeAccount;

