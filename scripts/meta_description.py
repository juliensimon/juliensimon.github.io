"""Cut a long text to a meta description without an ellipsis.

Search snippets read as prose, so the cut lands on a sentence end, else a
clause break (comma, semicolon, colon, dash), else a word, never mid-word and
never "...". A cut that is not a sentence end gets a closing period, and
dangling function words are dropped first ("... preserving the" -> "... preserving").
"""
import re

_DANGLING = {
    'a', 'an', 'the', 'of', 'and', 'or', 'to', 'for', 'in', 'on', 'at', 'by', 'with',
    'from', 'as', 'that', 'which', 'is', 'are', 'was', 'were', 'be', 'your', 'my',
    'our', 'their', 'its', 'this', 'these', 'those', 'into', 'than', 'but', 'so', 'every', 'each', 'any', 'all', 'some', 'other',
    'about', 'over', 'under', 'between', 'how', 'what', 'when', 'where', 'while', 'if',
}


def cut_description(text: str, limit: int, minimum: int) -> str:
    """Return `text` unchanged if it fits in `limit`, else a clean cut of it."""
    text = re.sub(r'\s+', ' ', text).strip().rstrip('…').rstrip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    # Sentence end: the longest prefix that ends a sentence.
    ends = [m.end() for m in re.finditer(r'[.!?](?=\s)', cut)]
    ends = [e for e in ends if e >= minimum]
    if ends:
        return cut[:ends[-1]].rstrip()
    # A cut that lands exactly on the next word boundary keeps the last word.
    if text[limit:limit + 1] == ' ':
        body = cut
    else:
        body = cut[:cut.rfind(' ')] if ' ' in cut else cut
    # Clause break: prefer it when it keeps at least `minimum` characters.
    clause = max(body.rfind(', '), body.rfind('; '), body.rfind(': '), body.rfind(' - '), body.rfind(' — '))
    if clause >= minimum:
        body = body[:clause]
    # Never leave a parenthesis or a quote open.
    if body.count('(') > body.count(')'):
        body = body[:body.rfind('(')].rstrip(' ,;:-—')
    if body.count('"') % 2:
        body = body[:body.rfind('"')].rstrip(' ,;:-—')
    words = body.rstrip(' ,;:-—').split(' ')
    while len(words) > 3 and words[-1].lower().strip(',;:') in _DANGLING:
        words.pop()
    return ' '.join(words).rstrip(' ,;:-—') + '.'
