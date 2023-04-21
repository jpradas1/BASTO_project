from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time, os, shutil
import pandas as pd
from datetime import datetime
import numpy as np

import warnings
warnings.filterwarnings('ignore')

class TCF_Scraping(object):
    url = 'https://tableroforrajero.crea.org.ar/dashboardcrea2/index.php/crea_session_manager'
    driver = 0
    years, zones = [], []

    def __init__(self, absolute_path: str):
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.download.folderList", 2) 
        firefox_profile.set_preference("browser.download.dir", absolute_path)
        firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
        firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)

        self.driver = webdriver.Firefox(firefox_profile=firefox_profile)
        self.driver.get(self.url)
    
    def _webd_click(self, by: By, key: str):
        this_click = WebDriverWait(self.driver, 20)\
            .until(EC.element_to_be_clickable((by, key)))\
            .click()
        return this_click
    
    def _find_element(self, by: By, key: str):
        this_element = self.driver.find_element(by, key)
        return this_element
    
    def quit(self):
        self.driver.quit()

    def _select_values(self, by: By, key1: str, key2: str, value: str):
        self._find_element(by, key1).click()

        elements = []
        flag, ii = True, 1
        while flag:
            try:
                select_element = self.driver.find_element(by, key2.format(ii))
                elements.append(select_element.text)
                ii += 1
            except:
                flag = False

        index = elements.index(value) + 1
        try:
            select_element = self.driver.find_element(by, key2.format(index))
            select_element.click()
        except:
            print('Not available {}'.format(value))
        return elements
    
    def _update_table(self):
        self._webd_click(By.XPATH, r'/html/body/div/div[2]/form/table/tbody/tr[1]/td[10]/button')

    def _custom_name(self, year: str, region: str):
        download_dir = './dataset/'
        region = region.replace('.','').replace('-','').replace(' ','_')
        new_path = download_dir + region + '/'
        old_name = "Tablero de seguimiento forrajero.csv"
        name = year + '_' + region + '.csv'

        if not os.path.exists(new_path):
            os.makedirs(new_path)

        os.rename(os.path.join(download_dir, old_name), os.path.join(new_path, name))

    def _download_csv(self, year: str, region: str):
        self._update_table()
        self._webd_click(By.XPATH, r'/html/body/div/div[4]/div/div[2]/div[1]/a[1]')

        download_dir = './dataset/'
        old_name = "Tablero de seguimiento forrajero.csv"

        while not os.path.exists(os.path.join(download_dir, old_name)):
            time.sleep(1)

        self._custom_name(year, region)

    def development(self):
        self._webd_click(By.CSS_SELECTOR, 'a.btn.btn-default')
        self._webd_click(By.ID, 'acept')
        self._webd_click(By.ID, 'invited_user')
        self._webd_click(By.CSS_SELECTOR,
                         'a.btn btn-default btn-lg crea-menu-button'.replace(' ', '.'))
        self._webd_click(By.XPATH,
                         r'/html/body/div/div[2]/form/table/tbody/tr[1]/td[11]/button')


        years = self._select_values(By.XPATH,
                                   r'//*[@id="year_chosen"]',
                                   r'/html/body/div/div[2]/form/table/tbody/tr[1]/td[3]/div/div/ul/li[{}]',
                                   '2005')
        
        self._select_values(By.XPATH, 
                                r'//*[@id="month_chosen"]',
                                r'/html/body/div/div[2]/form/table/tbody/tr[2]/td[2]/div/div/ul/li[{}]',
                                '12')
        
        zones = self._select_values(By.XPATH,
                            r'//*[@id="entity_id_chosen"]',
                            r'/html/body/div/div[2]/form/table/tbody/tr[3]/td[2]/div/div/ul/li[{}]',
                            'Centro')
        
        self.years = years
        self.zones = zones
    
    def downloading(self):
        jj = 1
        for zone in self.zones:
            ii = 1

            self._select_values(By.XPATH,
                                r'//*[@id="entity_id_chosen"]',
                                r'/html/body/div/div[2]/form/table/tbody/tr[3]/td[2]/div/div/ul/li[{}]',
                                zone)
            # if jj == 1:
            #     print(self.years, self.zones)

            for year in self.years:
                time.sleep(2)
                self._select_values(By.XPATH,
                                    r'//*[@id="year_chosen"]',
                                    r'/html/body/div/div[2]/form/table/tbody/tr[1]/td[3]/div/div/ul/li[{}]',
                                    year)

                self._download_csv(year, zone)

                progress = f"Downloading file {ii} of {len(self.years)} zone {jj} of {len(self.zones)}"
                ii = ii + 1
                print(progress, end='\r')

            self.ETL(zone)
            jj = jj + 1

        self.quit()
        self.concat()
        print('Done!!!')

    def ETL(self, region: str):
        # self.quit()
        region = region.replace('.','').replace('-','').replace(' ','_')
        path = './dataset/' + region + '/'
        file_list, files = os.listdir(path), []

        for file_name in file_list:
            files.append(file_name)

        dfs = [pd.read_csv(path + f).set_index('Recurso').T for f in files[::-1]]

        for df in dfs:
            df.drop('Total', inplace=True)
            df.reset_index(inplace=True)
            df.rename(columns={'index': 'Fecha'}, inplace=True)
            df['Fecha'] = df['Fecha'].str.replace('([A-z]*\')', '', regex=True)#.replace("'", '')
            df['Fecha2'] = np.arange(1,13,1).astype(str)
            df['Fecha'] = df['Fecha2'] + '-' + df['Fecha']
            df.drop(columns=['Fecha2'], inplace=True)

        concat = pd.concat(dfs)
        concat['Fecha'] = concat['Fecha'].apply(lambda x: datetime.strptime(x, '%m-%y'))
        concat['Fecha'] = pd.to_datetime(concat['Fecha']).dt.strftime('%m-%Y')

        for c in concat.columns[1:]:
            concat[c] = concat[c].replace('n/d', np.nan).str.replace('.','').str.replace(',','.')
            concat[c] = concat[c].astype(float)

        concat.to_csv('./dataset/' + region + '.csv', index=False)

        if os.path.exists('./dataset/' + region + '.csv'):
            shutil.rmtree(path)

    def concat(self):
        path = './dataset/'
        file_list = os.listdir(path)[1:]
        dfs = [pd.read_csv(path + file).set_index('Fecha') for file in file_list]
        for df in dfs:
            df.dropna(how='all', inplace=True)

        this_concat = pd.concat(dfs)
        name = 'All_Harvest.csv'
        this_concat.to_csv(path + name)
        
        if os.path.exists(path + name):
            for file in file_list:
                os.remove(path + file)

if __name__ == "__main__":
    path = '/home/uqbar/Desktop/Data-Science/Henry_PF/BASTO-project/dataset/'
    TCF = TCF_Scraping(path)
    TCF.development()
    TCF.downloading()