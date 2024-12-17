'use client';

import { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import province from './geojson/province.geojson.json';
// import municipalities from './geojson/municipality.geojson.json'
// import district from './geojson/district.geojson.json'
// import ward from './geojson/ward.geojson.json'
import { Dropdown } from 'primereact/dropdown'; // Import PrimeReact Dropdown
import ChartDemo from '../charts/page';

const LeafletMap = () => {
    const [districts, setDistricts] = useState([]);
    const [municipalities, setMunicipalities] = useState([]);
    const [provinces, setProvinces] = useState([]);
    const [displayChart, setDisplayChart] = useState(false); // Chart state

    const chartRef = useRef(null); // Ref for the chart section

    const fetchData = async () => {
        try {
            const districtsRes = await fetch('http://127.0.0.1:8000/api/districts/');
            const municipalitiesRes = await fetch('http://127.0.0.1:8000/api/municipalities/');
            const provincesRes = await fetch('http://127.0.0.1:8000/api/provinces/');

            const districtsData = await districtsRes.json();
            const municipalitiesData = await municipalitiesRes.json();
            const provincesData = await provincesRes.json();

            setDistricts(districtsData);
            setMunicipalities(municipalitiesData);
            setProvinces(provincesData);
        } catch (error) {
            console.log(error);
        }
    };

    const mapRef = useRef();
    const [filters, setFilters] = useState({
        fiscalYear: 'All',
        province: null,
        district: null,
        municipality: null,
        ward: null
    });

    const fiscalYears = ['2023/24', '2022/23', '2021/22'];
    const provinceMap = {
        1: 'Koshi',
        2: 'Madhesh',
        3: 'Bagmati',
        4: 'Lumbini',
        5: 'Gandaki',
        6: 'Karnali',
        7: 'Sudurpashchim'
    };

    const wards = ['Ward 1', 'Ward 2', 'Ward 3']; // Replace with actual data

    useEffect(() => {
        if (!mapRef.current) {
            mapRef.current = L.map('map').setView([28.232, 83.979], 8);

            L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            }).addTo(mapRef.current);

            renderGeoJSON();
        }

        fetchData();

        return () => {
            if (mapRef.current) {
                mapRef.current.remove();
                mapRef.current = null;
            }
        };
    }, []);

    const renderGeoJSON = () => {
        if (!mapRef.current) return;

        // Clear existing layers
        mapRef.current.eachLayer((layer) => {
            if (layer instanceof L.GeoJSON) {
                mapRef.current.removeLayer(layer);
            }
        });

        const provinceStyle = { color: '#3388ff', weight: 2, fillOpacity: 0.5 };
        const provinceHighlightStyle = { color: '#ff7800', weight: 3, fillOpacity: 0.7 };

        // Filter provinces based on filters
        const filteredGeoJSON = {
            ...province,
            features: province.features.filter((feature) => {
                const matchesProvince = filters.province === null || feature.properties.name === filters.province;
                return matchesProvince;
            })
        };

        L.geoJSON(filteredGeoJSON, {
            style: provinceStyle,
            onEachFeature: (feature, layer) => {
                // Highlight on hover
                layer.on('mouseover', () => layer.setStyle(provinceHighlightStyle));
                layer.on('mouseout', () => layer.setStyle(provinceStyle));

                // Bind tooltips
                if (feature.properties && feature.properties.name) {
                    layer.bindTooltip(feature.properties.name, {
                        permanent: false,
                        direction: 'center',
                        className: 'province-tooltip'
                    });
                }

                // Bind popup
                layer.bindPopup(`<b>${feature.properties.title_en} Province </b><br><b>${feature.properties.title_ne}  प्रदेश</b><br>Province : ${feature.id}`);

                // Handle click event to update filters
                layer.on('click', () => {
                    setFilters((prevFilters) => ({
                        ...prevFilters,
                        province: feature.properties.name || null // Set province filter on click
                    }));
                });
            }
        }).addTo(mapRef.current);
    };

    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        setFilters((prevFilters) => ({
            ...prevFilters,
            [name]: value || null
        }));
    };

    const toggleChart = async() => {
        await setDisplayChart(true);

        // Scroll to chart section
        if (chartRef.current) {
            chartRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    };

    return (
        <div className='flex flex-col gap-5 items-center'>
            <div className="filters-container text-xl bg-white flex px-6">
                <label className="filter-label block  font-semibold text-gray-700 ">
                    Fiscal Year
                    <Dropdown
                        name="fiscalYear"
                        value={filters.fiscalYear}
                        onChange={handleFilterChange}
                        options={fiscalYears}
                        className="filter-select w-48 text-xs"
                        filter
                    />
                </label>

                <label className="filter-label block font-semibold text-gray-700">
                    Province
                    <Dropdown
                        name="province"
                        value={filters.province}
                        onChange={handleFilterChange}
                        options={provinces.map((province) => ({
                            label: provinceMap[province.name_en],
                            value: province.name_en
                        }))}
                        placeholder="Select Province"
                        className="filter-select w-48 text-xs"
                        filter
                    />
                </label>

                <label className="filter-label block font-semibold text-gray-700">
                    District
                    <Dropdown
                        name="district"
                        value={filters.district}
                        onChange={handleFilterChange}
                        options={districts.map((district) => ({
                            label: district.name_en,
                            value: district.name_en
                        }))}
                        placeholder="Select District"
                        className="filter-select w-48 text-xs"
                        filter
                    />
                </label>

                <label className="filter-label block  font-semibold text-gray-700">
                    Municipality
                    <Dropdown
                        name="municipality"
                        value={filters.municipality}
                        onChange={handleFilterChange}
                        options={municipalities.map((municipality) => ({
                            label: municipality.name_en,
                            value: municipality.name_en
                        }))}
                        placeholder="Select Municipality"
                        className="filter-select w-48 text-xs"
                        filter
                    />
                </label>

                <label className="filter-label block font-semibold text-gray-700">
                    Ward
                    <Dropdown
                        name="ward"
                        value={filters.ward}
                        onChange={handleFilterChange}
                        options={wards.map((ward) => ({
                            label: ward,
                            value: ward
                        }))}
                        placeholder="Select Ward"
                        className="filter-select w-48 text-xs"
                        filter
                    />
                </label>

                <button
                    onClick={toggleChart}
                    className="bg-blue-500 text-white px-4 py-2 rounded mt-5"
                >
                    Show Chart
                </button>
            </div>

            <div id="map" style={{ height: '90vh', width: '90vw' }}></div>

            {displayChart && (
                <div ref={chartRef}>
                    <ChartDemo />
                </div>
            )}
        </div>
    );
};

export default LeafletMap;
