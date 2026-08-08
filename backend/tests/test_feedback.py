"""フィードバック API のテスト。"""


def test_submit_feedback_with_rating(client):
    res = client.post("/api/v1/feedback", json={"rating": 5, "comment": "使いやすいです"})
    assert res.status_code == 201
    assert res.json()["rating"] == 5


def test_submit_feedback_with_comment_only(client):
    res = client.post("/api/v1/feedback", json={"rating": None, "comment": "改善希望"})
    assert res.status_code == 201


def test_submit_empty_feedback_rejected(client):
    res = client.post("/api/v1/feedback", json={"rating": None, "comment": ""})
    assert res.status_code == 422


def test_rating_out_of_range_rejected(client):
    res = client.post("/api/v1/feedback", json={"rating": 6, "comment": "test"})
    assert res.status_code == 422


def test_list_feedback(client):
    client.post("/api/v1/feedback", json={"rating": 4, "comment": "いいね"})
    res = client.get("/api/v1/feedback")
    assert res.status_code == 200
    assert len(res.json()) >= 1
