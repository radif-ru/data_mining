from urllib.parse import urljoin


def flat_text(items):
    return "\n".join(items)


def hh_user_url(user_id):
    return urljoin("https://hh.ru/", user_id)


def hh_sphere_activities_clean(item):
    if isinstance(item, str):
        item = item.split(",")
    return item


def concatenate_items(items):
    result = " ".join(items)
    return result
