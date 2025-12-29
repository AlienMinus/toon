import re
from .ast import ToonObject, ToonDocument

def _parse_helper(lines, start_index, indent_level):
    data = {}
    i = start_index
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        current_indent = len(line) - len(line.lstrip(' '))
        if current_indent < indent_level:
            break

        if current_indent > indent_level:
            # This should not happen in a correctly formatted file
            # but we skip the line to be robust.
            i += 1
            continue
        
        stripped_line = line.strip()

        if ":" not in stripped_line:
            i += 1
            continue

        key_part, value = stripped_line.split(":", 1)
        key_part = key_part.strip()
        value = value.strip()

        # Match key[len]{...} for lists of objects
        obj_list_match = re.match(r'(\w+)\[(\d+)\]\{(.*)\}$', key_part)
        if obj_list_match and not value:
            key = obj_list_match.group(1)
            num_items = int(obj_list_match.group(2))
            inner_keys = obj_list_match.group(3).split(',')
            
            list_of_dicts = []
            j = i + 1
            items_parsed = 0
            # The next lines are the values, indented.
            while j < len(lines) and items_parsed < num_items:
                value_line = lines[j]
                if not value_line.strip():
                    j += 1
                    continue
                
                value_indent = len(value_line) - len(value_line.lstrip(' '))
                if value_indent <= current_indent:
                    break # indent should be greater

                inner_values = [v.strip() for v in value_line.strip().split(',')]
                if len(inner_keys) == len(inner_values):
                    item_dict = dict(zip(inner_keys, inner_values))
                    list_of_dicts.append(item_dict)
                
                items_parsed += 1
                j += 1
            
            data[key] = list_of_dicts
            i = j
            continue

        # Match key[len] for lists of strings
        list_match = re.match(r'(\w+)\[\d+\]$', key_part)
        if list_match:
            key = list_match.group(1)
        else:
            key = key_part
        
        if not value: # Nested dictionary
            sub_data, i = _parse_helper(lines, i + 1, indent_level + 2)
            data[key] = sub_data
        else: # Simple value or list of strings
            if "," in value:
                data[key] = [v.strip() for v in value.split(",")]
            else:
                data[key] = value
            i += 1
            
    return data, i

def parse(lines):
    doc = ToonDocument()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        current_indent = len(line) - len(line.lstrip(' '))
        if current_indent > 0:
            # For now, we only parse top-level objects, so we skip indented lines.
            i += 1
            continue
        
        stripped_line = line.strip()

        if ":" in stripped_line:
            key, value = stripped_line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if not value: # Nested object
                obj = ToonObject(name=key)
                obj.attributes, i = _parse_helper(lines, i + 1, 2)
                doc.add(obj)
            else: # Simple key-value
                if "," in value:
                    doc.add_simple(key, [v.strip() for v in value.split(",")])
                else:
                    doc.add_simple(key, value)
                i += 1
        else:
            i += 1
    return doc
