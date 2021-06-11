def clear_employer_title(text: str) -> str:
    return ''.join(text)\
        .replace('\u202f', ' ').replace('\n', '').replace('  ', '')\
        .replace('\\xa', ' ')
