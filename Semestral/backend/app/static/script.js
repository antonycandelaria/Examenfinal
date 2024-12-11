document.addEventListener('DOMContentLoaded', function () {
    // Cargar los vehículos al inicio
    loadVehicles();

    // Configurar el botón de actualización de la lista
    const updateBtn = document.getElementById('update-btn');
    if (updateBtn) {
        updateBtn.addEventListener('click', loadVehicles);
    }
});

// Función para mostrar el indicador de carga
function showLoading() {
    document.getElementById('loading-indicator').style.display = 'block';
}

// Función para ocultar el indicador de carga
function hideLoading() {
    document.getElementById('loading-indicator').style.display = 'none';
}

// Función para cargar los vehículos
function loadVehicles() {
    showLoading();  // Mostrar el indicador de carga

    fetch('/api/vehicles')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const vehicleList = document.querySelector('#vehicle-list tbody');
            if (!vehicleList) {
                throw new Error('No se encontró el elemento con ID "vehicle-list".');
            }
            vehicleList.innerHTML = ''; // Limpiar la tabla antes de llenarla nuevamente
            data.forEach(vehicle => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${vehicle.id}</td>
                    <td>${vehicle.brand}</td>
                    <td>${vehicle.model}</td>
                    <td>${vehicle.year}</td>
                    <td>${vehicle.price_per_day}</td>
                    <td>
                        <a href="/vehicles/${vehicle.id}">Detalles</a> |
                        <a href="#" class="delete-btn" data-id="${vehicle.id}" data-url="{{ url_for('api.delete_vehicle', vehicle_id=vehicle.id) }}">Eliminar</a>
                    </td>
                `;
                vehicleList.appendChild(row);
            });

            // Agregar eventos de eliminación
            document.querySelectorAll('.delete-btn').forEach(function (button) {
                button.addEventListener('click', function (e) {
                    e.preventDefault();
                    const vehicleId = button.getAttribute('data-id');
                    if (confirm('¿Estás seguro de que deseas eliminar este vehículo?')) {
                        deleteVehicle(vehicleId);
                    }
                });
            });
        })
        .catch(error => {
            console.error('Error al cargar los vehículos:', error);
            alert(`Ocurrió un error al cargar los vehículos: ${error.message}`);
        })
        .finally(() => {
            hideLoading();  // Ocultar el indicador de carga después de la respuesta
        });
}

// Función para eliminar un vehículo
function deleteVehicle(vehicleId) {
    showLoading();  // Mostrar el indicador de carga

    fetch(`/delete_vehicle/${vehicleId}`, {  // Usamos la URL corregida
        method: 'GET'  // Se espera un método GET porque el backend usa GET para eliminar (de acuerdo con tu código)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.message === 'Vehicle deleted') {
                alert('Vehículo eliminado correctamente');
                loadVehicles(); // Recargar la lista de vehículos
            } else {
                alert('Hubo un error al eliminar el vehículo');
            }
        })
        .catch(error => {
            console.error('Error al eliminar el vehículo:', error);
            alert(`Error al eliminar el vehículo: ${error.message}`);
        })
        .finally(() => {
            hideLoading();  // Ocultar el indicador de carga después de la eliminación
        });
}

