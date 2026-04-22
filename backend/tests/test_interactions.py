from datetime import date


def test_create_interaction(client):
    response = client.post("/api/interactions", json={
        "interaction_type": "Meeting",
        "date": "2026-04-22",
        "topics_discussed": "Product X efficacy",
        "sentiment": "positive",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["sentiment"] == "positive"
    assert data["topics_discussed"] == "Product X efficacy"


def test_update_interaction_sentiment(client):
    create = client.post("/api/interactions", json={"interaction_type": "Call", "date": "2026-04-22"})
    interaction_id = create.json()["id"]
    response = client.patch(f"/api/interactions/{interaction_id}", json={"sentiment": "neutral"})
    assert response.status_code == 200
    assert response.json()["sentiment"] == "neutral"


def test_delete_interaction(client):
    create = client.post("/api/interactions", json={"interaction_type": "Call", "date": "2026-04-22"})
    interaction_id = create.json()["id"]
    response = client.delete(f"/api/interactions/{interaction_id}")
    assert response.status_code == 204
    get = client.get(f"/api/interactions/{interaction_id}")
    assert get.status_code == 404
