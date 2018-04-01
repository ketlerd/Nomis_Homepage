from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
import time


#landing page
#index
class landing:
    #verify a valid search page load
    def search(driver, searchString):
        driver.get("https://www.nomissolutions.com/")
        elem = driver.find_element_by_id('gsc-i-id1')
        elem.send_keys(searchString)
        elem.send_keys(Keys.RETURN)
        elem.click
        assert "Search" in driver.title, "Search page did not load correctly."

        time.sleep(5)
    
    #verify a failed search (internal error)
    #going at this functionality harder will throw a 500 error
    #Nomis should further fuzz and test this, might be a vuln here
    def failedSearch(driver, searchString):
        driver.get("https://www.nomissolutions.com/")
        elem = driver.find_element_by_id('gsc-i-id1')
        elem.send_keys(searchString)
        elem.send_keys(Keys.RETURN)
        elem.click
        elem = driver.find_element_by_class_name('gsc-results')

        #internal error from a long string is promising, buffer overflow vuln?
        assert "Internal Error" in elem.text, "Should have thrown internal error due to long search string."
        time.sleep(5)

    #verify XSS attempts are caught by cloudflare
    def xssInjection(driver, searchString):
        driver.get("https://www.nomissolutions.com/")
        elem = driver.find_element_by_id('gsc-i-id1')
        elem.send_keys(searchString)
        elem.send_keys(Keys.RETURN)
        elem.click
        elem = driver.find_element_by_class_name('cf-error-overview')

        assert "One more step" in elem.text, "CloudFlare didn't catch the XSS attack, should have halted with captcha."


#404 page 
#has some various newsletter subs and stuff
#seem to be largely non-functional
class notFound:

    #verify subscribe to newsletter (which appears to fail silently)
    def subscribe(driver, email):
        driver.get("https://www.nomissolutions.com/admin")
        #assert "Solutions" in driver.title
        elem = driver.find_element_by_name('email')
        elem.send_keys(email)
        elem.send_keys(Keys.RETURN)
        time.sleep(5)

#resources page
class resources:
    
    #subscribe to newsletter
    def subscribe(driver, email, first, last):
        driver.get("https://blog.nomissolutions.com/resources")
        time.sleep(5)
        elem = driver.find_element_by_name('email')
        elem.send_keys(email)
        elem = driver.find_element_by_name('firstname')
        elem.send_keys(first)
        elem = driver.find_element_by_name('lastname')
        elem.send_keys(last)

        error = driver.find_element_by_class_name('hs-error-msgs').text
        assert "Please enter your business email address." in error, "Does not correctly return validation error. Should print: Please enter your business email address. This form does not accept addresses from test.com."



#Sign up for sales call
class getStarted:
    #populate various fields, with defaults should none be specified
    def learnMore(driver, first=None, last=None, title=None, email=None, company=None, phone=None):
        driver.get("https://info.nomissolutions.com/get-started")
        
        if first == None || first == '':
            first = 'first name'
        if last == None || last == '':
            last = 'last name'
        #strip whitespace since title is a dropdown
        #and I want it picking at least _something_
        if title == None || title.strip() == '':
            title = 'Other'
        if email == None || email == '':
            email = "test@test.com"
        if company == None || company == '':
            company = 'n/a'
        if phone == None || phone == '':
            phone = "555-555-5555"

        driver.find_element_by_name('firstname').send_keys(first)
        driver.find_element_by_name('lastname').send_keys(last)

        select = Select(driver.find_element_by_name('hs_persona'))
        select.select_by_visible_text(title)

        driver.find_element_by_name('email').send_keys(email)
        driver.find_element_by_name('company').send_keys(company)
        driver.find_element_by_name('phone').send_keys(phone)

        #I won't submit since it does allow a lot of junk data through
        #Don't want to fill the sales inbox full of junk

        


        


