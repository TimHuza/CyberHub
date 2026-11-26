from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from core.markdown import render_markdown

from .models import Command, Tab


def _sidebar_context(active_tab=None):
    """Everything clv_base.html needs: the tab list, the active tab and the search data."""
    tabs = list(Tab.objects.all())
    # Plain data for clv_search.js. json_script in the template escapes it safely.
    search_data = [{"name": tab.name, "description": tab.description, "url": reverse("commands:tab_detail", args=[tab.pk])} for tab in tabs]
    return {"tabs": tabs, "active_tab": active_tab, "search_data": search_data}


@login_required
def library(request):
    """Landing page: intro, category search, a card for every tab and the Advanced command search."""
    # select_related joins category and tab into the same query, instead of one query per command.
    commands = Command.objects.select_related("category__tab").order_by("category__tab__order", "category__order", "order", "name")
    # The #command-<pk> part tells the tab page which row to scroll to and open.
    command_search_data = [
        {
            "name": command.name,
            "description": command.description,
            "location": f"{command.category.tab.name} › {command.category.name}",
            "url": reverse("commands:tab_detail", args=[command.category.tab_id]) + f"#command-{command.pk}",
        }
        for command in commands
    ]
    context = {**_sidebar_context(), "command_search_data": command_search_data}
    return render(request, "commands/library.html", context)


@login_required
def tab_detail(request, pk):
    """One tab with its categories and their commands."""
    tab = get_object_or_404(Tab, pk=pk)
    # prefetch_related loads all commands in one extra query, not one query per category.
    categories = list(tab.categories.prefetch_related("commands"))

    for category in categories:
        for command in category.commands.all():
            # Rendered here (like NTT's note_detail) with the shared sanitizing renderer.
            command.parameters_html = render_markdown(command.parameters) if command.parameters else ""
            command.examples_html = render_markdown(command.examples) if command.examples else ""
            command.has_details = bool(command.syntax or command.parameters or command.examples)

    context = {**_sidebar_context(active_tab=tab), "tab": tab, "categories": categories}
    return render(request, "commands/tab_detail.html", context)
