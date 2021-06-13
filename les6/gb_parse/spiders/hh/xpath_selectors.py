PAGINATION = {
    "selector": '//div[@data-qa="pager-block"]//a[@data-qa="pager-page"]/@href',
    "callback": "parse",
}

VACANCY = {
    "selector": '//div[contains(@data-qa, "vacancy-serp__vacancy")]//'
                'a[@data-qa="vacancy-serp__vacancy-title"]/@href',
    "callback": "vacancy_parse",
}

VACANCY_DATA = {
    "title": {"xpath": '//h1[@data-qa="vacancy-title"]/text()'},
    "salary": {"xpath": '//p[@class="vacancy-salary"]/span/text()'},
    "description": {"xpath": '//div[@data-qa="vacancy-description"]//text()'},
    "skills": {"xpath": '//div[@class="bloko-tag-list"]//'
                        'div[contains(@data-qa, "skills-element")]/'
                        'span[@data-qa="bloko-tag__text"]/text()'},
    "author": {"xpath": '//a[@data-qa="vacancy-company-name"]/@href'},
}

COMPANY_VACANCYES = {
    "selector": '//div[contains(@data-qa, "vacancy-serp__vacancy")]//'
                'a[@data-qa="vacancy-serp__vacancy-title"]/@href',
    "callback": "vacancy_parse",
}

COMPANY_DATA = {
    "company_name": {"xpath": "//div[@class='company-header']//h1/span[@data-qa='company-header-title-name']/text()"},
    "company_site": {"xpath": "//a[@data-qa='sidebar-company-site']/@href"},
    "sphere_activities": {"xpath": "//div[contains(text(), 'Сферы деятельности')]/../p//text()"}
}
