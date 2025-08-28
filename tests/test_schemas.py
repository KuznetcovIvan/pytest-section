from contextlib import nullcontext as does_not_raise
from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas import DynamicTradingResultsQuery, TradingResultsQuery


# fmt: off
@pytest.mark.parametrize('data, expectation', [
    ({}, does_not_raise()),
    ({'oil_id': 'A106'}, does_not_raise()),
    ({'delivery_basis_id': 'PDK'}, does_not_raise()),
    ({'delivery_type_id': 'J'}, does_not_raise()),
    ({'oil_id': 'D410', 'delivery_basis_id': 'PDK', 'delivery_type_id': 'J'}, does_not_raise()),            # noqa: E501

    ({'oil_id': None}, does_not_raise()),
    ({'delivery_basis_id': None}, does_not_raise()),
    ({'delivery_type_id': None}, does_not_raise()),

    ({'oil_id': 'A10'}, pytest.raises(ValidationError)),
    ({'oil_id': 'A1067'}, pytest.raises(ValidationError)),
    ({'oil_id': ''}, pytest.raises(ValidationError)),

    ({'delivery_basis_id': 'PD'}, pytest.raises(ValidationError)),
    ({'delivery_basis_id': 'PDKM'}, pytest.raises(ValidationError)),
    ({'delivery_basis_id': ''}, pytest.raises(ValidationError)),

    ({'delivery_type_id': ''}, pytest.raises(ValidationError)),
    ({'delivery_type_id': 'JJ'}, pytest.raises(ValidationError)),

    ({'oil_id': 'A10', 'delivery_type_id': 'JJ'}, pytest.raises(ValidationError)),                          # noqa: E501
])
# fmt: on
def test_schema_trading_results_query(data, expectation):
    with expectation:
        TradingResultsQuery(**data)

# fmt: off
@pytest.mark.parametrize('data, expectation', [
    ({'start_date': '2025-07-17', 'end_date': '2025-07-18'}, does_not_raise()),

    ({'start_date': date(2025, 7, 17), 'end_date': date(2025, 7, 18)}, does_not_raise()),                   # noqa: E501

    ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'oil_id': 'A106'}, does_not_raise()),           # noqa: E501
    ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'delivery_basis_id': 'PDK'}, does_not_raise()), # noqa: E501
    ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'delivery_type_id': 'J'}, does_not_raise()),    # noqa: E501

    ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'oil_id': None}, does_not_raise()),             # noqa: E501
    ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'delivery_basis_id': None}, does_not_raise()),  # noqa: E501
    ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'delivery_type_id': None}, does_not_raise()),   # noqa: E501

    ({'end_date': '2025-07-18'}, pytest.raises(ValidationError)),
    ({'start_date': '2025-07-17'}, pytest.raises(ValidationError)),
    ({}, pytest.raises(ValidationError)),

    ({'start_date': '17/07/2025', 'end_date': '18/07/2025'}, pytest.raises(ValidationError)),               # noqa: E501

    ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'oil_id': 'A10'}, pytest.raises(ValidationError)),                              # noqa: E501
    ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'oil_id': 'A1067'}, pytest.raises(ValidationError)),                            # noqa: E501
    ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'oil_id': ''}, pytest.raises(ValidationError)),                                 # noqa: E501

    ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'delivery_basis_id': 'PD'}, pytest.raises(ValidationError)),                    # noqa: E501
    ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'delivery_basis_id': 'PDKM'}, pytest.raises(ValidationError)),                  # noqa: E501
    ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'delivery_basis_id': ''}, pytest.raises(ValidationError)),                      # noqa: E501

    ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'delivery_type_id': ''}, pytest.raises(ValidationError)),                       # noqa: E501
    ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'delivery_type_id': 'JJ'}, pytest.raises(ValidationError)),                     # noqa: E501

    ({'start_date': '2025-07-17', 'end_date': '2025-07-18', 'oil_id': 'A10', 'delivery_type_id': 'JJ'}, pytest.raises(ValidationError)),    # noqa: E501
])
# fmt: on
def test_schema_dynamic_trading_results_query(data, expectation):
    with expectation:
        DynamicTradingResultsQuery(**data)
