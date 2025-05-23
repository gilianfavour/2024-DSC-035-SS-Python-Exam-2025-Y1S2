from app.extensions import db
from datetime import datetime

class Course(db.Model):
    __tablename__ = 'courses'
    
    id =db.Column(db.Integer, primary_key = True, nullable = False)
    course_code= db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255), nullable = False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id') )
    program = db.relationship('Program', backref= 'courses')
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate =datetime.utcnow)
       
   
    
    def __init__(self, course_code,description, program_id):
        super(Course,self).__init__()
        self.course_code  = course_code 
        self.description = description
        self.program_id = program_id
       
        
    def course_info(self):
        return f'{self.course_code} {self.description}'