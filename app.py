from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, quote, unquote

app = Flask(__name__)

def rewrite_links(content, base_url):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Rewrite all relevant resource links to maintain the proxy behavior
    for tag, attribute in [('a', 'href'), ('link', 'href'), ('script', 'src'), ('img', 'src')]:
        for resource in soup.find_all(tag):
            if attribute in resource.attrs:
                # Check if the resource link is already a proxy link
                if '/proxy?url=' not in resource.attrs[attribute]:
                    resource_url = resource.attrs[attribute]
                    # Handle relative URLs
                    full_url = urljoin(base_url, resource_url)
                    resource.attrs[attribute] = f'/proxy?url={quote(full_url)}&base_url={quote(base_url)}'

    # Add JavaScript code to handle link clicks and maintain the proxy behavior
    script = f'''
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        var links = document.querySelectorAll('a[href^="/proxy?url="]');
        links.forEach(function(link) {{
            link.addEventListener('click', function(event) {{
                event.preventDefault();
                var url = decodeURIComponent(this.getAttribute('href').split('url=')[1].split('&')[0]);
                var base_url = decodeURIComponent(this.getAttribute('href').split('base_url=')[1]);
                window.location.href = '/proxy?url=' + encodeURIComponent(url) + '&base_url=' + encodeURIComponent(base_url);
            }});
        }});
    }});
    </script>
    '''
    soup.head.append(BeautifulSoup(script, 'html.parser'))

    return str(soup)

@app.route('/')
def index():
    # Proxy the request to the desired URL
    response = requests.get('https://livetv.sx/enx/')  # Replace with the desired URL
    response.encoding = 'utf-8'  # Ensure correct encoding

    # Rewrite the links in the HTML content to maintain the proxy behavior
    modified_content = rewrite_links(response.text, response.url)

    # Return the modified HTML content
    return Response(modified_content, status=response.status_code, content_type=response.headers['content-type'])

@app.route('/proxy')
def proxy():
    # Get the original URL and base URL from the query parameters
    original_url = request.args.get('url')
    base_url = request.args.get('base_url')

    # Construct the full URL for the proxy request
    full_url = urljoin(base_url, original_url)

    # Proxy the request to the specified URL
    response = requests.get(full_url, stream=True)
    content_type = response.headers.get('content-type', 'text/html')

    # If the response is HTML, rewrite the links
    if 'text/html' in content_type:
        response.encoding = 'utf-8'  # Ensure correct encoding
        modified_content = rewrite_links(response.text, base_url)
        return Response(modified_content, status=response.status_code, content_type=content_type)

    # For non-HTML content, return it as is
    return Response(response.content, status=response.status_code, content_type=content_type)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
