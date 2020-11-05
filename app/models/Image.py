from app.classes.Database import Database
from app.classes.Upload import Upload
from app.models.User import User
from flask import session
from flask import current_app as flask_app
import uuid, time

class Image():
    # Initialises the class
    def __init__(self):
        return None

    def get_images(self, limit=20):
        """
        Get method.

        Processes request, fetches image IDs from DB, and limits the number displayed to 20.
        """
        error = None
        images = False
        # Validates and sends the request to the DB.
        try:
            database = Database()
            images = database.get_images(limit)

        except Exception as err:
             # Identifies if flask is the cause of the error, and raises error if true.
            flask_app.logger.info(err)
            error = err

        if error:
            # Raise error from failed Firebase request.
            raise Exception(error)
        else:
            # Return on success. 
            return images

    def get_category_images(self, category, limit=20):
        """
        Get method

        Fetches image IDs from a selected category from the DB, and limits the number displayed to 20. 
        """
        
        error = None
        images = False
        # Validates and sends the request to the DB.
        try:
            database = Database()
            images = database.get_category_images(category, limit)

        except Exception as err:
             # Identifies if flask is the cause of the error, and raises error if true.
            flask_app.logger.info(err)
            error = err

        if error:
            # Raise error from failed Firebase request.
            raise Exception(error)
        else:
            # Return on success. 
            return images

    def get_image(self, image_id):
        """
        Get method.

        Processes request and fetches image ID, and displays the fetched image for the user.
        """
        error = None
        image = False
        
        # Validates the request and fetches the ID from the DB.
        try:
            database = Database()
            image = database.get_image(image_id)

        except Exception as err:
             # Identifies if flask is the cause of the error, and raises error if true.
            flask_app.logger.info(err)
            error = err

        if error:
            # Raise error from failed Firebase request.
            raise Exception(error)
        else:
            # Return on success
            return image

    def delete_image(self, image_id):
        """
        Delete method.

        Fetches the image ID from the DB, and removes it from the DB.
        """
        
        error = None
        
        # Validates the request, fetches the ID from the DB, and deletes it from the DB.
        try:
            database = Database()
            database.delete_image(image_id)

        except Exception as err:
            # Identifies if flask is the cause of the error, and raises error if true.
            flask_app.logger.info(err)
            error = err

        if error:
            # Raise error from failed Firebase request.
            raise Exception(error)
        else: 
            # Return on success.
            return

    def get_user_images(self, limit=20):
        """
        Get method.

        Fetches the user's images from the 'my images' list in the DB, and displays a maximum of 20 images from this list.
        """
        
        # Validates required registration fields.
        error = None
        images = False
        user_id = False
        if (session['user'] and session['user']['localId']):
            user_id = session['user']['localId']
        try:
            # Attempts to fetch the images associated with the users' ID from the DB.
            database = Database()
            images = database.get_images(limit, user_id)

        except Exception as err:
            # Identifies if flask is the cause of the error, and raises error if true.
            flask_app.logger.info(err)
            error = err

        if error:
            # Raise error on failed Firebase request.
            raise Exception(error)
        else:
            # Return on success.
            return images

    def upload(self, request):
        """
        Upload method.

        Requests to upload an image from the user to the DB. 
        """

        # Checks that the required fields are filled, and sent to the DB.
        image_id        = str(uuid.uuid1())
        name            = request.form['name']
        description     = request.form['description']
        category        = request.form['category']
        image_filter    = request.form['filter']

        # Validates required registration fields
        error = None
        user_id = False

        # Associates the session User ID with the localID on the DB.
        if (session['user'] and session['user']['localId']):
            user_id     = session['user']['localId']
            user_name   = session['user']['first_name'] + " " + session['user']['last_name']
            user_avatar = session['user']['avatar']
        else: 
            # Raises error if the user is not logged in as the localID and the user ID are not able to be associated.
            error = 'You must be logged in to upload an image.'

        # Raises error if there is no image requested to be sent to the DB.
        if 'image' not in request.files:
            error = 'A file is required.'
        else:
            # Requests that the image be sent to the DB, if the above requirements are met.
            file = request.files['image']

        # Raises a specific error based on which of the following requirements are not met.
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
                # Attempts to send the following information to the DB asssociated with the image ID in the following format.
                try: 
                    uploader = Upload()
                    upload_location = uploader.upload(file, image_id)
                    image_data = {
                        "id":                   image_id,
                        "upload_location":      '/' + upload_location,
                        "user_id":              user_id,
                        "user_name":            user_name,
                        "user_avatar":          user_avatar,
                        "name":                 name,
                        "description":          description,
                        "category":             category,
                        "filter":               image_filter,
                        "created_at":           int(time.time())
                    }
                    database = Database()
                    uploaded = database.save_image(image_data, image_id)
                except Exception as err:
                    # Raise error upon failed Firebase upload.
                    error = err
        if error:
            # Raises an error if Flask fails to upload the information to Firebase, and displays a message for the user.
            flask_app.logger.info('################ UPLOAD ERROR #######################')
            flask_app.logger.info(error)
            raise Exception(error)
        else:
            # Returns image ID upon successful upload.
            return image_id

    def update(self, image_id, request):
        """
        Update method.

        Requests that the information associated with an image ID is updated (on the Firebase list for that particular image ID) based on the information the user enters.
        """
        # Fills the form with the new input from the user
        name            = request.form['name']
        description     = request.form['description']
        category        = request.form['category']
        image_filter    = request.form['filter']
        created_at      = request.form['created_at'] 
        upload_location = request.form['upload_location']  

        # Validates required registration fields
        error = None
        user_id = False

        # Checks that the user is logged in based on the userID and localID. 
        if (session['user'] and session['user']['localId']):
            user_id     = session['user']['localId']
            user_name   = session['user']['first_name'] + " " + session['user']['last_name']
            user_avatar = session['user']['avatar']
        else: 
            # Raises error upon failed update as the user is not logged in.
            error = 'You must be logged in to update an image.'

        # Validates the required fields to check for missing information, and raises an error based on the missing info.
        if not error:
            if not name:
                error = 'An name is required.'
            elif not description:
                error = 'A description is required.'
            elif not category:
                error = 'A category is required.'
            else:
                try:
                    # Tries another method to update the image information, attempting to send it to the specified image ID in the DB.
                    image_data = {
                        "id":                   image_id,
                        "upload_location":      upload_location,
                        "user_id":              user_id,
                        "user_name":            user_name,
                        "user_avatar":          user_avatar,
                        "name":                 name,
                        "description":          description,
                        "category":             category,
                        "filter":               image_filter,
                        "created_at":           created_at
                    }
                    database = Database()
                    uploaded = database.save_image(image_data, image_id)
                except Exception as err:
                    # Raise error if update was unsuccessful, as the information could not be sent to the DB.
                    error = err
        if error:
            # Identifies if flask is causing the error. If true: raise error and displays this error to the user.
            flask_app.logger.info('################ UPDATE ERROR #######################')
            flask_app.logger.info(error)
            raise Exception(error)
        else:
            # Returns the image ID upon success and updates the image information.
            return