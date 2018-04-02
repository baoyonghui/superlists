#!/usr/bin/env python3

from selenium import webdriver

browser = webdriver.Chrome()

browser.get('http://localhost:8000')

assert 'Django' in browser.title
