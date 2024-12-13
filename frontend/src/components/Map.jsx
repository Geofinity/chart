import { useEffect, useRef } from "react";
import L from "leaflet";
import province from "../data/geojson/province.geojson.json";

const Map = () => {
  const mapRef = useRef();

  useEffect(() => {
    if (!mapRef.current) {
      mapRef.current = L.map("map").setView([28.232, 83.979], 9);

      L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }).addTo(mapRef.current);

      // Style for provinces
      const provinceStyle = {
        color: "#3388ff",
        weight: 2,
        fillOpacity: 0.5,
      };

      const provinceHighlightStyle = {
        color: "#ff7800",
        weight: 3,
        fillOpacity: 0.7,
      };

      // Add GeoJSON layer
      L.geoJSON(province, {
        style: provinceStyle,
        onEachFeature: (feature, layer) => {
          // Hover interaction for styling
          layer.on("mouseover", () => {
            layer.setStyle(provinceHighlightStyle);
          });

          layer.on("mouseout", () => {
            layer.setStyle(provinceStyle);
          });

          // Bind tooltip for province name
          if (feature.properties && feature.properties.name) {
            layer.bindTooltip(feature.properties.name, {
              permanent: false, // Tooltip only appears on hover
              direction: "center", // Centered tooltip
              className: "province-tooltip", // Custom CSS class for styling
            });
          }

          // Optional: Bind popup for more details
          layer.bindPopup(
            `<b>${feature.properties.name}</b><br>Population: ${feature.properties.population}<br>Province ID: ${feature.id}`
          );
        },
      }).addTo(mapRef.current);
    }

    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, []);

  return <div id="map" className="mx-24" style={{ height: "100vh" }}></div>;
};

export default Map;
