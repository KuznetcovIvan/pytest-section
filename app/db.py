from datetime import datetime as dt

from sqlalchemy import (
    Column,
    Computed,
    Date,
    DateTime,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

Base = declarative_base()
engine = create_async_engine(settings.database_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session


UNIQUE_COLUMNS = ('date', 'exchange_product_id')


class TradingResults(Base):
    __tablename__ = 'spimex_trading_results'
    __table_args__ = (
        UniqueConstraint(*UNIQUE_COLUMNS, name='uix_date_product'),
    )

    id = Column(Integer, primary_key=True, comment='Уникальный идентификатор')
    exchange_product_id = Column(String, comment='Код Инструмента')
    exchange_product_name = Column(String, comment='Наименование Инструмента')
    oil_id = Column(
        String,
        Computed(
            'substring(exchange_product_id from 1 for 4)', persisted=True
        ),
        comment='exchange_product_id[:4]',
    )
    delivery_basis_id = Column(
        String,
        Computed(
            'substring(exchange_product_id from 5 for 3)', persisted=True
        ),
        comment='exchange_product_id[4:7]',
    )
    delivery_basis_name = Column(String, comment='Базис поставки')
    delivery_type_id = Column(
        String,
        Computed('right(exchange_product_id, 1)', persisted=True),
        comment='exchange_product_id[-1]',
    )
    volume = Column(Integer, comment='Объем Договоров в единицах измерения')
    total = Column(Integer, comment='Объем Договоров, руб.')
    count = Column(Integer, comment='Количество Договоров, шт.')
    date = Column(Date, comment='Дата торгов')
    created_on = Column(
        DateTime, default=dt.now, comment='Дата и время создания записи'
    )
    updated_on = Column(
        DateTime,
        default=dt.now,
        onupdate=dt.now,
        comment='Дата и время обновления записи',
    )

    def __repr__(self):
        return (
            f'{type(self).__name__}'
            f'{self.id=}, '
            f'{self.exchange_product_id=}, '
            f'{self.oil_id=}, '
            f'{self.delivery_basis_id=}, '
            f'{self.delivery_type_id=}, '
            f'{self.volume=}, '
            f'{self.count=}, '
            f'{self.date=}'
        )
