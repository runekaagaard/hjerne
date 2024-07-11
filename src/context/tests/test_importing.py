import pytest
from context.importing import merge_python_imports

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
    result = merge_python_imports(sample_src_code, sample_dest_code)
    
    # Check that all original imports are preserved
    assert "import sys" in result
    assert "from django.http import HttpResponse" in result
    
    # Check that new imports are added
    assert "import os" in result
    assert "from django.db import models" in result
    
    # Check the order of imports
    lines = result.split('\n')
    assert lines.index("import os") < lines.index("import sys")
    assert lines.index("from django.db import models") < lines.index("from django.http import HttpResponse")
    
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
    result = merge_python_imports(src_code, dest_code)
    
    assert "from django.db import models" in result
    assert "from django.http import HttpResponse, JsonResponse" in result
    assert result.count("from django.http import") == 1  # Ensure there's only one import statement for django.http

def test_merge_python_imports_with_no_imports():
    src_code = "def some_function():\n    pass\n"
    dest_code = "class SomeClass:\n    pass\n"
    result = merge_python_imports(src_code, dest_code)
    
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
    result = merge_python_imports(src_code, dest_code)
    
    assert "from module1 import (" in result
    assert "func1," in result
    assert "func2," in result
    assert "func3" in result
    assert "import module2 as m2" in result
    assert "import module2" not in result  # This should be replaced by the 'as' import
