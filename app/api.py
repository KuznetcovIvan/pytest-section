from datetime import date

from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.crud import get_trading_dates, read_trading_results_from_db
from app.db import get_async_session
from app.schemas import (
    DynamicTradingResultsQuery,
    TradingResultsDB,
    TradingResultsQuery,
)
from app.validators import query_filter_validators

spimex_router = APIRouter(prefix='/api', tags=['Trading results'])

SLUG_TRADING_DATES = 'trading-dates'
SUMMARY_TRADING_DATES = 'Cписок дат последних торговых дней'

SLUG_RESULTS_BY_DATE = 'results-by-date'
SUMMARY_RESULTS_BY_DATE = 'Cписок торгов за заданный период'

SLUG_LAST_RESULTS = 'last-results'
SUMMARY_LAST_RESULTS = 'Cписок последних торгов'


@spimex_router.get(
    f'/{SLUG_TRADING_DATES}',
    response_model=list[date],
    summary=SUMMARY_TRADING_DATES,
)
@cache(namespace=SLUG_TRADING_DATES)
async def get_last_trading_dates(
    session: AsyncSession = Depends(get_async_session),
    days: int = Query(..., gt=0, le=settings.max_days_limit),
):
    return await get_trading_dates(session, days)


@spimex_router.get(
    f'/{SLUG_RESULTS_BY_DATE}',
    response_model=list[TradingResultsDB],
    summary=SUMMARY_RESULTS_BY_DATE,
)
@cache(namespace=SLUG_RESULTS_BY_DATE)
async def get_dynamics(
    session: AsyncSession = Depends(get_async_session),
    filters: DynamicTradingResultsQuery = Depends(),
):
    return await read_trading_results_from_db(
        session, query_filter_validators(filters)
    )


@spimex_router.get(
    f'/{SLUG_LAST_RESULTS}',
    response_model=list[TradingResultsDB],
    summary=SUMMARY_LAST_RESULTS,
)
@cache(namespace=SLUG_LAST_RESULTS)
async def get_trading_results(
    session: AsyncSession = Depends(get_async_session),
    filters: TradingResultsQuery = Depends(),
):
    return await read_trading_results_from_db(
        session, query_filter_validators(filters), last=True
    )
