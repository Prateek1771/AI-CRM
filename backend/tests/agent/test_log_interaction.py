from unittest.mock import MagicMock, patch
from app.agent.tools.log_interaction import extract_interaction_fields


def test_extract_fields_from_summary():
    summary = "Met Dr. Smith today, discussed Product X efficacy, positive sentiment, shared brochure"
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.hcp_name = "Dr. Smith"
    mock_response.topics_discussed = "Product X efficacy"
    mock_response.sentiment = "positive"
    mock_response.materials_shared = ["brochure"]
    mock_response.interaction_type = "Meeting"
    mock_response.date = None
    mock_response.samples_distributed = None
    mock_response.outcomes = None
    mock_response.follow_up_actions = None
    mock_response.model_dump.return_value = {
        "hcp_name": "Dr. Smith",
        "topics_discussed": "Product X efficacy",
        "sentiment": "positive",
        "materials_shared": ["brochure"],
        "interaction_type": "Meeting",
        "date": None,
        "samples_distributed": None,
        "outcomes": None,
        "follow_up_actions": None,
    }
    mock_llm.with_structured_output.return_value.invoke.return_value = mock_response

    result = extract_interaction_fields(summary, mock_llm)
    assert result["hcp_name"] == "Dr. Smith"
    assert result["sentiment"] == "positive"
    assert "brochure" in result["materials_shared"]
