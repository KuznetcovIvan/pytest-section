import datetime as dt

from pydantic import BaseModel, Field


class TradingResultsDB(BaseModel):
    """Схема вывода результатов торгов."""

    exchange_product_id: str = Field(..., title='Код инструмента')
    exchange_product_name: str = Field(..., title='Наименование инструмента')
    oil_id: str = Field(..., title='ID нефтепродукта')
    delivery_basis_id: str = Field(..., title='ID базиса поставки')
    delivery_basis_name: str = Field(..., title='Базис поставки')
    delivery_type_id: str = Field(..., title='ID типа поставки')
    volume: int = Field(..., title='Объем')
    total: int = Field(..., title='Сумма, руб.')
    count: int = Field(..., title='Количество договоров')
    date: dt.date = Field(..., title='Дата торгов')

    class Config:
        orm_mode = True


class TradingResultsQuery(BaseModel):
    """Схема для фильтрации последних торгов."""

    oil_id: str | None = Field(None, min_length=4, max_length=4)
    delivery_type_id: str | None = Field(None, min_length=1, max_length=1)
    delivery_basis_id: str | None = Field(None, min_length=3, max_length=3)


class DynamicTradingResultsQuery(TradingResultsQuery):
    """Схема для фильтрации торгов за период."""

    start_date: dt.date
    end_date: dt.date
