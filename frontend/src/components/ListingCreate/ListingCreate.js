import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

import NewBrandRequest from "../NewBrandRequest/NewBrandRequest";

function ListingCreate() {
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        price: '',
        year: '',
        engine: '',
        listing_photo: null,
        currency: '',
        region: '',
        brand: '',
        model_name: '',
        body_type: ''
    });
    const [brandsModels, setBrandsModels] = useState({ brands: [], brandsModels: {} });
    const [models, setModels] = useState([]);
    const [regions, setRegions] = useState([]);
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const [currencies, setCurrencies] = useState([]);

    const formStyle = {
        display: 'flex',
        flexDirection: 'column',
        maxWidth: '500px',
        margin: 'auto',
        gap: '10px',
    };

    const inputStyle = {
        padding: '8px 10px',
        border: '1px solid #ccc',
        borderRadius: '4px',
        fontSize: '16px'
    };

    const buttonStyle = {
        padding: '10px 15px',
        backgroundColor: '#4CAF50',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '16px'
    };

    useEffect(() => {
    const fetchBrandModelData = async () => {
        try {
            const { data } = await axios.get('api/cars/data/');
            console.log("Данные, полученные с сервера:", data);  // Логируем данные с сервера
            setBrandsModels(data);
        } catch (error) {
            setError('Ошибка при загрузке данных о брендах и моделях');
        }
    };
    fetchBrandModelData();
}, []);


    useEffect(() => {
        const fetchRegions = async () => {
            try {
                const { data } = await axios.get('api/listings/regions/');
                setRegions(data.regions);
            } catch (error) {
                console.error('Ошибка при загрузке регионов:', error);
            }
        };
        fetchRegions();
    }, []);

    useEffect(() => {
        const fetchCurrencies = async () => {
            try {
                const { data } = await axios.get('api/currencies/list/');
                setCurrencies(data);
            } catch (error) {
                console.error('Ошибка при загрузке валют:', error);
            }
        };
        fetchCurrencies();
    }, []);

    const handleSubmit = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem('token');

    const formDataToSend = new FormData();
    Object.keys(formData).forEach(key => {
        let value = formData[key];
        if (['price', 'year', 'engine', 'currency', 'brand', 'model_name'].includes(key)) {
            value = parseInt(value, 10);
        }
        formDataToSend.append(key, value);
    });

    try {
        const response = await axios.post('api/listings/create/', formDataToSend, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        if (response.status === 201) {
            console.log('Объявление успешно создано', response.data);
            navigate('/listingsuserlist');
        }

    } catch (error) {
        if (error.response?.data?.detail === "The description contains prohibited words. Please edit and resubmit.") {
            // Если сервер вернул сообщение о запретных словах
            setError('В описании объявления найдены запрещённые слова. Пожалуйста, исправьте и отправьте снова.');
        } else {
            // Обработка других ошибок
            console.error('Ошибка запроса:', error.response?.data || error.message);
            setError(error.response?.data?.detail || 'Произошла ошибка при создании объявления');
        }
    }
};


   const handleBrandChange = (event) => {
    const brandId = parseInt(event.target.value, 10);  // Приводим значение к числу
    console.log("Выбранный brandId:", brandId);  // Логируем brandId
    console.log("Ключи brandsModels:", Object.keys(brandsModels));  // Логируем ключи brandsModels

    setFormData({ ...formData, brand: brandId, model_name: '' });

    if (brandsModels && brandsModels.brands_models && brandsModels.brands_models[brandId]) {  // Доступ к brands_models
        const filteredModels = brandsModels.brands_models[brandId];  // Извлекаем модели из правильного поля
        console.log("Модели для выбранного бренда:", filteredModels);  // Логируем модели для бренда
        setModels(filteredModels);  // Устанавливаем модели
    } else {
        console.log("Модели не найдены для brandId:", brandId);  // Логируем отсутствие моделей
        setModels([]);
    }
};



   useEffect(() => {
    console.log("Состояние моделей изменилось:", models);
}, [models]);




    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleFileChange = (event) => {
        setFormData({ ...formData, listing_photo: event.target.files[0] });
    };

    return (
        <>
            <form onSubmit={handleSubmit} style={formStyle} encType="multipart/form-data">
                <input
                    type="text"
                    name="title"
                    value={formData.title}
                    onChange={handleChange}
                    placeholder="Title"
                    style={inputStyle}
                />
                <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                    placeholder="Description"
                    style={{ ...inputStyle, height: '100px' }}
                />
                <input
                    type="number"
                    name="price"
                    value={formData.price}
                    onChange={handleChange}
                    placeholder="Price"
                    style={inputStyle}
                />
                <input
                    type="number"
                    name="year"
                    value={formData.year}
                    onChange={handleChange}
                    placeholder="Year"
                    style={inputStyle}
                />
                <input
                    type="text"
                    name="engine"
                    value={formData.engine}
                    onChange={handleChange}
                    placeholder="Engine"
                    style={inputStyle}
                />

                <select
                    name="region"
                    value={formData.region}
                    onChange={handleChange}
                    style={inputStyle}
                >
                    <option value="">Выберите регион</option>
                    {regions.map((region, index) => (
                        <option key={index} value={region[0]}>
                            {region[1]}
                        </option>
                    ))}
                </select>

                <select
                    name="currency"
                    value={formData.currency}
                    onChange={handleChange}
                    style={inputStyle}
                >
                    <option value="">Выберите валюту</option>
                    {currencies.map((currency) => (
                        <option key={currency.id} value={currency.id}>
                            {currency.currency_code} - {currency.rate}
                        </option>
                    ))}
                </select>

                <select
                    name="brand"
                    value={formData.brand}
                    onChange={handleBrandChange}
                    style={inputStyle}
                >
                    <option value="">Select Brand</option>
                    {Array.isArray(brandsModels.brands) && brandsModels.brands.map(brand => (
                        <option key={brand.id} value={brand.id}>{brand.name}</option>
                    ))}
                </select>


                <select
                name="model_name"
                value={formData.model_name}
                onChange={handleChange}
                style={inputStyle}
            >
                <option value="">Select Model</option>
                {models.map(model => (
                    <option key={model.id} value={model.id}>{model.name}</option>  // Правильное отображение модели
                ))}
            </select>



                <select
                    name="body_type"
                    value={formData.body_type}
                    onChange={handleChange}
                    style={inputStyle}
                >
                    <option value="">Select Body Type</option>
                    <option value="sedan">Sedan</option>
                    <option value="hatchback">Hatchback</option>
                    <option value="suv">SUV</option>
                    <option value="wagon">Wagon</option>
                    <option value="coupe">Coupe</option>
                    <option value="convertible">Convertible</option>
                    <option value="minivan">Minivan</option>
                    <option value="pickup">Pickup</option>
                </select>

                <input type="file" name="listing_photo" onChange={handleFileChange} style={inputStyle} />
                <button type="submit" style={buttonStyle}>Create Listing</button>
                {error && <p style={{ color: 'red' }}>{error}</p>}
            </form>

            {/* Отдельный компонент для запроса нового бренда */}
            <NewBrandRequest />
        </>
    );
}

export default ListingCreate;
