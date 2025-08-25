import pytest

from app.config import settings
from app.crud import get_trading_dates


@pytest.mark.asyncio
async def test_settings_loaded():
    assert settings.database_url.startswith('postgresql')


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'days, expected_len', ((0, 0), (1, 2), (2, 4), (3, 5), (10, 5))
)
async def test_get_trading_dates(db_session, days, expected_len):
    result = await get_trading_dates(db_session, days)
    assert isinstance(result, list)
    assert len(result) == expected_len
    assert result == sorted(result, reverse=True)
