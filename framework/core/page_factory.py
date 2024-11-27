from typing import Dict, Any
import inspect
from core.web_element_wrapper import Element

def find_by(by, value):
    def decorator(func):
        func._finder = (by, value)
        return func
    return decorator

class PageFactory:
    @staticmethod
    def init_elements(page_instance):
        for name, member in inspect.getmembers(page_instance.__class__):
            if hasattr(member, '_finder'):
                finder = getattr(member, '_finder')
                setattr(page_instance, name, 
                    Element(page_instance.driver, *finder))