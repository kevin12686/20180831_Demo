from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .models import station


def get_bike_data():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--lang=zh-tw")
    driver = webdriver.Chrome(executable_path=settings.CHROME_PATH, options=chrome_options)
    driver.get("https://i.youbike.com.tw/station/list")
    data_list = driver.find_elements('id', 'setarealist')[0].text.split('\n')
    driver.quit()
    result_list = list()
    for each in data_list:
        temp = each.split(' ')
        result_list.append(
            {'key': {'area': temp[0], 'location': temp[1]}, 'default': {'bikes': temp[2], 'spaces': temp[3]}})
    return result_list


def update_station():
    status = False
    data = get_bike_data()
    for each in data:
        try:
            station.objects.update_or_create(**each['key'], defaults=each['default'])
            status = True
        except Exception:
            print('[Warning] Update fail with \'%s\'' % repr(each))
    if status:
        print('[Info] Update Success.')


# Create your views here.

def index(request):
    if request.method == 'GET':
        data = dict(request.GET).get('area', list())
        objects = station.objects.all().order_by('area', 'location')
        areas = {each.area for each in objects}
        if len(data) > 0:
            temp = station.objects.none()
            for each in data:
                temp |= objects.filter(area=each)
            objects = temp
        else:
            objects = station.objects.none()
        return render(request, 'index.html', {'areas': areas, 'objects': objects, 'data': data})
    elif request.method == 'POST':
        pass
    else:
        return HttpResponse(status=403)


def update(request):
    if request.method == 'GET':
        startup = False
        if station.objects.count() == 0:
            startup = True
        return render(request, 'update.html', {'startup': startup})
    elif request.method == 'POST':
        status = False
        job = request.POST.get('job', '')
        if job == 'update':
            update_station()
            status = True
        return JsonResponse({'status': status})
    else:
        return HttpResponse(status=403)
