from contextlib import nullcontext as does_not_raise
from datetime import date, timedelta

import pytest
from fastapi import HTTPException

from app.config import settings
from app.schemas import DynamicTradingResultsQuery
from app.validators import query_filter_validators


# fmt: off
@pytest.mark.parametrize('query, expectation', [
    (
        DynamicTradingResultsQuery(
            start_date=date(2025, 7, 17),
            end_date=date(2025, 7, 17)
        ), does_not_raise()
     ),
    (
        DynamicTradingResultsQuery(
            start_date=date(2025, 7, 18),
            end_date=date(2025, 7, 17)
        ), pytest.raises(HTTPException)),
    (
        DynamicTradingResultsQuery(
            start_date=date(2025, 7, 17),
            end_date=date(2025, 7, 17)
            + timedelta(days=settings.max_days_range + 1)
        ), pytest.raises(HTTPException)),
])
# fmt: on
def test_query_filter_validators(query, expectation):
    with expectation:
        query_filter_validators(query)
