from agents.article_fetcher import clean_html_to_text


def test_clean_html_to_text_ignores_noise_and_keeps_title_and_body():
    html = """
    <!doctype html>
    <html>
      <head>
        <title>Example Article</title>
        <script>console.log('ignore')</script>
        <style>.x{display:none}</style>
      </head>
      <body>
        <nav>Home About</nav>
        <div class="cookie-banner">Accept cookies</div>
        <main>
          <article>
            <p>First paragraph of the article.</p>
            <p>Second paragraph of the article.</p>
          </article>
        </main>
        <aside class="ads">Ad content</aside>
        <footer>Footer content</footer>
        <div id="comments">Comment text</div>
      </body>
    </html>
    """

    cleaned = clean_html_to_text(html)

    assert cleaned == "Example Article\n\nFirst paragraph of the article.\n\nSecond paragraph of the article."
