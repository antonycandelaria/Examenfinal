
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from . import db
from .models import Vehicle

# Define tu Blueprint para las rutas API y frontend
api_bp = Blueprint('api', __name__)

# --- Rutas del frontend ---
@api_bp.route('/', methods=['GET'])
def home():
    """Ruta para la página de inicio."""
    return render_template('index.html')

@api_bp.route('/vehicles', methods=['GET'])
def vehicles_page():
    """Ruta para mostrar la lista de vehículos (frontend)."""
    vehicles = Vehicle.query.all()  # Obtener todos los vehículos de la base de datos
    return render_template('vehicles_details.html', vehicles=vehicles)  # Pasar los vehículos a la plantilla

@api_bp.route('/add', methods=['GET', 'POST'])
def add_vehicle_page():
    """Ruta para agregar vehículos desde el formulario del frontend."""
    if request.method == 'POST':
        try:
            data = request.form
            new_vehicle = Vehicle(
                brand=data['brand'],
                model=data['model'],
                year=int(data['year']),
                price_per_day=float(data['price_per_day'])
            )
            db.session.add(new_vehicle)
            db.session.commit()
            return redirect(url_for('api.vehicles_page'))
        except Exception as e:
            db.session.rollback()
            return render_template('error.html', message=f"Error al agregar vehículo: {str(e)}")
    return render_template('add_vehicle.html')

@api_bp.route('/api/vehicles', methods=['GET'])
def get_vehicles_api():
    try:
        vehicles = Vehicle.query.all()
        return jsonify([vehicle.to_dict() for vehicle in vehicles])
    except Exception as e:
        return jsonify({'error': f'Error fetching vehicles: {str(e)}'}), 500

@api_bp.route('/api/vehicles', methods=['POST'])
def add_vehicle_api():
    """API para agregar un nuevo vehículo desde un cliente externo."""
    try:
        data = request.get_json()
        new_vehicle = Vehicle(
            brand=data['brand'],
            model=data['model'],
            year=int(data['year']),
            price_per_day=float(data['price_per_day'])
        )
        db.session.add(new_vehicle)
        db.session.commit()
        return jsonify(new_vehicle.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api_bp.route('/delete_vehicle/<int:vehicle_id>', methods=['POST'])
def delete_vehicle(vehicle_id):
    # Lógica para eliminar el vehículo
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    flash('Vehículo eliminado con éxito', 'success')
    return redirect(url_for('api.vehicles_page'))
    

@api_bp.route('/api/vehicle/<int:vehicle_id>', methods=['GET'])
def vehicle_details(vehicle_id):
    """Ruta para mostrar los detalles de un vehículo específico."""
    vehicle = Vehicle.query.get(vehicle_id)  # Obtén el vehículo directamente desde la base de datos
    if vehicle:
        return render_template('vehicles_details.html', vehicle=vehicle)

    else:
        return "Vehicle not found", 404

@api_bp.route('/vehicle/update/<int:vehicle_id>', methods=['POST'])
def update_vehicle(vehicle_id):
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if vehicle:
            data = request.form
            vehicle.brand = data.get('brand', vehicle.brand)
            vehicle.model = data.get('model', vehicle.model)
            vehicle.year = data.get('year', vehicle.year)
            vehicle.availability_status = data.get('availability_status', vehicle.availability_status)
            vehicle.price_per_day = data.get('price_per_day', vehicle.price_per_day)
            
            db.session.commit()
            return redirect(url_for('api.vehicles_page', vehicle_id=vehicle.id))
        else:
            return jsonify({'error': 'Vehicle not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error updating vehicle: {str(e)}'}), 400