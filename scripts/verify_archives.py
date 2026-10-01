from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as directory:
    target=Path(directory)
    for archive in (ROOT/'dist').glob('*.zip'):
        with zipfile.ZipFile(archive) as z:
            assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist())
            z.extractall(target/'plugins')
        folder=next(p for p in (target/'plugins').iterdir() if archive.name.startswith(p.name+'-'))
        for path,digest in json.loads((folder/'CONTENTS.sha256.json').read_text()).items():
            assert hashlib.sha256((folder/path).read_bytes()).hexdigest()==digest
    subprocess.run([sys.executable,'-m','pytest',str(ROOT/'tests'),'-q'],env={**os.environ,'PLUGIN_TEST_ROOT':str(target)},check=True)
print('Extracted ZIP hashes and all regression tests passed.')
