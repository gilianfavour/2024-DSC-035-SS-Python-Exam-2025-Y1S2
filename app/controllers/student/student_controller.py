# importing libraries
from flask import Blueprint, request,jsonify
from app.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST,HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from app.models.student.student_model import Student
import validators
from app.extensions import db
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity,create_refresh_token


# naming student blueprint
students = Blueprint('students', __name__, url_prefix='/api/v1/students')

# Register srudent
@students.route('/register', methods = ['POST'])
def register_student():
    
    data = request.json
    
    student_name = data.get(student_name)
    email = data.get(email)
    contact = data.get(contact)
    date_of_birth = data.get(date_of_birth)
    

    # validations
    try:
        if not student_name or not email or not contact or not date_of_birth:
            return jsonify({
                'error': 'All feilds required'
            }), HTTP_400_BAD_REQUEST
            
            
        if not validators.email(email):
            return jsonify({
                'error': 'Enter a valid email'
                }), HTTP_400_BAD_REQUEST
            
            # creating a new student
            
        new_student = Student(
                student_name =student_name, 
                email= email,
                contact = contact,
                date_of_birth = date_of_birth)
            
        db.session.add(new_student)
        db.session.commit()
        db.session.refresh(new_student)
        db.session.rollback()
            
            # keeping track of student name
        new_program = new_program.program_info()
            
    except Exception as e:
        db.session.rollback()
        return jsonify({
                'error': str(e)
            }), HTTP_500_INTERNAL_SERVER_ERROR
        
        
        
# Get all students
@students.get('/all')
def get_all_students():
    
    try:
        
        all_students = Student.query.all()
        
        students_data = []
        
        for student in all_students:
            student_info ={
                'student_name' :student.student_name, 
                'email': student.email,
                'contact' : student.contact,
                'date_of_birth' : student.date_of_birth,
                'program':[],
                'course':[]
                
            }
            
            if hasattr(student,'programs'):   #check if the attribute has the data we want to access.
                student_info['programs'] = [{   #use a list
                    'tyoe': program.tyoe,
                    'duration':program.duration
                }for program in student.books]
                
            if hasattr(student,'courses'):
                student_info['courses']= [{
                    'course_code':course.course_code,
                    'description':course.description,
                    'origin':course.origin,
                    } for course in student.companys]
                        
            students_data.append(student_info)
            
        return jsonify({
                'message': 'All students retrived successfully',
                'total_students':len(students_data),
                'author': students_data
                
            }),HTTP_200_OK
            
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
        


# deleting a student by id
@students.route('/delete/<int:id>', methods=['DELETE'])
def delete_student(id):
    
    try:
        
        current_student = get_jwt_identity()
        logined_in_student = Student.query.filter_by(id=current_student).first()
        
        
        #  get author by id
        student = Student.query.filter_by(id=id).first()
        
        if not student:
            return jsonify({
                'error':'Student not found'
            }), HTTP_400_BAD_REQUEST
            
        elif student.id == current_student:
            return jsonify({
                'error': 'You are not authorized to delete the details'
            }), HTTP_403_FORBIDDEN
            
            
        else:
          
          
          #loop to delete the user associated with courses
          for course in student.courses:
              db.session.delete(course)
            
            #loop to delete the user associated with books
          for program in student.programs:
              db.session.delete(program)
            
            
        db.session.delete(student)
        db.session.commit()
            
            
        return jsonify({
                'message':'student deleted succesfully',
                
            })
            
         
            
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }),HTTP_404_NOT_FOUND

