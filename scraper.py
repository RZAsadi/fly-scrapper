import asyncio
from pyppeteer import launch
from time import sleep
from easyocr import Reader
from unidecode import unidecode
import requests
from multiprocessing import Pool
import jdatetime

class FlyScrapper:
    def __init__(self, reader: Reader, fly_info: dict = None) -> None:

        self.reader = reader
        self.flights_details = {}

        if fly_info is None:
            fly_info = {'fromCity': 'MHD', 'toCity': 'THR', 'wayType': 'OneWay', 'flyDate': jdatetime.datetime.now().strftime("%Y/%m/%d")}
            self.flyFromCity = fly_info['fromCity']
            self.flyToCity = fly_info['toCity']
            self.flyWayType = fly_info['wayType']
            self.flyDate = fly_info['flyDate']
        else:
            self.fly_info = fly_info
            try:
                self.flyFromCity = fly_info['fromCity']
                self.flyToCity = fly_info['toCity']
                self.flyWayType = fly_info['wayType']
                self.flyDate = fly_info['flyDate']
            except Exception as e:
                return print('ERROR:', e)

    
    async def runner(self, url):
        self.url = url
        print(self.url)
        await self.main()

    async def launch_browser(self):
        self.browser = await launch()
        self.page = await self.browser.newPage()

    async def open_login_page(self):
        await self.page.goto(self.url)
    

    async def get_captcha(self):
        await self.page.waitForXPath('//*[@id="imgCaptcha"]')
        captcha_section = await self.page.xpath('//*[@id="imgCaptcha"]')
        captcha_url = await (await captcha_section[0].getProperty("src")).jsonValue()
        img_byte = requests.get(captcha_url).content
        ret = self.imageToText(img_byte)

        if ret == False:
            await self.open_login_page()
            return await self.get_captcha()
        
        return ret
    
    async def submit_login_form(self, cap):
        await self.page.waitForXPath('//*[@id="txtCaptchaNumber"]')
        await self.page.evaluate("document.querySelector('#txtCaptchaNumber').value = '';")
        text_box = await self.page.xpath('//*[@id="txtCaptchaNumber"]')
        await text_box[0].type(cap)

        await self.page.waitForXPath('//*[@id="btnLogin"]')
        login_button = await self.page.xpath('//*[@id="btnLogin"]')
        await login_button[0].click()
        await self.page.waitForNavigation()

        try:
            await self.page.waitForXPath('//*[@id="frmLogin"]/table/tbody/tr[1]/td/table[1]', {'timeout': 1000})
            print('Login Failed\ntrying again...')
            new_cap = await self.get_captcha()
            return await self.submit_login_form(cap=new_cap)
        except Exception as e:
            print('Login Success')
        
        #
            (1)


    async def setup_flight(self):
        await self.page.evaluate(f"document.querySelector('select#dplFrom').value = '{self.flyFromCity}';")
        await self.page.evaluate(f"__doPostBack('dplFrom','{self.flyFromCity}');")
        sleep(0.5)
        await self.page.evaluate(f"document.querySelector('select#dplTo').value = '{self.flyToCity}';")
        await self.page.evaluate(f"__doPostBack('dplTo','{self.flyToCity}');")
        sleep(0.5)
        await self.page.evaluate(f"document.querySelector('select#dplReservationRouteType').value = '{self.flyWayType}';")
        await self.page.evaluate(f"__doPostBack('dplReservationRouteType','{self.flyWayType}');")
        sleep(0.5)
        await self.page.evaluate(f"document.querySelector('input#txtDepartureDate').value = '{self.flyDate}';")
        sleep(0.5)

        submit_form = await self.page.xpath('//*[@id="btnSubmit"]')
        await submit_form[0].click()
        await self.page.waitForNavigation()

        #sleep(1.5)
    

    async def check_if_fly_exist(self):
        try:
            await self.page.waitForSelector('td#Module_Error1__tdError', {'timeout': 500})
            print('No fly available')
            return
        except:
            pass


    async def grab_flights_details(self):
        all_flights = []
        flights = await self.page.querySelector('#tdMain > table.tblSR > tbody')
        flights = await flights.xpath('//*[@class="df"]')
        for flight in flights:
            detail = {}

            #Get status start
            status_td = await flight.querySelector('td:nth-child(8)')
            status_div = await status_td.querySelector('div') 
            status_text_content = await self.page.evaluate('(element) => element.textContent', status_div)
            detail["status"] = str(status_text_content).strip().replace('\xa0','')
            #Get status end

            if 'OnTime' not in str(status_text_content).strip().replace('\xa0',''): continue

            #Get the prices start
            prices_body_tr = await flight.querySelectorAll('tbody > tr')
            prices = []

            for price in prices_body_tr:
                prc = await price.querySelector('td:nth-child(2) > span > label')
                price_text_content = await self.page.evaluate('(element) => element.textContent', prc)
                prices.append(str(price_text_content).strip().replace('\xa0',''))

            detail["prices"] = prices
            #Get the prices end

            #Get route start
            route_td = await flight.xpath('//*[@class="df"]/td[2]')
            route_text_content = await self.page.evaluate('(element) => element.textContent', route_td[0])
            detail["route"] = str(route_text_content).strip().replace('\xa0','')
            #Get route end

            #Get date start
            date_td = await flight.querySelector('td:nth-child(3)')
            date_text_content = await self.page.evaluate('(element) => element.textContent', date_td)
            detail["date"] = str(date_text_content).strip().replace('\xa0','')
            #Get date end

            #Get departure start
            departure_td = await flight.querySelector('td:nth-child(4)')
            departure_text_content = await self.page.evaluate('(element) => element.textContent', departure_td)
            detail["departure"] = str(departure_text_content).strip().replace('\xa0','')
            #Get departure end

            #Get arrival start
            arrival_td = await flight.querySelector('td:nth-child(5)')
            arrival_text_content = await self.page.evaluate('(element) => element.textContent', arrival_td)
            detail["arrival"] = str(arrival_text_content).strip().replace('\xa0','')
            #Get arrival end

            #Get name start
            name_td = await flight.querySelector('td:nth-child(6)')
            name_text_content = await self.page.evaluate('(element) => element.textContent', name_td)
            detail["name"] = str(name_text_content).strip().replace('\xa0','').replace('\n', '')
            #Get name end

            #Get number start
            number_td = await flight.querySelector('td:nth-child(7)')
            number_text_content = await self.page.evaluate('(element) => element.textContent', number_td)
            detail["number"] = str(number_text_content).strip().replace('\xa0','')
            #Get number end

            all_flights.append(detail)
        
        self.flights_details[self.url] = all_flights

    
    async def main(self):
        await self.launch_browser()

        await self.open_login_page()

        cap = await self.get_captcha()

        await self.submit_login_form(cap)

        await self.setup_flight()

        await self.check_if_fly_exist()

        await self.grab_flights_details()

        await self.browser.close()

        return self.flights_details
    
    def imageToText(self, img):
        try:
            result = self.reader.readtext(img, allowlist='١٢٣٤٥٦٧٨٩٠', low_text=0.1)
            if result and result[0]:  # Check if result is not empty and has at least one element
                predict = unidecode(result[0][1])
                return predict
            else:
                return False  # Return False if no text was found
        except Exception as e:
            print('Captcha Error:', e)
            return False


async def run_all(urls, fly_inf):
    # Create a list of FlyScrapper instances
    scrappers = [FlyScrapper(reader=reader, fly_info=fly_inf) for url in urls]
    
    # Run the FlyScrapper instances concurrently
    await asyncio.gather(*(scrapper.runner(url) for scrapper, url in zip(scrappers, urls)))

# Create the list of URLs to scrape
urls = [
    'https://sepehr.nedaparvaz.ir/Systems/Login.aspx',
    'https://opo24.ir/Systems/Login.aspx',
    'https://www.mehrabseir.ir/Systems/Login.aspx'
]


if __name__ == '__main__':
    reader = Reader(lang_list=['en', 'fa'], gpu=False)
    inf = {'fromCity': 'MHD', 'toCity': 'THR', 'wayType': 'OneWay', 'flyDate': '1402/10/11'}
    asyncio.run(run_all(urls, fly_inf=inf))
    
    