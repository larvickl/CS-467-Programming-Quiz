from bleach import Cleaner
from bleach.css_sanitizer import CSSSanitizer
from bleach.linkifier import LinkifyFilter

# Default allowed protocols in URLs.
allowed_protocols = {
    'http', 
    'mailto', 
    'https'}

# Default allowed HTML tags.
allowed_tags = {
    'a', 
    'abbr', 
    'acronym', 
    'area', 
    'article', 
    'aside', 
    'b', 
    'bdi', 
    'bdo', 
    'blockquote', 
    'br', 
    'caption', 
    'center', 
    'cite', 
    'code', 
    'col', 
    'colgroup', 
    'data', 
    'dd', 
    'del', 
    'details', 
    'dfn', 
    'div', 
    'dl', 
    'dt', 
    'em', 
    'figcaption', 
    'figure', 
    'footer', 
    'h1', 
    'h2', 
    'h3', 
    'h4', 
    'h5', 
    'h6', 
    'header', 
    'hgroup', 
    'hr', 
    'i', 
    'img', 
    'ins', 
    'kbd', 
    'li', 
    'map', 
    'mark', 
    'nav', 
    'ol', 
    'p', 
    'pre', 
    'q', 
    'rp', 
    'rt', 
    'rtc', 
    'ruby', 
    's', 
    'samp', 
    'small', 
    'span', 
    'strike', 
    'strong', 
    'sub', 
    'summary', 
    'sup', 
    'table', 
    'tbody', 
    'td', 
    'th', 
    'thead', 
    'time', 
    'tr', 
    'tt', 
    'u', 
    'ul', 
    'var', 
    'wbr'}

# Default allowed HTML attributes.
allowed_attributes = {
    'blockquote': ['cite'], 
    'hr': ['align', 'width', 'size'], 
    'img': ['align', 'src', 'height', 'alt', 'width'], 
    'tbody': ['align', 'charoff', 'char'], 
    'th': ['align', 'charoff', 'scope', 'rowspan', 'colspan', 'char', 'headers'], 
    'colgroup': ['align', 'span', 'charoff', 'char'], 
    'td': ['align', 'charoff', 'rowspan', 'colspan', 'char', 'headers'], 
    'ol': ['start'], 
    'del': ['datetime', 'cite'], 
    'tr': ['align', 'charoff', 'char'], 
    'tfoot': ['align', 'charoff', 'char'], 
    'q': ['cite'], 
    'table': ['align', 'summary', 'charoff', 'char'], 
    'a': ['hreflang', 'href'], 
    'thead': ['align', 'charoff', 'char'], 
    'ins': ['datetime', 'cite'], 
    'bdo': ['dir'], 
    'col': ['align', 'span', 'charoff', 'char'],
    "*": ["style"]}

# Default allowed CSS propertites in Style attributes.
allowed_styles = {
    'border-right-color', 
    'azimuth', 
    'volume', 
    'cursor', 
    'font-style', 
    'overflow', 
    'vertical-align', 
    'background-color', 
    'height', 
    'unicode-bidi', 
    'width', 
    'font-family', 
    'font', 
    'speak-numeral', 
    'white-space', 
    'speak-punctuation', 
    'letter-spacing', 
    'pause-after', 
    'font-weight', 
    'pitch-range', 
    'voice-family', 
    'border-collapse', 
    'float', 
    'pitch', 
    'border-left-color', 
    'text-align', 
    'clear', 
    'pause', 
    'speak-header', 
    'text-decoration', 
    'display', 
    'pause-before', 
    'border-top-color', 
    'border-color', 
    'font-variant', 
    'speech-rate', 
    'richness', 
    'line-height', 
    'stress', 
    'font-size', 
    'color', 
    'border-bottom-color', 
    'elevation', 
    'speak', 
    'direction', 
    'text-indent'}

def clean_styled_html(
        dirty_html: str, 
        allowed_tags: set = allowed_tags, 
        allowed_attributes: dict[str, list[str]] = allowed_attributes, 
        allowed_styles: set = allowed_styles,
        allowed_protocols: set = allowed_protocols,
        strip_markup: bool = False,
        strip_comments: bool = True,
        linkify: bool = True) -> str:
    """This function takes unsafe text that may contain HTML (e.g., user input) and 
    removes all unapproved markup.  It can additionally convert all text that looks like
    links into links.

    Parameters
    ----------
    dirty_html : str
        The (possibly) dirty HTML to be sanitized.
    allowed_tags : set, optional
        The set of allowed HTML tags, by default allowed_tags
    allowed_attributes : dict[str, list[str]], optional
        The dict defining which attributes may be used with which tags, 
        by default allowed_attributes.
    allowed_styles : set, optional
        The set of allowed styles, by default allowed_styles
    allowed_protocols : set, optional
        The set of allowed protocols, by default allowed_protocols
    strip_markup : bool, optional
        Strip unapproved markup rather than escaping it if True, by default False
    strip_comments : bool, optional
        Strip HTML comments if True, by default True
    linkify : bool, optional
        Convert link-like text to links using the Bleach LinkifyFilter if True, by defualt False.

    Returns
    -------
    str
        Sanitized HTML.
    """
    css_sanitizer = CSSSanitizer(allowed_css_properties=allowed_styles)
    # Define Cleaner filters.
    filters = []
    if linkify is True:
        filters.append(LinkifyFilter)
    # Define Cleaner.
    cleaner = Cleaner(
        tags=allowed_tags, 
        attributes=allowed_attributes, 
        protocols=allowed_protocols, 
        strip=strip_markup, 
        strip_comments=strip_comments, 
        css_sanitizer=css_sanitizer,
        filters=filters)
    # Clean HTML.
    clean_html = cleaner.clean(dirty_html)
    return clean_html
