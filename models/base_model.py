#!/usr/bin/python3
"""Defines a BaseModel class"""
import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
Base = declarative_base()


class BaseModel:
    """defines the BaseModel of the AirBnB clone
    Attributes:
        id (sqlalchemy String): The BaseModel id.
        created_at (sqlalchemy DateTime): The datetime at creation.
        updated_at (sqlalchemy DateTime): The datetime of last update.
    """

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())


    def __init__(self, *args, **kwargs):
        """
        initialize a new BaseModel

        Args:
            *args (any): unused.
            **kwargs (dict): key/value pairs of attributes.
        """
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        tform = "%Y-%m-%dT%H:%M:%S.%f"
        if len(kwargs) != 0:
            for i, j in kwargs.items():
                if i == "created_at" or i == "updated_at":
                    self.__dict__[i] = datetime.strptime(j, tform)
                else:
                    self.__dict__[i] = j

    def save(self):
        """update the update_at attr with the current datetime"""
        self.updated_at = datetime.today()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        returns the dict representation of the BaseModel instance.

        includes the key/value pair __class__ representing the class
        name of the object
        """
        baseDict = self.__dict__.copy()
        baseDict["created_at"] = self.created_at.isoformat()
        baseDict["updated_at"] = self.updated_at.isoformat()
        baseDict["__class__"] = self.__class__.__name__
        baseDict.pop("_sa_instance_state", None)
        return baseDict
    
    def delete(self):
        """Delete the current instance from storage."""
        models.storage.delete(self)

    def __str__(self):
        """returns the print representation of the BaseModel instance."""
        className = self.__class__.__name__
        return "[{}] ({}) {}".format(className, self.id, self.__dict__)
