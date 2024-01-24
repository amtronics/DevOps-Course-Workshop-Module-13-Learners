from data.database import db
from sqlalchemy.dialects.mssql import DATETIMEOFFSET
from datetime import datetime, timedelta
from pytz import utc, timezone

local_timezone = timezone("Europe/London")

COMPLETE = 'Complete'
QUEUED = 'Queued'

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(100), nullable=False)
    customer = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    date_placed = db.Column(DATETIMEOFFSET, nullable=False)
    date_processed = db.Column(DATETIMEOFFSET, nullable=True)
    download = db.Column(db.LargeBinary, nullable=True)

    def __init__(self, product, customer, date_placed, date_processed, download):
        self.product = product
        self.customer = customer
        self.date_placed = date_placed
        self.date_processed = date_processed
        self.status = 'Complete' if self.date_processed else 'Queued'
        self.download = download

    def __repr__(self):
        return f"<Order {self.id}: {self.product}, {self.customer}, {self.date_placed}, {self.date_processed} >"

    @property
    def date_placed_local(self):
        return self.date_placed.astimezone(local_timezone)

    @property
    def date_processed_local(self):
        return self.date_processed.astimezone(local_timezone)

    def set_as_processed(self):
        self.date_processed = datetime.now(tz=utc)
        self.status = COMPLETE
