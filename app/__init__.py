from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Настройте подключение к шаблонам Jinja2
templates = Jinja2Templates(directory="app/templates")

# Место для хранения сайтов и их данных
try:
    with open('sites_data.txt', 'r') as f:
        sites_data = eval(f.read())
except:
    sites_data = []

temp = 'http://192.168.3.39:{}'


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Отображаем главную страницу со списком добавленных сайтов
    return templates.TemplateResponse("index.html", {"request": request, "sites": sites_data})


@app.get("/add_site", response_class=HTMLResponse)
async def add_site(request: Request, site_url:str): 
    try:
        site_url = temp.format(site_url)
        response = requests.get(site_url, timeout=1)
        soup = BeautifulSoup(response.text, "html.parser")

        # favicon = soup.find("link", rel="shortcut icon")
        favicon = soup.select('link[href*=favicon]')
        if favicon:
            if isinstance(favicon, list): favicon = favicon[0]
            favicon_url = f'{site_url}{favicon["href"].replace(".","")}'
        else:
            favicon_url = f"{site_url}/favicon.ico"

        title_tag = soup.find("title")
        site_title = title_tag.string if title_tag else site_url

        for i in sites_data:
            if site_url in i['site_url']:
                raise BaseException
        sites_data.append({"site_title": site_title, "favicon_url": favicon_url, "site_url": site_url})

        with open('sites_data.txt', 'w') as f:
            f.write(str(sites_data))

    except Exception as e:
        print(f"Ошибка при получении данных сайта: {e}")

    return templates.TemplateResponse("index.html", {"request": request, "sites": sites_data})
