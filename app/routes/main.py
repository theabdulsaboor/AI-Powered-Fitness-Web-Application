from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user, login_user
from app.models.user import User
from app.models.workout_plan import WorkoutPlan
from app.models.workout_generator import WorkoutGenerator
from app import db
from app.workout_profiles import WORKOUT_PROFILES

bp = Blueprint('main', __name__)
workout_generator = WorkoutGenerator()

@bp.route('/')
def index():
    return render_template('main/index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    workout_plans = WorkoutPlan.query.filter_by(user_id=current_user.id).order_by(WorkoutPlan.created_at.desc()).all()
    return render_template('main/dashboard.html', workout_plans=workout_plans, WORKOUT_PROFILES=WORKOUT_PROFILES)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.age = request.form.get('age')
        current_user.gender = request.form.get('gender')
        current_user.fitness_goal = request.form.get('fitness_goal')
        current_user.fitness_level = request.form.get('fitness_level')
        current_user.equipment = request.form.get('equipment')
        current_user.days_per_week = request.form.get('days_per_week')
        
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('main.profile'))
    
    return render_template('main/profile.html')

@bp.route('/profile-setup')
@login_required
def profile_setup():
    # Check if user has already completed their profile
    if all([current_user.age, current_user.gender, current_user.fitness_goal, 
            current_user.fitness_level, current_user.equipment, current_user.days_per_week]):
        return redirect(url_for('main.dashboard'))
    return render_template('main/profile_setup.html')

@bp.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    # Update user profile with form data
    current_user.age = request.form.get('age')
    current_user.gender = request.form.get('gender')
    current_user.fitness_goal = request.form.get('fitness_goal')
    current_user.fitness_level = request.form.get('fitness_level')
    current_user.equipment = request.form.get('equipment')
    current_user.days_per_week = request.form.get('days_per_week')
    
    db.session.commit()
    
    # Generate workout plan
    user_data = {
        'age': current_user.age,
        'gender': current_user.gender,
        'fitness_goal': current_user.fitness_goal,
        'fitness_level': current_user.fitness_level,
        'equipment': current_user.equipment,
        'days_per_week': current_user.days_per_week
    }
    
    workout_plan_data = workout_generator.generate_workout_plan(user_data)
    
    workout_plan = WorkoutPlan(
        user_id=current_user.id,
        workout_profile=workout_plan_data['workout_profile'],
        model_version=workout_plan_data['model_version'],
        confidence_score=workout_plan_data['confidence_score']
    )
    
    db.session.add(workout_plan)
    db.session.commit()
    
    flash('Your profile has been updated and your workout plan has been generated!', 'success')
    return redirect(url_for('main.dashboard'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('main.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.')
            return redirect(url_for('main.register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Registration successful! Let\'s set up your profile.', 'success')
        return redirect(url_for('main.profile_setup'))
    
    return render_template('main/register.html')

@bp.route('/generate-workout', methods=['GET', 'POST'])
@login_required
def generate_workout():
    if request.method == 'POST':
        # Check if user has completed their profile
        if not all([current_user.age, current_user.gender, current_user.fitness_goal, 
                   current_user.fitness_level, current_user.equipment, current_user.days_per_week]):
            flash('Please complete your profile before generating a workout plan.')
            return redirect(url_for('main.profile'))
        
        user_data = {
            'age': current_user.age,
            'gender': current_user.gender,
            'fitness_goal': current_user.fitness_goal,
            'fitness_level': current_user.fitness_level,
            'equipment': current_user.equipment,
            'days_per_week': current_user.days_per_week
        }
        
        workout_plan_data = workout_generator.generate_workout_plan(user_data)
        
        workout_plan = WorkoutPlan(
            user_id=current_user.id,
            workout_profile=workout_plan_data['workout_profile'],
            model_version=workout_plan_data['model_version'],
            confidence_score=workout_plan_data['confidence_score']
        )
        
        db.session.add(workout_plan)
        db.session.commit()
        
        return jsonify(workout_plan.to_dict())
    
    return render_template('main/generate_workout.html', WORKOUT_PROFILES=WORKOUT_PROFILES)

@bp.route('/delete-workout/<int:plan_id>', methods=['POST'])
@login_required
def delete_workout(plan_id):
    workout_plan = WorkoutPlan.query.get_or_404(plan_id)
    
    # Ensure the user owns this workout plan
    if workout_plan.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(workout_plan)
    db.session.commit()
    
    return jsonify({'message': 'Workout plan deleted successfully'}) 