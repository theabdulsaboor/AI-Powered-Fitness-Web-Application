from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.workout_plan import WorkoutPlan
import sqlite3
from functools import wraps
from app.workout_profiles import WORKOUT_PROFILES

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
@admin_required
def index():
    users_count = User.query.count()
    plans_count = WorkoutPlan.query.count()
    return render_template('admin/index.html', users_count=users_count, plans_count=plans_count)

@bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/users/<int:user_id>')
@login_required
@admin_required
def get_user_details(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'username': user.username,
        'email': user.email,
        'age': user.age,
        'gender': user.gender,
        'fitness_goal': user.fitness_goal,
        'fitness_level': user.fitness_level,
        'equipment': user.equipment,
        'days_per_week': user.days_per_week,
        'created_at': user.created_at.strftime('%Y-%m-%d %H:%M')
    })

@bp.route('/workout-plans')
@login_required
@admin_required
def workout_plans():
    plans = WorkoutPlan.query.all()
    return render_template('admin/workout_plans.html', plans=plans, WORKOUT_PROFILES=WORKOUT_PROFILES)

@bp.route('/workout-plans/<int:plan_id>', methods=['GET', 'DELETE'])
@login_required
@admin_required
def workout_plan_details(plan_id):
    plan = WorkoutPlan.query.get_or_404(plan_id)
    
    if request.method == 'DELETE':
        db.session.delete(plan)
        db.session.commit()
        return jsonify({'message': 'Workout plan deleted successfully'})
    
    return jsonify({
        'id': plan.id,
        'username': plan.user.username,
        'workout_profile': plan.workout_profile,
        'confidence_score': plan.confidence_score,
        'created_at': plan.created_at.strftime('%Y-%m-%d %H:%M')
    })

@bp.route('/sql-console', methods=['GET', 'POST'])
@login_required
@admin_required
def sql_console():
    if request.method == 'POST':
        query = request.form.get('query', '')
        try:
            # Execute the query
            result = db.session.execute(query)
            if result.returns_rows:
                rows = result.fetchall()
                columns = result.keys()
                return jsonify({
                    'success': True,
                    'data': [dict(zip(columns, row)) for row in rows]
                })
            else:
                db.session.commit()
                return jsonify({
                    'success': True,
                    'message': 'Query executed successfully'
                })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })
    
    return render_template('admin/sql_console.html') 