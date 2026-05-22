from .base import Renderer
from .markdown import MarkdownRenderer
from .html import HTMLRenderer
from .text import PlainTextRenderer
from .json_renderer import JsonRenderer

RENDERERS = {
    "markdown": MarkdownRenderer,
    "html": HTMLRenderer,
    "text": PlainTextRenderer,
    "json": JsonRenderer,
}

__all__ = [
    "Renderer", "MarkdownRenderer", "HTMLRenderer",
    "PlainTextRenderer", "JsonRenderer", "RENDERERS",
]
