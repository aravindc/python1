from mysql.connector import MySQLConnection
from mysql.connector import Error
from dbconfig import read_db_config
import logging
import os
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def connect():
    """ Connect to Mysql databse """
    db_config = read_db_config()
    try:
        conxn = MySQLConnection(**db_config)
        if conxn.is_connected():
            logger.info('Connected to database')
    except Error as e:
        logger.error(e)
    # finally:
    #    conxn.close()
    #    logger.info('Connection Closed')
    return conxn


def insert_data(conxn, tabname, json_file):
    try:
        cursor = conxn.cursor()
        json_data = open(json_file).read()
        temp_str = os.path.splitext(json_file)[0]
        end = None
        ins_dt = temp_str[temp_str.find('_') + 1:end]
        if tabname == 'tesco':
            qrystr = """INSERT INTO tesco(productid, imgsrcl, productdesc, producturl) VALUES(%s, %s, %s, %s)"""
        elif tabname == 'sains':
            qrystr = """INSERT INTO sains(productid, imgsrcl, productdesc, producturl, priceunit, offerdesc, ins_ts) VALUES(%s, %s, %s, %s, %s, %s, %s)"""
            for item in json.loads(json_data):
                logger.info(item)
                cursor.execute(qrystr, (item['productid'], 'https:' + item['imgsrcl'], item['productdesc'], item['producturl'], item['priceunit'], item['offerdesc'], ins_dt))
            conxn.commit()
    except Error as e:
        print('Error:', e)
    finally:
        cursor.close()
        # conxn.close()
        logger.info('Cursor closed')


def get_file_name(conxn, tabname):
    try:
        cursor = conxn.cursor()
        if tabname == 'tesco':
            qrystr = """SELECT date_format(max(ins_ts)+1,'%Y%m%d') from tesco"""
        elif tabname == 'sains':
            qrystr = """SELECT date_format(max(ins_ts)+1,'%Y%m%d') from sains"""
        cursor.execute(qrystr)
        row = cursor.fetchone()
        if row is None:
            retval = '20180215'
        else:
            retval = row
    except Error as e:
        logger.error(e)
    finally:
        cursor.close()
    return retval


if __name__ == '__main__':
    conx = connect()
    json_file = 'c:/tmp/python1/test_20180208.json'
    insert_data(conx, 'sains', json_file)
    conx.close()
