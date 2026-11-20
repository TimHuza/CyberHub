from django.urls import reverse
from .views import COMPONENTS


def components(request):
    """Add the component list (with real URLs) to every template."""
    items = []
    for component in COMPONENTS:
        url = reverse(component["url_name"]) if component["url_name"] else None
        items.append({**component, "url": url})
    return {"components": items}
