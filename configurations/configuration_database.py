import databases
import sqlalchemy

# SQLAlchemy specific code, as with any other app
# DATABASE_URL = "mysql://admin:adminamili@amilidb.ctlqdwf7wjsv.us-east-1.rds.amazonaws.com:3306/users_db"

DATABASE_URL = "mysql://root:Corazon666@localhost:3306/test-statistic"


def create_tables():
    database = databases.Database(DATABASE_URL)
    metadata = sqlalchemy.MetaData()

    user = sqlalchemy.Table(
        "users",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.BIGINT, primary_key=True),
        sqlalchemy.Column("email", sqlalchemy.String(length=255)),
        sqlalchemy.Column("name", sqlalchemy.String(length=255)),
        sqlalchemy.Column("password", sqlalchemy.String(length=255)),
        sqlalchemy.Column("product_key", sqlalchemy.String(length=255)),
    )

    parameter = sqlalchemy.Table(
        "parameters",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.BIGINT, primary_key=True),
        sqlalchemy.Column("date", sqlalchemy.String(length=255)),
        sqlalchemy.Column("humidity_above", sqlalchemy.FLOAT),
        sqlalchemy.Column("humidity_below", sqlalchemy.FLOAT),
        sqlalchemy.Column("lux", sqlalchemy.FLOAT),
        sqlalchemy.Column("temperature", sqlalchemy.FLOAT),
        sqlalchemy.Column("status", sqlalchemy.String(length=255)),
        sqlalchemy.Column("user_id", sqlalchemy.BIGINT, sqlalchemy.ForeignKey("users.id")),
        sqlalchemy.Column("statistic_id", sqlalchemy.BIGINT, sqlalchemy.ForeignKey("statistics.id")),
    )

    statistic = sqlalchemy.Table(
        "statistics",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.BIGINT, primary_key=True),
        sqlalchemy.Column("median", sqlalchemy.FLOAT),
        sqlalchemy.Column("parameter_id", sqlalchemy.BIGINT, sqlalchemy.ForeignKey("parameters.id")),
    )

    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)

    return user, parameter, statistic, database
