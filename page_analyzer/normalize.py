from urllib.parse import urlparse

def normalize(url: str) -> str:
    parsed = urlparse(url.lower())
    if not parsed.hostname:
        raise ValueError('Invalid URL')
    
    hostname = parsed.hostname

    if hostname.startswith('www.'):
        hostname = hostname[4:]

    netloc = hostname
    if parsed.port: 
        if (parsed.scheme == 'http' and parsed.port != 80) or \
           (parsed.scheme == 'https' and parsed.port != 443):
            netloc = f':{parsed.port}'

    return f"{parsed.scheme}://{netloc}"