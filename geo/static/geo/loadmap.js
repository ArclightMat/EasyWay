function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
const formaction = document.getElementById('manage_local').action;
let dirty = false;

function deleteLocal(id) {
    $.ajax({
        url: '/api/locals/' + id,
        type: 'DELETE',
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function () {
            document.location.reload(true);
        }
    });
}

function loadForm(id) {
    $.ajax({
        url: '/api/locals/' + id,
        type: 'GET',
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function (data) {
            data = data.features[0]; // Gets first (and only) feature inside the FeatureCollection
            dirty = true;
            document.getElementById('manage_local').action = `${formaction}api/edit_local/${id}`;
            document.getElementById('name').value = data.properties.name;
            document.getElementById('comments').value = data.properties.comments;
            document.getElementById('rank').value = data.properties.rank;
            // GeoJSON coords are lon, lat:
            document.getElementById('lon').value = data.geometry.coordinates[0];
            document.getElementById('lat').value = data.geometry.coordinates[1];
        }
    });
}

function onEachFeature(feature, layer) {
    layer.bindPopup(`<strong>Nome do local:</strong> ${feature.properties.name}
                    <hr>
                    <strong>Descrição:</strong> ${feature.properties.comments}<br>
                    <hr>
                    <button type="button" class="btn btn-primary" onclick="loadForm(${feature.properties.pk})" data-toggle="modal" data-target="#createModal">Editar</button>
                    <button type="button" class="btn btn-danger" onclick="deleteLocal(${feature.properties.pk})">Deletar</button>
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
        if (dirty) {
            document.getElementById('manage_local').action = formaction;
            document.getElementById('manage_local').reset();
            dirty = false;
        }
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