"""Compatibility helper uses the same inline classification as the API."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location("inline_pipeline_compat",Path(__file__).with_name("main.py"))
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
def test_pipeline():
    assert module.mock_categorize_feedback("The water pipe broke outside the clinic.")=="Water"
    assert module.mock_categorize_feedback("The school needs a teacher.")=="Education"
