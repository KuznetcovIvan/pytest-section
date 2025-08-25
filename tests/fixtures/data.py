from datetime import date

import pytest

from app.db import TradingResults


@pytest.fixture(scope='session')
def trading_results():
    return [
        TradingResults(
            exchange_product_id='A106PDK001J',
            exchange_product_name='Бензин АИ-100-К5, ПДК',
            delivery_basis_name='Предкомбинатская-группа станций',
            volume=100,
            total=9000000,
            count=2,
            date=date(2025, 7, 16),
        ),
        TradingResults(
            exchange_product_id='A106MST002K',
            exchange_product_name='Бензин АИ-100-К5, Москва',
            delivery_basis_name='Московская станция',
            volume=120,
            total=9500000,
            count=3,
            date=date(2025, 7, 17),
        ),
        TradingResults(
            exchange_product_id='B205NVO003J',
            exchange_product_name='Бензин АИ-95-К5, Новосибирск',
            delivery_basis_name='Новосибирская станция',
            volume=130,
            total=9800000,
            count=3,
            date=date(2025, 7, 17),
        ),
        TradingResults(
            exchange_product_id='C303KZN004L',
            exchange_product_name='Дизель Евро-5, Казань',
            delivery_basis_name='Казанский терминал',
            volume=140,
            total=10000000,
            count=4,
            date=date(2025, 7, 18),
        ),
        TradingResults(
            exchange_product_id='D410PDK005J',
            exchange_product_name='Дизель зимний Евро-5, ПДК',
            delivery_basis_name='Предкомбинатская-группа станций',
            volume=150,
            total=10500000,
            count=4,
            date=date(2025, 7, 18),
        ),
    ]
