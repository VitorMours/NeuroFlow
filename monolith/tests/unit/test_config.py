import pytest 
import importlib

class TestConfig:
    
    def test_is_running(self) -> None:
        assert True 
        
    def test_if_all_configs_exists(self) -> None:
        module = importlib.import_module("config")
        assert hasattr(module, "Config")