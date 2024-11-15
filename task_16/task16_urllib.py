# task16_urllib3.py
import certifi
import urllib3
import json
from urllib.parse import urlencode
import pytest
from models import *


class TestTrelloUrllib3API:
    @pytest.fixture(autouse=True)
    def setup(self):
        urllib3.disable_warnings()
        self.http = urllib3.PoolManager(cert_reqs='CERT_NONE')

    def make_request(self, method, url, fields=None, body=None):
        #helper method to make requests with proper encoding
        if fields:
            url = f"{url}?{urlencode(fields)}"

        response = self.http.request(
            method,
            url,
            json=body
        )
        return response

    def test_complete_flow(self, base_url, auth_params):
        #board creation
        board_request = BoardRequest()
        response = self.make_request(
            'POST',
            f"{base_url}/boards",
            fields={
                **auth_params,
                "name": board_request.name,
                "defaultLists": "false"
            }
        )
        assert response.status == 200, f"Failed to create board. Response: {response.data.decode('utf-8')}"
        board_data = json.loads(response.data.decode('utf-8'))
        board_response = BoardResponse(**board_data)
        board_id = board_response.id
        print(f"Board created with ID: {board_id}")

        #list creation
        list_request = ListRequest(name="AQATask", idBoard=board_id)
        response = self.make_request(
            'POST',
            f"{base_url}/lists",
            fields={
                **auth_params,
                **list_request.__dict__
            }
        )
        assert response.status == 200, f"Failed to create list. Response: {response.data.decode('utf-8')}"
        list_data = json.loads(response.data.decode('utf-8'))
        list_id = list_data['id']
        print(f"List created with ID: {list_id}")

        #card creation
        card_request = CardRequest(idList=list_id)
        response = self.make_request(
            'POST',
            f"{base_url}/cards",
            fields={
                **auth_params,
                **card_request.__dict__
            }
        )
        assert response.status == 200, f"Failed to create card. Response: {response.data.decode('utf-8')}"
        card_data = json.loads(response.data.decode('utf-8'))
        card_id = card_data['id']
        print(f"Card created with ID: {card_id}")

        #due date
        due_date = "2024-12-12"
        response = self.make_request(
            'PUT',
            f"{base_url}/cards/{card_id}",
            fields={
                **auth_params,
                "due": due_date
            }
        )
        assert response.status == 200, f"Failed to add due date. Response: {response.data.decode('utf-8')}"
        card_data = json.loads(response.data.decode('utf-8'))
        assert card_data['due'] is not None
        print(f"Due date added: {due_date}")

        #label creation
        label_request = LabelRequest(
            name="AQATask",
            color="pink",
            idBoard=board_id
        )
        response = self.make_request(
            'POST',
            f"{base_url}/labels",
            fields={
                **auth_params,
                **label_request.__dict__
            }
        )
        assert response.status == 200, f"Failed to create label. Response: {response.data.decode('utf-8')}"
        label_data = json.loads(response.data.decode('utf-8'))
        label_id = label_data['id']
        print(f"Label created with ID: {label_id}")

        #adding label
        response = self.make_request(
            'PUT',
            f"{base_url}/cards/{card_id}",
            fields=auth_params,
            body={"idLabels": label_id}
        )
        assert response.status == 200, f"Failed to add label to card. Response: {response.data.decode('utf-8')}"
        card_data = json.loads(response.data.decode('utf-8'))
        assert label_id in card_data['idLabels']
        print("Label added to card successfully")

    #testing separatly all
    def test_separate_steps(self, base_url, auth_params):

        # Create board
        board_request = BoardRequest()
        response = self.make_request(
            'POST',
            f"{base_url}/boards",
            fields={
                **auth_params,
                "name": board_request.name,
                "defaultLists": "false"
            }
        )
        assert response.status == 200
        board_data = json.loads(response.data.decode('utf-8'))
        board_id = board_data['id']

        # Create list
        list_request = ListRequest(name="AQATask", idBoard=board_id)
        response = self.make_request(
            'POST',
            f"{base_url}/lists",
            fields={
                **auth_params,
                **list_request.__dict__
            }
        )
        assert response.status == 200
        list_data = json.loads(response.data.decode('utf-8'))
        assert ResponseValidator.validate_list(list_data)