"""Retrieve immutable upstream files; refuse changed bytes. No model inference."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import ssl
import urllib.request
import certifi

ROOT = Path(__file__).resolve().parents[1]

def fetch(upstream=None):
    manifest = json.loads((ROOT / 'data/source_manifest.json').read_text())
    target = ROOT / 'input'
    target.mkdir(exist_ok=True)
    for record in manifest['files']:
        path = target / record['local_name']
        if not path.exists():
            temporary = path.with_suffix('.part')
            if upstream:
                shutil.copyfile(Path(upstream) / record['path'], temporary)
            else:
                url = manifest['repository'].replace('github.com', 'raw.githubusercontent.com')
                url += '/' + manifest['commit'] + '/' + record['path']
                with urllib.request.urlopen(url, timeout=120, context=ssl.create_default_context(cafile=certifi.where())) as response:
                    temporary.write_bytes(response.read())
            if hashlib.sha256(temporary.read_bytes()).hexdigest() != record['sha256']:
                raise ValueError(f'Checksum mismatch: {temporary}')
            temporary.replace(path)
        if hashlib.sha256(path.read_bytes()).hexdigest() != record['sha256']:
            raise ValueError(f'Checksum mismatch: {path}')
        print('Verified', record['local_name'], record['sha256'])

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--upstream', type=Path, help='Optional existing read-only checkout')
    fetch(ap.parse_args().upstream)
