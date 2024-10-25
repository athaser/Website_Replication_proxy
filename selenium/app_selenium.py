from flask import Flask, request, Response
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
import time

app = Flask(__name__)

from selenium.webdriver.chrome.options import Options

def get_rendered_html(url):
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")  # Disable GPU to avoid rendering issues
    options.add_argument("--remote-debugging-port=9222")  # Required for Docker

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    rendered_html = driver.page_source
    driver.quit()
    return rendered_html

def rewrite_links(content, base_url):
    soup = BeautifulSoup(content, 'html.parser')

    # Proxy links for <a>, <link>, <script>, and <img>
    for tag in soup.find_all(['a', 'link', 'script', 'img']):
        attr = 'href' if tag.name in ['a', 'link'] else 'src'
        if tag.has_attr(attr):
            original_url = tag[attr]
            full_url = urljoin(base_url, original_url)
            tag[attr] = f'/proxy?url={quote(full_url)}&base_url={quote(base_url)}'

    # Inject JavaScript for lazy loading
    lazy_script = '''
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const lazyElements = document.querySelectorAll('img[loading="lazy"]');
        lazyElements.forEach(element => {
            const src = element.getAttribute('data-src');
            if (src) {
                element.src = src;
            }
        });
    });
    </script>
    '''
    soup.head.append(BeautifulSoup(lazy_script, 'html.parser'))
    return str(soup)

@app.route('/')
def index():
    target_url = 'https://example.com'  # Replace with your target URL
    rendered_html = get_rendered_html(target_url)
    modified_content = rewrite_links(rendered_html, target_url)
    return Response(modified_content, content_type="text/html")

@app.route('/proxy')
def proxy():
    original_url = request.args.get('url')
    base_url = request.args.get('base_url')
    full_url = urljoin(base_url, original_url)
    rendered_html = get_rendered_html(full_url)
    modified_content = rewrite_links(rendered_html, base_url)
    return Response(modified_content, content_type="text/html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
