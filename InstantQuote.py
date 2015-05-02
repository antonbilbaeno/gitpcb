
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
        
        # wait = WebDriverWait(self.driver, 5)

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
        """
        Get instant quotes from all manufacturers that meet board
        specifications.

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
        
    def quoteOSHPark(self):
        """Function for navigating OSHPark's website."""

        url, user, pw = self.readConfig('oshpark', 'rigid')
        # Open new tab and go to URL
        self.newTab()
        self.driver.get(url)
        # Enter login information
        self.driver.find_element_by_css_selector('#user_email').send_keys(user)
        self.driver.find_element_by_css_selector('#user_password').send_keys(pw)
        # Click login button
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

    def quoteSunstonePCBExpress(self):
        """docstring"""
        url, name, pw = self.readConfig('sunstone', 'rigid')
        self.newTab()

    def quoteSunstoneValue(self):
        url, name, pw = self.readConfig('sunstone', 'rigid')
        self.newTab()

        while True:
            try:
                self.log.debug('Trying to load ' + url)
                self.driver.get(url)
                # WebDriverWait(self.driver, 5).until(EC.readystate_complete)
                self.log.debug('Loaded.')
            except TimeoutException as e:
                self.log.debug('TimeoutException' + str(e))
                continue
            else:
                break

        self.driver.find_element_by_css_selector('#ctl00_ctl00_cphSite_cphMain_txtEmail').send_keys(name)
        self.driver.find_element_by_css_selector('#ctl00_ctl00_cphSite_cphMain_txtPassword').send_keys(pw)

        self.driver.find_element_by_css_selector('#ctl00_ctl00_cphSite_cphMain_ibLogIn_Button').click()
        self.driver.find_element_by_css_selector('a.btn-grn:nth-child(2)').click()
        self.driver.find_element_by_css_selector('.mt-menu > li:nth-child(3) > a:nth-child(1)').click()

        # while True:
        #     try:
        #         self.driver.find_element_by_css_selector('#ctl00_ctl00_cphSite_cphMain_ibLogIn_Button').click()
        #     except TimeoutException, e:
        #         self.log.debug('TimeoutException' + str(e))
        #         continue
        #     else:
        #         break


        # while True:
        #     try:
        #         self.driver.find_element_by_css_selector('a.btn-grn:nth-child(2)').click()
        #     except TimeoutException, e:
        #         self.log.debug('TimeoutException' + str(e))
        #         continue
        #     else:
        #         break


        # self.driver.find_element_by_css_selector('a.btn-grn:nth-child(2)').click()

        # while True:
        #     try:
        #         self.driver.find_element_by_css_selector('.mt-menu > li:nth-child(3) > a:nth-child(1)').click()
        #     except TimeoutException, e:
        #         self.log.debug('TimeoutException' + str(e))
        #         continue
        #     else:
        #         break
        
        # a.btn-grn:nth-child(2)
        # self.driver.find_element_by_id('.mt-menu > li:nth-child(3) > a:nth-child(1)').click()        

    def quoteDirty(self):
        url, name, pw = self.readConfig('dirty', 'rigid')
        self.newTab()
        self.driver.get(url)

    def readConfig(self, company, boardType):
        try:
            url = self.user[boardType]['instant'][company]['url']
            user = self.user[boardType]['instant'][company]['u']
            pw = self.user[boardType]['instant'][company]['pw']
            return url, user, pw
        except KeyError as value:
            self.log.error('Trying to read config file.')
            self.log.error('Company: ' + company + \
                    ', boardType: ' + boardType)
            self.log.error('KeyError: ' + str(value))


class Automator(object):
    """

    """
    def __init__(self):
        self.validProcesses = []

class Board(object):
    """
    The Board class contains information about a printed circuit board
    including the name, author, revision, and specifications that the
    board must meet.
    """
    def __init(self, boardPath):
        # Design information
        self.name = None
        self.rev = None #revision
        self.author = None #name of designer
        self.lastEdited = None #date
        self.spec = Specification(boardPath)

    def load(configFile):
        pass

