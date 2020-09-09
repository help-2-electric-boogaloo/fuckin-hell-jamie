from app.classes.Database import Database
from app.classes.Upload import Upload
from app.models.User import User
from flask import session
from flask import current_app as flask_app
import uuid, time

class Image():

    def __init__(self):
        return None

    def get_images(self, limit=20):
        
        error = None
        images = False
        
        try:
            database = Database()
            images = database.get_images(limit)

        except Exception as err:
            flask_app.logger.info(err)
            error = err

        if error:
            raise Exception(error)
        else:
            return images

    def get_user_images(self, limit=20):
        
        error = None
        images = False
        user_id = False
        if (session['user'] and session['user']['localId']):
            user_id = session['user']['localId']
        try:
            database = Database()
            images = database.get_images(limit, user_id)

        except Exception as err:
            flask_app.logger.info(err)
            error = err

        if error:
            raise Exception(error)
        else:
            return images

    def upload(self, request):
        
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        tags = request.form['tags']
        image_filter = request.form['filter']

        # Validates required registration fields
        error = None
        user_id = False

        if (session['user'] and session['user']['localId']):
            user_id = session['user']['localId']
        else: 
            error = 'You must be logged in to upload an image.'

        if 'image' not in request.files:
            error = 'A file is required.'
        else:
            file = request.files['image']
        
        if not error:
            if file.filename == '':
                error = 'A file is required.'
            elif not name:
                error = 'An name is required.'
            elif not description:
                error = 'A description is required.'
            elif not category:
                error = 'A category is required.'
            else:
                try:
                    uploader = Upload()
                    image_id = str(uuid.uuid1())
                    upload_location = uploader.upload(file, image_id)
                    image_data = {
                        "id": image_id,
                        "upload_location": upload_location,
                        "user_id": user_id,
                        "name": name,
                        "description": description,
                        "category": category,
                        "tags": tags,
                        "filter": image_filter,
                        "created_at": time.time()
                    }
                    database = Database()
                    uploaded = database.save_image(image_data, image_id)
                except Exception as err:
                    error = err
        if error:
            app.logger.info('################ UPLOAD ERROR #######################')
            flask_app.logger.info(error)
            raise Exception(error)
        else:
            return