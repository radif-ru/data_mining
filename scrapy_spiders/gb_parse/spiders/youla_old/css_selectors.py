import re


def get_author_id(resp):
    marker = "window.transitState = decodeURIComponent"
    for script in resp.css("script"):
        try:
            if marker in script.css("::text").extract_first():
                re_pattern = re.compile(r"youlaId%22%2C%22([a-zA-Z|\d]+)%22%2C%22avatar")
                result = re.findall(re_pattern, script.css("::text").extract_first())
                return (
                    resp.urljoin(f"/user/{result[0]}").replace("auto.", "", 1)
                    if result
                    else None
                )
        except TypeError:
            pass


BRANDS = {
    "selector": ".TransportMainFilters_brandsList__2tIkv a.blackLink",
    "callback": "brand_parse",
}
PAGINATION = {
    "selector": "div.Paginator_block__2XAPy a.Paginator_button__u1e7D",
    "callback": "brand_parse",
}

CARS = {
    "selector": "article.SerpSnippet_snippet__3O1t2 a.SerpSnippet_name__3F7Yu",
    "callback": "car_parse",
}

CAR_DATA = {
    "title": lambda resp: resp.css("div.AdvertCard_advertTitle__1S1Ak::text").get(),
    "price": lambda resp: float(
        resp.css("div.AdvertCard_price__3dDCr::text").get().replace("\u2009", "")
    ),
    "photos": lambda resp: [
        itm.attrib.get("src") for itm in resp.css("figure.PhotoGallery_photo__36e_r img")
    ],
    "characteristics": lambda resp: [
        {
            "name": itm.css(".AdvertSpecs_label__2JHnS::text").extract_first(),
            "value": itm.css(".AdvertSpecs_data__xK2Qx::text").extract_first()
                     or itm.css(".AdvertSpecs_data__xK2Qx a::text").extract_first(),
        }
        for itm in resp.css("div.AdvertCard_specs__2FEHc .AdvertSpecs_row__ljPcX")
    ],
    "descriptions": lambda resp: resp.css(
        ".AdvertCard_descriptionInner__KnuRi::text"
    ).extract_first(),
    "author": lambda resp: get_author_id(resp),
}
