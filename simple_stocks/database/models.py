import datetime
import uuid

from peewee import BooleanField, CharField, DateTimeField, ForeignKeyField, IntegerField, Model

from simple_stocks.app import app


class BaseModel(Model):
    def to_json(self):
        to_json_fields = getattr(self._meta, "json_fields", ())
        json_repr = {}
        for field in to_json_fields:
            field_value = getattr(self, field)
            if isinstance(field_value, datetime.datetime):
                field_value = field_value.isoformat()
            json_repr[field] = field_value
        return json_repr

    class Meta:
        database = app.db


class User(BaseModel):
    email = CharField(unique=True)

    class Meta:
        table_name = "users"


class Portfolio(BaseModel):
    user = ForeignKeyField(User, backref="portfolios")
    name = CharField(max_length=60)

    class Meta:
        table_name = "portfolios"


class Transaction(BaseModel):
    portfolio = ForeignKeyField(Portfolio, backref="transactions")
    stock_ticker = CharField(max_length=6)
    tx_type = CharField(max_length=10)
    nb_shares = IntegerField()
    tx_date = DateTimeField()

    class Meta:
        table_name = "transactions"


class ApiKey(BaseModel):
    api_key = CharField(default=lambda: str(uuid.uuid4()), primary_key=True, unique=True)
    user = ForeignKeyField(User, backref="api_keys")
    active = BooleanField(default=True)
    created_on = DateTimeField(default=datetime.datetime.utcnow)
    description = CharField(max_length=100, null=True)

    class Meta:
        table_name = "api_keys"
        json_fields = ("api_key", "active", "created_on", "description")
