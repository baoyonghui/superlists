from django.urls import resolve
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
import re

class HomePageTest(TestCase):

    @staticmethod
    def remove_csrf(html_code):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html_code)

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        
        #通过请求返回的文本与通过渲染返回的文本，其csrf_token是不同的
        #所以需要去掉csrf_token在进行比较 
        expected_html = render_to_string('home.html', request=request)
        expected_html = self.remove_csrf(expected_html)
        response_html = response.content.decode()
        response_html = self.remove_csrf(response_html)
        self.assertEqual(response_html, expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)
        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string('home.html',  
                {'new_item_text':  'A new list item'}, 
                request=request)
        expected_html = self.remove_csrf(expected_html)
        response_html = response.content.decode()
        response_html = self.remove_csrf(response_html)
        self.assertEqual(response_html, expected_html)

