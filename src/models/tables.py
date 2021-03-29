import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Courier(Base):
    __tablename__ = 'courier'

    courier_id = sa.Column(sa.Integer, primary_key=True)
    cargo = sa.Column(sa.Integer)


class CourierRegion(Base):
    __tablename__ = 'courier_region'

    cg_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    courier_id = sa.Column(sa.Integer, sa.ForeignKey('courier.courier_id'))
    region = sa.Column(sa.Integer)


class WorkingHours(Base):
    __tablename__ = 'working_hours'

    wh_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    courier_id = sa.Column(sa.Integer, sa.ForeignKey('courier.courier_id'))
    start = sa.Column(sa.String)
    stop = sa.Column(sa.String)


class Orders(Base):

    """""
    Синтаксис SQL содержит слово ORDER, поэтому отойдём от канонов и назовем таблицу во
    множественном числе дабы избежать возможных ошибок
    """""

    __tablename__ = 'orders'

    order_id = sa.Column(sa.Integer, primary_key=True)
    weight = sa.Column(sa.Numeric(2, 2))
    region = sa.Column(sa.Integer)
    status = sa.Column(sa.Integer)
    complete_time = sa.Column(sa.String, nullable=True)


class DeliveryHours(Base):
    __tablename__ = 'delivery_hours'

    dh_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    order_id = sa.Column(sa.Integer, sa.ForeignKey('orders.order_id'))
    start = sa.Column(sa.String)
    stop = sa.Column(sa.String)


class Delivery(Base):
    __tablename__ = 'delivery'

    delivery_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    assign_time = sa.Column(sa.String)
    status = sa.Column(sa.Integer)
    courier_id = sa.Column(sa.Integer, sa.ForeignKey('courier.courier_id'))
    cargo = sa.Column(sa.Integer)


class Assigning(Base):
    __tablename__ = 'assigning'

    assigning_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    order_id = sa.Column(sa.Integer, sa.ForeignKey('orders.order_id'))
    delivery_id = sa.Column(sa.Integer, sa.ForeignKey('delivery.delivery_id'))
    status = sa.Column(sa.Integer)