def main():
    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME)

    driver.implicitly_wait(10) # seconds

    landingPage = landing
    
    #valid search
    landing.search(driver, "test")
    
    #server error for long search strings, should fuzz but gonna not do that right now
    #possibly a web vuln here
    landing.failedSearch(driver, "Bacon ipsum dolor amet turducken leberkas meatball t-bone, doner boudin salami frankfurter fatback beef. Rump spare ribs tenderloin, ham bresaola flank beef. Bresaola prosciutto meatloaf strip steak pancetta. Meatball short loin salami, biltong pork chop hamburger drumstick cupim sirloin doner pastrami tongue frankfurter pork belly porchetta. Hamburger turkey ball tip frankfurter pig pork chop salami shankle alcatra prosciutto capicola porchetta boudin bacon. Pork loin leberkas pancetta strip steak prosciutto sausage.Bacon ipsum dolor amet turducken leberkas meatball t-bone, doner boudin salami frankfurter fatback beef. Rump spare ribs tenderloin, ham bresaola flank beef. Bresaola prosciutto meatloaf strip steak pancetta. Meatball short loin salami, biltong pork chop hamburger drumstick cupim sirloin doner pastrami tongue frankfurter pork belly porchetta. Hamburger turkey ball tip frankfurter pig pork chop salami shankle alcatra prosciutto capicola porchetta boudin bacon. Pork loin leberkas pancetta strip steak prosciutto sausage.Bacon ipsum dolor amet turducken leberkas meatball t-bone, doner boudin salami frankfurter fatback beef. Rump spare ribs tenderloin, ham bresaola flank beef. Bresaola prosciutto meatloaf strip steak pancetta. Meatball short loin salami, biltong pork chop hamburger drumstick cupim sirloin doner pastrami tongue frankfurter pork belly porchetta. Hamburger turkey ball tip frankfurter pig pork chop salami shankle alcatra prosciutto capicola porchetta boudin bacon. Pork loin leberkas pancetta strip steak prosciutto sausage.Bacon ipsum dolor amet turducken leberkas meatball t-bone, doner boudin salami frankfurter fatback beef. Rump spare ribs tenderloin, ham bresaola flank beef. Bresaola prosciutto meatloaf strip steak pancetta. Meatball short loin salami, biltong pork chop hamburger drumstick cupim sirloin doner pastrami tongue frankfurter pork belly porchetta. Hamburger turkey ball tip frankfurter pig pork chop salami shankle alcatra prosciutto capicola porchetta boudin bacon. Pork loin leberkas pancetta strip steak prosciutto sausage.Bacon ipsum dolor amet turducken leberkas meatball t-bone, doner boudin salami frankfurter fatback beef. Rump spare ribs tenderloin, ham bresaola flank beef. Bresaola prosciutto meatloaf strip steak pancetta. Meatball short loin salami, biltong pork chop hamburger drumstick cupim sirloin doner pastrami tongue frankfurter pork belly porchetta. Hamburger turkey ball tip frankfurter pig pork chop salami shankle alcatra prosciutto capicola porchetta boudin bacon. Pork loin leberkas pancetta strip steak prosciutto sausage.")

    #mid-sized search strings return no results correctly
    landing.search(driver, "Bacon ipsum dolor amet turducken leberkas meatball t-bone, doner boudin salami frankfurter fatback beef. Rump spare ribs tenderloin, ham bresaola flank beef. Bresaola prosciutto meatloaf strip steak pancetta. Meatball short loin salami, biltong pork chop hamburger drumstick cupim sirloin doner pastrami tongue frankfurter pork belly porchetta. Hamburger turkey ball tip frankfurter pig pork chop salami shankle alcatra prosciutto")

    landing.xssInjection(driver, "<script>alert('test');</script>")

    #resources page
    #signup form test
    resourcesPage = resources
    resources.subscribe(driver, "test@test.com", "foo", "bar")

    #get started
    #sales call signup
    #allows XSS submission and the like, sorry sales team for that junk record
    started = getStarted
    started.learnMore(driver,'david','','Executive','test1@test.com','none','666-666-6666')
    

    driver.close()


main()