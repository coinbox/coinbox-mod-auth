import cbpos

import cbmod.base.models.common as common
from cbmod.auth.models import User

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method, Comparator


class Clock(cbpos.database.Base, common.Item):
    __tablename__ = 'clocks'

    id  = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship('User', backref=backref('clock_records', order_by=id))
    date_time_in  = Column(DateTime, nullable=False, unique=False)
    date_time_out = Column(DateTime, nullable=False, unique=False)

    @hybrid_property
    def display(self):
        return '%s in: %s | out: %s'%(self.user.username, self.date_time_in, self.date_time_out)
    
    @display.expression
    def display(self):
        return '%s in: %s | out: %s'%(self.user.username, self.date_time_in, self.date_time_out)

    def __repr__(self):
        return "<Clock - %s in: %s | out: %s>" % (self.user.username, self.date_time_in, self.date_time_out)



class ClockAuthorizations(cbpos.database.Base, common.Item):
    __tablename__ = 'clock_auth'

    id  = Column(Integer, primary_key=True)
    clock_id = Column(Integer, ForeignKey('clocks.id'), nullable=True)
    clock = relationship('Clock', backref=backref('clock_auth', order_by=id))
    auth_user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    auth_user = relationship('User')


    