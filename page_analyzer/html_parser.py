from bs4 import BeautifulSoup

def truncate_text(text, max_length=200):
    """Truncate text to max_length and add ellipsis if needed."""
    if not text:
        return None
    if len(text) > max_length:
        return text[:max_length] + '...'
    return text

def get_h1(soup):
    """Extract h1 tag content from soup."""
    h1_text = soup.h1.get_text(strip=True) if soup.h1 else None
    return truncate_text(h1_text) if h1_text else None

def get_title(soup):
    """Extract title tag content from soup."""
    title_text = soup.title.get_text(strip=True) if soup.title else None
    return truncate_text(title_text) if title_text else None

def get_description(soup):
    """Extract meta description from soup."""
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        return truncate_text(meta_desc.get('content'))
    return None

def extract_page_metadata(soup):
    """Extract all page metadata at once."""
    return {
        'h1': get_h1(soup),
        'title': get_title(soup),
        'description': get_description(soup)
    }