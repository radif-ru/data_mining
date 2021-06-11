PAGINATION = {
    'next': '//div[@data-qa="pager-block"]//a[@data-qa="pager-next"]/@href'
}

VACANCY = {
    'urls_list': '//div[contains(@class, "vacancy-serp-item")]'
                 '//a[@class="bloko-link" '
                 'and @data-qa="vacancy-serp__vacancy-title"]/@href',
    'title': '//div[@class="vacancy-title"]//h1/text()',
    'salary': '//p[@class="vacancy-salary"]/span/text()',
    'description': {
        'required_experience': '//div[@class="vacancy-description"]'
                               '/div[1]//p[1]//text()',
        'employment': '//div[@class="vacancy-description"]'
                      '/div[1]//p[2]//text()',
        'detailed': '//div[@data-qa="vacancy-description"]//text()'
    },
    'key_skills': '//div[@class="bloko-tag-list"]'
                  '//div[contains(@data-qa, "skills-element")]//text()',
    'employer_url': '//a[@class="vacancy-company-name"]/@href'
}

EMPLOYER = {
    'title_vars': [
        '//span[@class="company-header-title-name"]//text()',
        '//div[@class="tmpl_hh_home_intro__title"]//text()'
    ],
    'website_vars': [
        '//a[@data-qa="sidebar-company-site"]/@href',
        '//div[@class="tmpl_hh_home_intro"]/a/@href'
    ],
    'activity': '//div[@class="tmpl_hh_red"]'
                '//div[@class="tmpl_hh_red__item"]//p/text()',
    'description': '//div[@class="company-description"]//p/text()',
    'other_vacancies': '//a[@data-qa="employer-page__employer-vacancies-link"]'
                       '/@href'

}
