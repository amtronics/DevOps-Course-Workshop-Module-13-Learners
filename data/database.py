from datetime import datetime, timedelta
from pytz import timezone, utc
from sqlalchemy import desc, asc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

db = SQLAlchemy()
from data.order import Order, QUEUED


def get_all_orders():
    return db.session.query(Order).all()

def get_orders_to_display():
    return (db.session.query(Order)
        .filter(or_(Order.date_processed == None, Order.date_processed >= _display_cutoff()))
        .order_by(asc(Order.date_placed))
        .limit(100)
        .all())

def get_queued_count():
    return db.session.query(Order).filter(Order.status == QUEUED).count()

def get_recently_processed_count():
    return db.session.query(Order).filter(Order.date_processed >= _display_cutoff()).count()

def get_recently_placed_count():
    return db.session.query(Order).filter(Order.date_placed >= _display_cutoff()).count()

def _display_cutoff():
    return datetime.now(utc) - timedelta(minutes=10)

def add_order(product, customer, date_placed, date_processed, download):
    order = Order(product, customer, date_placed, date_processed, download)
    db.session.add(order)
    db.session.commit()
    return order


def save_order(order):
    db.session.add(order)
    db.session.commit()


def add_orders(orders):
    db.session.bulk_save_objects(orders)
    db.session.commit()


def clear_orders():
    db.session.query(Order).delete()
    db.session.commit()


def count_orders():
    return db.session.query(Order).count()


def initialise_database(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()  # creates table if not present
