import requests

class TestTicketsAPI:
    def test_create(self):
        #Arrange
        data_in = {
            "row": 137,
            "place":1000,
            "name_movie": "move1",
            "price": 700
        }     
           
        data_expect = [{
            'id' : 1,
           "row": 137,
            "place":1000,
            "name_movie": "move1",
            "price": 700
        }]
        #Act
        response_post = requests.post("http://localhost:6666/tickets",data=data_in)
        print(response_post)
        response_get = requests.get("http://localhost:6666/tickets")
        #Assert
        assert response_post.status_code == 200
        assert response_get.status_code == 200
        assert data_expect==response_get.json()
    