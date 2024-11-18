from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class BoardRequest:
    name: str = "AQATESTLAB15"

@dataclass
class ListRequest:
    name: str
    idBoard: str

@dataclass
class CardRequest:
    idList: str
    name: str = "Test Card"

@dataclass
class LabelRequest:
    name: str
    color: str
    idBoard: str


@dataclass
class BoardResponse:
    id: str
    name: str
    desc: Optional[str] = None
    closed: Optional[bool] = None
    idOrganization: Optional[str] = None
    url: Optional[str] = None
    additional_fields: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, id: str, name: str, **kwargs):
        self.id = id
        self.name = name
        self.desc = kwargs.get('desc')
        self.closed = kwargs.get('closed')
        self.idOrganization = kwargs.get('idOrganization')
        self.url = kwargs.get('url')
        self.additional_fields = {k: v for k, v in kwargs.items()
                                if k not in ['id', 'name', 'desc', 'closed', 'idOrganization', 'url']}

@dataclass
class ListResponse:
    id: str
    name: str
    idBoard: str

@dataclass
class CardResponse:
    id: str
    name: str
    idList: str
    due: Optional[str] = None
    idLabels: Optional[List[str]] = None

@dataclass
class LabelResponse:
    id: str
    name: str
    color: str
    idBoard: str

class ResponseValidator:
    @staticmethod
    def validate_board(response_data: dict) -> bool:
        required_fields = ['id', 'name']
        return all(field in response_data for field in required_fields)

    @staticmethod
    def validate_list(response_data: dict) -> bool:
        required_fields = ['id', 'name', 'idBoard']
        return all(field in response_data for field in required_fields)

    @staticmethod
    def validate_card(response_data: dict) -> bool:
        required_fields = ['id', 'name', 'idList']
        return all(field in response_data for field in required_fields)

    @staticmethod
    def validate_label(response_data: dict) -> bool:
        required_fields = ['id', 'name', 'color', 'idBoard']
        return all(field in response_data for field in required_fields)