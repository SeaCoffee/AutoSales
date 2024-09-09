import {useEffect} from "react";
import axios from "axios";

function SimpleRegionSelect() {
    const [region, setRegion] = useState('');

        useEffect(() => {
        const fetchRegions = async () => {
            try {
                const {data} = await axios.get('api/listings/regions/');
                setRegions(data);
                console.log('Загруженные регионы:', data);
            } catch (error) {
                console.error('Ошибка при загрузке регионов:', error);
            }
        };
        fetchRegions();
    }, []);


    const handleRegionChange = (event) => {
        setRegion(event.target.value);
        console.log('Выбранный регион:', event.target.value);
    };

    return (
        <select name="region" value={region} onChange={handleRegionChange}>
            <option value="">Выберите регион</option>

        </select>
    );
}
