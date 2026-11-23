import nh3
from django.utils.safestring import SafeString, mark_safe
from markdown_it import MarkdownIt

# html=False shows raw HTML in a note as text, so saved XSS examples stay readable and harmless.
# breaks=True turns a single Enter into a new line, like GitHub comments.
# Images stay off until we decide how notes should store them.
_parser = MarkdownIt("commonmark", {"html": False, "breaks": True}).enable(["table", "strikethrough"]).disable("image")

# An allowlist: anything not named here is removed, including tags we never thought of.
_ALLOWED_TAGS = {
    "a", "blockquote", "br", "code", "del", "em", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "li",
    "ol", "p", "pre", "s", "strong", "table", "tbody", "td", "th", "thead", "tr", "ul",
}
_ALLOWED_ATTRIBUTES = {"a": {"href", "title"}, "ol": {"start"}, "td": {"style"}, "th": {"style"}}
_ALLOWED_URL_SCHEMES = {"http", "https", "mailto"}


def render_markdown(text: str) -> SafeString:
    """Convert Markdown to sanitized HTML that is safe to show in a template."""
    html = _parser.render(text)
    # Second layer of defence: even if the parser had a bug, unsafe output is removed here.
    clean_html = nh3.clean(
        html,
        tags=_ALLOWED_TAGS,
        attributes=_ALLOWED_ATTRIBUTES,
        url_schemes=_ALLOWED_URL_SCHEMES,
        filter_style_properties={"text-align"},  # Tables use this for column alignment.
    )
    return mark_safe(clean_html)
