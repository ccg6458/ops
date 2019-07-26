# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related utilities."""

# flake8: noqa  # flake8 has real problems linting this file on Python 2

from pprint import pformat

from sqlalchemy import desc, or_
from sqlalchemy.sql.sqltypes import Date, DateTime
from flask import current_app
from app.lib.extensions import db

# Alias common SQLAlchemy names
Column = db.Column
relationship = db.relationship



class CRUDMixin(object):
    """Mixin that adds convenience methods for
    CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    def create_from_dict(cls, d):
        """Create a new record and save it the database."""
        assert isinstance(d, dict)
        instance = cls(**d)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in list(kwargs.items()):
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except Exception as e:
                current_app.logger.info(e)
                db.session.rollback()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        if commit:
            try:
                db.session.commit()
            except:
                db.session.rollback()
        return self

    def to_dict(self, fields_list=None):
        """
        Args:
            fields (str list): 指定返回的字段
        """
        column_list = fields_list or [
            column.name for column in self.__table__.columns
            ]
        return {
            column_name: getattr(self, column_name)
            for column_name in column_list
            }

    @classmethod
    def create_or_update(cls, query_dict, update_dict=None):
        instance = db.session.query(cls).filter_by(**query_dict).first()
        if instance:  # update
            if update_dict is not None:
                return instance.update(**update_dict)
            else:
                return instance
        else:  # create new instance
            query_dict.update(update_dict or {})
            return cls.create(**query_dict)
