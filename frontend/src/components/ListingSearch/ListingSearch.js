import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ListingSearch() {
    const [filters, setFilters] = useState({
        brand: '',
        model_name: '',
        body_type: '',
        min_year: '',
        max_year: '',
        region: '',
        price_min: '',
        price_max: '',
        active: false, // Булевое значение для чекбокса
    });

    const [brandsModels, setBrandsModels] = useState({ brands: [], brands_models: {} });
    const [models, setModels] = useState([]);
    const [regions, setRegions] = useState([]);
    const [currencies, setCurrencies] = useState([]);
    const [error, setError] = useState('');
    const [searchResults, setSearchResults] = useState([]);

    // Загрузка данных брендов и моделей
    useEffect(() => {
        const fetchBrandModelData = async () => {
            try {
                const { data } = await axios.get('api/cars/data/');
                setBrandsModels(data);
            } catch (error) {
                setError('Ошибка при загрузке данных о брендах и моделях');
            }
        };
        fetchBrandModelData();
    }, []);

    // Загрузка регионов
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

    // Загрузка валют
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

    // Обработка изменения бренда
    const handleBrandChange = (event) => {
        const brandId = event.target.value;
        setFilters((prevFilters) => ({
            ...prevFilters,
            brand: brandId,
            model_name: '', // Обнуление модели при изменении бренда
        }));

        if (brandsModels && brandsModels.brands_models) {
            const filteredModels = brandsModels.brands_models[brandId] || [];
            setModels(filteredModels);
        } else {
            setModels([]);
        }
    };

    // Обработка изменения региона
    const handleChange = (event) => {
        const { name, value } = event.target;
        setFilters(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleRegionChange = (event) => {
    const selectedRegion = event.target.value;
    setFilters((prevFilters) => ({
        ...prevFilters,
        region: selectedRegion,
    }));
}

    const handleSubmit = async (e) => {
            e.preventDefault();

            const params = {};
            Object.keys(filters).forEach((key) => {
                if (filters[key] !== '' && filters[key] !== false && filters[key] !== null) {
                    params[key] = filters[key];
                }
            });


            if (params.region === '' || isNaN(params.region)) {
                delete params.region;
            }

            try {
                const response = await axios.get('api/listings/list/', { params });
                console.log('Результаты поиска:', response.data);
                setSearchResults(response.data.data || []);
            } catch (error) {
                console.error('Ошибка запроса:', error.response?.data || error.message);
                setError(error.response?.data?.detail || 'Произошла ошибка при выполнении поиска');
            }
        };



    const renderRegions = () => {
    if (!regions || !Array.isArray(regions)) {
        return <option value="">Нет доступных регионов</option>;
    }

    return regions.map((region) => (
        <option key={region[0]} value={region[0]}>
            {region[1]}
        </option>
    ));

    };


    // Рендер результатов поиска
   const renderSearchResults = () => {
    if (searchResults.length === 0) {
        return <p>Нет результатов для отображения</p>;
    }

    return (
        <ul>
            {searchResults.map((listing, index) => (
                <li key={index}>
                    <h3>{listing.title}</h3>
                    <p>{listing.description}</p>
                    {listing.listing_photo && <img src={listing.listing_photo} alt="Listing" width="200" />}
                </li>
            ))}
        </ul>
    );
};



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
        fontSize: '16px',
    };

    const buttonStyle = {
        padding: '10px 15px',
        backgroundColor: '#4CAF50',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '16px',
    };

    return (
        <div>
            <form onSubmit={handleSubmit} style={formStyle}>
                {/* Выбор бренда */}
                <select
                    name="brand"
                    value={filters.brand}
                    onChange={handleBrandChange}
                    style={inputStyle}
                >
                    <option value="">Выберите бренд</option>
                    {brandsModels.brands.map((brand) => (
                        <option key={brand.id} value={brand.id}>
                            {brand.name}
                        </option>
                    ))}
                </select>

                {/* Выбор модели */}
                <select
                    name="model_name"
                    value={filters.model_name}
                    onChange={handleChange}
                    style={inputStyle}
                >
                    <option value="">Выберите модель</option>
                    {models.map((model) => (
                        <option key={model.id} value={model.id}>
                            {model.name}
                        </option>
                    ))}
                </select>

                {/* Выбор типа кузова */}
                <select
                    name="body_type"
                    value={filters.body_type}
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

                 <select
                name="region"
                value={filters.region}
                onChange={handleRegionChange}
                style={inputStyle}
            >
                <option value="">Выберите регион</option>
                {renderRegions()}
            </select>


                {/* Чекбокс для фильтрации активных объявлений */}
                <label>
                    Активные:
                    <input
                        type="checkbox"
                        name="active"
                        checked={filters.active}
                        onChange={(e) =>
                            setFilters((prevFilters) => ({
                                ...prevFilters,
                                active: e.target.checked,
                            }))
                        }
                        style={inputStyle}
                    />
                </label>

                <input
                    type="number"
                    name="min_year"
                    value={filters.min_year}
                    onChange={handleChange}
                    placeholder="Мин. год"
                    style={inputStyle}
                />
                <input
                    type="number"
                    name="max_year"
                    value={filters.max_year}
                    onChange={handleChange}
                    placeholder="Макс. год"
                    style={inputStyle}
                />
                <input
                    type="number"
                    name="price_min"
                    value={filters.price_min}
                    onChange={handleChange}
                    placeholder="Мин. цена"
                    style={inputStyle}
                />
                <input
                    type="number"
                    name="price_max"
                    value={filters.price_max}
                    onChange={handleChange}
                    placeholder="Макс. цена"
                    style={inputStyle}
                />

                <button type="submit" style={buttonStyle}>
                    Поиск
                </button>

                {error && <p style={{ color: 'red' }}>{error}</p>}
            </form>

            {/* Результаты поиска */}
            <div>
                <h2>Результаты поиска:</h2>
                {renderSearchResults()}
            </div>
        </div>
    );
}

export default ListingSearch;

