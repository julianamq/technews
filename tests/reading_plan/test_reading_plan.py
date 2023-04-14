from tech_news.analyzer.reading_plan import ReadingPlanService
import pytest
from unittest.mock import patch

new_mock = [
    {
        "url": "https://blog.betrybe.com/teste/teste-de-mock1",
        "title": "Luis Vabo",
        "timestamp": "14/04/2023",
        "writer": "podcast",
        "reading_time": 3,
        "summary": "youtube",
        "category": "vídeo",
    },
    {
        "url": "https://blog.betrybe.com/teste/teste-de-mock2",
        "title": "Giovanna Mel",
        "timestamp": "14/04/2023",
        "writer": "podcast 2",
        "reading_time": 10,
        "summary": "resso",
        "category": "audio",
    },
]


@patch("tech_news.analyzer.reading_plan.ReadingPlanService._db_news_proxy",
       return_value=new_mock)
def test_reading_plan_group_news(mock_db_news_proxy):
    with pytest.raises(ValueError):
        ReadingPlanService.group_news_for_available_time(-1)

    result = ReadingPlanService.group_news_for_available_time(27)

    assert len(result["readable"]) == 1
    assert len(result["unreadable"]) == 1
    if len(result["readable"]) > 0:
        assert result["readable"][0]["unfilled_time"] == 26