## Purpose
Saves the output to google drive.

## Execution order:
```bash
docker pull ibmfunctions/action-python-v3.7
```
```bash
docker run --rm -v "$PWD:/tmp" ibmfunctions/action-python-v3.7 bash -c "cd /tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt"
```
```bash
zip -r save-to-drive.zip __main__.py drive.py credentials.json virtualenv
```
```bash
ibmcloud fn action create saveToDrive save-to-drive.zip --kind python:3.7 --web true
```
or
```bash
ibmcloud fn action update saveToDrive save-to-drive.zip --kind python:3.7 --web true
```