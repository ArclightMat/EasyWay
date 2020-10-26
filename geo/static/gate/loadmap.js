let marcozero = [-23.550394, -46.633947]; // Marco Zero de São Paulo
let map = L.map('map').setView(marcozero, 12);
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Dados do Mapa: &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagens por: © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoiYXJjbGlnaHRtYXQiLCJhIjoiY2tncHV5d2F0MWJoYTJxcDl2d2VtbzR5eiJ9.jQZU37rYZi96-KuO6w8vGw'
}).addTo(map);
L.control.scale().addTo(map)
L.marker(marcozero).bindPopup('Marco Zero de Sâo Paulo').addTo(map);