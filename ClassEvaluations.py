import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
import numpy as np
import matplotlib.pyplot as plt
from Course_Evaluations import config


class ClassEvaluations:

    def __init__(self, links: list):
        self.driver = webdriver.Chrome()
        self.links = links
        self.dfs = {}
        self.plots = []
        self.courses = []
        self.__generate_dfs()
        self.__generate_plots()

    def __netbadge_login(self):
        username = config.username
        password = config.password
        try:
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#user"))).send_keys(
                username)
            self.driver.find_element_by_css_selector("#pass").send_keys(password)
            self.driver.find_element_by_css_selector("""#loginBoxes > fieldset.secondaryContent > span.col2 > form > 
                    p:nth-child(3) > input[type="submit"]:nth-child(1)""").click()
        except TimeoutException:
            print("Timeout or first link isn't a UVA link.")

    def __generate_dfs(self):
        logged_in = False
        for link in self.links:
            try:
                self.driver.get(link)
            except WebDriverException:
                print("{} is an invalid link.".format(link))
            if not logged_in:
                self.__netbadge_login()
                logged_in = True
            try:
                html = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                            """#questions > form > 
                                                                                            table > tbody > tr > 
                                                                                            td:nth-child(1) > 
                                                                                            table:nth-child(7)""")))
                tables = []
                for t in pd.read_html(html.get_attribute('outerHTML')):
                    if t.shape[0] == 1:
                        tables.append(t)
                df = pd.concat(tables, ignore_index=True)
                question_stds = [[], [], [], [], []]
                for index, row in df.iterrows():
                    for i in range(0, 5):
                        question_stds[i].append(row[i + 5][6:10])
                num = 10
                for lst in question_stds:
                    df[num] = pd.Series(lst).values
                    num += 1
                for i in range(0, 5):
                    df[i] = df[i].apply(lambda x: x.strip("%"))

                for i in range(5, 10):
                    df[i] = df[i].apply(lambda x: x[0:4])

                df = df.apply(pd.to_numeric)

                columns = ["<1", "1-3", "4-6", "7-9", "10+", "Question 2", "Question 3", "Question 4", "Question 5",
                           "Question 6",
                           "Question 2 STD", "Question 3 STD", "Question 4 STD", "Question 5 STD", "Question 6 STD"]
                df.columns = columns
                course = self.driver.find_element_by_css_selector(
                    """#questions > form > table > tbody > tr > td:nth-child(1) > h2 > span""").text
                self.courses.append(course)
                self.dfs[course] = df
            except TimeoutException:
                print("Timeout or no reviews found at {}.".format(link))

    def __generate_plots(self):
        for course, df in self.dfs.items():
            fig = plt.figure()
            question_1_frequencies = [df["<1"].mean(), df["1-3"].mean(), df["4-6"].mean(), df["7-9"].mean(),
                                      df["10+"].mean()]
            bar_labels = ["<1", "1-3", "4-6", "7-9", "10+"]
            y_pos = np.arange(len(bar_labels))
            plt.bar(y_pos, question_1_frequencies)
            plt.xticks(y_pos, bar_labels)
            plt.xlabel("Time spent (hours)")
            plt.ylabel("Relative frequencies")
            plt.title("{} average time spent outside of class".format(course))
            self.plots.append(fig)
            for i in range(2, 7):
                fig = plt.figure()
                df.boxplot("Question {}".format(i))
                plt.title(course)
                self.plots.append(fig)

    def show_plots(self):
        for fig in self.plots:
            fig.show()

    def save_plots(self):
        for course in self.courses:
            for i in range(1, 7):
                if i == 1:
                    self.plots[i].savefig("{} time spent.png".format(course))
                else:
                    self.plots[i].savefig("{} question {}.png".format(course, i))

        print("Pictures saved!")
