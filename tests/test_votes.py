def test_vote_on_post(authorized_client, test_posts):
    data = {"post_id": test_posts[0].id, "dir": 1}
    res = authorized_client.post("/savotes/", json=data)
    assert res.status_code == 201

def test_vote_twice_post(authorized_client, test_posts, test_votes):
    data = {"post_id": test_posts[3].id, "dir": 1}
    res = authorized_client.post("/savotes/", json=data)
    assert res.status_code == 409

def test_unvote(authorized_client, test_posts, test_votes):
    data = {"post_id": test_posts[3].id, "dir": 0}
    res = authorized_client.post("/savotes/", json=data)
    assert res.status_code == 201

def test_unvote_not_exist(authorized_client, test_posts, test_votes):
    data = {"post_id": test_posts[1].id, "dir": 0}
    res = authorized_client.post("/savotes/", json=data)
    assert res.status_code == 404

def test_vote_not_exist(authorized_client, test_posts, test_votes):
    data = {"post_id": 55, "dir": 1}
    res = authorized_client.post("/savotes/", json=data)
    assert res.status_code == 404

def test_vote_unauthorized(client, test_posts):
    data = {"post_id": test_posts[0].id, "dir": 1}
    res = client.post("/savotes/", json=data)
    assert res.status_code == 401