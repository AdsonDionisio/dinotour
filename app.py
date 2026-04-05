import os
import re
import uuid
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Site

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key' # In a real app, use a random environment variable
basedir = os.path.abspath(os.path.dirname(__name__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.config['UPLOAD_VR_FOLDER'] = os.path.join(basedir, 'static', 'vr_uploads')
os.makedirs(app.config['UPLOAD_VR_FOLDER'], exist_ok=True)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def dms2dd(dms_str):
    pattern = r"(\d+)°\s+(\d+)'\s+([\d,]+)\"\s+([NSWE])"
    match = re.search(pattern, dms_str)
    if not match:
        return 0.0
    
    degrees = float(match.group(1))
    minutes = float(match.group(2))
    seconds = float(match.group(3).replace(',', '.'))
    direction = match.group(4)
    
    dd = degrees + minutes/60 + seconds/3600
    
    if direction in ['S', 'W']:
        dd *= -1
        
    return dd

@app.cli.command("seed")
def seed_db():
    db.create_all()
    
    # Create Admin user
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin')
        admin.set_password('IntegraMaker2025')
        db.session.add(admin)
        print("Admin user created")
        
    # Sites data provided by user
    DADOS_BRUTOS = [
        ("Passagem das Pedras", "06° 44' 1,86\" S", "38° 15' 39,42\" W"),
        ("Lagoa dos Patos", "06° 45' 41,28\" S", "38° 14' 45,06\" W"),
        ("Piau-Caicara", "06° 44' 24,78\" S", "38° 19' 54,48\" W"),
        ("Pedregulho", "06° 45' 22,26\" S", "38° 20' 54,66\" W"),
        ("Piedade", "06° 44' 55,62\" S", "38° 20' 57,24\" W"),
        ("Serrote do Pimenta - Fazenda Estreito", "06° 43' 18,54\" S", "38° 11' 44,16\" W"),
        ("Matadouro", "06° 45' 6,78\" S", "38° 13' 42,96\" W"),
        ("Riacho do Caze - Riacho Santa Rosa", "06° 41' 48,06\" S", "38° 13' 57,48\" W"),
        ("Serrote da Bencao de Deus", "06° 42' 49,74\" S", "38° 14' 38,16\" W"),
        ("Floresta dos Borbas", "06° 41' 2,04\" S", "38° 20' 33,48\" W"),
        ("Saguim", "06° 43' 24,24\" S", "38° 20' 16,02\" W"),
        ("Varzea dos Ramos - Tapera", "06° 46' 9,48\" S", "38° 06' 40,38\" W"),
        ("Lagoa do Forno", "06° 48' 32,10\" S", "38° 10' 29,28\" W"),
        ("Fazenda Paraiso", "06° 48' 45,90\" S", "38° 09' 50,40\" W"),
        ("Mae D'agua", "06° 49' 19,20\" S", "38° 12' 2,70\" W"),
        ("Curral Velho", "06° 49' 0,78\" S", "38° 12' 21,42\" W"),
        ("Rio Novo", "06° 45' 18,06\" S", "38° 24' 35,70\" W"),
        ("Riacho Novo-Araca", "06° 44' 59,70\" S", "38° 24' 40,38\" W"),
        ("Juazeirinho-Zoador", "06° 44' 41,10\" S", "38° 25' 8,64\" W"),
        ("Barragem do Domicio", "06° 44' 9,90\" S", "38° 26' 17,28\" W"),
        ("Engenho Novo", "06° 42' 52,20\" S", "38° 24' 44,22\" W"),
        ("Pereiros", "06° 47' 18,66\" S", "38° 29' 11,82\" W"),
        ("Poco do Motor", "06° 44' 7,74\" S", "38° 15' 30,42\" W"),
        ("Serrote do Letreiro", "06° 41' 36,12\" S", "38° 18' 29,88\" W"),
        ("Cabra-Assada", "06° 49' 53,52\" S", "38° 23' 59,94\" W")
    ]
    
    for name, lat_dms, lng_dms in DADOS_BRUTOS:
        if not Site.query.filter_by(name=name).first():
            lat = dms2dd(lat_dms)
            lng = dms2dd(lng_dms)
            site = Site(name=name, description="Sítio Arqueológico / Paleontológico", latitude=lat, longitude=lng)
            db.session.add(site)
            print(f"Site Added: {name}")
            
    db.session.commit()
    print("Database seeded.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/sites')
def get_sites():
    sites = Site.query.all()
    sites_list = []
    for s in sites:
        sites_list.append({
            'id': s.id,
            'name': s.name,
            'description': s.description,
            'latitude': s.latitude,
            'longitude': s.longitude,
            'youtube_url': s.youtube_url or '#',
            'photo_url': url_for('static', filename='uploads/' + s.photo_filename) if s.photo_filename else None,
            'vr_url': url_for('vr_viewer', id=s.id) if s.image_vr_filename else None
        })
    return jsonify(sites_list)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Credenciais inválidas")
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    sites = Site.query.all()
    return render_template('admin.html', sites=sites)

@app.route('/admin/site/add', methods=['POST'])
@login_required
def add_site():
    name = request.form.get('name')
    description = request.form.get('description')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    youtube_url = request.form.get('youtube_url')
    
    photo_filename = None
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            filename = secure_filename(photo.filename)
            unique_name = f"{uuid.uuid4().hex}_{filename}"
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))
            photo_filename = unique_name
            
    photo_vr_filename = None
    if 'photo_vr' in request.files:
        photo_vr = request.files['photo_vr']
        if photo_vr.filename != '':
            filename = secure_filename(photo_vr.filename)
            unique_name = f"{uuid.uuid4().hex}_{filename}"
            photo_vr.save(os.path.join(app.config['UPLOAD_VR_FOLDER'], unique_name))
            photo_vr_filename = unique_name
    
    new_site = Site(name=name, description=description, 
                    latitude=float(latitude), longitude=float(longitude),
                    youtube_url=youtube_url, photo_filename=photo_filename, image_vr_filename=photo_vr_filename)
    db.session.add(new_site)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/site/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_site(id):
    site = Site.query.get_or_404(id)
    if request.method == 'POST':
        site.name = request.form.get('name')
        site.description = request.form.get('description')
        site.latitude = float(request.form.get('latitude'))
        site.longitude = float(request.form.get('longitude'))
        site.youtube_url = request.form.get('youtube_url')
        
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename != '':
                filename = secure_filename(photo.filename)
                unique_name = f"{uuid.uuid4().hex}_{filename}"
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))
                site.photo_filename = unique_name
                
        if 'photo_vr' in request.files:
            photo_vr = request.files['photo_vr']
            if photo_vr.filename != '':
                filename = secure_filename(photo_vr.filename)
                unique_name = f"{uuid.uuid4().hex}_{filename}"
                photo_vr.save(os.path.join(app.config['UPLOAD_VR_FOLDER'], unique_name))
                site.image_vr_filename = unique_name
                
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
        
    return render_template('edit_site.html', site=site)

@app.route('/admin/site/delete/<int:id>')
@login_required
def delete_site(id):
    site = Site.query.get_or_404(id)
    db.session.delete(site)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/vr/<int:id>')
def vr_viewer(id):
    site = Site.query.get_or_404(id)
    if not site.image_vr_filename:
        return "Este sítio ainda não possui imagem 360", 404
    return render_template('vr.html', site=site)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
