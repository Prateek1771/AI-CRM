def test_create_hcp(client):
    response = client.post("/api/hcps", json={"name": "Dr. Smith", "specialty": "Cardiology"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Dr. Smith"
    assert data["specialty"] == "Cardiology"
    assert "id" in data


def test_list_hcps_no_filter(client):
    client.post("/api/hcps", json={"name": "Dr. Smith"})
    client.post("/api/hcps", json={"name": "Dr. Jones"})
    response = client.get("/api/hcps")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_hcps_with_search(client):
    client.post("/api/hcps", json={"name": "Dr. Smith"})
    client.post("/api/hcps", json={"name": "Dr. Jones"})
    response = client.get("/api/hcps?q=smith")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["name"] == "Dr. Smith"


def test_get_hcp_not_found(client):
    response = client.get("/api/hcps/nonexistent-id")
    assert response.status_code == 404
