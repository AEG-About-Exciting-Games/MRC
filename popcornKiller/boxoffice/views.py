import requests
import json
import os

from django.shortcuts import render
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


def fetch_api_daily_data(date):
    url = ('http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
           f'?key={API_KEY}&targetDt={date}')

    response = requests.get(url)

    if response.status_code != 200:
        return None

    try:
        movies = response.json()
    except json.JSONDecodeError:
        return None

    return movies


def daily_view(request):
    date = request.GET.get('date', None)
    if date:
        data = fetch_api_daily_data(date)
        if data:
            daily_box_office_list = (data.get('boxOfficeResult', {})
                                     .get('dailyBoxOfficeList', {}))
            return render(request, 'index_view.html', {'box_office_list': daily_box_office_list})
        else:
            return render(request, 'index_view.html', {'error': 'Failed to fetch API data or invalid JSON'})
    else:
        return render(request, 'index_view.html', {'error': 'No date provided'})
