# importing libraries
from app.extensions import db
from datetime import datetime

# class for the student model
class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True, nullable = False)
    student_name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(255), nullable = False)
    contact = db.Column(db.Integer, nullable = False)
    date_of_birth = db.Column(db.String, nullable = False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id') )
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    program = db.relationship('Program', backref= 'students')
    course =db.relationship('Course', backref ='students')
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def __init__(self, student_name,email, contact, date_of_birth, course_id, program_id):
        super(Student,self).__init__()
        self.student_name = student_name
        self.email = email
        self.contact = contact
        self.date_of_birth = date_of_birth
        self.course_id = course_id
        self.program_id = program_id
        
    
    def student_info(self):
            
            return(f'{self.student_name} {self.email}')