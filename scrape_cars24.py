import requests
from bs4 import BeautifulSoup
import random
import time
import mysql.connector as connection
import json

file = open("C://Users//91964//Desktop//My_sql_details.json")  # getting my username password of mysql from another file
mysql = json.load(file)
file.close()

host = mysql['host']
user = mysql['user']
passwd = mysql['passwd']

try:
    my_db = connection.connect(host=host, user=user, passwd=passwd, use_pure=True) # connecting to data base
    query = "CREATE DATABASE IF NOT EXISTS Used_cars;"
    cursor = my_db.cursor()
    cursor.execute(query)
    print('Database {} created'.format('Used_cars'))
    my_db.close()

except Exception as e:
    print('Database Used_car cannot be created', str(e))

try:
    my_db = connection.connect(host=host, user=user, passwd=passwd, database='Used_cars', use_pure=True) # creating table with required features
    query = "CREATE TABLE IF NOT EXISTS car_details(Name VARCHAR(100)," \
            "Price VARCHAR(20),Distance_travelled VARCHAR(20)," \
            "Date_of_purchase VARCHAR(20), Ownership VARCHAR(20)," \
            "Fuel_type VARCHAR(20),Transmission VARCHAR(20)," \
            "Date_of_Insurance VARCHAR(20),Type_of_insurance VARCHAR(20)," \
            "City VARCHAR(20));"

    cursor = my_db.cursor()
    cursor.execute(query)
    print('Table {} created'.format('car_details'))
    my_db.close()

except Exception as e:
    print('Table Details cannot be created', str(e))

# scraping used cars data from cars24 website

cities = {'NewDelhi': 2, 'Noida': 134, 'Gurgaon': 5, 'Mumbai': 2378, 'Kolkata': 777,
          'Hyderabad': 3686, 'Chennai': 5732, 'Bangalore': 4709, 'Pune': 2423, 'Ahmedabad': 1692}

cars = []

for city in cities.keys():

    time.sleep(random.randint(2, 10))
    page = 1

    while page > 0:

        url = 'https://www.cars24.com/buy-used-car?sort=P&page={page}&storeCityId={city}'.format(page=page,
                                                                                                 city=cities[city])

        time.sleep(random.randint(1, 5))

        try:
            req = requests.get(url)
            soup = BeautifulSoup(req.text, 'html.parser')
            items = soup.find_all('div', {'itemprop': 'makesOffer'})

        except Exception as e:
            print('Exeption occured in url request:', str(e))

        if len(items) > 0:

            for item in items:

                item_link = item.select('a')[0]['href']
                req_link = requests.get(item_link)
                soup_link = BeautifulSoup(req_link.text, 'html.parser')

                try:
                    name = soup_link.select('._29zr1')[0].select('p')[0].text

                except:
                    name = 'No Name'

                try:
                    price = soup_link.select('._29zr1')[0].select('h4')[0].text

                except:
                    price = 'No Price'

                soup_details = soup_link.select('.media.RD6HR')

                for i in range(len(soup_details)):

                    details = soup_link.select('.media.RD6HR')[i].select('.media-body._3fGRT')[0].text

                    try:
                        if 'Kilometers' in details:
                            km = details

                    except:
                        km = 'Not Available'

                    try:
                        if 'Year of Purchase' in details:
                            purchase_date = details

                    except:
                        purchase_date = 'Not Available'

                    try:
                        if 'Owner' in details:
                            owner = details

                    except:
                        owner = 'Not Available'

                    try:
                        if 'Fuel' in details:
                            fuel = details

                    except:
                        fuel = 'Not Available'

                    try:
                        if 'Transmission' in details:
                            transmission = details

                    except:
                        transmission = 'Not Available'

                    try:
                        if 'Insurance' in details:

                            try:
                                if 'Insurance Type' in details:
                                    ins_type = details
                            except:
                                ins_type = 'Not Available'

                        else:
                            ins_date = details

                    except:
                        ins_date = 'Not Available'

                Name = ' '.join(name.split()[1:])
                Price = ''.join(price.split()[1].split(','))
                Distance = km.replace('Kilometers', '').replace(',', '')[:-3]
                Date_purchased = purchase_date.replace('Year of Purchase', '')
                Ownership = owner.replace('Owner', '').strip()
                Fuel_type = fuel.replace('Fuel', '')
                Transmission = transmission.replace('Transmission', '')
                insurance_date = ins_date.replace('Insurance', '')
                insurance_type = ins_type.replace('Insurance Type', '')

                # print('{}  : completed'.format(item_link))

                car_details = {'Name': Name, 'Price': Price, 'Distance_travelled': Distance,
                               'Date_of_purchase': Date_purchased, 'Ownership': Ownership,
                               'Fuel_type': Fuel_type, 'Transmission': Transmission,
                               'Date_of_Insurance': insurance_date, 'Type_of_insurance': insurance_type,
                               'City': city}

                cars.append(car_details)
            print('Page number {} is completed'.format(page))

        else:
            print('Scrapping {} completed'.format(city))
            break

        page += 1

try:
    my_db = connection.connect(host=host, user=user, passwd=passwd,
                               database='Used_cars', use_pure=True)  # inserting the scraped data to mysql database table

    query = "INSERT INTO car_details(Name,Price,Distance_travelled," \
            "Date_of_purchase,Ownership,Fuel_type,Transmission,Date_of_Insurance," \
            "Type_of_insurance,City) " \
            "VALUES (%(Name)s,%(Price)s,%(Distance_travelled)s," \
            "%(Date_of_purchase)s,%(Ownership)s,%(Fuel_type)s,%(Transmission)s," \
            "%(Date_of_Insurance)s,%(Type_of_insurance)s,%(City)s);"

    cursor = my_db.cursor()

    cursor.executemany(query, cars)

    print('Values inserted')

    my_db.commit()

    my_db.close()

except Exception as e:
    print('values cannot be inserted', str(e))
