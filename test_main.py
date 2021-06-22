from fastapi.testclient import TestClient
import main   


client = TestClient(main.app)

def test_read_main():
    response = client.get("/get_story/")
    assert response.status_code == 401
    assert response.json() == {"msg": "Hello World"}




