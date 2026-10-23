"""Return the built IPA to the authorized workstation without publishing it."""
import hashlib
import json
import os
from pathlib import Path
import urllib.request

ipa = Path(os.environ['RUNNER_TEMP']) / 'artifacts/SuperMarioOdyssey-iphone-unsigned.ipa'
size = ipa.stat().st_size
offset = 0
digest = hashlib.sha256()
with ipa.open('rb') as source:
    while data := source.read(64 * 1024**2):
        digest.update(data)
        request = urllib.request.Request(
            os.environ['TRANSFER_URL'] + '/ipa', data=data, method='POST',
            headers={'X-Transfer-Token': os.environ['TRANSFER_TOKEN'],
                     'X-Offset': str(offset), 'Content-Type': 'application/octet-stream'})
        with urllib.request.urlopen(request, timeout=180) as response:
            acknowledged = int(response.read())
        offset += len(data)
        if acknowledged != offset:
            raise RuntimeError('Workstation did not acknowledge the expected byte count')
        print(f'Returned {offset}/{size} IPA bytes', flush=True)
receipt = json.dumps({'size': size, 'sha256': digest.hexdigest()}).encode()
request = urllib.request.Request(
    os.environ['TRANSFER_URL'] + '/complete', data=receipt, method='POST',
    headers={'X-Transfer-Token': os.environ['TRANSFER_TOKEN'], 'Content-Type': 'application/json'})
with urllib.request.urlopen(request, timeout=180) as response:
    print(response.read().decode())
