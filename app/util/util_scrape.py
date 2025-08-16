def safe_extract_text(element, selector: str) -> str:
    try:
        found = element.select_one(selector)
        return found.get_text(strip=True) if found else ""
    except (AttributeError, TypeError):
        return ""


def safe_extract_attr(element, selector: str, attr: str) -> str:
    try:
        found = element.select_one(selector)
        return found.get(attr, "") if found else ""
    except (AttributeError, TypeError):
        return ""
