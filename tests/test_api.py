from datetime import date
from http import HTTPStatus

import pytest
from httpx import ASGITransport, AsyncClient
from pydantic import parse_raw_as

from app.config import settings
from app.main import app
from app.schemas import TradingResultsDB


# fmt: off
@pytest.mark.asyncio
@pytest.mark.parametrize('params, expected_status', [
        ({'days': 1}, HTTPStatus.OK),
        ({'days': '1'}, HTTPStatus.OK),
        ({'days': 0}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ({'days': -1}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ({'days': settings.max_days_limit + 1}, HTTPStatus.UNPROCESSABLE_ENTITY), # noqa: E501
        ({'days': 'str'}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ({'days': 1, 'extra': 2}, HTTPStatus.OK),
        (None, HTTPStatus.UNPROCESSABLE_ENTITY),
])
# fmt: on
async def test_get_last_trading_dates(
    params: dict[str, int] | dict[str, str] | None,
    expected_status: HTTPStatus | HTTPStatus,
):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        response = await client.get('/api/trading-dates', params=params)
        assert response.status_code == expected_status
        if response.status_code == HTTPStatus.OK:
            dates = parse_raw_as(list[date], response.text)
            assert dates == sorted(dates, reverse=True)


# fmt: off
@pytest.mark.asyncio
@pytest.mark.parametrize('params, expected_status, expected_count', [
        ({'start_date': '2025-07-17', 'end_date': '2025-07-18'}, HTTPStatus.OK, 4),                             # noqa: E501
        ({'start_date': '2025-07-17', 'end_date': '2025-07-17'}, HTTPStatus.OK, 2),                             # noqa: E501
        ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'oil_id': 'A106'},HTTPStatus.OK, 1),            # noqa: E501
        ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'delivery_type_id': 'J'}, HTTPStatus.OK, 2),    # noqa: E501
        ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'delivery_basis_id': 'PDK'}, HTTPStatus.OK, 1), # noqa: E501
        ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'oil_id': 'XXXX'}, HTTPStatus.OK, 0),           # noqa: E501
        ({'start_date': 'str', 'end_date': '2025-07-18'}, HTTPStatus.UNPROCESSABLE_ENTITY, None),               # noqa: E501
        ({'start_date': '2025-07-18', 'end_date': '2025-07-17'}, HTTPStatus.UNPROCESSABLE_ENTITY, None),        # noqa: E501
        ({'start_date': '2025-07-17'}, HTTPStatus.UNPROCESSABLE_ENTITY, None),
        ({'end_date': '2025-07-18'}, HTTPStatus.UNPROCESSABLE_ENTITY, None),
        (None, HTTPStatus.UNPROCESSABLE_ENTITY, None),
])
# fmt: on
async def test_get_dynamics(params, expected_status, expected_count):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        response = await client.get('/api/results-by-date', params=params)
        assert response.status_code == expected_status
        if response.status_code == HTTPStatus.OK:
            trading_results = parse_raw_as(
                list[TradingResultsDB], response.text
            )
            assert len(trading_results) == expected_count
            assert trading_results == sorted(
                trading_results,
                key=lambda tr: (-tr.date.toordinal(), tr.exchange_product_id),
            )


@pytest.mark.asyncio
@pytest.mark.parametrize('params, expected_status, expected_count', [
        (None, HTTPStatus.OK, 2),
        ({'extra': 2}, HTTPStatus.OK, 2),
        ({'oil_id': 'D410'}, HTTPStatus.OK, 1),
        ({'delivery_basis_id': 'KZN'}, HTTPStatus.OK, 1),
        ({'delivery_type_id': 'J'}, HTTPStatus.OK, 1),
        ({'oil_id': 'A106'}, HTTPStatus.OK, 0),
        ({'oil_id': 'XXX'}, HTTPStatus.UNPROCESSABLE_ENTITY, None),
        ({'delivery_basis_id': 'PD'}, HTTPStatus.UNPROCESSABLE_ENTITY, None),
        ({'delivery_type_id': 'JJ'}, HTTPStatus.UNPROCESSABLE_ENTITY, None),
])
async def test_get_trading_results(params, expected_status, expected_count):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        response = await client.get('/api/last-results', params=params)
        assert response.status_code == expected_status
        if response.status_code == HTTPStatus.OK:
            trading_results = parse_raw_as(
                list[TradingResultsDB], response.text
            )
            assert len(trading_results) == expected_count
            assert trading_results == sorted(
                trading_results,
                key=lambda tr: (-tr.date.toordinal(), tr.exchange_product_id),
            )
