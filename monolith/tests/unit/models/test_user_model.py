import pytest
from src.models.user_model import User

class TestUserModel:
    def test_create_user(self) -> None:
        user_instance = User(
                first_name = "Lucas",
                last_name = "Moura",
                email = "lucas.moura@email.com",
                password = "32322916aA!"
        )
        assert type(user_instance) == User
        
    def test_user_string_represetation(self) -> None:
        user_instance = User(
                first_name = "Lucas",
                last_name = "Moura",
                email = "lucas.moura@gmail.com",
                password = "32322916aA!")
        assert str(user_instance) == "Lucas Moura: lucas.moura@gmail.com"
        
    def test_get_user_first_name(self, create_default_static_user) -> None:
        assert create_default_static_user.first_name == "Lucas"
        
    def test_get_user_last_name(self, create_default_static_user) -> None:
        assert create_default_static_user.last_name == "Moura"
    
    def test_get_user_email(self, create_default_static_user) -> None:
        assert create_default_static_user.email == "lucas.moura@email.com"
        
    def test_get_user_password(self, create_default_static_user) -> None:
        assert create_default_static_user.password == "32322916aA!"
        
    def test_modify_user_frst_name(self, create_default_static_user) -> None:
        create_default_static_user.first_name = "Pietro"
        assert create_default_static_user.first_name == "Pietro"
        
    def test_modify_user_last_name(self, create_default_static_user) -> None:
        create_default_static_user.last_name = "Juan"
        assert create_default_static_user.last_name == "Juan"
    
    def test_modify_user_email(self, create_default_static_user) -> None:
        create_default_static_user.email = "email@teste.com"
        assert create_default_static_user.email == "email@teste.com"
        
    def test_modify_user_password(self, create_default_static_user) -> None:
        create_default_static_user.password = "123123123aA!"
        assert create_default_static_user.password == "123123123aA!"

    def test_wrong_primitive_type_in_first_name(self, create_default_static_user) -> None:
        with pytest.raises(TypeError):
            create_default_static_user.first_name(123)

    def test_wrong_primitive_value_for_last_name(self, create_default_static_user) -> None:
        with pytest.raises(TypeError):
            create_default_static_user.last_name(123)

    def test_wrong_primitive_type_for_email(self, create_default_static_user) -> None:
        with pytest.raises(TypeError):
            create_default_static_user.email(123)