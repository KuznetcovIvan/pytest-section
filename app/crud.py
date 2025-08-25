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
    request = select(TradingResults)
    if last:
        max_date = select(func.max(TradingResults.date)).scalar_subquery()
        request = request.where(TradingResults.date == max_date)
    if filters.oil_id:
        request = request.where(TradingResults.oil_id == filters.oil_id)
    if filters.delivery_type_id:
        request = request.where(
            TradingResults.delivery_type_id == filters.delivery_type_id
        )
    if filters.delivery_basis_id:
        request = request.where(
            TradingResults.delivery_basis_id == filters.delivery_basis_id
        )
    if isinstance(filters, DynamicTradingResultsQuery):
        request = request.where(
            TradingResults.date.between(filters.start_date, filters.end_date)
        )
    request = request.order_by(
        desc(TradingResults.date), TradingResults.exchange_product_id
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
