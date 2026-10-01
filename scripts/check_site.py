from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1]/'docs'
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key in ('href','src') and value:self.links.append(value)
count=0
for p in ROOT.rglob('*.html'):
    parser=Links();parser.feed(p.read_text())
    for link in parser.links:
        u=urlsplit(link)
        if u.scheme or not u.path:continue
        dest=(p.parent/unquote(u.path)).resolve()
        assert dest.is_relative_to(ROOT.resolve()),(p,link)
        if dest.is_dir():dest=dest/'index.html'
        assert dest.is_file(),(p,link)
        count+=1
print(f'Checked {count} local page, asset and download links.')
