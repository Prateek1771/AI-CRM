import pytest
from app.agent.tools.search_hcp import search_hcp_by_name
from app.models.hcp import HCP


def test_search_hcp_exact_match(db):
    hcp = HCP(name="Dr. Smith", specialty="Cardiology")
    db.add(hcp)
    db.commit()

    result = search_hcp_by_name("Dr. Smith", db)
    assert result["found"] is True
    assert result["hcp"]["name"] == "Dr. Smith"
    assert result["hcp"]["id"] == hcp.id


def test_search_hcp_partial_match(db):
    hcp = HCP(name="Dr. Smith")
    db.add(hcp)
    db.commit()

    result = search_hcp_by_name("Smith", db)
    assert result["found"] is True
    assert result["hcp"]["name"] == "Dr. Smith"


def test_search_hcp_not_found(db):
    result = search_hcp_by_name("Dr. Unknown", db)
    assert result["found"] is False
    assert result["hcp"] is None
