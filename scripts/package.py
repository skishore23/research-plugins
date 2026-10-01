#!/usr/bin/env python3
"""Build reproducible single-plugin ZIPs from an allowlisted source tree."""
from pathlib import Path
import hashlib,json,zipfile
import jsonschema
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SCHEMA=json.loads((ROOT/'scripts/plugin.schema.json').read_text())


def build():
    out=ROOT/'dist';out.mkdir(exist_ok=True)
    records=[]
    for p in sorted((ROOT/'plugins').iterdir()):
        manifest=json.loads((p/'plugin.json').read_text())
        jsonschema.Draft202012Validator(SCHEMA).validate(manifest)
        interface=manifest['extensions']['com.openai']['interface']
        assert manifest['name']==p.name
        assert len(interface['displayName'])<=30 and len(interface['shortDescription'])<=30
        assert len(interface['longDescription'])<=4000
        assert len(interface['defaultPrompt'])<=3 and all(len(x)<=128 and '\n' not in x for x in interface['defaultPrompt'])
        for field in ['logo','composerIcon']:
            asset=(p/interface[field]).resolve();assert asset.is_relative_to(p.resolve())
            with Image.open(asset) as im:assert im.format=='PNG' and 256<=im.width==im.height<=4096
            assert asset.stat().st_size<=5*1024*1024
        assert manifest['extensions']['com.openai']['review']['commerce'] is False
        assert manifest['extensions']['com.openai']['publication']['countries']==[]
        compatibility=json.loads((p/'.codex-plugin/plugin.json').read_text())
        assert compatibility['name']==manifest['name'] and compatibility['version']==manifest['version']
        assert not compatibility.get('apps') and not manifest.get('apps')
        assert not manifest['extensions']['com.openai'].get('apps') and not (p/'.app.json').exists()
        for k,v in compatibility['interface'].items(): assert interface[k]==v
        files=[]
        for f in sorted(p.rglob('*')):
            if f.is_symlink():raise ValueError('symlink: '+str(f))
            if f.is_file() and '__pycache__' not in f.parts and f.suffix!='.pyc':files.append(f)
        hashes={str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
        archive=out/f'{p.name}-{manifest["version"]}.zip'
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
            for f in files:
                info=zipfile.ZipInfo(str(f.relative_to(p.parent)),date_time=(2026,10,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
                z.writestr(info,f.read_bytes())
            info=zipfile.ZipInfo(p.name+'/CONTENTS.sha256.json',date_time=(2026,10,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,json.dumps(hashes,indent=2)+'\n')
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            for name,digest in hashes.items(): assert hashlib.sha256(z.read(p.name+'/'+name)).hexdigest()==digest
        records.append({'name':p.name,'version':manifest['version'],'file':archive.name,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'bytes':archive.stat().st_size})
    (out/'releases.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(records,indent=2))
if __name__=='__main__':build()
