from datetime import date
from http import HTTPStatus

import pytest
from httpx import ASGITransport, AsyncClient

from app.config import settings
from app.main import app


class TestGetLastTradingDates:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'params, expected_status',
        [
            ({'days': 1}, HTTPStatus.OK),
            ({'days': '1'}, HTTPStatus.OK),
            ({'days': 0}, HTTPStatus.UNPROCESSABLE_ENTITY),
            ({'days': -1}, HTTPStatus.UNPROCESSABLE_ENTITY),
            (
                {'days': settings.max_days_limit + 1},
                HTTPStatus.UNPROCESSABLE_ENTITY,
            ),
            ({'days': 'str'}, HTTPStatus.UNPROCESSABLE_ENTITY),
            ({'days': 1, 'night': 2}, HTTPStatus.OK),
            (None, HTTPStatus.UNPROCESSABLE_ENTITY),
        ],
    )
    async def test_get_last_trading_dates(self, params, expected_status):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url='http://test'
        ) as client:
            response = await client.get('/api/trading-dates', params=params)
            assert response.status_code == expected_status
            if response.status_code == HTTPStatus.OK:
                body = response.json()
                assert isinstance(body, list)
                assert body == sorted(body, reverse=True)
                assert all(
                    isinstance(date.fromisoformat(td), date) for td in body
                )
