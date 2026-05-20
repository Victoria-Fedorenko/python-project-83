from urllib.parse import urlparse

def normazile(url: str) -> str:
    parsed = urlparse(url.lower())
    if not parsed.hostname:
        raise ValueError('Invalid URL')
    
    hostname = parsed.hostname

    if hostname.startswith('www.'):
        hostname = hostname[4:]

    if parsed.port: 
        if (parsed.scheme == 'http' and parsed.port != 80) or \
           (parsed.scheme == 'https' and parsed.port != 443):
            hostname = f':{parsed.port}'

    return f"{parsed.scheme}://{hostname}"