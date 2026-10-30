def test_create_ticket(client):
    response = client.post(
        "/tickets/",
        json={
            "title": "Laptop cannot connect to Wi-Fi",
            "description": "The laptop detects the network but fails to connect.",
            "priority": "high",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "Ticket created successfully"
    assert data["data"]["id"] is not None
    assert data["data"]["title"] == "Laptop cannot connect to Wi-Fi"
    assert data["data"]["priority"] == "high"


def test_list_tickets(client):
    client.post(
        "/tickets/",
        json={
            "title": "Printer is not working",
            "description": "The office printer does not respond to print jobs.",
            "priority": "medium",
        },
    )

    response = client.get("/tickets/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Printer is not working"
    assert data[0]["priority"] == "medium"


def test_get_ticket(client):
    create_response = client.post(
        "/tickets/",
        json={
            "title": "Email application crashes",
            "description": "The email application closes unexpectedly when opened.",
            "priority": "high",
        },
    )

    ticket_id = create_response.json()["data"]["id"]

    response = client.get(f"/tickets/{ticket_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == ticket_id
    assert data["title"] == "Email application crashes"
    assert data["priority"] == "high"


def test_get_ticket_not_found(client):
    response = client.get("/tickets/9999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}


def test_update_ticket(client):
    create_response = client.post(
        "/tickets/",
        json={
            "title": "Keyboard not working",
            "description": "Several keys on the keyboard do not respond.",
            "priority": "low",
        },
    )

    ticket_id = create_response.json()["data"]["id"]

    update_response = client.put(
        f"/tickets/{ticket_id}",
        json={
            "title": "Keyboard completely unresponsive",
            "description": "The entire keyboard has stopped responding.",
            "priority": "high",
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == ticket_id
    assert data["title"] == "Keyboard completely unresponsive"
    assert data["description"] == "The entire keyboard has stopped responding."
    assert data["priority"] == "high"


def test_delete_ticket(client):
    create_response = client.post(
        "/tickets/",
        json={
            "title": "Mouse stopped working",
            "description": "The mouse no longer responds when connected.",
            "priority": "medium",
        },
    )

    ticket_id = create_response.json()["data"]["id"]

    delete_response = client.delete(f"/tickets/{ticket_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Ticket deleted successfully"

    get_response = client.get(f"/tickets/{ticket_id}")

    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Ticket not found"}


def test_create_ticket_invalid_data(client):
    response = client.post(
        "/tickets/",
        json={
            "title": "Bug",
            "description": "The application crashes.",
            "priority": "urgent",
        },
    )

    assert response.status_code == 422


def test_update_ticket_not_found(client):
    response = client.put(
        "/tickets/9999",
        json={
            "title": "Updated network issue",
            "description": "The network connection keeps dropping.",
            "priority": "high",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}


def test_delete_ticket_not_found(client):
    response = client.delete("/tickets/9999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}


def test_list_tickets_pagination(client):
    titles = ["First network issue", "Second network issue", "Third network issue"]

    for title in titles:
        client.post(
            "/tickets/",
            json={
                "title": title,
                "description": "A network issue needs technical support.",
                "priority": "medium",
            },
        )

    response = client.get("/tickets/?skip=1&limit=1")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Second network issue"


def test_list_tickets_invalid_limit(client):
    response = client.get("/tickets/?limit=101")

    assert response.status_code == 422


def test_list_tickets_invalid_skip(client):
    response = client.get("/tickets/?skip=-1")

    assert response.status_code == 422


def test_list_tickets_by_priority(client):
    tickets = [
        ("Network problem", "Network connection keeps dropping.", "high"),
        ("Printer problem", "Printer does not respond.", "medium"),
        ("Mouse problem", "Mouse occasionally disconnects.", "low"),
    ]

    for title, description, priority in tickets:
        client.post(
            "/tickets/",
            json={"title": title, "description": description, "priority": priority},
        )

    response = client.get("/tickets/?priority=high")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Network problem"
    assert data[0]["priority"] == "high"


def test_list_tickets_invalid_priority(client):
    response = client.get("/tickets/?priority=urgent")

    assert response.status_code == 422


def test_list_tickets_priority_pagination(client):
    tickets = [
        ("First high priority issue", "A high priority network issue.", "high"),
        ("Medium priority issue", "A medium priority printer issue.", "medium"),
        ("Second high priority issue", "A high priority server issue.", "high"),
        ("Third high priority issue", "A high priority database issue.", "high"),
    ]

    for title, description, priority in tickets:
        client.post(
            "/tickets/",
            json={"title": title, "description": description, "priority": priority},
        )

    response = client.get("/tickets/?priority=high&skip=1&limit=1")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Second high priority issue"
    assert data[0]["priority"] == "high"


def test_create_ticket_default_priority(client):
    response = client.post(
        "/tickets/",
        json={
            "title": "Default priority test",
            "description": "Testing the default ticket priority",
        },
    )

    assert response.status_code == 201
    assert response.json()["data"]["priority"] == "medium"
