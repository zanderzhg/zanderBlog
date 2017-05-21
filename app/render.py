# -*- coding:utf-8 -*-
# Zander学Python
'''
QQ:867662267
'''

from flask_misaka import Misaka,misaka as m
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name

class HighlighterRenderer(m.HtmlRenderer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def blockcode(self, text, lang):
        if not lang:
            return '\n<pre><code>{}</code></pre>\n'.format(text.strip())
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter(linenos=True)

        return highlight(text, lexer, formatter)