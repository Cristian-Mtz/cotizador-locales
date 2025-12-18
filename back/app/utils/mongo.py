from __future__ import annotations
from typing import Any, Dict

def mongo_to_out(doc: Dict[str, Any]) -> Dict[str, Any]:
    if "_id" in doc and "id" not in doc:
        doc["id"] = str(doc.pop("_id"))
    return doc
