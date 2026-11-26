from django.db import models

# CLV is one shared reference library: no user field. Content is added only
# through data migrations (e.g. 0002_seed_library), never from CLV pages.


class Tab(models.Model):
    """A top-level library section, e.g. Python or Networking (shown as a "category" in the UI)."""

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    """A group of commands inside a tab, e.g. Reachability inside Networking."""

    tab = models.ForeignKey(Tab, on_delete=models.RESTRICT, related_name="categories")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "categories"
        constraints = [
            models.UniqueConstraint(fields=["tab", "name"], name="unique_category_name_in_tab"),
        ]

    def __str__(self) -> str:
        return self.name


class Command(models.Model):
    """A saved command. Parameters and examples are Markdown, rendered on display."""

    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name="commands")
    name = models.CharField(max_length=100)
    description = models.TextField()
    syntax = models.TextField(blank=True)
    parameters = models.TextField(blank=True)
    examples = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        constraints = [
            models.UniqueConstraint(fields=["category", "name"], name="unique_command_name_in_category"),
        ]

    def __str__(self) -> str:
        return self.name
