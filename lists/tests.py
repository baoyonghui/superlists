from django.urls import resolve
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
import re
from lists.models import Item

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

class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        self.client.post('/lists/new', 
                data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', 
                data={'item_text': 'A new list item'})

        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
        #self.assertEqual(response.status_code, 302)
        #self.assertEqual(response['location'], '/lists/the-only-list-in-the-world')
    
class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        #print ('start')
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')
        #print (response.content)
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()
        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')


