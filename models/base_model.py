#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """A base class for all hbnb models"""

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            today = datetime.now()
            time_format = "%Y-%m-%dT%H:%M:%S.%f"

            if 'id' not in kwargs:
                kwargs['id'] = str(uuid.uuid4())

            u_a = 'updated_at'
            if u_a in kwargs:
                kwargs[u_a] = datetime.strptime(kwargs[u_a], time_format)
            else:
                kwargs[u_a] = today

            c_a = 'created_at'
            if c_a in kwargs:
                kwargs[c_a] = datetime.strptime(kwargs[c_a], time_format)
            else:
                kwargs[c_a] = today

            if '__class__' in kwargs:
                del kwargs['__class__']

            self.__dict__.update(kwargs)
        storage.new(self)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary
