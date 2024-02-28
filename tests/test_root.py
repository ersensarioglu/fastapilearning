def test_root(client):
    print("Root path")
    res = client.get("/")
    assert res.json().get('message') == 'Welcome to my API!!'
    assert res.status_code == 200