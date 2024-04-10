# -*- coding: utf-8 -*-
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


def waiting(xphat):
    while True:
        try:
            driver.find_element(By.XPATH, xphat)
            break
        except NoSuchElementException:
            continue


def get_links(id):
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    tables = soup.find('div', {'id': "ViewerControl1_TreeViewFilesn0Nodes"})
    tables = tables.find_all('table')

    root = 'https://digitarq.arquivos.pt/'
    link_temp = ''
    links = []

    for i in range(0, len(tables)):

        # click in file
        xphat = f'//*[@id="ViewerControl1_TreeViewFilesn{i + 1}"]'
        waiting(xphat)
        time.sleep(1)
        driver.find_element(By.XPATH, xphat).click()

        flag = True

        while flag:
            content = driver.page_source
            soup = BeautifulSoup(content, 'html.parser')

            # link download
            xphat = '//*[@id="ViewerControl1_HyperLinkDownload"]'
            waiting(xphat)
            time.sleep(1)
            link = soup.find('a', {'id': "ViewerControl1_HyperLinkDownload"}).get('href')

            if link_temp != link:
                links.append(root + link + '\n')

                with open(f'{id}.txt', 'a') as temp:
                    temp.write(root + link + '\n')

                link_temp = link
                flag = False

    # verification
    with open(f'{id}.txt') as new_file:
        new_file = new_file.readlines()

        if len(new_file) == len(tables):
            print(f'{id} pass')
        else:
            print(f'{id} not pass')

    df = pd.DataFrame({'id': [f'https://digitarq.arquivos.pt/viewer?id={id}'], 'links': [''.join(links)]})
    return df


def main():
    global driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    with open('input.txt', encoding='utf-8') as file:
        urls = file.readlines()

    dfs = []

    for url in urls:
        url = url.strip()
        id = url.replace('https://digitarq.arquivos.pt/viewer?id=', '').replace('https://digitarq.arquivos.pt/details?id=', '')

        driver.get(f'https://digitarq.arquivos.pt/viewer?id={id}')
        df_temp = get_links(id)
        dfs.append(df_temp)

    driver.quit()

    df_final = pd.concat(dfs, ignore_index=True)
    df_final.to_excel('output.xlsx', index=False)


if __name__ == '__main__':
    main()