class InstantQuote(object):
    """
    A Process has an InstantQuote object. InstantQuotes contain a list
    of Elements.
    """
    def __init__(self, path):
        with open(path, 'r') as f:
            self.elements = yaml.load(f)

    def execute(self):
        #for each item in yaml, get element from type/id and do the actions
        pass


# When defining a class in Python2, you must inherit "object"
# ...search new style vs old style classes in Python
class Manufacturer(object):
    """
    The Manufacturer class contains the basic information about a PCB
    manufacturer. Each Manufacturer may have multiple Processes.

    Parameters:
        configFile - path to ConfigObj file
    """

    def __init__(self, mfrPath):
        # Manufacturer information
        self.name = None
        self.type = None #broker, mfr, batch service, etc.
        self.city = None
        self.country = None
        self.processes = [] #list of processes

        #TODO
        # Information for custom quoting via email
        self.email = None #contact email for custom quotes
        self.subject = None #custom subject line for each mfr
        self.message = None #custom message for each mfr

    def load(configFile):
        pass

class Matchmaker(object):
    """
    The Matchmaker class asserts the following: (in order)
    1. QUOTE <-> MFERS
        -assert location
    2. QUOTE <-> PROCESS
        -of valid mfers:
            -assert quantities and lead times are available
    3. BOARD <-> PROCESS
        -of available processes:
            -assert Board.spec meets Process.spec
    """
    def __init__(self):
        pass

    def match(quote):
        #return list of valid processes
        pass
        
class Process(object):
    """
    A Manufacturer may have multiple processes that they offer.
    e.g. 2-layer value boards, 4-layer custom quote, etc.
    
    The process class describes the capabilities of a process as well
    as the instructions to complete an automated quote.

    """
    def __init__(self, processPath, instantQuotePath):
        # Process information
        self.mfr = None #Manufacturer name
        self.name = None #ValueProto, QuickTurn, etc.
        self.spec = Specification(processPath)
        self.instantQuote = InstantQuote(instantQuotePath)

        # Process options
        self.quantities = []
        self.leadTimes = []
        self.shipping = [] #shipping options
        self.coupons = []

    def instantQuote(self):

        pass



    def load(configFile):
        pass

    def 

class Quote(object):
    def __init__(self):
        # Quote information
        self.user = None
        self.name = None #name given by user
        self.options = None #secondary name option for user
        self.id = -1 #quote id number
        self.board = Board()

        # Requirements
        self.quantities = []
        self.leadTimes = []
        self.shipping = []
        self.countryRestrictions = []
        self.cityRestrictions = []

        #TODO
        self.stencil = []

class Specification(object):
    def __init__(self):
        # Standard specifications
        self.x = -1
        self.y = -1
        self.layers = []
        self.trace = -1
        self.space = -1
        self.drill = -1
        self.annularRing = -1
        self.thickness = []
        self.drillAspectRatio = -1
        self.outerCopper = []
        self.innerCopper = []
        self.finish = []
        self.silk = []
        self.silkColor = []
        self.maskType = []
        self.maskFinish = []
        self.maskColor = []
        self.material = []
        self.standard = [] #IPC2, IPC3, MIL
                
        # Advanced specifications
        self.electricalTest = None
        self.tabRoute = None
        self.cutout = None
        self.score = None
        self.counterbore = None
        self.countersink = None
        self.controlledImpedance = None
        self.controlledDielectric = None
        self.bevel = None
        self.platedEdge = None
        self.platedSlot = None
        self.viaBlindBuried = None
        self.maxWarpTwist = None #percentage

    def printTemplate(self):
        cfg = ConfigObj()
        cfg.filename = 'blankSpec.cfg'
        # OR USE YAML


        # In Python3, an OrderedMeta (metaclass) can be used to return
        # a list of the variables in order.

        # for var in vars(self):
        #     print 'var string', var
        
        # members = [attr for attr in dir(self) if not callable(attr) and not attr.startswith("__")]
        # print 'members', members







    
    




if __name__ == '__main__':
    quoter = InstantQuote()
    quoter.quoteSunstoneValue()
