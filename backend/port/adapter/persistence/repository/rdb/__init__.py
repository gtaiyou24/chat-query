from sqlalchemy.orm import declarative_base

# TODO : use sqlalchemy.orm.DeclarativeBase
#        see https://docs.sqlalchemy.org/en/20/orm/quickstart.html
DataBase = declarative_base()

from .rdb_unit_of_work import RDBUnitOfWork
