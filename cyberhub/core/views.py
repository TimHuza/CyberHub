from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Each component on the dashboard. When a component is built, set
# "url_name" to its URL name (e.g. "notes:list") and the card gets an Open button.
# "icon" is a Font Awesome icon name; "tile" is a CSS class for the coloured square.
COMPONENTS = [
    {"code": "NTT", "name": "Note Taker", "description": "Markdown notes organised in folders.",
     "icon": "fa-note-sticky", "tile": "ch-tile-cyan", "url_name": "notes:list"},
    {"code": "QEF", "name": "Quiz Exam Forge", "description": "Quizzes generated from your notes and material.",
     "icon": "fa-clipboard-question", "tile": "ch-tile-red", "url_name": None},
    {"code": "CLV", "name": "Command Library Vault", "description": "Searchable commands in tabs and categories.",
     "icon": "fa-terminal", "tile": "ch-tile-violet", "url_name": "commands:library"},
    {"code": "AIM", "name": "AI Mentor", "description": "Local AI tutor over your notes and school files.",
     "icon": "fa-robot", "tile": "ch-tile-cyan", "url_name": None},
    {"code": "PTM", "name": "Progress Tracking Manager", "description": "Learning activity and statistics.",
     "icon": "fa-chart-line", "tile": "ch-tile-red", "url_name": None},
]

# Placeholders until PTM exists. None means "no data yet", not zero.
STATS = [
    {"label": "Study hours this week", "icon": "fa-hourglass-half", "value": None},
    {"label": "Questions answered this week", "icon": "fa-circle-question", "value": None},
    {"label": "Day streak", "icon": "fa-fire", "value": None},
]

PROGRESS = [
    {"label": "Notes reviewed", "percent": None},
    {"label": "Quiz average", "percent": None},
    {"label": "Weekly goal", "percent": None},
]


@login_required
def home(request):
    """Dashboard: welcome banner, PTM stats (placeholders for now), component cards."""
    context = {"stats": STATS, "progress": PROGRESS}
    return render(request, "core/home.html", context)
