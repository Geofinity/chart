'use client';

import { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import province from './geojson/province.geojson.json';
import { Dropdown } from 'primereact/dropdown';
import ChartDemo from '../charts/page';

const LeafletMap = () => {
    const [districts, setDistricts] = useState([]);
    const [municipalities, setMunicipalities] = useState([]);
    const [provinces, setProvinces] = useState([]);
    const [wards, setWards] = useState([]);
    const [displayChart, setDisplayChart] = useState(false);
    const [displayWard, setdisplayWard]= useState(false)
    const chartRef = useRef(null);

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
        5: 'Lumbini',
        4: 'Gandaki',
        6: 'Karnali',
        7: 'Sudurpashchim'
    };

    const fetchData = async () => {
        try {
            const districtsRes = await fetch('http://127.0.0.1:8000/api/districts/');
            const municipalitiesRes = await fetch('http://127.0.0.1:8000/api/municipalities/');
            const provincesRes = await fetch('http://127.0.0.1:8000/api/provinces/');
            const wardsRes = await fetch('http://127.0.0.1:8000/api/wards/');

            setDistricts(await districtsRes.json());
            setMunicipalities(await municipalitiesRes.json());
            setProvinces(await provincesRes.json());
            setWards(await wardsRes.json());
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        if (!mapRef.current) {
            mapRef.current = L.map('map').setView([28.232, 83.979], 8);

            L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '&copy; OpenStreetMap'
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


    const handleFilterChange = (name, value) => {
        let updatedFilters = { ...filters, [name]: value };

        // Automatically filter related dropdowns
        if (name === 'province') {
            updatedFilters.district = null;
            updatedFilters.municipality = null;
            updatedFilters.ward = null;
            setdisplayWard(false)
        }
        if (name === 'district') {
            updatedFilters.municipality = null;
            updatedFilters.ward = null;

            // Update province automatically
            const district = districts.find((d) => d.name_en === value);
            updatedFilters.province = district ? district.province.name_en : filters.province;
            setdisplayWard(false)
        }
        if (name === 'municipality') {
            updatedFilters.ward = null;

            // Update district and province automatically
            const municipality = municipalities.find((m) => m.name_en === value);
            updatedFilters.district = municipality ? municipality.district.name_en : filters.district;
            updatedFilters.province = municipality ? municipality.district.province.name_en : filters.province;
            setdisplayWard(true)
              
        }

        setFilters(updatedFilters);
    };

    const toggleChart = async () => {
        await setDisplayChart(true);
        chartRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    return (
        <div className="flex flex-col gap-5 items-center">
            <div className="filters-container text-xl bg-white flex px-6">
                {/* Fiscal Year Dropdown */}
                <label className="filter-label block font-semibold text-gray-700">
                    Fiscal Year
                    <Dropdown name="fiscalYear" value={filters.fiscalYear} onChange={(e) => handleFilterChange('fiscalYear', e.value)} options={fiscalYears} className="filter-select w-48 text-xs" filter />
                </label>

                {/* Province Dropdown */}
                <label className="filter-label block font-semibold text-gray-700">
                    Province
                    <Dropdown
                        name="province"
                        value={filters.province}
                        onChange={(e) => handleFilterChange('province', e.value)}
                        options={provinces.map((province) => ({
                            label: provinceMap[province.name_en],
                            value: province.name_en
                        }))}
                        placeholder="Select Province"
                        className="filter-select w-48 text-xs"
                        filter
                    />
                </label>

                {/* District Dropdown */}
                <label className="filter-label block font-semibold text-gray-700">
                    District
                    <Dropdown
                        name="district"
                        value={filters.district}
                        onChange={(e) => handleFilterChange('district', e.value)}
                        options={districts
                            .filter((d) => !filters.province || d.province.name_en === filters.province)
                            .map((district) => ({
                                label: district.name_en,
                                value: district.name_en
                            }))}
                        placeholder="Select District"
                        className="filter-select w-48 text-xs"
                        filter
                    />
                </label>

                {/* Municipality Dropdown */}
                <label className="filter-label block font-semibold text-gray-700">
                    Municipality
                    <Dropdown
                        name="municipality"
                        value={filters.municipality}
                        onChange={(e) => handleFilterChange('municipality', e.value)}
                        options={municipalities
                            .filter((m) => (!filters.district || m.district.name_en === filters.district) && (!filters.province || m.district.province.name_en === filters.province))
                            .map((municipality) => ({
                                label: municipality.name_en,
                                value: municipality.name_en
                            }))}
                        placeholder="Select Municipality"
                        className="filter-select w-48 text-xs"
                        filter
                    />
                </label>

                {/* Ward Dropdown */}
                <label className="filter-label block font-semibold text-gray-700">
                    Ward
                    {displayWard?<Dropdown
                        name="ward"
                        value={filters.ward}
                        onChange={(e) => handleFilterChange('ward', e.value)}
                        options={wards
                            .filter((w) => !filters.municipality || w.municipality.name_en === filters.municipality)
                            .map((ward) => ({
                                label: `Ward ${ward.name_en}`,
                                value: ward.name_en
                            }))}
                        placeholder="Select Ward"
                        className="filter-select w-48 text-xs"
                        filter
                        
                    />:<Dropdown
                    name="ward"
                    value={filters.ward}
                    onChange={(e) => handleFilterChange('ward', e.value)}
                    options={wards
                        .filter((w) => !filters.municipality || w.municipality.name_en === filters.municipality)
                        .map((ward) => ({
                            label: `Ward ${ward.name_en}`,
                            value: ward.name_en
                        }))}
                    placeholder="Select Ward"
                    className="filter-select w-48 text-xs"
                    filter
                    disabled
                    
                /> }
                </label>

                <button onClick={toggleChart} className="bg-blue-500 text-white px-4 py-2 rounded mt-5">
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
