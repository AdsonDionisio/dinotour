document.addEventListener("DOMContentLoaded", function() {
    // Inicialização do mapa no centro da Paraíba/Sousa (pode ser ajustado)
    // Coordenadas aproximadas de Sousa: -6.7578, -38.2268
    var map = L.map('map').setView([-6.7578, -38.2268], 11);

    // Tiles (estilo 'terrain/outdoors' para remeter ao layout da montanha e relevo)
    L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
        maxZoom: 17,
        attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a>'
    }).addTo(map);

    var markers = [];

    // Busca os dados dos sítios da nossa API
    fetch('/api/sites')
        .then(response => response.json())
        .then(data => {
            var templateHtml = document.getElementById("popup-template").innerHTML;
            var redIcon = new L.Icon({
                iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
                shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowSize: [41, 41]
            });

            data.forEach(site => {
                var markerOptions = { title: site.name };
                
                // Se não houver video link ou for '#' (padrão do backend quando vazio), aplicamos o ícone vermelho
                if (!site.youtube_url || site.youtube_url === '#' || site.youtube_url.trim() === '') {
                    markerOptions.icon = redIcon;
                }
                
                var marker = L.marker([site.latitude, site.longitude], markerOptions).addTo(map);
                
                // Adiciona um pequeno balão tooltip que aparece imediatamente no HOVER
                marker.bindTooltip(site.name, {direction: 'top', offset: [0, -10]});
                
                // Formata os botões de ação e dados no Template do popup
                // Se o youtube link estiver vazio, usamos um fallback visual
                var ytLink = site.youtube_url && site.youtube_url !== '#' ? site.youtube_url : '#';
                
                // Criar Link do Gmaps "Traçar Rota"
                var gmapsLink = `https://www.google.com/maps/dir/?api=1&destination=${site.latitude},${site.longitude}`;
                var photoTag = site.photo_url ? `<img src="${site.photo_url}" style="width:100%; height:100%; object-fit:cover;">` : `<img src="/static/img/indisponivel.png" style="width:100%; height:100%; object-fit:cover;" alt="Imagem indisponível">`;
                
                var vrButton = site.vr_url ? `<a href="${site.vr_url}" target="_blank" class="btn-secondary" style="background:#5d6148; color:#fff;">🌎 Entrar em 360°</a>` : '';

                var content = templateHtml
                                .replace('{photo_content}', photoTag)
                                .replace('{title}', site.name)
                                .replace('{desc}', site.description || '')
                                .replace('{youtube_link}', ytLink)
                                .replace('{gmaps_link}', gmapsLink)
                                .replace('{vr_button}', vrButton);

                marker.bindPopup(content);
                markers.push(marker);
            });
            
            // Auto ajusta o zoom/bound caso haja marcadores
            if (markers.length > 0) {
                var group = new L.featureGroup(markers);
                map.fitBounds(group.getBounds().pad(0.1));
            }
        });
});
