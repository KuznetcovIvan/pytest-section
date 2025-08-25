from datetime import timedelta
from http import HTTPStatus

from fastapi import HTTPException

from app.config import settings
from app.schemas import DynamicTradingResultsQuery, TradingResultsQuery

DATE_ERROR = 'start_date={} больше end_date={}'
RANGE_ERROR = 'Выборка не может превышать {} дней'


def query_filter_validators(
    filters: TradingResultsQuery | DynamicTradingResultsQuery,
):
    if isinstance(filters, DynamicTradingResultsQuery):
        if filters.start_date > filters.end_date:
            raise HTTPException(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                DATE_ERROR.format(filters.start_date, filters.end_date),
            )
        if (filters.end_date - filters.start_date) > timedelta(
            days=settings.max_days_range
        ):
            raise HTTPException(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                RANGE_ERROR.format(settings.max_days_range),
            )
    return filters
