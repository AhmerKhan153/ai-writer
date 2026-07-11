import re
from html.parser import HTMLParser
from typing import Optional

from requests import RequestException, get


class ArticleTextParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title_parts = []
        self.body_parts = []
        self._skip_depth = 0
        self._in_title = False
        self._context_stack = []
        self._noise_stack = []
        self._block_tags = {
            "p",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "li",
            "blockquote",
            "pre",
            "figcaption",
            "td",
            "th",
            "div",
            "section",
        }

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs_dict = dict(attrs)

        if self._skip_depth:
            if tag in {"script", "style", "svg", "noscript", "iframe", "object", "embed"}:
                self._skip_depth += 1
            return

        if self._is_noise_tag(tag, attrs_dict):
            self._noise_stack.append(tag)
            self._skip_depth += 1
            return

        if tag == "title":
            self._in_title = True
            return

        if tag in {"article", "main", "body", "section"}:
            self._context_stack.append(tag)
            return

        if tag in self._block_tags and self._context_stack:
            self.body_parts.append("\n\n")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if self._skip_depth:
            if self._noise_stack and tag == self._noise_stack[-1]:
                self._noise_stack.pop()
                self._skip_depth = max(0, self._skip_depth - 1)
            elif tag in {"script", "style", "svg", "noscript", "iframe", "object", "embed"}:
                self._skip_depth = max(0, self._skip_depth - 1)
            return

        if tag == "title":
            self._in_title = False
            return

        if tag in {"article", "main", "body", "section"} and self._context_stack:
            self._context_stack.pop()

    def handle_data(self, data):
        if self._in_title:
            self.title_parts.append(data)
            return

        if self._skip_depth:
            return

        if not self._context_stack:
            return

        text = re.sub(r"\s+", " ", data).strip()
        if text:
            self.body_parts.append(text)

    def _is_noise_tag(self, tag, attrs):
        if tag in {"nav", "footer", "aside", "form", "button", "header", "menu", "svg", "img", "iframe", "script", "style", "noscript", "link"}:
            return True

        class_name = " ".join(attrs.get("class", "").split()).lower()
        element_id = attrs.get("id", "").lower()
        combined = f"{class_name} {element_id}"
        noisy_tokens = ["nav", "menu", "sidebar", "ad", "advert", "cookie", "comment", "footer", "social", "toolbar"]
        return any(token in combined for token in noisy_tokens)


def _normalize_paragraphs(text: str) -> str:
    paragraphs = []
    for paragraph in re.split(r"\n\s*\n", text or ""):
        cleaned = re.sub(r"\s+", " ", paragraph).strip()
        if cleaned:
            paragraphs.append(cleaned)
    return "\n\n".join(paragraphs)


def clean_html_to_text(html: str) -> str:
    parser = ArticleTextParser()
    parser.feed(html or "")
    parser.close()

    title = _normalize_paragraphs(" ".join(parser.title_parts))
    body = _normalize_paragraphs("".join(parser.body_parts))

    if title and body:
        return f"{title}\n\n{body}"
    if title:
        return title
    return body


def fetch_article(url: str) -> Optional[str]:
    try:
        response = get(url, timeout=15)
        if response.status_code == 200:
            return clean_html_to_text(response.text)
        print(f"Error fetching article from {url}: Status code {response.status_code}")
        return None
    except RequestException as e:
        print(f"Error fetching article from {url}: {e}")
        return None
