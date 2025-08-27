from datetime import date

import pytest

from app.crud import get_trading_dates, read_trading_results_from_db
from app.db import TradingResults
from app.schemas import DynamicTradingResultsQuery, TradingResultsQuery


@pytest.mark.asyncio
@pytest.mark.parametrize('days, expected_len', [(0, 0), (1, 1), (10, 3)])
async def test_get_trading_dates(db_session, days, expected_len):
    result = await get_trading_dates(db_session, days)
    assert isinstance(result, list), 'Результат не список'
    assert len(result) == expected_len, (
        f'Ожидали {expected_len} дат, получили {len(result)}'
    )
    assert all(isinstance(trading_date, date) for trading_date in result), (
        'Есть элементы не типа date'
    )
    assert result == sorted(result, reverse=True), (
        'Список дат не отсортирован по убыванию'
    )


# fmt: off
@pytest.mark.asyncio
@pytest.mark.parametrize('filters, last, expected_count', [
        (TradingResultsQuery(), False, 5),
        (TradingResultsQuery(), True, 2),
        (TradingResultsQuery(oil_id='A106'), False, 2),
        (TradingResultsQuery(oil_id='D410'), False, 1),
        (TradingResultsQuery(delivery_basis_id='PDK'), False, 2),
        (TradingResultsQuery(delivery_basis_id='NVO'), False, 1),
        (TradingResultsQuery(delivery_type_id='J'), False, 3),
        (TradingResultsQuery(delivery_type_id='L'), False, 1),
        (TradingResultsQuery(oil_id='D410'), True, 1),
        (TradingResultsQuery(delivery_basis_id='PDK'), True, 1),
        (DynamicTradingResultsQuery(start_date=date(2025, 7, 17), end_date=date(2025, 7, 18)), False, 4),  # noqa: E501
        (DynamicTradingResultsQuery(start_date=date(2025, 7, 17), end_date=date(2025, 7, 17)), False, 2),  # noqa: E501
])
# fmt: on
async def test_read_trading_results_from_db(
    db_session, filters, last, expected_count
):
    rows = await read_trading_results_from_db(db_session, filters, last=last)
    assert isinstance(rows, list), 'Результат не список'
    assert all(isinstance(tr, TradingResults) for tr in rows), (
        'Не все элементы TradingResults'
    )
    assert len(rows) == expected_count, (
        f'Ожидали {expected_count} строк, получили {len(rows)}'
    )
    assert rows == sorted(
        rows, key=lambda tr: (-tr.date.toordinal(), tr.exchange_product_id)
    ), 'Нарушен порядок сортировки'
    if getattr(filters, 'oil_id', None) is not None:
        assert all(tr.oil_id == filters.oil_id for tr in rows), (
            'oil_id не совпадает'
        )
    if getattr(filters, 'delivery_basis_id', None) is not None:
        assert all(
            tr.delivery_basis_id == filters.delivery_basis_id
            for tr in rows
        ), 'delivery_basis_id не совпадает'
    if getattr(filters, 'delivery_type_id', None) is not None:
        assert all(
            tr.delivery_type_id == filters.delivery_type_id for tr in rows
        ), 'delivery_type_id не совпадает'
    if isinstance(filters, DynamicTradingResultsQuery):
        assert all(
            filters.start_date <= tr.date <= filters.end_date for tr in rows
        ), 'Дата вне диапазона'
    if last:
        max_date = max(tr.date for tr in rows)
        assert all(tr.date == max_date for tr in rows), (
            'Есть строки не с последней датой'
        )
