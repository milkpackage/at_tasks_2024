import requests
import pytest
from models import *


class TestTrelloSyncAPI:
    def test_create_board(self, base_url, auth_params):
        board_request = BoardRequest()
        response = requests.post(
            f"{base_url}/boards",
            params={
                **auth_params,
                "name": board_request.name,
                "defaultLists": "false"  # Prevent creation of default lists
            }
        )
        assert response.status_code == 200, f"Failed to create board. Response: {response.text}"
        board_data = response.json()
        board_response = BoardResponse(**board_data)
        assert ResponseValidator.validate_board(board_data)
        return board_response.id

    def test_create_list(self, base_url, auth_params):
        board_id = self.test_create_board(base_url, auth_params)
        list_request = ListRequest(name="AQATask", idBoard=board_id)
        response = requests.post(
            f"{base_url}/lists",
            params={**auth_params, **list_request.__dict__}
        )
        assert response.status_code == 200, f"Failed to create list. Response: {response.text}"
        list_data = response.json()
        assert ResponseValidator.validate_list(list_data)
        return list_data['id']

    def test_complete_flow(self, base_url, auth_params):
        # Create board
        board_request = BoardRequest()
        response = requests.post(
            f"{base_url}/boards",
            params={
                **auth_params,
                "name": board_request.name,
                "defaultLists": "false"
            }
        )
        assert response.status_code == 200, f"Failed to create board. Response: {response.text}"
        board_data = response.json()
        board_response = BoardResponse(**board_data)
        board_id = board_response.id
        print(f"Board created with ID: {board_id}")

        # Create list
        list_request = ListRequest(name="AQATask", idBoard=board_id)
        response = requests.post(
            f"{base_url}/lists",
            params={**auth_params, **list_request.__dict__}
        )
        assert response.status_code == 200, f"Failed to create list. Response: {response.text}"
        list_data = response.json()
        list_id = list_data['id']
        print(f"List created with ID: {list_id}")

        # Create card
        card_request = CardRequest(idList=list_id)
        response = requests.post(
            f"{base_url}/cards",
            params={**auth_params, **card_request.__dict__}
        )
        assert response.status_code == 200, f"Failed to create card. Response: {response.text}"
        card_data = response.json()
        card_id = card_data['id']
        print(f"Card created with ID: {card_id}")

        # Add due date
        due_date = "2024-12-12"
        response = requests.put(
            f"{base_url}/cards/{card_id}",
            params={**auth_params, "due": due_date}
        )
        assert response.status_code == 200, f"Failed to add due date. Response: {response.text}"
        card_data = response.json()
        assert card_data['due'] is not None
        print(f"Due date added: {due_date}")

        # Create label
        label_request = LabelRequest(
            name="AQATask",
            color="pink",
            idBoard=board_id
        )
        response = requests.post(
            f"{base_url}/labels",
            params={**auth_params, **label_request.__dict__}
        )
        assert response.status_code == 200, f"Failed to create label. Response: {response.text}"
        label_data = response.json()
        label_id = label_data['id']
        print(f"Label created with ID: {label_id}")

        # Add label to card
        response = requests.put(
            f"{base_url}/cards/{card_id}",
            params=auth_params,
            data={"idLabels": label_id}
        )
        assert response.status_code == 200, f"Failed to add label to card. Response: {response.text}"
        card_data = response.json()
        assert label_id in card_data['idLabels']
        print("Label added to card successfully")