def test_submit_success(client):
    payload = {
        "value": "8.8.8.8",
        "tags": ["network", "dns"]
    }
    response = client.post("/submit", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data, dict)
    assert "id" in data


def test_submit_invalid_value(client):
    payload = {
        "value": "not-an-ip-or-hash",
        "tags": ["bad"]
    }
    response = client.post("/submit", json=payload)
    assert response.status_code == 400
    assert "error" in response.json()


def test_query_with_value(client):
    client.post("/submit", json={"value": "1.1.1.1", "tags": ["cloudflare"]})
    response = client.get("/data", params={"value": "1.1.1.1"})
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) >= 1
    assert data["data"][0]["value"] == "1.1.1.1"
    assert "tags" in data["data"][0]
    assert "type" in data["data"][0]


def test_query_with_no_match(client):
    response = client.get("/data", params={"value": "255.255.255.255"})
    assert response.status_code == 404
    assert "error" in response.json()
