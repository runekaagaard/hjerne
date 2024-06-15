import mimetypes, os, sys, warnings
from tree_sitter_languages import get_language, get_parser

def top_level_nodes(tree):
    cursor = tree.walk()
    cursor.goto_first_child()
    yield cursor.node

    while cursor.goto_next_sibling():
        yield cursor.node

def top_level_symbols(tree, query):
    for top_level_node in top_level_nodes(tree):
        captures = query.captures(top_level_node)
        if not captures:
            continue
        node, capture_name = captures[0]
        assert capture_name == 'symbol.name'

        yield {"node": top_level_node, "symbol_name": node.text.decode()}

def top_level_symbol_at(file_path, row):
    file_path = os.path.abspath(os.path.expanduser(file_path))
    _, tree, query = init_file(file_path)

    for symbol in top_level_symbols(tree, query):
        node = symbol['node']

        if (node.start_point[0] <= row <= node.end_point[0]):
            return symbol

    return None

def code_for_context(context):
    file_path = os.path.abspath(os.path.expanduser(context.file))
    with open(file_path, 'r') as f:
        source_code = f.read()

    symbol_name = context.symbol
    _, tree, query = init_file(file_path)

    for symbol in top_level_symbols(tree, query):
        if symbol['symbol_name'] == symbol_name:
            return symbol['node'].text.decode()

    return ""

def update_symbol(file_path, symbol_name, replacement_code):
    file_path = os.path.abspath(os.path.expanduser(file_path))
    with open(file_path, 'r') as f:
        source_code = f.read().encode()

    _, tree, query = init_file(file_path)

    for symbol in top_level_symbols(tree, query):
        if symbol['symbol_name'] == symbol_name:
            start_byte = symbol['node'].start_byte
            end_byte = symbol['node'].end_byte
            updated_code = source_code[:start_byte] + replacement_code.encode() + source_code[end_byte:]
            break
    else:
        raise ValueError(f"Symbol '{symbol_name}' not found in {file_path}")

    with open(file_path, 'w') as f:
        f.write(updated_code.decode())

def parse_markdown(source_code):
    """                                                                                                
     Extract all ```python ... ``` blocks and join them with an empty line between them.                
     """
    import re
    pattern = re.compile(r'```python(.*?)```', re.DOTALL)
    matches = pattern.findall(source_code.decode())
    return "\n\n".join(matches).encode()

def update_file(source_file_path, replacement_file_path, destination_file_path):
    source_file_path = os.path.abspath(os.path.expanduser(source_file_path))
    replacement_file_path = os.path.abspath(os.path.expanduser(replacement_file_path))
    destination_file_path = os.path.abspath(os.path.expanduser(destination_file_path))

    with open(source_file_path, 'r') as source_file:
        source_code = source_file.read().encode()

    _, source_tree, source_query = init_file(source_file_path)
    _, replacement_tree, replacement_query = init_file(replacement_file_path)

    replacement_symbols = {
        symbol['symbol_name']: symbol['node'] for symbol in top_level_symbols(replacement_tree, replacement_query)
    }
    updated_code = source_code.decode()
    for symbol in reversed(list(top_level_symbols(source_tree, source_query))):
        symbol_name = symbol['symbol_name']
        if symbol_name in replacement_symbols:
            start_byte = symbol['node'].start_byte
            end_byte = symbol['node'].end_byte
            replacement_node = replacement_symbols[symbol_name]
            replacement_text = replacement_node.text.decode()
            updated_code = updated_code[:start_byte] + replacement_text + updated_code[end_byte:]

    destination_dir = os.path.dirname(destination_file_path)
    os.makedirs(destination_dir, exist_ok=True)
    with open(destination_file_path, 'w') as destination_file:
        destination_file.write(updated_code)

def init_file(file_path, from_markdown=False):
    file_path = os.path.abspath(os.path.expanduser(file_path))
    with open(file_path, 'r') as f:
        source_code = f.read().encode()

    if from_markdown is True:
        source_code = parse_markdown(source_code)

    try:
        language_name = mimetypes.guess_type(file_path)[0].split("/")[-1].split("-")[-1]
    except:
        language_name = "python"

    with warnings.catch_warnings():
        warnings.simplefilter('ignore', FutureWarning)
        language = get_language(language_name)

        current_dir = os.path.dirname(__file__)
        query_file_path = os.path.join(current_dir, f"queries/{language_name}.scm")
        with open(query_file_path, 'r') as f:
            query_content = f.read()

        parser = get_parser(language_name)
        tree = parser.parse(source_code)
        query = language.query(query_content)

        return parser, tree, query
