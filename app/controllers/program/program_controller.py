from flask import Blueprint, request,jsonify
from app.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND
from app.models.program.program_model import Program
from app.extensions import db
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity,create_refresh_token

programs = Blueprint('programs', __name__, url_prefix='/api/v1/programs')

@programs.route('/register', methods = ['POST'])
def register_program():
    
    data = request.json
    
    type = data.get(type)
    duration = data.get(duration)
    

    try:
        if not type or not duration :
            return jsonify({
                'error': 'All feilds required'
            }), HTTP_400_BAD_REQUEST
            
            # creating a new program
            
        new_program = Program(
                type =type, 
                duration= duration)
            
        db.session.add(new_program)
        db.session.commit()
        db.session.refresh(new_program)
        db.session.rollback()
            
            # keeping track of program name
        new_program = new_program.program_info()
            
    except Exception as e:
        db.session.rollback()
        return jsonify({
                'error': str(e)
            }), HTTP_500_INTERNAL_SERVER_ERROR
        

# Updating program details

@programs.route('/edit/<int:id>', methods=['PUT'])
@jwt_required()
def update_program(id):
    
    try:
        
        current_program = get_jwt_identity()
        logined_in_program = program.query.filter_by(id=current_program).first()
        
        
        #  get authpor by id
        program = Program.query.filter_by(id=id).first()
        
        if not program:
            return jsonify({
                'error':'Program not found'
            }), HTTP_400_BAD_REQUEST
            
            
            
        else:
            type = request.get_json().get('type',program.type)
            duration =  request.get_json().get('duration',program.duration)
                
            if type != program.type and program.query.filter_by(type=type).first():
                return jsonify({
                    'error':'Course type already in use'
                }), HTTP_409_CONFLICT
           
           
            program.type = type
            program.duration = duration
            
            
            db.session.commit()
            
            program_name = Program.program_info()
            
            return jsonify({
                'message':program_name + "'s details have been successfully updated",
                'program':{
                    'id':program.id,
                    'type':program.type,
                    'duration':program.duration,
                    
            }
            })
            
         
            
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }),HTTP_404_NOT_FOUND

