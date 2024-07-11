import ast
from typing import List, Tuple

def merge_python_imports(src_code: str, destination_code: str) -> str:
    """
    Extracts top level import statements in the src_code and merges them into the destination_code. If a symbol is
    already imported from a module, we insert new imports in the same import statement. Otherwise after the last
    top level import statement.
    """
    src_tree = ast.parse(src_code)
    dest_tree = ast.parse(destination_code)

    src_imports = extract_imports(src_tree)
    dest_imports = extract_imports(dest_tree)

    if not src_imports and not dest_imports:
        return destination_code

    merged_imports = merge_imports(src_imports, dest_imports)

    return insert_imports(destination_code, merged_imports)

def extract_imports(tree: ast.AST) -> List[ast.Import]:
    return [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]

def extract_imports(tree: ast.AST) -> List[ast.Import]:
    return [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]

def merge_imports(src_imports: List[ast.Import], dest_imports: List[ast.Import]) -> List[ast.Import]:
    merged = []
    for src_import in src_imports:
        if isinstance(src_import, ast.Import):
            merged = merge_import(src_import, merged)
        elif isinstance(src_import, ast.ImportFrom):
            merged = merge_import_from(src_import, merged)
    
    for dest_import in dest_imports:
        if isinstance(dest_import, ast.Import):
            merged = merge_import(dest_import, merged)
        elif isinstance(dest_import, ast.ImportFrom):
            merged = merge_import_from(dest_import, merged)
    
    return merged

def merge_import(src_import: ast.Import, dest_imports: List[ast.Import]) -> List[ast.Import]:
    for alias in src_import.names:
        existing_import = next((imp for imp in dest_imports if isinstance(imp, ast.Import) and any(a.name == alias.name for a in imp.names)), None)
        if existing_import:
            existing_alias = next(a for a in existing_import.names if a.name == alias.name)
            if alias.asname and alias.asname != existing_alias.asname:
                existing_import.names.remove(existing_alias)
                existing_import.names.append(alias)
        else:
            dest_imports.append(ast.Import(names=[alias]))
    return dest_imports

def merge_import_from(src_import: ast.ImportFrom, dest_imports: List[ast.Import]) -> List[ast.Import]:
    existing_import = next((imp for imp in dest_imports if isinstance(imp, ast.ImportFrom) and imp.module == src_import.module), None)
    if existing_import:
        existing_names = set(a.name for a in existing_import.names)
        new_names = [alias for alias in src_import.names if alias.name not in existing_names]
        existing_import.names.extend(new_names)
        existing_import.names.sort(key=lambda x: x.name)
    else:
        dest_imports.append(src_import)
    return dest_imports

def insert_imports(code: str, imports: List[ast.Import]) -> str:
    lines = code.splitlines()
    import_lines = []
    for imp in imports:
        import_lines.extend(ast.unparse(imp).splitlines())

    last_import_index = -1
    for i, line in enumerate(lines):
        if line.startswith(('import ', 'from ')):
            last_import_index = i

    if last_import_index == -1:
        return '\n'.join(import_lines + [''] + lines)
    else:
        return '\n'.join(lines[:last_import_index + 1] + import_lines + [''] + lines[last_import_index + 1:])
