from django.test import TestCase
import unittest


# Create your tests here.
class TestSequenceFunctions(unittest.TestCase):
    def test_selenium_phantomjs(self):
        #selenium 2.42.1 with phantomjs1.9.2 windows
        from selenium import webdriver

        #driver = webdriver.PhantomJS(executable_path='D:\phantomjs-1.9.2-windows\phantomjs.exe') # or add to your PATH
        driver = webdriver.PhantomJS() # or add to your PATH
        driver.set_window_size(1024, 768) # optional
        driver.get('http://127.0.0.1:8000/management/projects/1/submission/pdf/')
        #PDF not work?
        driver.save_screenshot('submission.png') # save a screenshot to disk