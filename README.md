# Ovia

Dependencies
  - asyncio
  - aiohttp
  - pandas
  - numpy
  - json
  - warnings
  - NOAA token (request page: https://www.ncdc.noaa.gov/cdo-web/token)
  
Files
  - PopulationByFIPS.xlsx

When run, Ovia.py gets the average temperature for any US county in the contiguous US that has a population greater than 50,000. After Ovia.py is finished running, the county GHCND code and temperature will be printed out.
