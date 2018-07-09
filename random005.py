import requests
import logging
import csv
from bs4 import BeautifulSoup
import time
from PIL import Image
from resizeimage import resizeimage


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

base_url = 'https://rewards.nab.com.au'
# ?sorting.currentsortfield=description&sorting.currentsortascending=true&Paging.PageSize=48&Paging.CurrentPage=2
item_url = '#!pgno={}&res=48&sort=description&sortasc=true'

# a['class': 'product-box-main'] - Product URL
# img['class': 'product-box-image'] - Product Image
# span['class': 'h3 product-heading'] - Product Description
# span['class': 'h4 product-points'] - Points


# afl - 2
# kids - 2
# fashnlife - 3
# giftcards - 3
# homewares - 6
# travel - 3
# tickets - 2
# sports - 4
# technology - 5
# charity - 3
# business - 2
# office - 2
# premium - 1
# financial - ignore

def resizeImage(imageFile):
    with open(imageFile, 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(image, [400, 290])
            cover.save('test_image.jpg', image.format)


def getItems(menuItems):
    allRewards = []
    for menuItem in menuItems:
        logger.info('Working on: {}'.format(menuItem['URL']))
        response = requests.get(menuItem['URL'])
        soup = BeautifulSoup(response.content, "html.parser")
        page_ul = soup.find('ul', attrs={'class': 'pagination'}).findAll('li')
        logger.info(max(page_ul))
        break


def getMenuItems():
    menuObj = []
    response = requests.get(base_url+'/rewards')
    soup = BeautifulSoup(response.content, "html.parser")
    for menuitem in soup.findAll('li', attrs={'class': "is-submenu-item"}):
        newMenuItem = {}
        if (menuitem['class'][0] == 'is-submenu-item'):
            newMenuItem['Name'] = menuitem.text
            newMenuItem['URL'] = base_url + menuitem.a['href']
            menuObj.append(newMenuItem)
    return menuObj


if __name__ == '__main__':
    menus = getMenuItems()
    getItemPages(menus)
    # logger.info(menus)
