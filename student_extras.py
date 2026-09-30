from django import template

register = template.Library()


@register.filter
def initials(name):
    """'Ali Raza' -> 'AR', 'Ali' -> 'AL'."""
    parts = str(name).split()
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()
