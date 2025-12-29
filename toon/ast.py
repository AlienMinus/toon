from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ToonObject:
    name: str
    attributes: Dict[str, object] = field(default_factory=dict)

    def __repr__(self):
        return f"<ToonObject {self.name}>"


@dataclass
class ToonDocument:
    objects: Dict[str, ToonObject] = field(default_factory=dict)
    simple_values: Dict[str, object] = field(default_factory=dict)

    def add(self, obj: ToonObject):
        self.objects[obj.name] = obj

    def add_simple(self, key, value):
        self.simple_values[key] = value

    def to_dict(self):
        data = {
            name: obj.attributes
            for name, obj in self.objects.items()
        }
        data.update(self.simple_values)
        return data
