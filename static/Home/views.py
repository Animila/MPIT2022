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
    api = requests.get(url).json()['results']
    if api == {}:
        context = {'error': 'К сожалению данная вакансия скрыта или удалена заказчиком'}
    else:
        data = api['vacancies'][0]['vacancy']
        context['category'] = data['category']['specialisation'].split(', ')
        context['title_work'] = data['job-name']
        context['employment'] = data['employment']
        context['schedule'] = data['schedule']
        context['duty'] = data['duty']
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

    return render(request, 'Home/vacantions_page.html', context=context)


def get_data(data):
    """Полученние данных"""
    vac = {}
    for i in data:
        salary_min = i['vacancy']['salary_min']
        salary_max = i['vacancy']['salary_max']
        salary = (salary_max, salary_min)
        print(i)
        print(salary_max, salary_min)
        title_job = i['vacancy']['job-name']
        id = i['vacancy']['id']
        company = i['vacancy']['company']['name']
        company_code = i['vacancy']['company']['ogrn']
        if 'category' in i['vacancy']:
            category = i['vacancy']['category']['specialisation'].split(', ')
            vac[id] = {
                'title_job': title_job, 'id': id, 'company': company,'company_code':company_code, 'category': category, 'salary': salary
            }
            print(vac[id])
        else:
            vac[id] = {'title_job': title_job, 'id': id, 'company': company,'company_code': company_code, 'salary': salary}
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
    else:
        data = answer['results']['vacancies']
        context['vac'] = get_data(data)
    return render(request, 'Home/vacations_list.html', context=context)

# if 'education' in request.GET:
#     print(request.GET['education'])
#     for ed in request.GET['education'].split():
#         url_add += f"&education={ed}"


# for item in answer['results']['vacancies']:
#     if 'education' in item['vacancy']['requirement']:
#         if 'Высшее' in item['vacancy']['requirement']['education'] and 'HIGH' in request.GET['education'].split():
#             data_result.append(item)
#             count += 1
#         elif 'Среднее профессиональное' in item['vacancy']['requirement']['education'] and 'MIDDLE_SPECIAL' in request.GET['education'].split():
#             data_result.append(item)
#             count += 1
#         elif 'Неоконченное высшее' in item['vacancy']['requirement']['education'] and 'UNFINISHED_HIGH' in request.GET['education'].split():
#             data_result.append(item)
#             count += 1
#         elif 'Среднее' in item['vacancy']['requirement']['education'] and 'MIDDLE' in request.GET['education'].split():
#             data_result.append(item)
#             count += 1
# else:
#     data_result = answer['results']['vacancies']
# print(data_result)
# print(count)