# Utility helpers for Notion API wrapper
from typing import Any, Dict


def simplify_properties(notion_properties: Dict[str, Any]) -> Dict[str, Any]:
    """Convert Notion API property objects into simpler Python types where possible."""
    out = {}
    for k, v in notion_properties.items():
        t = v.get("type")
        out[k] = v.get(t)
    return out
