import databases
import sqlalchemy

DATABASE_URL = "sqlite:///store.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Определение таблиц
users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("first_name", sqlalchemy.String, index=True),
    sqlalchemy.Column("last_name", sqlalchemy.String, index=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True, index=True),
    sqlalchemy.Column("password", sqlalchemy.String),
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("product_id", sqlalchemy.ForeignKey("products.id")),
    sqlalchemy.Column("order_date", sqlalchemy.DateTime),
    sqlalchemy.Column("status", sqlalchemy.String),
)

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("name", sqlalchemy.String, index=True),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Float),
)