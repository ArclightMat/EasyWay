const csrftoken = getCookie('csrftoken');
const formaction = document.getElementById('manage_local').action;
const apikey = 'pk.eyJ1IjoiYXJjbGlnaHRtYXQiLCJhIjoiY2tncHV5d2F0MWJoYTJxcDl2d2VtbzR5eiJ9.jQZU37rYZi96-KuO6w8vGw';
let control, map, current_latlng;
let dirty = false;

function hideAlert(id) {
    if (id !== undefined) {
        $.ajax({
            url: 'api/user/' + id,
            type: 'PATCH',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: {
                'show_alerts': false,
            },
        })
    }
}

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
            map.closePopup();
        }
    });
}

function onLocationFound(e) {
    current_latlng = e.latlng;
}

function setRoute(id) {
    $.ajax({
        url: '/api/locals/' + id,
        type: 'GET',
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function (data) {
            data = data.features[0]; // Gets first (and only) feature inside the FeatureCollection
            let latlng = {'lat': data.geometry.coordinates[1], 'lng': data.geometry.coordinates[0]};
            if (current_latlng !== undefined)
                control.spliceWaypoints(0, 1, current_latlng);
            control.spliceWaypoints(1, 1, latlng);
            map.closePopup();
        }
    });

}

function onEachFeature(feature, layer) {
    if (user === undefined)
        layer.bindPopup(`<strong>Nome do local:</strong> ${feature.properties.name}
                    <hr>
                    <strong>Descrição:</strong> ${feature.properties.comments}<br>
                    <hr>
                    <button type="button" class="btn btn-primary" onclick="setRoute(${feature.properties.pk})">Ir</button>
                    `);

    else
        layer.bindPopup(`<strong>Nome do local:</strong> ${feature.properties.name}
                    <hr>
                    <strong>Descrição:</strong> ${feature.properties.comments}<br>
                    <hr>
                    <button type="button" class="btn btn-primary" onclick="setRoute(${feature.properties.pk})">Ir</button>
                    <button type="button" class="btn btn-warning" onclick="loadForm(${feature.properties.pk})" data-toggle="modal" data-target="#createModal">Editar</button>
                    <button type="button" class="btn btn-danger" onclick="deleteLocal(${feature.properties.pk})">Deletar</button>
                    `);
}

$.get('/api/locals').done(function (data) {
    // region init
    map = L.map('map').setView([-23.550394, -46.633947], 12); // Coords: Marco Zero de SP
    map.locate({setView: true, maxZoom: 15}); // Get current location
    map.on('locationfound', onLocationFound);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Dados do Mapa: &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagens por: © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: apikey
    }).addTo(map);
    map.on('click', function onMapClick(e) {
        if (dirty) {
            document.getElementById('manage_local').action = formaction;
            document.getElementById('manage_local').reset();
            dirty = false;
        }
        let popup = L.popup();
        if (user === undefined)
            popup
                .setLatLng(e.latlng)
                .setContent('Para criar um novo local, faça login.')
                .openOn(map);
        else
            popup
                .setLatLng(e.latlng)
                .setContent('Deseja criar um novo local aqui?<hr><button type="button" class="btn btn-primary" data-toggle="modal" data-target="#createModal">Criar local</button>')
                .openOn(map);
        document.getElementById('lat').value = e.latlng.lat;
        document.getElementById('lon').value = e.latlng.lng;
    });
    control = L.Routing.control({
        router: L.Routing.mapbox(apikey),
        geocoder: L.Control.Geocoder.mapbox(apikey),
        waypoints: [null]
    }).addTo(map);
    // endregion
    // region icons
    let AccessibilityIcon = L.Icon.extend({
        options: {
            iconSize: [48, 48],
            popupAnchor: [0, 10]
        }
    })
    let blueIcon = new AccessibilityIcon({iconUrl: '/static/geo/images/Accessibility_BLUE.svg'});
    let yellowIcon = new AccessibilityIcon({iconUrl: '/static/geo/images/Accessibility_YELLOW.svg'});
    let redIcon = new AccessibilityIcon({iconUrl: '/static/geo/images/Accessibility_RED.svg'});
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