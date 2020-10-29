function onEachFeature(feature, layer) {
    layer.bindPopup(`<strong>Nome do local:</strong> ${feature.properties.name}
                    <hr>
                    <strong>Descrição:</strong> ${feature.properties.comments}<br>
                    <hr>
                    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#">Editar</button>
                    <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#">Deletar</button>
                    `);
}

$.get('/api/locals').done(function (data) {
    // region init
    let map = L.map('map').setView([-23.550394, -46.633947], 12); // Coords: Marco Zero de SP
    map.locate({setView: true, maxZoom: 15}); // Get current location
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Dados do Mapa: &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagens por: © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoiYXJjbGlnaHRtYXQiLCJhIjoiY2tncHV5d2F0MWJoYTJxcDl2d2VtbzR5eiJ9.jQZU37rYZi96-KuO6w8vGw'
    }).addTo(map);
    map.on('click', function onMapClick(e) {
        let popup = L.popup();
        popup
            .setLatLng(e.latlng)
            .setContent('Deseja criar um novo local aqui?<hr><button type="button" class="btn btn-primary" data-toggle="modal" data-target="#createModal">Criar local</button>')
            .openOn(map);
        document.getElementById('lat').value = e.latlng.lat;
        document.getElementById('lon').value = e.latlng.lng;
    });
    // endregion
    // region icons
    let AccessibilityIcon = L.Icon.extend({
        options: {
            iconSize: [48, 48],
            popupAnchor: [0, 10]
        }
    })
    let blueIcon = new AccessibilityIcon({iconUrl: '/static/generic/Accessibility_BLUE.svg'});
    let yellowIcon = new AccessibilityIcon({iconUrl: '/static/generic/Accessibility_YELLOW.svg'});
    let redIcon = new AccessibilityIcon({iconUrl: '/static/generic/Accessibility_RED.svg'});
    // endregion

    L.control.scale().addTo(map);
    L.geoJSON(data, {
        pointToLayer: function (feature, latlng) {
            if (feature.properties.rank === 1)
                return L.marker(latlng, {icon: redIcon});
            else if (feature.properties.rank === 2)
                return L.marker(latlng, {icon: yellowIcon});
            else
                return L.marker(latlng, {icon: blueIcon});
        },
        onEachFeature: onEachFeature
    }).addTo(map);
});