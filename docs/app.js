'use strict';
const tabs = [...document.querySelectorAll('[data-tab]')];
for (const button of tabs) button.addEventListener('click',()=>{
  for(const tab of tabs) tab.setAttribute('aria-pressed',String(tab===button));
  for(const panel of document.querySelectorAll('[data-panel]')) panel.hidden=panel.dataset.panel!==button.dataset.tab;
});
const breakButton=document.querySelector('#break-continuity');
if(breakButton) breakButton.addEventListener('click',()=>{
  const broken=breakButton.getAttribute('aria-pressed')!=='true';
  breakButton.setAttribute('aria-pressed',String(broken));
  breakButton.textContent=broken?'Restore the handoff':'Remove the handoff';
  document.querySelector('#owner').textContent=broken?'Mira still owns the key':'Jo receives the key';
  document.querySelector('#continuity-result').textContent=broken?'Continuity error: departure requires key.owner=Jo, but the planned state still says Mira.':'Plan passes: ownership changes from Mira to Jo before the gate is opened. Three shots total exactly 12 seconds.';
});
