# importing libraries
from app.extensions import db
from datetime import datetime

# class for the student model
class Program(db.Model):
    __tablename__ = 'programs'
    
    id = db.Column(db.Integer, primary_key=True, nullable = False)
    type = db.Column(db.String(200), nullable = False)
    duration = db.Column(db.String(20), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    updated_at = datetime.utcnow
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id') )
    course = db.relationship('Course', backref= 'programs')
    
    def __init__(self, type,duration, course_id):
        super(Program,self).__init__()
        self.type = type
        self.duration = duration
        course_id = course_id
        
        
    
    def program_info(self):
            
            return(f'{self.type} {self.duration}')
        
       
        
        