import pytest
from ..importing import merge_python_imports

@pytest.fixture
def sample_src_code():
    return """
import os
from django.db import models

def some_function():
    pass
"""

@pytest.fixture
def sample_dest_code():
    return """
import sys
from django.http import HttpResponse

class SomeClass:
    pass
"""

def test_merge_python_imports(sample_src_code, sample_dest_code):
    result = merge_python_imports(sample_src_code, sample_dest_code, debug=True)
    
    # Check that all original imports are preserved
    assert "import sys" in result
    assert "from django.http import HttpResponse" in result
    
    # Check that new imports are added
    assert "import os" in result
    assert "from django.db import models" in result
    
    # Check that imports are present
    lines = result.split('\n')
    assert "import os" in lines
    assert "import sys" in lines
    db_index = lines.index("from django.db import models")
    http_index = lines.index("from django.http import HttpResponse")
    assert db_index < http_index, f"'from django.db import models' (index: {db_index}) should come before 'from django.http import HttpResponse' (index: {http_index})"
    
    # Check that non-import code is preserved
    assert "class SomeClass:" in result
    assert "def some_function():" not in result  # This should not be in the result

def test_merge_python_imports_with_existing_imports():
    src_code = """
from django.db import models
from django.http import JsonResponse
"""
    dest_code = """
from django.db import models
from django.http import HttpResponse
"""
    result = merge_python_imports(src_code, dest_code, debug=True)
    
    assert "from django.db import models" in result
    assert "from django.http import HttpResponse, JsonResponse" in result
    http_import_count = result.count("from django.http import")
    assert http_import_count == 1, f"Expected 1 'from django.http import' statement, but found {http_import_count}"

def test_merge_python_imports_with_no_imports():
    src_code = "def some_function():\n    pass\n"
    dest_code = "class SomeClass:\n    pass\n"
    result = merge_python_imports(src_code, dest_code, debug=True)
    
    assert result == dest_code  # No changes should be made

def test_merge_python_imports_with_complex_imports():
    src_code = """
from module1 import (
    func1,
    func2,
)
import module2 as m2
"""
    dest_code = """
from module1 import func3
import module2
"""
    result = merge_python_imports(src_code, dest_code, debug=True)
    
    assert "from module1 import (" in result
    assert "func1," in result
    assert "func2," in result
    assert "func3" in result
    assert "import module2 as m2" in result
    assert "import module2" not in result  # This should be replaced by the 'as' import
