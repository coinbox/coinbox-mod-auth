import cbpos

import cbmod.base.models.common as common

from cbmod.auth.models import Role, Permission, MenuRestriction, \
        role_permission_link, permission_restriction_link

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method, Comparator

import bcrypt

current = None

class User(cbpos.database.Base, common.Item):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    encoded_password = Column('password', String(60), nullable=False)
    hidden = Column(Boolean, default=False)
    super = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=True)

    role = relationship('Role', order_by="Role.id", backref="users")

    @hybrid_property
    def password(self):
        return self.encoded_password

    @password.setter
    def password(self, value):
        self.encoded_password = self.encode(value)

    @hybrid_property
    def menu_restrictions(self):
        session = cbpos.database.session()
        """
        this is the literal sql query that i came up with, the one generated by sqlalchemy is slightly different
            SELECT a1.root, a1.item FROM (
            SELECT DISTINCT mr.* FROM menurestrictions as mr, permissions as p, roles as r, users as u, permission_restriction as pr, role_permission as rp
            WHERE u.id=%s AND u.role_id=r.id AND rp.role_id=r.id AND rp.permission_id=p.id AND pr.permission_id=p.id AND pr.restriction_id=mr.id
            ) as a1
        query = session.query(MenuRestriction.root, MenuRestriction.item).from_statement(query_txt)
        """
        query = session.query(MenuRestriction).filter((User.id == self.id) & \
            (User.role_id == Role.id) & (role_permission_link.c.role_id == Role.id) & \
            (role_permission_link.c.permission_id == Permission.id) & \
            (permission_restriction_link.c.permission_id == Permission.id) & \
            (permission_restriction_link.c.restriction_id == MenuRestriction.id)).distinct()
        return query.all()

    def login(self, password):
        return bcrypt.hashpw(password, self.encoded_password) == self.encoded_password

    def encode(self, password):
        return bcrypt.hashpw(password, bcrypt.gensalt())

    @hybrid_property
    def display(self):
        return self.username
    
    @display.expression
    def display(self):
        return self.username

    def __repr__(self):
        return "<User %s>" % (self.username,)
