from datetime import date

from sqlalchemy import desc, distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import TradingResults
from app.schemas import DynamicTradingResultsQuery, TradingResultsQuery


async def read_trading_results_from_db(
    session: AsyncSession,
    filters: TradingResultsQuery | DynamicTradingResultsQuery,
    *,
    last: bool = False,
) -> list[TradingResults]:
    conditions = []
    if last:
        max_date = select(func.max(TradingResults.date)).scalar_subquery()
        conditions.append(TradingResults.date == max_date)
    if filters.oil_id:
        conditions.append(TradingResults.oil_id == filters.oil_id)
    if filters.delivery_type_id:
        conditions.append(
            TradingResults.delivery_type_id == filters.delivery_type_id
        )
    if filters.delivery_basis_id:
        conditions.append(
            TradingResults.delivery_basis_id == filters.delivery_basis_id
        )
    if isinstance(filters, DynamicTradingResultsQuery):
        conditions.append(
            TradingResults.date.between(filters.start_date, filters.end_date)
        )
    request = (
        select(TradingResults)
        .where(*conditions)
        .order_by(
            desc(TradingResults.date), TradingResults.exchange_product_id
        )
    )
    result = await session.execute(request)
    return result.scalars().all()


async def get_trading_dates(session: AsyncSession, days: int) -> list[date]:
    request = (
        select(distinct(TradingResults.date))
        .order_by(desc(TradingResults.date))
        .limit(days)
    )
    result = await session.execute(request)
    return result.scalars().all()
