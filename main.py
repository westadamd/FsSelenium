import json
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import HtmlTestRunner


class TestCaseExecution(unittest.TestCase):

    def test_1_login_and_logout(self):
        with open('login-and-logout-test-case-suite.json') as test_case_suite:
            test_cases_dict = json.load(test_case_suite)
        for test_case in test_cases_dict:
            self.username = test_case['username']
            self.password = test_case['password']
            self.expected = test_case['expected']
            with self.subTest(test_case['test-case']):
                self.create_driver()
                self.login()
                self.assertEqual(self.errors, self.expected)
                if not self.errors:
                    self.logout()
                self.driver.quit()

    def test_2_create_project(self):
        with open('create-project-test-case-suite.json') as test_case_suite:
            test_cases_dict = json.load(test_case_suite)
        for test_case in test_cases_dict:
            self.username = test_case['username']
            self.password = test_case['password']
            self.expected = test_case['expected']
            self.project_name = test_case['project-name']
            with self.subTest(test_case['test-case']):
                self.create_driver()
                self.login()
                self.add_project()
                if not self.errors:
                    self.logout()
                self.driver.quit()

    def test_3_search_project(self):
        with open('search-project-test-case-suite.json') as test_case_suite:
            test_cases_dict = json.load(test_case_suite)
        for test_case in test_cases_dict:
            self.username = test_case['username']
            self.password = test_case['password']
            self.expected = test_case['expected']
            self.project_name = test_case['project-name']
            with self.subTest(test_case['test-case']):
                self.create_driver()
                self.login()
                self.search_project()
                if not self.errors:
                    self.logout()
                self.driver.quit()

    def create_driver(self):
        self.driver = webdriver.Chrome('C:/Program Files (x86)/chromedriver.exe')
        self.driver.get("http://paramount-demo.frogslayerdev.com/")

    def login(self):
        self.errors = []
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='email']")))
        email_element = self.driver.find_element_by_xpath("//input[@type='email']")
        email_element.send_keys(self.username)
        password_element = self.driver.find_element_by_xpath("//input[@type='password']")
        password_element.send_keys(self.password)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='projects-page']")))
        except TimeoutException:
            try:
                self.driver.find_element_by_xpath("//input[@type='email' and @class='form-control']")
            except NoSuchElementException:
                self.errors.append(email_element.get_attribute("type") + ': ' + email_element.get_attribute("title"))
            try:
                self.driver.find_element_by_xpath("//input[@type='password' and @class='form-control']")
            except NoSuchElementException:
                self.errors.append(
                    password_element.get_attribute("type") + ": " + password_element.get_attribute("title"))
            try:
                self.driver.find_element_by_xpath("//ul[@class='alert alert-danger']")
            except NoSuchElementException:
                pass
            else:
                self.errors.append(self.driver.find_element_by_xpath("//span[@data-bind='text: message']").text)

    def logout(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-bind="click: logout"]')))
        self.driver.find_element_by_xpath("//a[@data-bind='click: logout']").click()

    def add_project(self):
        self.driver.find_element_by_xpath(
            '//a[@data-bind="requiresAuth: \'CREATE_PROJECT\', click: app.navigateToProjectAdd"]').click()
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@data-bind="hasFocus: true, value: name"]')))
        self.driver.find_element_by_xpath('//input[@data-bind="hasFocus: true, value: name"]').send_keys(
            self.project_name)
        self.driver.find_element_by_xpath('//button[@data-bind="click: $parent.save"]').click()
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@data-bind="text: name"]')))
        except TimeoutException:
            try:
                self.driver.find_element_by_xpath('//input[@data-bind="hasFocus: true, value: name"]')
            except NoSuchElementException:
                self.assertRaises(NoSuchElementException)
            else:
                self.errors.append(self.driver.find_element_by_xpath(
                    '//input[@data-bind="hasFocus: true, value: name"]').get_attribute('title'))
                self.assertEqual(self.errors, self.expected)
        else:
            self.assertEqual(self.driver.find_element_by_xpath('//span[@data-bind="text: name"]').text,
                             self.project_name)

    def search_project(self):
        try:
            self.driver.find_element_by_xpath("//input[@id='search']").send_keys(self.project_name)
        except NoSuchElementException:
            self.assertRaises(NoSuchElementException)
        else:
            try:
                self.driver.find_element_by_xpath(
                    "//button[@data-bind='css: {active: app.searchesView }, click: handleSearch ']").click()
            except NoSuchElementException:
                self.assertRaises(NoSuchElementException)
            try:
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='searches-page']")))
            except TimeoutException:
                self.assertRaises(TimeoutException)
            else:
                try:
                    wait = WebDriverWait(self.driver, 10)
                    wait.until(
                        EC.visibility_of_element_located((By.XPATH, "//a[@data-bind='click: self.navigateToProject']")))
                except TimeoutException:
                    self.errors.append("TimeoutException")
                    self.assertEquals(self.errors, self.expected)
                else:
                    self.driver.find_element_by_xpath("//a[@data-bind='click: self.navigateToProject']").click()
                    try:
                        wait = WebDriverWait(self.driver, 10)
                        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@data-bind="text: name"]')))
                        project_name_from_search = self.driver.find_element_by_xpath(
                            '//span[@data-bind="text: name"]').text
                        self.assertEqual(project_name_from_search, self.project_name)
                    except TimeoutException:
                        self.assertRaises(TimeoutException)


if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output="results"))
