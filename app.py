from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-testing')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///themes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False)
    primary_color = db.Column(db.String(20), nullable=False)
    secondary_color = db.Column(db.String(20), nullable=False)
    text_color = db.Column(db.String(20), nullable=False)
    background_color = db.Column(db.String(20), nullable=False)
    accent_color = db.Column(db.String(20), nullable=True)
    preview_image = db.Column(db.String(200), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'text_color': self.text_color,
            'background_color': self.background_color,
            'accent_color': self.accent_color,
            'preview_image': self.preview_image
        }

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    active_theme_id = db.Column(db.Integer, db.ForeignKey('theme.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    active_theme = db.relationship('Theme', backref='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Context processor to make active theme available in all templates
@app.context_processor
def inject_active_theme():
    active_theme = None
    active_theme_id = None
    
    if current_user.is_authenticated:
        active_theme_id = current_user.active_theme_id
        if active_theme_id:
            active_theme = Theme.query.get(active_theme_id)
    elif 'theme_id' in session:
        active_theme_id = session['theme_id']
        active_theme = Theme.query.get(active_theme_id)
        
    return {'active_theme': active_theme, 'active_theme_id': active_theme_id}

# Routes
@app.route('/')
def index():
    themes = Theme.query.all()
    return render_template('index.html', themes=themes)

@app.route('/theme/<int:theme_id>')
def theme_detail(theme_id):
    theme = Theme.query.get_or_404(theme_id)
    return render_template('theme_detail.html', theme=theme)

@app.route('/apply_theme/<int:theme_id>', methods=['POST'])
def apply_theme(theme_id):
    theme = Theme.query.get_or_404(theme_id)
    
    if current_user.is_authenticated:
        current_user.active_theme_id = theme_id
        db.session.commit()
    else:
        session['theme_id'] = theme_id
        session.modified = True  # Ensure the session is saved
    
    # Check if this is an AJAX request
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    # Return a redirect response for non-AJAX requests
    if not is_ajax:
        return redirect(url_for('index'))
    
    # Return JSON for AJAX requests
    return jsonify({'success': True, 'message': 'Theme applied successfully'})

@app.route('/api/themes')
def api_themes():
    themes = Theme.query.all()
    return jsonify([theme.to_dict() for theme in themes])

@app.route('/api/theme/<int:theme_id>')
def api_theme(theme_id):
    theme = Theme.query.get_or_404(theme_id)
    return jsonify(theme.to_dict())

# User management routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash('Successfully logged in!', 'success')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('Invalid username or password', 'error')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('register.html')
            
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
            
        user = User(username=username)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Registration successful!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration', 'error')
            return render_template('register.html')
            
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/themes')
def themes():
    all_themes = Theme.query.all()
    return render_template('themes.html', themes=all_themes)

@app.route('/set_theme', methods=['POST'])
def set_theme():
    theme_id = request.form.get('theme_id')
    if theme_id:
        theme = Theme.query.get_or_404(theme_id)
        if current_user.is_authenticated:
            current_user.active_theme_id = theme.id
            db.session.commit()
        else:
            session['theme_id'] = theme.id
            
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': 'Theme applied successfully'})
            
    return redirect(url_for('themes'))

def init_db():
    with app.app_context():
        db.create_all()
        
        # Only add sample data if the themes table is empty
        if Theme.query.count() == 0:
            sample_themes = [
                Theme(
                    name='Dark Theme',
                    description='A sleek dark theme that\'s easy on the eyes',
                    category='dark',
                    primary_color='#2b2b2b',
                    secondary_color='#3a3a3a',
                    text_color='#ffffff',
                    background_color='#1a1a1a',
                    accent_color='#0080ff'
                ),
                Theme(
                    name='Light Theme',
                    description='A clean, bright theme for daytime use',
                    category='light',
                    primary_color='#ffffff',
                    secondary_color='#f0f0f0',
                    text_color='#333333',
                    background_color='#f8f8f8',
                    accent_color='#0080ff'
                ),
                Theme(
                    name='Sunset Orange',
                    description='Warm orange tones inspired by sunset',
                    category='color',
                    primary_color='#ff7700',
                    secondary_color='#ff9944',
                    text_color='#ffffff',
                    background_color='#331100',
                    accent_color='#ffcc00'
                ),
                Theme(
                    name='Ocean Blue',
                    description='Cool blue tones inspired by the ocean',
                    category='color',
                    primary_color='#0066cc',
                    secondary_color='#0099ff',
                    text_color='#ffffff',
                    background_color='#003366',
                    accent_color='#00ccff'
                ),
                Theme(
                    name='Forest Green',
                    description='Refreshing green tones inspired by forests',
                    category='color',
                    primary_color='#006633',
                    secondary_color='#009933',
                    text_color='#ffffff',
                    background_color='#003300',
                    accent_color='#66cc33'
                ),
                Theme(
                    name='Purple Rain',
                    description='Rich purple tones inspired by twilight',
                    category='dark',
                    primary_color='#6600cc',
                    secondary_color='#9933ff',
                    text_color='#ffffff',
                    background_color='#330066',
                    accent_color='#cc99ff'
                ),
                Theme(
                    name='Ruby Red',
                    description='Deep red tones for a bold look',
                    category='color',
                    primary_color='#cc0000',
                    secondary_color='#ff3333',
                    text_color='#ffffff',
                    background_color='#660000',
                    accent_color='#ff9999'
                ),
                Theme(
                    name='Mint Fresh',
                    description='Soothing mint tones for a fresh feel',
                    category='light',
                    primary_color='#00cc99',
                    secondary_color='#33ffcc',
                    text_color='#333333',
                    background_color='#e6fff9',
                    accent_color='#00ffcc'
                ),
                Theme(
                    name='Midnight Blue',
                    description='Deep blue tones for night mode',
                    category='dark',
                    primary_color='#000033',
                    secondary_color='#000066',
                    text_color='#ffffff',
                    background_color='#000022',
                    accent_color='#0000cc'
                ),
                Theme(
                    name='Golden Hour',
                    description='Warm golden tones inspired by sunset',
                    category='light',
                    primary_color='#ffcc00',
                    secondary_color='#ffdd66',
                    text_color='#333333',
                    background_color='#fff9e6',
                    accent_color='#ffd700'
                ),
                Theme(
                    name='Neon Dreams',
                    description='Vibrant neon colors for a cyberpunk feel',
                    category='dark',
                    primary_color='#ff00ff',
                    secondary_color='#00ffff',
                    text_color='#ffffff',
                    background_color='#000033',
                    accent_color='#ff00cc'
                ),
                Theme(
                    name='Coffee Break',
                    description='Warm brown tones inspired by coffee',
                    category='light',
                    primary_color='#996633',
                    secondary_color='#cc9966',
                    text_color='#333333',
                    background_color='#fff5e6',
                    accent_color='#ffcc99'
                ),
                Theme(
                    name='Arctic Frost',
                    description='Cool, icy blues and whites for a crisp, clean look',
                    category='light',
                    primary_color='#e0f7fa',
                    secondary_color='#b2ebf2',
                    text_color='#006064',
                    background_color='#ffffff',
                    accent_color='#00bcd4'
                ),
                Theme(
                    name='Emerald City',
                    description='Rich emerald greens with gold accents',
                    category='color',
                    primary_color='#2e7d32',
                    secondary_color='#388e3c',
                    text_color='#ffffff',
                    background_color='#1b5e20',
                    accent_color='#ffd700'
                ),
                Theme(
                    name='Desert Sunset',
                    description='Warm desert tones with pink and orange hues',
                    category='color',
                    primary_color='#ff9e80',
                    secondary_color='#ff6e40',
                    text_color='#ffffff',
                    background_color='#bf360c',
                    accent_color='#ff3d00'
                )
            ]
            
            for theme in sample_themes:
                db.session.add(theme)
                
            db.session.commit()
            print("Database initialized with sample themes")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)