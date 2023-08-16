"""
Name: main.py
Author: David Hanley
Date: 16-Aug-2023

Gets the Sunshine record for Scotland_W region for a specified Year and Month

"""
from requests import request
import argparse
from datetime import datetime
import os
import re
import pickle

data_path = 'data'

def process_data(met_office_raw_data: str, data_file: str) -> dict:
    print('Processing data ...')
    data_set: dict = {}
    raw_data: list = met_office_raw_data.split('\n')[6:-1]
    regex = re.compile(r"---|\d+\.?\d*")
    for data in raw_data:
        data_elememts = regex.findall(data)
        for idx in range(0,24,2):
            month: str = f'{(idx // 2) + 1}'
            sunshine_hours: str = data_elememts[idx]   
            year: str = data_elememts[idx+1]

            # add to dictionary
            data_set[(year,month)] = sunshine_hours  

    # save to file as JSON
    print(f'Caching data to file {data_file} ...')
    with open(data_file, 'wb') as data_file:
        pickle.dump(data_set,data_file)

    return data_set


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', action='store_true', help='Update dataset from Met Office website')
    parser.add_argument('-r', help='Region', choices=['Scotland_W','Scotland_E','Scotland_N'], default='Scotland_W')
    parser.add_argument('-m', type=int, help='Month <mm> as a integer', default=datetime.now().month)
    parser.add_argument('-y', type=int, help='Year <yyyy> as a integer', default=datetime.now().year)
    args = parser.parse_args()

    data: dict = {}
    data_file: str = os.path.join(data_path,args.r)

    if args.u or not os.path.isfile(data_file):
        print(f'Getting data for {args.r} from Met Office website ..')
        resp = request('GET', url=f'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Sunshine/ranked/{args.r}.txt')
        if resp.status_code == 200:
            data = process_data(resp.text, data_file)
        else:
            print(f'Error: {resp.status_code}\nCould not get data set: {resp.url}')
            exit()
    else:
        print(f'Loading data from file {data_file} ...')
        with open(data_file, 'rb') as data_file:
            data: dict = pickle.load(data_file)
    
    try:
        hours = data[(str(args.y),str(args.m))]
        print(f'Sunshine Hours for {str(args.m)}/{str(args.y)}: {hours}')
    except KeyError as _:
        print(f'No data exists for {str(args.m)}/{str(args.y)}')
    

if __name__ == '__main__':
    main()