from .parser import parse


def load(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return parse(f.readlines()).to_dict()


def loads(text: str):
    return parse(text.splitlines()).to_dict()


def dump(data: dict, path: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(dumps(data))


def _dumps_helper(data, indent_level=0):
    lines = []
    indent = "  " * indent_level

    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{indent}{key}:")
            lines.extend(_dumps_helper(value, indent_level + 1))
        elif isinstance(value, list):
            if not value:
                lines.append(f"{indent}{key}[0]:")
            elif all(isinstance(i, str) for i in value):
                lines.append(f"{indent}{key}[{len(value)}]: {', '.join(value)}")
            elif all(isinstance(i, dict) for i in value):
                # All items in list are dicts.
                if not value:
                    lines.append(f"{indent}{key}[0]:")
                    continue
                inner_keys = ",".join(value[0].keys()) # Assume all dicts have same keys.
                lines.append(f"{indent}{key}[{len(value)}]{{inner_keys}}:")
                for item in value:
                    inner_values = ",".join(str(v) for v in item.values())
                    lines.append(f"{indent}  {inner_values}")
            else:
                # Fallback for mixed lists.
                lines.append(f"{indent}{key}[{len(value)}]:")
                for item in value:
                    lines.append(f"{indent}  - {str(item)}")
        else:
            lines.append(f"{indent}{key}: {value}")
            
    return lines

def dumps(data: dict):
    lines = []
    num_items = len(data)
    for i, (name, attrs) in enumerate(data.items()):
        is_complex = isinstance(attrs, (dict, list))

        if isinstance(attrs, dict):
            lines.append(f"{name}:")
            lines.extend(_dumps_helper(attrs, 1))
        elif isinstance(attrs, list):
            if not attrs:
                lines.append(f"{name}[0]:")
            elif all(isinstance(i, str) for i in attrs):
                lines.append(f"{name}[{len(attrs)}]: {', '.join(attrs)}")
            elif all(isinstance(i, dict) for i in attrs):
                if attrs:
                    inner_keys = ",".join(attrs[0].keys())
                    lines.append(f"{name}[{len(attrs)}]"+"{"+f"{inner_keys}"+"}:")
                    for item in attrs:
                        inner_values = ",".join(str(v) for v in item.values())
                        lines.append(f"  {inner_values}")
                else:
                    lines.append(f"{name}[0]:")
            else:
                lines.append(f"{name}[{len(attrs)}]:")
                for item in attrs:
                    lines.append(f"  - {str(item)}")
        else:
            lines.append(f"{name}: {attrs}")
        
        if is_complex and i < num_items - 1:
            lines.append("")

    return "\n".join(lines)