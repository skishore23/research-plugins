#!/usr/bin/env python3
"""Build an entirely static GitHub Pages catalog from public plugin files only."""
import html,json,re,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs';OUT.mkdir(exist_ok=True)
E=html.escape


def page(title,body,prefix='./'):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} · Research Plugins</title><meta name="description" content="Open-source skills and executable tools for film planning, reproducible agent experiments and policy authoring."><meta name="theme-color" content="#f5f2e9"><link rel="stylesheet" href="{prefix}styles.css"><script defer src="{prefix}app.js"></script></head><body><a class="skip" href="#content">Skip to content</a><header class="shell"><a class="brand" href="{prefix}">research / plugins <span>by Kishore Shimikeri</span></a><nav aria-label="Main"><a href="{prefix}#plugins">Plugins</a><a href="{prefix}#lab">Explore</a><a href="https://github.com/skishore23/research-plugins">Source ↗</a></nav></header><main id="content" class="shell">{body}</main><footer class="shell"><span>Independent tools. Open source. October 2026.</span><nav aria-label="Footer"><a href="{prefix}research.html">Research notes</a><a href="https://github.com/skishore23/research-plugins/issues">Support ↗</a><a href="https://github.com/skishore23">GitHub ↗</a></nav></footer></body></html>'''


def md(text):
    def inline(s):
        s=E(s)
        s=re.sub(r'\[([^\]]+)\]\((https://[^)]+)\)',r'<a href="\2">\1</a>',s)
        s=re.sub(r'(?<!["(>])(https://[^\s<]+)',lambda m:'<a href="'+m[1].rstrip('.')+'">'+m[1].rstrip('.')+'</a>'+('.' if m[1].endswith('.') else ''),s) if '<a ' not in s else s
        s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
        return s
    blocks=[]
    for block in text.strip().split('\n\n'):
        if block.startswith('|'):
            rows=block.splitlines();head=rows[0];body=[x for x in rows[1:] if not re.fullmatch(r'[| :\-]+',x)]
            def row(s,tag):return '<tr>'+''.join(f'<{tag}>{inline(c.strip())}</{tag}>' for c in s.strip('|').split('|'))+'</tr>'
            blocks.append('<div class="table-wrap"><table>'+row(head,'th')+''.join(row(s,'td') for s in body)+'</table></div>')
        elif block.startswith('#'):
            n=len(block)-len(block.lstrip('#'));blocks.append(f'<h{n}>'+inline(block[n:].strip())+f'</h{n}>')
        else:blocks.append('<p>'+inline(block.replace('\n',' '))+'</p>')
    return '\n'.join(blocks)


def build():
    subprocess.run([sys.executable,str(ROOT/'scripts/package.py')],check=True)
    for name in ['styles.css','app.js']:shutil.copy2(ROOT/'site'/name,OUT/name)
    (OUT/'.nojekyll').write_text('')
    (OUT/'downloads').mkdir(exist_ok=True)
    releases=json.loads((ROOT/'dist/releases.json').read_text())
    for row in releases:shutil.copy2(ROOT/'dist'/row['file'],OUT/'downloads'/row['file'])
    shutil.copy2(ROOT/'dist/releases.json',OUT/'downloads/releases.json')
    cards=[]
    features={'comfy-story-planner':['Exact shot and dialogue timing','Explicit character and object continuity','Candidate prompts and SRT export'], 'worldzero-lab':['Matched seeds and decision budgets','Original simulation kernel','Deterministic trace replay'], 'heimdall-policy-lab':['Source-derived guard catalog','Schema and composition checks','Fail-open and unused-guard findings']}
    tags={'comfy-story-planner':'01 / Create','worldzero-lab':'02 / Experiment','heimdall-policy-lab':'03 / Inspect'}
    for slug in ['comfy-story-planner','worldzero-lab','heimdall-policy-lab']:
        p=ROOT/'plugins'/slug;m=json.loads((p/'plugin.json').read_text());i=m['extensions']['com.openai']['interface'];title=i['displayName']
        dest=OUT/slug;dest.mkdir(exist_ok=True);shutil.copy2(p/'assets/icon.png',dest/'icon.png');shutil.copy2(p/'LICENSE',dest/'license.txt')
        archive=f'{slug}-{m["version"]}.zip'
        cards.append(f'''<article class="card"><img src="{slug}/icon.png" width="70" height="70" alt=""><p class="tag">{tags[slug]}</p><h3>{title}</h3><p>{E(i['shortDescription'])}.</p><ul>{''.join('<li>'+x+'</li>' for x in features[slug])}</ul><div class="links"><a href="{slug}/">Explore plugin ↗</a><a href="downloads/{archive}">Download ZIP ↓</a></div></article>''')
        cmds={'comfy-story-planner':'python scripts/planner.py storyboard examples/film-plan.json','worldzero-lab':'python scripts/lab.py --seeds 17 --policies forager experimenter --decisions 20','heimdall-policy-lab':'python scripts/policy_lab.py lint examples/tool-policy.json'}
        prompts=''.join('<p class="prompt">“'+E(x)+'”</p>' for x in i['defaultPrompt'])
        body=f'''<div class="page-hero reveal"><img src="icon.png" alt="" width="85" height="85"><p class="eyebrow">{tags[slug]} · v{m['version']}</p><h1>{title}</h1><p class="lead">{E(i['longDescription'])}</p><div class="actions"><a class="button" href="../downloads/{archive}">Download plugin ZIP ↓</a><a class="button secondary" href="https://github.com/skishore23/research-plugins/tree/main/plugins/{slug}">Inspect source ↗</a></div><p class="small">Free · {m['license']} · Publisher: Kishore Shimikeri</p></div><section class="two-col"><div><p class="eyebrow">Start a conversation</p><h2>Try a concrete task.</h2>{prompts}</div><div><p class="eyebrow">Run the included example</p><h2>Inspect the result.</h2><p>Extract the ZIP and open its plugin folder. Use Python 3.11 or newer with file and shell access.</p>{'<pre>python -m venv .venv\n.venv/bin/python -m pip install -r requirements.txt</pre><p class="small">Use the virtual environment’s Python for the command below. Installation downloads dependencies. On Windows, use .venv/Scripts/python.</p>' if (p/'requirements.txt').exists() else '<p>No third-party Python dependencies.</p>'}<pre>{E(cmds[slug])}</pre><p class="notice">This is a portable skills package. Directory publication is pending; downloading a ZIP does not install it in every ChatGPT host. If the host cannot execute Python, results must remain marked “not run.”</p></div></section><section><h2>Scope and documentation</h2><p>{E((p/'references'/next(x.name for x in (p/'references').glob('*contract.md'))).read_text().split('\n\n')[1])}</p><nav><a href="guide.html">Workflow guide</a><a href="privacy.html">Privacy</a><a href="terms.html">Terms</a><a href="support.html">Support</a><a href="license.txt">License</a></nav></section>'''
        (dest/'index.html').write_text(page(title,body,'../'))
        for source,target in [('PRIVACY.md','privacy'),('TERMS.md','terms'),('SUPPORT.md','support')]:
            (dest/(target+'.html')).write_text(page(title+' — '+target,'<article class="prose">'+md((p/source).read_text())+'</article>','../'))
        contract=next((p/'references').glob('*contract.md'))
        (dest/'guide.html').write_text(page(title+' guide','<article class="prose">'+md(contract.read_text())+'</article>','../'))
    result=json.loads((ROOT/'site/worldzero-example.json').read_text())
    worldrows=''.join(f'<tr><td>{row["policy"]}</td><td>{row["result"]["decisions"]}</td><td>{row["result"]["energy"]:.3f}</td><td>{row["result"]["status"]}</td><td>{"Verified" if row["replay"]["verified"] else "Failed"}</td></tr>' for row in result['runs'])
    shutil.copy2(ROOT/'site/worldzero-example.json',OUT/'worldzero-example.json')
    shutil.copy2(ROOT/'plugins/comfy-story-planner/examples/film-plan.json',OUT/'film-plan.json')
    body='''<div class="hero"><div class="reveal"><p class="eyebrow">From open-source projects to useful conversations</p><h1>Make something.<br>Then <em>check it.</em></h1><p class="lead">Three focused plugins for planning films, studying agents, and inspecting policies. Real tools, readable evidence, and the source behind every result.</p><div class="actions"><a class="button" href="#plugins">Explore the collection ↓</a><a class="button secondary" href="#lab">Try the examples</a></div><p class="small">Free, open-source skills packages · Directory publication pending</p></div><div class="diagram" aria-hidden="true"><svg viewBox="0 0 500 500"><circle cx="250" cy="250" r="170" fill="none" stroke="#c5cdbb"/><circle cx="250" cy="250" r="110" fill="none" stroke="#c5cdbb" stroke-dasharray="3 9"/><path d="M90 250H410M250 90V410" stroke="#d5d9cc"/><g class="orbit"><circle cx="250" cy="80" r="37" fill="#b64127"/><path d="M236 69h28v22h-28zM242 72v16M258 72v16" fill="none" stroke="#f5f2e9" stroke-width="2"/></g><g class="orbit reverse"><circle cx="250" cy="360" r="30" fill="#07535d"/><circle cx="250" cy="360" r="13" fill="none" stroke="#f5f2e9" stroke-width="2"/><circle cx="250" cy="360" r="4" fill="#f5f2e9"/></g><circle cx="250" cy="250" r="53" fill="#172d2b"/><path d="M226 250l16 16 33-34" fill="none" stroke="#e3eebc" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="396" cy="337" r="9" fill="#174dab"/></svg><span class="diagram-label">Create · Experiment · Inspect</span></div></div><div class="rule"><span><strong>03</strong> focused workflows</span><span><strong>23</strong> passing regression tests</span><span><strong>0</strong> publisher data uploads</span></div><section id="plugins"><div class="section-head"><div><p class="eyebrow">The first collection</p><h2>A small tool.<br>A complete workflow.</h2></div><p>Each plugin pairs instructions with executable code extracted or derived from an existing project. Choose the one that fits your next task.</p></div><div class="cards">'''+''.join(cards)+'''</div></section><section id="lab"><p class="eyebrow">A closer look</p><h2>See what “checked” means.</h2><p class="lead">Explore the boundaries as well as the happy path.</p><div class="lab"><div class="tabs" aria-label="Example selector"><button data-tab="film" aria-pressed="true">Film continuity</button><button data-tab="world" aria-pressed="false">Agent experiments</button><button data-tab="policy" aria-pressed="false">Policy structure</button></div><div class="panel" data-panel="film"><h3>Who has the key?</h3><p>A three-shot film needs more than three prompts. Each shot must start from a state the previous shots established.</p><div class="timeline"><div class="shot"><span>00:00—00:04</span><strong>The offer</strong><p>Mira holds the key.</p></div><div class="shot"><span>00:04—00:08</span><strong>The handoff</strong><p id="owner">Jo receives the key</p></div><div class="shot"><span>00:08—00:12</span><strong>The departure</strong><p>Jo uses the key to open the gate.</p></div></div><button class="demo-action" id="break-continuity" aria-pressed="false">Remove the handoff</button><p class="result" id="continuity-result" aria-live="polite">Plan passes: ownership changes from Mira to Jo before the gate is opened. Three shots total exactly 12 seconds.</p><p class="small">Interactive explanation of the tested continuity case. Full validation runs in the Python plugin. <a href="film-plan.json">Download the actual plan ↗</a></p></div><div class="panel" data-panel="world" hidden><h3>Repeat the experiment.</h3><p>Recorded output from the packaged WorldZero kernel: seed 17, two policies, 20 decisions each. Both traces were replayed successfully.</p><div class="table-wrap"><table><thead><tr><th>Policy</th><th>Decisions</th><th>Energy</th><th>Outcome</th><th>Replay</th></tr></thead><tbody>'''+worldrows+'''</tbody></table></div><p class="result">Both episodes reached the decision budget. A censored run does not establish completed survival, causal discovery or model quality.</p><p class="small">This is recorded evidence, not a live browser simulation. <a href="worldzero-example.json">Inspect output and trace digests ↗</a></p></div><div class="panel" data-panel="policy" hidden><h3>Catch the mistake before deployment.</h3><pre>"guards": [{
  "id": "tools.allowlist",
  "target": "tool_calls",
  "with": { "allowed_tools": ["read_story", "plan_shots"] }
}],
"compose": { "root": "tools_allowlist" }</pre><p class="result">The complete bundled example passes schema and static composition checks. A misspelled “allowed_toolz” parameter is rejected. A fail-open setting produces a warning.</p><p class="small">The lint tool does not intercept requests or verify runtime behavior. <a href="heimdall-policy-lab/">Explore the policy workflow ↗</a></p></div></div></section><section class="two-col" id="start"><div><p class="eyebrow">Bring your own question</p><h2>From a prompt<br>to an inspectable artifact.</h2><p class="lead">The result should be something you can read, rerun, and improve.</p></div><ol class="steps"><li>Download one plugin and inspect its source.</li><li>Load it in a compatible skills host with file and shell access.</li><li>Install the documented Python dependencies when needed.</li><li>Ask a starter question, then keep the output and evidence.</li></ol></section><section><div class="section-head"><div><p class="eyebrow">Part of a larger body of work</p><h2>Built from working projects.</h2></div><p>The collection grew from a review of 51 repositories. Read the public project triage and the reasoning behind this first batch.</p></div><nav><a href="research.html">Read the research ↗</a><a href="https://skishore23.github.io/worldzero/">WorldZero browser demo ↗</a><a href="https://github.com/skishore23/polysignal/pull/9">PolySignal Research work ↗</a></nav></section>'''
    (OUT/'index.html').write_text(page('Make something. Then check it.',body))
    (OUT/'research.html').write_text(page('Project research','<article class="prose">'+md((ROOT/'docs-research.md').read_text())+'</article>'))
    print('Built static site:',OUT)
if __name__=='__main__':build()
