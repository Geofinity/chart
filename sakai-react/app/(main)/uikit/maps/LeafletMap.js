"use client";

import { useEffect, useRef, useState } from "react";
import L from "leaflet";
import province from "./geojson/province.geojson.json";

const LeafletMap = () => {
  const mapRef = useRef();
  const [filters, setFilters] = useState({
    fiscalYear: "All",
    province: "All",
    district: "All",
    municipality: "All",
    ward: "All",
  });

  const fiscalYears = ["2023/24", "2022/23", "2021/22"];
  const provinces= [
    "Koshi",
    "Madhesh",
    "Bagmati",
    "Gandaki",
    "Lumbini",
    "Karnali",
    "Sudurpashchim"
]

  const districts = [
    "Achham", "Arghakhanchi", "Baglung", "Baitadi", "Bajhang", "Bajura", 
    "Banke", "Bara", "Bardiya", "Bhaktapur", "Bhojpur", "Chitwan", 
    "Dadeldhura", "Dailekh", "Dang", "Darchula", "Dhading", "Dhankuta", 
    "Dhanusha", "Dolakha", "Dolpa", "Doti", "Gorkha", "Gulmi", 
    "Humla", "Ilam", "Jajarkot", "Jhapa", "Jumla", "Kailali", 
    "Kalikot", "Kanchanpur", "Kapilvastu", "Kaski", "Kathmandu", "Kavrepalanchok", 
    "Khotang", "Lalitpur", "Lamjung", "Mahottari", "Makwanpur", "Manang", 
    "Morang", "Mugu", "Mustang", "Myagdi", "Nawalparasi East", "Nawalparasi West", 
    "Nuwakot", "Okhaldhunga", "Palpa", "Panchthar", "Parbat", "Parsa", 
    "Pyuthan", "Ramechhap", "Rasuwa", "Rautahat", "Rolpa", "Rukum East", 
    "Rukum West", "Rupandehi", "Salyan", "Sankhuwasabha", "Saptari", "Sarlahi", 
    "Sindhuli", "Sindhupalchok", "Siraha", "Solukhumbu", "Sunsari", "Surkhet", 
    "Syangja", "Tanahun", "Taplejung", "Terhathum", "Udayapur"
]
; // Replace with actual data
  const municipalities = ["Municipality 1", "Municipality 2"]; // Replace with actual data
  const wards = ["Ward 1", "Ward 2", "Ward 3"]; // Replace with actual data

  useEffect(() => {
    if (!mapRef.current) {
      mapRef.current = L.map("map").setView([28.232, 83.979], 7);

      L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }).addTo(mapRef.current);

      renderGeoJSON();
    }

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

    const provinceStyle = { color: "#3388ff", weight: 2, fillOpacity: 0.5 };
    const provinceHighlightStyle = { color: "#ff7800", weight: 3, fillOpacity: 0.7 };

    // Filter provinces based on filters
    const filteredGeoJSON = {
      ...province,
      features: province.features.filter((feature) => {
        const matchesProvince =
          filters.province === "All" || feature.properties.name === filters.province;
        // Add logic for district, municipality, and ward filtering if data is available
        return matchesProvince;
      }),
    };

    L.geoJSON(filteredGeoJSON, {
      style: provinceStyle,
      onEachFeature: (feature, layer) => {
        layer.on("mouseover", () => layer.setStyle(provinceHighlightStyle));
        layer.on("mouseout", () => layer.setStyle(provinceStyle));

        if (feature.properties && feature.properties.name) {
          layer.bindTooltip(feature.properties.name, {
            permanent: false,
            direction: "center",
            className: "province-tooltip",
          });
        }

        layer.bindPopup(
          `<b>${feature.properties.title_en} Province </b><br><b>${feature.properties.title_ne}  प्रदेश</b><br>Province : ${feature.id}`
        );
      },
    }).addTo(mapRef.current);
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prevFilters) => ({
      ...prevFilters,
      [name]: value,
    }));
    renderGeoJSON(); // Re-render GeoJSON with updated filters
  };

  return (
    <div>
      <div style={{ marginBottom: "10px", padding: "10px" }}>
        <label>
          Fiscal Year:
          <select name="fiscalYear" onChange={handleFilterChange} value={filters.fiscalYear}>
            <option value="All">All</option>
            {fiscalYears.map((year) => (
              <option key={year} value={year}>
                {year}
              </option>
            ))}
          </select>
        </label>
        <label>
          Province:
          <select name="province" onChange={handleFilterChange} value={filters.province}>
            <option value="All">All</option>
            {provinces.map((province) => (
              <option key={province} value={province}>
                {province}
              </option>
            ))}
          </select>
        </label>
        <label>
          District:
          <select name="district" onChange={handleFilterChange} value={filters.district}>
            <option value="All">All</option>
            {districts.map((district) => (
              <option key={district} value={district}>
                {district}
              </option>
            ))}
          </select>
        </label>
        <label>
          Municipality:
          <select name="municipality" onChange={handleFilterChange} value={filters.municipality}>
            <option value="All">All</option>
            {municipalities.map((municipality) => (
              <option key={municipality} value={municipality}>
                {municipality}
              </option>
            ))}
          </select>
        </label>
        <label>
          Ward:
          <select name="ward" onChange={handleFilterChange} value={filters.ward}>
            <option value="All">All</option>
            {wards.map((ward) => (
              <option key={ward} value={ward}>
                {ward}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div id="map" style={{ height: "75vh", width: "100vw" }}></div>
    </div>
  );
};

export default LeafletMap;
