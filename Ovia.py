import asyncio
import aiohttp
from aiohttp import ClientSession
import pandas as pd
import warnings
import json
import numpy as np
warnings.filterwarnings("ignore")

population_dataframe = pd.read_excel('PopulationByFIPS.xlsx')
overfifty = population_dataframe[population_dataframe['Population'] >= 50000]

fips = [str(fips).zfill(5) for fips in overfifty['Fips']]
urls = ['https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&locationid=FIPS:'+fip+'&startdate=2018-07-01&enddate=2018-07-01&units=standard&limit=1000' for fip in fips]

class Ovia(object):
    
    def __init__(self, urls, noaa_token):
        
        self.urls = urls
        self.noaa_token = noaa_token
        
    async def fetch(self, url):
    
        async with self.session.get(url) as response:

            return await response.read()
        
    async def run(self):
    
        self.tasks = []

        async with ClientSession(headers={'token': self.noaa_token}) as self.session:

            for url in self.urls:

                # NOAA only allows five requests per second
                await asyncio.sleep(.25)

                task = asyncio.ensure_future(self.fetch(url))
                self.tasks.append(task)

            self.responses = asyncio.gather(*self.tasks)

            return await self.responses
        
    def GetData(self):
        
        self.loop = asyncio.get_event_loop()

        self.future = asyncio.ensure_future(self.run())

        self.loop.run_until_complete(self.future)
        
        return [json.loads(data) for data in temps.future.result() if 'results' in json.loads(data).keys()]
                
if __name__ == '__main__':
    
    temps = Ovia(urls, API_TOKEN_HERE)
    
    # Dicts by county
    data_dict = temps.GetData()
    
    for lst in [data['results'] for data in data_dict]:
    
        vals = []

        for dic in lst:

            if dic['datatype'] == 'TOBS':

                vals.append(dic['value'])

        print(lst[0]['station'], np.average(vals))
