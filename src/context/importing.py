def merge_python_imports(src_code, destination_code):
    """
    Extracts top level import statements in the src_code and merges them into the destination_code. If a symbol is
    already imported from a module, we insert new imports in the same import statement. Otherwise after the last
    top level import statement.
    """
