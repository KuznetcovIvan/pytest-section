from datetime import date
from http import HTTPStatus

import pytest
from pydantic import ValidationError, parse_raw_as

from app.config import settings
from app.schemas import TradingResultsDB


class TestGetLastTradingDates:
    # fmt: off
    @pytest.mark.parametrize('params, expected_status', [
            ({'days': 1}, HTTPStatus.OK),
            ({'days': '1'}, HTTPStatus.OK),
            ({'days': 1, 'extra': 2}, HTTPStatus.OK),
            ({'days': 0}, HTTPStatus.UNPROCESSABLE_ENTITY),
            ({'days': -1}, HTTPStatus.UNPROCESSABLE_ENTITY),
            ({'days': settings.max_days_limit + 1}, HTTPStatus.UNPROCESSABLE_ENTITY), # noqa: E501
            ({'days': 'str'}, HTTPStatus.UNPROCESSABLE_ENTITY),
            (None, HTTPStatus.UNPROCESSABLE_ENTITY),
    ])
    # fmt: on
    async def test_get_last_trading_dates(
        self, client, params, expected_status
    ):
        response = await client.get('/api/trading-dates', params=params)
        assert response.status_code == expected_status, (
            f'Статус {response.status_code} вместо {expected_status}'
        )
        if response.status_code == HTTPStatus.OK:
            try:
                dates = parse_raw_as(list[date], response.text)
            except ValidationError as error:  # pragma: no cover
                pytest.fail(
                    f'JSON не соответствует формату [list[date]]: {error}'
                )
            assert dates == sorted(dates, reverse=True), (
                'Даты не отсортированы по убыванию'
            )


class TestGetDynamics:
    # fmt: off
    @pytest.mark.parametrize('params, expected_status, expected_count', [
            ({'start_date': '2025-07-17', 'end_date': '2025-07-18'}, HTTPStatus.OK, 4),                             # noqa: E501
            ({'start_date': '2025-07-17', 'end_date': '2025-07-17'}, HTTPStatus.OK, 2),                             # noqa: E501
            ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'oil_id': 'A106'},HTTPStatus.OK, 1),            # noqa: E501
            ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'delivery_type_id': 'J'}, HTTPStatus.OK, 2),    # noqa: E501
            ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'delivery_basis_id': 'PDK'}, HTTPStatus.OK, 1), # noqa: E501
            ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'oil_id': 'XXXX'}, HTTPStatus.OK, 0),           # noqa: E501
            ({'start_date': 'str', 'end_date': '2025-07-18'}, HTTPStatus.UNPROCESSABLE_ENTITY, None),               # noqa: E501
            ({'start_date': '2025-07-18', 'end_date': '2025-07-17'}, HTTPStatus.UNPROCESSABLE_ENTITY, None),        # noqa: E501
            ({'start_date': '2025-07-17'}, HTTPStatus.UNPROCESSABLE_ENTITY, None),                                  # noqa: E501
            ({'end_date': '2025-07-18'}, HTTPStatus.UNPROCESSABLE_ENTITY, None),                                    # noqa: E501
            (None, HTTPStatus.UNPROCESSABLE_ENTITY, None),
    ])
    # fmt: on
    async def test_get_dynamics(
        self, client, params, expected_status, expected_count
    ):
        response = await client.get('/api/results-by-date', params=params)
        assert response.status_code == expected_status, (
            f'Статус {response.status_code} вместо {expected_status}'
        )
        if response.status_code == HTTPStatus.OK:
            try:
                trading_results = parse_raw_as(
                    list[TradingResultsDB], response.text
                )
            except ValidationError as error:  # pragma: no cover
                pytest.fail(
                    f'JSON не соответствует формату '
                    f'[list[TradingResultsDB]]: {error}'
                )   
            assert len(trading_results) == expected_count, (
                f'Ожидали {expected_count} записей, '
                f'получили {len(trading_results)}'
            )
            assert trading_results == sorted(
                trading_results, key=lambda tr: (
                    -tr.date.toordinal(), tr.exchange_product_id
                )
            ),'Нарушен порядок сортировки'
                
    async def test_get_dynamics_when_range_exceeds_limit(self, client, mocker):
        mocker.patch('app.config.settings.max_days_range', 0)
        response = await client.get('/api/results-by-date', params={
                'start_date': '2025-07-17',
                'end_date': '2025-07-18',
        })
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, (
        f'При превышении лимита max_days_range '
        f'ожидался статус 422 вместо {response.status_code}')


class TestGetTradingResults:
    # fmt: off
    @pytest.mark.parametrize('params, expected_status, expected_count', [
            (None, HTTPStatus.OK, 2),
            ({'extra': 2}, HTTPStatus.OK, 2),
            ({'oil_id': 'D410'}, HTTPStatus.OK, 1),
            ({'delivery_basis_id': 'KZN'}, HTTPStatus.OK, 1),
            ({'delivery_type_id': 'J'}, HTTPStatus.OK, 1),
            ({'oil_id': 'A106'}, HTTPStatus.OK, 0),
            ({'oil_id': 'XXX'}, HTTPStatus.UNPROCESSABLE_ENTITY, None),
            ({'delivery_basis_id': 'PD'}, HTTPStatus.UNPROCESSABLE_ENTITY, None),  # noqa: E501
            ({'delivery_type_id': 'JJ'}, HTTPStatus.UNPROCESSABLE_ENTITY, None),   # noqa: E501
    ])
    # fmt: on
    async def test_get_trading_results(
        self, client, params, expected_status, expected_count
    ):
        response = await client.get('/api/last-results', params=params)
        assert response.status_code == expected_status, (
            f'Статус {response.status_code} вместо {expected_status}'
        )
        if response.status_code == HTTPStatus.OK:
            try:
                trading_results = parse_raw_as(
                    list[TradingResultsDB], response.text
                )
            except ValidationError as error:  # pragma: no cover
                pytest.fail(
                    f'JSON не соответствует формату '
                    f'[list[TradingResultsDB]]: {error}'
                )
            assert len(trading_results) == expected_count, (
                f'Ожидали {expected_count} записей, '
                f'получили {len(trading_results)}'
            )
            assert trading_results == sorted(
                trading_results, key=lambda tr: (
                    -tr.date.toordinal(), tr.exchange_product_id
                )
            ), 'Нарушен порядок сортировки'
