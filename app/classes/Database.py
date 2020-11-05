import os
import tempfile
import pyrebase
import requests
import json
from collections import OrderedDict
from flask import current_app as flask_app
from app import SITE_ROOT

class Database():
    """ 
    Database Class. 
  
    Class to interact with Firebase Realtime Database. 
  
    """

    def __init__(self):
        """ 
        Initialise class with configuration 
    
        """
        # Load Firebase config data, including Service Account file
        firebase_config_file = os.path.join(SITE_ROOT, 'firebase.json')
        firebase_config = json.load(open(firebase_config_file))
        firebase_config["serviceAccount"] = os.path.join(SITE_ROOT, 'firebase.admin.json')
        
        # Initialize Firebase auth and database
        self.firebase = pyrebase.initialize_app(firebase_config)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()

        # Create readable errors based on Firebase errors
        self.readable_errors = {
            "INVALID_PASSWORD": "This is an invalid password",
            "EMAIL_NOT_FOUND": "This email has not been registered",
            "EMAIL_EXISTS": "This email already exists. Try logging in instead.",
            "TOO_MANY_ATTEMPTS_TRY_LATER": "Too many attempts, please try again later",
            "USER_DISABLED": "This account has been disabled by an administrator.",
        }

    # Image Requests
    def get_images(self, limit=20, user_id=False):
        """
        Get method.

        Requests to fetch a maximum of 20 images from the DB.
        """
        
        try:
            if (user_id):
                # Attempts to fetch images and display them in order of userID.
                images = self.db.child("images").order_by_child("user_id").equal_to(user_id).limit_to_first(limit).get()
            else:
                images = self.db.child("images").order_by_child("user_id").limit_to_first(limit).get()
            
            # Returns the maximum of 20 images in order of image value.
            flask_app.logger.info('####################### images val #####################')
            flask_app.logger.info(images.val())
            if isinstance(images.val(), OrderedDict):
                # Return on success
                return images
            else:
                # Fails to return images due to process errors.
                return False
            
        except Exception as err:
            # Raise error upon failed fetch request.
            self.process_error(err)

    def get_category_images(self, category, limit=20):
        """
        Get method.

        Attempts to retrieve a maximum of 20 images in a selected catergory from the DB.
        """
        try:
            # Displays images in order of catergory 
            images = self.db.child("images").order_by_child("category").equal_to(category).limit_to_first(limit).get()

            if isinstance(images.val(), OrderedDict):
                # Returns images upon success.
                return images
            else:
                # Fails to return images in catergory due to error(s).
                return False
            
        except Exception as err:
            # Raise error due to process errors.
            self.process_error(err)
        
    def get_image(self, image_id):
        """
        Get method.

        Requests a specific image based on imageID from the DB.
        """
        # Validates the get request.
        error = None
        image = False
        
        try:
            # Tries to display images with that specific ID.
            image = self.db.child("images").child(image_id).get()

        except Exception as err:
            # Checks if flask causes the error and raises an error if true.
            flask_app.logger.info(err)
            error = err

        if error:
            # Raise error due to failed DB request.
            raise Exception(error)
        else:
            # Return image with the specified value upon success.
            return image.val()

    def save_image(self, image_data, image_id):
        """
        Save method.

        Stores the image data under the corresponding imageID in the DB.
        """
        try:
            # Sets the image data corresponding to the imageID in the DB. 
            self.db.child("images").child(image_id).set(image_data)
        except Exception as err:
            # Raises error due to proccess error(s).
            self.process_error(err)

    def delete_image(self, image_id):
        """
        Delete method.

        Requests to remove the imageID and its corresponding data from the DB.
        """
        try:
            # Fetches and removes the image ID from the DB. 
            self.db.child("images").child(image_id).remove()
        except Exception as err:
            # Raises error upon process failure.
            self.process_error(err)

    def remove_matching_value(self, data, value):
        """
        Remove method.

        Attempts to remove data that matches the input value from the DB.
        """
        # Clears out data that matches the selected input from the DB.
        return_data = []
        for key in data:
            if key != value:
                return_data.append(key)
                # Returns new data after removal upon success.
        return return_data


    # User and Account Requests
    def register(self, user_data, password):
        try:
            # Authenticates a user in the DB upon successful account creation. 
            user_auth = self.auth.create_user_with_email_and_password(user_data['email'], password)
            user_data['localId'] = user_auth['localId']
            self.db.child("users").child(user_auth['localId']).set(user_data)
            return user_auth
        except Exception as err:
            # Raise error if there is a process error during the request.
            self.process_error(err)

    def login(self, email, password):
        """
        Login method.

        Requests to log a registered user into the DB.
        """
        try:
            # Requests the user to sign in using the registered email and password in the DB for that userID.
            user_auth = self.auth.sign_in_with_email_and_password(email, password)
            user = self.db.child("users").child(user_auth['localId']).get().val()
            # Returns the user profile upon successful login.
            return user
        except Exception as err:
            # Raises error upon exception during the login process.
            self.process_error(err)

    def update_user(self, user_data):
        """
        Update method.

        Attempts to update the user's information in relation to their ID in the DB.
        """
        try:
            # Uses the localID to update the user's corresponding information as entered by the user.
            self.db.child("users").child(user_data['localId']).update(user_data)
            # Returns the updated profile upon successful request to the DB.
            return
        except Exception as err:
            # Raises an error if there is a process failure during the request.
            self.process_error(err)

    # Processes the error and finds the cause of the error. Once the cause is found, a readable error is presented.
    def process_error(self, error):
        flask_app.logger.info(error)
        readable_error = self.get_readable_error(error)
        raise Exception(readable_error)

    # Fetches readable error message for the user, if error cause is undefinable: present "there was a problem with your request."
    def get_readable_error(self, error):
        error_json = error.args[1]
        error_messsage = json.loads(error_json)['error']['message']
        if error_messsage in self.readable_errors.keys(): 
            return self.readable_errors[error_messsage]
        else: 
            return "There was a problem with your request."