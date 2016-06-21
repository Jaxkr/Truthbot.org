from django import template
import mistune

register = template.Library()
markdown = mistune.Markdown(escape=True, hard_wrap=True)

@register.filter
def parsemarkdown(text):
    return markdown(text)