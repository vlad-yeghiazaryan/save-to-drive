import os
import json
from datetime import datetime
from drive import saveToDrive

def main(request):
  # main variables
  dateToday = datetime.today().strftime('%Y-%m-%d')
  if 'filename' not in request:
    request['filename'] = 'data'
  if 'gDrivePath' not in request:
    request['gDrivePath'] = 'scraped_data/default'
  fileFullName = f'{request["filename"]}-{dateToday}.json'
  gDrivePath = request['gDrivePath']

  # Create temp file
  with open(fileFullName, 'w') as file:
    if 'scraped_data' in request:
      json.dump(request['scraped_data'], file)
    else:
      json.dump(request['scraped_data'], file)
  # Saving data to drive
  saveToDrive(drivePath=gDrivePath, filePath=fileFullName)

  # remove instance from current dir
  os.remove(fileFullName)

  # Response message
  return {'message': f"Scrapped {fileFullName} was successfully saved to root/{gDrivePath} in the user's google drive."}

if __name__ == "__main__":
  sample = {'scraped_data': {'name': 'John Doe'}, 'filename': 'data',
  "gDrivePath":"Scraped/Names"}
  main(sample)
