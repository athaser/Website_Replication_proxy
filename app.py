from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, quote, unquote

app = Flask(__name__)

def rewrite_links(content, base_url):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Rewrite all links to maintain the proxy behavior
    for link in soup.find_all('a'):
        if 'href' in link.attrs:
            # Check if the link is already a proxy link
            if '/proxy?url=' not in link.attrs['href']:
                # Rewrite the URL to point to the proxy route and include both URL and base URL as query parameters
                link.attrs['href'] = f'/proxy?url={quote(link.attrs["href"])}&base_url={quote(base_url)}'

    # Add JavaScript code to handle link clicks and maintain the proxy behavior
    script = f'''
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        var links = document.querySelectorAll('a[href^="/proxy?url="]');
        links.forEach(function(link)
 {{
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
def index_agones():
    # Perform any necessary processing here
    # Then proxy the request to the desired URL
    response = requests.get('https://livetv.sx/enx/')  # Replace 'https://thepiratebay10.info/' with the desired URL, e.g. 'https://livetv.sx/enx/'

    # Rewrite the links in the HTML content to maintain the proxy behavior
    modified_content = rewrite_links(response.content, response.url)

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
    response = requests.get(full_url)

    # Rewrite the links in the HTML content to maintain the proxy behavior
    modified_content = rewrite_links(response.content, base_url)

    # Return the modified HTML content
    return Response(modified_content, status=response.status_code, content_type=response.headers['content-type'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
