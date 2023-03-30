from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import xlsxwriter
class BinaAz:
    
    def __init__(self):
        self.browserProfile = webdriver.ChromeOptions() 
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages':'en,en_US'}) #create olunan brauzer dilini eng qoyduq
        self.browser = webdriver.Chrome("chromedriver.exe", chrome_options=self.browserProfile)
        self.browser = webdriver.Chrome()
        self.browser.get("https://bina.az/")
        time.sleep(2)
        self.browser.find_element_by_css_selector("#js-quick-links_sale > ul:nth-child(3) > li:nth-child(2) > a").click()
        time.sleep(2)
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.browser.find_element_by_css_selector("#new_q > div.search-row > div.search-row__cell.search-row__cell--city").click()
        time.sleep(3)
        self.browser.find_element_by_xpath('//*[@id="new_q"]/div[1]/div[6]/div[1]/div[3]/div/ul/li[1]').click()
        self.addList=[["ad_id","price","currency","location","room","square","ad_loc_and_time"]]
       

    def getCurrentPageAd(self):
        time.sleep(2)
        allAdBox = self.browser.find_element_by_css_selector("#js-items-search > div.items_list")
        allAds = allAdBox.find_elements_by_class_name("items-i")
        for adElem in allAds:
            adId = adElem.get_attribute("data-item-id")
            adParam = adElem.find_element_by_class_name("card_params")
            adPrice = adParam.find_element_by_class_name("price-val").text
            adCurr = adParam.find_element_by_class_name("price-cur").text
            adLocation = adParam.find_element_by_class_name("location").text
            adTimeWhen = adParam.find_element_by_class_name("card_footer").find_element_by_class_name("city_when").text
            adRoom = adParam.find_element_by_class_name("name").find_elements_by_tag_name("li")[0].text
            adSquare = adParam.find_element_by_class_name("name").find_elements_by_tag_name("li")[1].text
            adDetails = [adId, adPrice, adCurr, adLocation, adRoom, adSquare ,adTimeWhen]
            self.addList.append(adDetails)


    def showAddElements(self):
        return (self.addList)


    def allPageData(self):
        #print(self.showAddElements())

        if(len(self.addList) !=0 ):
            self.exportData()

        while True:
            self.getCurrentPageAd()
            time.sleep(2)
            buttons = self.browser.find_elements_by_css_selector("#js-items-search > div.bottom_pagination > nav > div > span")
            lastbuttonContent = buttons[len(buttons)-1].text
            if(lastbuttonContent == "Növbəti"):
                buttons[len(buttons)-1].click()
                time.sleep(3)
                self.allPageData()
            else:
                break

    def exportData(self):
        with xlsxwriter.Workbook("bina_az_menzil.xlsx") as workbook:
            worksheet=workbook.add_worksheet("elan")

            for row_num, data in enumerate(self.addList):
                worksheet.write_row(row_num, 0, data)
                
                
adsData = BinaAz()
adsData.allPageData()
