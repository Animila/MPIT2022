from django.shortcuts import render
from Home.models import *
import requests


def index(request):
    """Главная страница"""
    context = {'title': 'Главная'}
    return render(request, 'Home/index.html', context=context)


def news(request):
    """Лист новостей"""
    context = {'title': 'Главная', 'data': News.objects.all()}
    return render(request, 'Home/news.html', context=context)


def news_detail(request, news_slug):
    """Подробные новости"""
    data = News.objects.filter(slug=news_slug)
    context = {'title': 'Главная', 'data': data}
    return render(request, 'Home/news_detail.html', context=context)


def vacation_page(request, vac_id, comp_code):
    """Подробные вакансии"""
    context = {'title': 'Вакансии',}
    url = f'http://opendata.trudvsem.ru/api/v1/vacancies/vacancy/{comp_code}/{vac_id}'
    print(url)
    api = requests.get(url).json()['results']
    if api == {}:
        context = {'error': 'К сожалению данная вакансия скрыта или удалена заказчиком'}
    else:
        data = api['vacancies'][0]['vacancy']
        context['title_work'] = data['job-name']
        context['employment'] = data['employment']
        context['schedule'] = data['schedule']
        context['duty'] = data['duty']
        context['vac_url'] = data['vac_url']

        if 'salary' in data:
            context['salary_min'] = data['salary_min']
            context['salary_max'] = data['salary_max']

        company = data['company']
        context['company_name'] = company['name']
        if 'phone' in company:
            context['company_phone'] = company['phone']
        if 'email' in company:
            context['company_email'] = company['email']
        if 'url' in company:
            context['company_url'] = company['url']
        context['addresses'] = data['addresses']['address'][0]['location']


        requirement = data['requirement']
        if 'education' in requirement:
            context['education'] = requirement['education']
        if 'experience' in requirement:
            context['exp'] = requirement['experience']
        if 'qualification' in requirement:
            context['qual'] = requirement['qualification']

        if 'term' in data:
            context['text'] = data['term']['text']

    return render(request, 'Home/vacantions_page.html', context=context)


def get_data(data):
    """Полученние данных"""
    vac = {}
    for i in data['vacancies']:
        salary_min = i['vacancy']['salary_min']
        salary_max = i['vacancy']['salary_max']
        salary = (salary_min, salary_max)
        title_job = i['vacancy']['job-name']
        id = i['vacancy']['id']
        company = i['vacancy']['company']['name']
        company_code = i['vacancy']['company']['ogrn']
        if 'category' in i['vacancy']:
            category = i['vacancy']['category']['specialisation'].split(', ')
            vac[id] = {
                'title_job': title_job, 'id': id, 'company': company,'company_code':company_code, 'category': category, 'salary': salary
            }
        else:
            vac[id] = {'title_job': title_job, 'id': id, 'company': company,'company_code': company_code, 'salary': salary, 'url': url}
    return vac.values()


def vacation_list(request):
    url = 'http://opendata.trudvsem.ru/api/v1/vacancies/?region_code=1400000000000'
    context = {'title': 'Список вакансий',}
    if request.GET != {}:
        url_add = f"&text={request.GET['search']}"
        url_search = f"{url}{url_add}"
        answer = requests.get(url_search).json()
    else:
        answer = requests.get(url).json()


    if answer['results'] == {}:
        context = {'error': 'Ничего не найдено'}

    data = answer['results']
    context['vac'] = get_data(data)
    return render(request, 'Home/vacations_list.html', context=context)
