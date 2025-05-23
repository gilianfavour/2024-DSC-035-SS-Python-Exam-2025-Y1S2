from flask import Blueprint, request,jsonify
from app.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR
from app.models.course.course_model import Course
from app.extensions import db


courses = Blueprint('courses', __name__, url_prefix='/api/v1/courses')

@courses.route('/register', methods = ['POST'])
def register_course():
    
    data = request.json
    
    course_code = data.get('course_code')
    description = data.get('description')
    

    try:
        if not type or not course_code or not description :
            return jsonify({
                'error': 'All feilds required'
            }), HTTP_400_BAD_REQUEST
            
            # creating a new course
            
        new_course = Course(
                course_code =course_code, 
                description= description)
            
        db.session.add(new_course)
        db.session.commit()
        db.session.refresh(new_course)
        db.session.rollback()
            
            # keeping track of course name
        new_course = new_course.course_info()
            
    except Exception as e:
        db.session.rollback()
        return jsonify({
                'error': str(e)
            }), HTTP_500_INTERNAL_SERVER_ERROR
        
