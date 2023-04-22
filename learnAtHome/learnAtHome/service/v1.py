from django.core.exceptions import FieldError
from learnAtHome.exceptions import VALIDATION_ERROR
from django.forms import ModelForm


class BaseService():
    def __init__(self) -> None:
        self._errors = {}

    def add_errors(self, error_key:str, error_message:str) -> bool:
        if not error_key:
            return False
        else:
            if error_message:
                if error_key in self._errors:
                    self._errors[error_key].append(error_message)
                else:
                    self._errors[error_key] = [error_message]
            else:
                self._errors[error_key] = []
            return True
    
    def get_errors(self) -> dict:
        return self._errors

    def has_errors(self) -> bool:
        return True if len(self._errors) else False


class BaseModelFormService(BaseService):
    FORM:ModelForm = None
    IS_SUPER_USER = False
    CLEANED_DATA = None

    def __init__(self, form) -> None:
        super().__init__()
        self.FORM = form
    
    def is_valid(self):
        return self.FORM.is_valid()
    
    def save(self, data:dict={}):
        if self.is_valid():
            pass
        else:
            return False
            
