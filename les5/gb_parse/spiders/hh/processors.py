def clear_employer_title(text):
    return ''.join(text)\
        .replace('\u202f', ' ').replace('\n', '').replace('  ', '')\
        .replace('\\xa', ' ')
