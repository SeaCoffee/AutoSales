import React, { useState } from 'react';
import axios from 'axios';

function NewBrandRequest() {
    const [newBrandName, setNewBrandName] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!newBrandName.trim()) {
            setError('Введите название нового бренда');
            return;
        }

        try {
            const token = localStorage.getItem('token');
            await axios.post('api/listings/brands/request/', { brand_name: newBrandName }, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setMessage('Запрос на добавление бренда успешно отправлен менеджеру');
            setNewBrandName('');
        } catch (error) {
            console.error('Ошибка при отправке запроса на новый бренд:', error.response?.data || error.message);
            setError('Ошибка при отправке запроса. Попробуйте снова.');
        }
    };

    return (
        <div style={{ marginTop: '20px' }}>
            <h3>Не нашли нужного бренда?</h3>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="new_brand_name"
                    value={newBrandName}
                    onChange={(e) => setNewBrandName(e.target.value)}
                    placeholder="Введите название нового бренда"
                    style={{ padding: '8px 10px', fontSize: '16px', marginRight: '10px' }}
                />
                <button type="submit" style={{ padding: '8px 15px', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                    Отправить запрос
                </button>
            </form>
            {message && <p style={{ color: 'green' }}>{message}</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
}

export default NewBrandRequest;
