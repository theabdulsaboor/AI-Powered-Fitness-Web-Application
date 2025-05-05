from app import db
from datetime import datetime
import pytz

class WorkoutPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Workout profile
    workout_profile = db.Column(db.Integer)
    
    # AI model metadata
    model_version = db.Column(db.String(20))
    confidence_score = db.Column(db.Float)
    
    def to_dict(self):
        # Convert UTC to local time
        local_tz = pytz.timezone('Asia/Karachi')  # Pakistan timezone
        local_time = self.created_at.replace(tzinfo=pytz.UTC).astimezone(local_tz)
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': local_time.strftime('%Y-%m-%d %H:%M'),
            'workout_profile': self.workout_profile,
            'model_version': self.model_version,
            'confidence_score': self.confidence_score
        } 