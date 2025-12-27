import importlib
import src.utils as utils
from faker import Faker
class TestUtils:

    def test_email_validator(self) -> None:
        module = importlib.import_module("src.utils.security")
        assert hasattr(module, "email_validator")

    def test_email_validator_normal_string(self) -> None:
        result = utils.security.email_validator("")
        assert result == False

    def test_email_validator_with_valid_email(self) -> None:
        fake = Faker()
        result = utils.security.email_validator(fake.email())
        assert result == True

