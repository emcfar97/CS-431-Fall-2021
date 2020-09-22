from .. import CONNECT, INSERT, SELECT, UPDATE, WEBDRIVER
from ..utils import login, progress, save_image, get_hash, get_name, get_tags, generate_tags, bs4, re, requests, time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException, ElementClickInterceptedException, NoSuchElementException

SITE = 'instagram'
CONNECTION = CONNECT()
DRIVER = WEBDRIVER(True)

def initialize(url='/chairekakia/saved/', retry=0):
    
    DRIVER.get(f'https://www.instagram.com{url}')
    query = set(CONNECTION.execute(SELECT[0], (SITE,), fetch=1))
    
    while True:

        DRIVER.find_element_by_tag_name('html').send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

        html = bs4.BeautifulSoup(DRIVER.page_source, 'lxml')
        hrefs = [
            (target.get('href'), 1, SITE) for target in 
            html.findAll('a', href=re.compile('/p/.+'))
            if (target.get('href'),) not in query
            ]
        CONNECTION.execute(INSERT[0], hrefs, 1)
            
        if not hrefs:
            if retry >= 2: break
            else: retry += 1
        else:
            query = set(CONNECTION.execute(SELECT[0], (SITE,), fetch=1))
            retry = 0

    CONNECTION.commit()
    
def page_handler(hrefs):

    if not hrefs: return
    size = len(hrefs)

    for num, (href,) in enumerate(hrefs):
        
        progress(size, num, SITE)
        DRIVER.get(f'https://www.instagram.com{href}')
        html = bs4.BeautifulSoup(DRIVER.page_source, 'lxml')
        artist = html.find('a', href=re.compile('/.+/')).text

        try:
            image = html.find(
                'img', src=re.compile('.+scontent.+'), style='object-fit: cover;'
                )
        except: continue

        name = get_name(image, 0, 1)
        save_image(name, image)
        tags, rating, exif = generate_tags(
            general=get_tags(DRIVER, name), 
            custom=True, rating=True, exif=True
            )
        if name.endswith(('jpg', 'jpeg')): save_image(name, image, exif)
        hash_ = get_hash(name) 
        
        CONNECTION.execute(UPDATE[3], (
            name, ' ', tags, rating, image, hash_, href),
            commit=1
            )
    
    progress(size, size, SITE)

def setup(initial=True):
    
    try:
        login(DRIVER, SITE)
        if initial: initialize(DRIVER)
        page_handler(CONNECTION.execute(SELECT[2], (SITE,), fetch=1))
    except Exception as error: print(f'{SITE}: {error}')
        
    DRIVER.close()
