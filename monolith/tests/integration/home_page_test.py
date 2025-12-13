# import pytest 
# from bs4 import BeautifulSoup
# from enum import Enum
# from playwright.sync_api import sync_playwright

# class RequestMethod(Enum):
#     get = 'GET'
#     post = 'POST'       
#     put = 'PUT'
#     delete = 'DELETE'


# def verify_request_method(route, request, method: RequestMethod):
#     assert request.method == method.value
#     route.continue_()

# def test_home_page_get(client):
#     response = client.get('/')
#     assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
#     assert response.status_code == 200 

# def test_home_page_post(client):
#     with sync_playwright() as p:
#         browser = p.chromium.launch()
#         page = browser.new_page()

#         page.route("**/",  lambda route, request: verify_request_method(route, request, RequestMethod.post))

#         response = client.post('http://localhost:5000/')
#         assert response.status_code == 405
#         soup = BeautifulSoup(response.data, 'html.parser')
#         error_title = soup.find(id="error-message")
#         redirect_link = soup.find(name="a")
#         assert error_title is not None
#         assert error_title.text == "Houve algum problema, por favor volte para a tela de login..."
#         assert redirect_link.text == "Home Page"

# def test_home_page_put(client):
#     response = client.put('/')
#     assert response.status_code == 405 
#     # TODO: Preciso adicionar a parte de verificar o comportamento para poder fazer com que o mesmo seja redirecionado de maneira correta

# def test_home_page_delete(client):
#     response = client.delete('/')
#     assert response.status_code == 405 
#     # TODO: Preciso adicionar a parte de verificar o comportamento para poder fazer com que o mesmo seja redirecionado de maneira correta

