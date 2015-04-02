import time
import logging
from configobj import ConfigObj
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import pyautogui
from ewmh import EWMH


class InstantQuote(object):
    """docstring for InstantQuote"""
    def __init__(self):
        super(InstantQuote, self).__init__()
        #Selenium Webdriver object


        fp = webdriver.FirefoxProfile()
        fp.set_preference('webdriver.load.strategy', 'unstable')
        # fp.set_preference("browser.download.folderList", 2)
        # fp.set_preference("browser.download.manager.showWhenStarting",False)
        # fp.set_preference("browser.download.dir", os.getcwd())
        # fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

        # browser = webdriver.Firefox(firefox_profile=fp)
        # browser.get("http://pypi.python.org/pypi/selenium")
        # browser.find_element_by_partial_link_text("selenium-2").click()

        # FirefoxProfile fp = new FirefoxProfile();
        # fp.setPreference("webdriver.load.strategy", "unstable"); // As of 2.19. from 2.9 - 2.18 use 'fast'
        # WebDriver driver = new FirefoxDriver(fp);

        # self.driver = webdriver.Firefox()
        self.driver = webdriver.Firefox(firefox_profile=fp)
        self.driver.implicitly_wait(5) #time to keep searching for elements after ____
        self.driver.set_page_load_timeout(5)
        
        #Logging
        self.log = logging.getLogger(__name__)
        # logging.basicConfig(level=logging.DEBUG)

        logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                level=logging.DEBUG)
        self.log.debug('Beginning ' + str(__name__) + ' module.')

        # logHandler = logging.FileHandler('pcbQuote.log')
        # logHandler = logging.StreamHandler()
        # logHandler.setLevel(level=logging.DEBUG)
        # logFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # logHandler.setFormatter(logFormat)
        # self.log.addHandler(logHandler)

        # Create board object with specs of board you want to get quoted
        self.brd = ConfigObj(file_error=True)
        self.brd.filename = 'boardConfig_template.ini'
        self.brd.reload()

        # Create user's information object
        self.user = ConfigObj(file_error=True)
        self.user.filename = 'user.ini'
        self.user.reload()

        offset = 40
        self.driver.set_window_position(1080, 920+offset) # Out[4]: {u'height': 920, u'width': 1080}
        self.driver.set_window_size(3286, 972-offset) # Out[3]: {u'x': 3286, u'y': 972}

    def newTab(self):
        """Open a new Firefox tab."""
        body = self.driver.find_element_by_tag_name('body')
        body.send_keys(Keys.CONTROL + 't')
        # Add functionality to re-select this tab.
        # Create a list of open tabs and store their name, current progress, etc.

    def instantQuote(self, boardType='rigid'):
        """Get instant quotes from all manufacturers that meet board specifications.

        :param boardType: 'rigid' or 'flex'
        """
        # Check that board config file meets spec of fab config and get quotes from appropriate fab    

    def quoteEPEC(self):
        """docstring"""
        fabSpec = ConfigObj(file_error=True)
        fabSpec.filename = 'fabConfig_EPEC.ini'
        fabSpec.reload()
        
        url, uname, pw = fabSpec['url'], fabSpec['u'], fabSpec['pw']
        
        self.newTab()

        self.driver.get(url)
        self.driver.find_element_by_id('userName').send_keys(uname)
        self.driver.find_element_by_id('Hpassword').send_keys(pw)
        self.driver.find_element_by_xpath('//input[@type="image" and @title="Login"]').click()
        self.driver.find_element_by_link_text('Build a Rigid PCB Quote').click()
        
        x = self.driver.find_element_by_id("appParam_%22XDimension%22").send_keys(self.brd['xSize'] + Keys.TAB) #tab needed so that Javascript(?) reloads before we look for new element
        y = self.driver.find_element_by_id("appParam_%22YDimension%22").send_keys(self.brd['ySize'] + Keys.TAB) #tab needed so that Javascript(?) reloads before we look for new element
        part = self.driver.find_element_by_id("appParam_%22PartNo%22").send_keys(self.brd['name'] + Keys.TAB) #tab needed so that Javascript(?) reloads before we look for new element
        rev = self.driver.find_element_by_id("appParam_%22RevisionNo%22").send_keys(self.brd['rev'] + Keys.TAB) #tab needed so that Javascript(?) reloads before we look for new element
        desc = self.driver.find_element_by_id("appParam_%22Description%22").send_keys(self.brd['desc'] + Keys.TAB) #tab needed so that Javascript(?) reloads before we look for new element
        # qty1 = self.driver.find_element_by_id("appParam_%22Cn_Row_Instances%22%400%3A%22Quantity%22").send_keys(Keys.CLEAR + self.brd['qty'][0] + Keys.TAB) #tab needed so that Javascript(?) reloads before we look for new element
        qty1 = self.driver.find_element_by_id("appParam_%22Cn_Row_Instances%22%400%3A%22Quantity%22").send_keys(Keys.BACKSPACE + Keys.BACKSPACE + Keys.BACKSPACE + self.brd['qty'][0] + Keys.TAB) #tab needed so that Javascript(?) reloads before we look for new element
        qty2 = self.driver.find_element_by_id("appParam_%22Cn_Row_Instances%22%401%3A%22Quantity%22").send_keys(self.brd['qty'][1] + Keys.TAB) #tab needed so that Javascript(?) reloads before we look for new element
        qty3 = self.driver.find_element_by_id("appParam_%22Cn_Row_Instances%22%402%3A%22Quantity%22").send_keys(self.brd['qty'][2] + Keys.TAB) #tab needed so that Javascript(?) reloads before we look for new element
        qty4 = self.driver.find_element_by_id("appParam_%22Cn_Row_Instances%22%403%3A%22Quantity%22").send_keys(self.brd['qty'][3] + Keys.TAB) #tab needed so that Javascript(?) reloads before we look for new element
        # layer = self.driver.find_element_by_id("appParam_%22LayerCount%22").select_by_visible_text(self.brd['layers'])
        layer = self.driver.find_element_by_id("appParam_%22LayerCount%22").send_keys(self.brd['layers'] + Keys.TAB)
        # layer.send_keys(Keys.TAB) #tab needed so that Javascript(?) reloads before we look for new element 
        minDrill_inches = float(self.brd['minDrill']) / 1000.0
        hole = self.driver.find_element_by_id("appParam_%22SmallestHoleSize%22").send_keys(Keys.BACKSPACE + Keys.BACKSPACE + Keys.BACKSPACE + Keys.BACKSPACE + str(minDrill_inches) + Keys.TAB) #tab needed so that Javascript(?) reloads before we look for new element

        finish = self.driver.find_element_by_id('appParam_%22FinishPlating%22').send_keys(self.brd['finish'])
        
    # Developer comment
    def quoteOSHPark(self):
        """docstring"""
        url, name, pw = self.readConfig('oshpark', 'rigid')

        self.newTab()

        self.driver.get(url)

        userCSS = '#user_email'
        user = self.driver.find_element_by_css_selector('#user_email')
        user.send_keys(uname)

        

        self.driver.find_element_by_css_selector('#user_password').send_keys(pw)
        self.driver.find_element_by_css_selector('.buttons > input:nth-child(1)').click()
        self.driver.find_element_by_css_selector('#ember291').click()
        self.driver.find_element_by_css_selector('#file_selector > input:nth-child(2)').click()

        e = EWMH()
        windows = e.getClientList()
        for window in windows:
            if e.getWmName(window) == 'File Upload':
                time.sleep(0.5)
                e.setActiveWindow(window)
                e.display.flush()

        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        # '''get file location from config file'''
        # pyautogui.typewrite(fileLocation)
        pyautogui.press('return')

    # Developer comment
    def quoteSunstonePCBExpress(self):
        """docstring"""
        url, name, pw = self.readConfig('sunstone', 'rigid')
        self.newTab()

    def quoteSunstoneValue(self):
        url, name, pw = self.readConfig('sunstone', 'rigid')
        self.newTab()

        # attempts = 0
        # while (attempts <= 30):
        try:
            # attempts += 1        
            self.log.debug('Attempt #' + str(attempts) + '... trying to load ' + url)
            self.driver.get(url)
            # WebDriverWait(self.driver, 5).until(WebDriverWait.readystate_complete)
            self.log.debug('Loaded.')
        except TimeoutException, e:
            self.log.debug('TimeoutException' + str(e))

        # self.driver.find_element_by_id('.btn-blu').click()
        self.driver.find_element_by_css_selector('#ctl00_ctl00_cphSite_cphMain_txtEmail').send_keys(name)
        self.driver.find_element_by_css_selector('#ctl00_ctl00_cphSite_cphMain_txtPassword').send_keys(pw)
        self.driver.find_element_by_css_selector('#ctl00_ctl00_cphSite_cphMain_ibLogIn_Button').click()
        self.driver.find_element_by_css_selector('a.btn-grn:nth-child(2)').click()
        self.driver.find_element_by_css_selector('.mt-menu > li:nth-child(3) > a:nth-child(1)').click()
        # a.btn-grn:nth-child(2)
        # self.driver.find_element_by_id('.mt-menu > li:nth-child(3) > a:nth-child(1)').click()        

    def quoteDirty(self):
        url, name, pw = self.readConfig('dirty', 'rigid')

        self.newTab()

        self.driver.get(url)
        
        
        #(503) 906-8190

    def readConfig(self, company, boardType):
        try:
            url = self.user[boardType]['instant'][company]['url']
            name = self.user[boardType]['instant'][company]['u']
            pw = self.user[boardType]['instant'][company]['pw']
            return url, name, pw
        except KeyError, value:
            self.log.error('Trying to read config file.')
            self.log.error('Company: ' + company + ', boardType: ' + boardType)
            self.log.error('KeyError: ' + str(value))


if __name__ == '__main__':
    quoter = InstantQuote()
    quoter.quoteSunstoneValue()