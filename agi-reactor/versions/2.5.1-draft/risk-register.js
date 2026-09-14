// Progressive enhancement: every risk remains in the initial HTML and text exports.
const riskRoot=document.querySelector             ('#ai-safety-risks');
if(riskRoot){
 const search=riskRoot.querySelector                  ('#risk-search') ;
 const domain=riskRoot.querySelector                   ('#risk-domain') ;
 const rows=Array.from(riskRoot.querySelectorAll             ('.risk-row'));
 const groups=Array.from(riskRoot.querySelectorAll             ('tbody[data-risk-group]'));
 const normalize=(value       )=>value.toLocaleLowerCase().normalize('NFKD');
 function filterRisks()     {
  const query=normalize(search.value.trim());let visible=0;
  for(const row of rows){row.hidden=!!((domain.value&&row.dataset.riskDomain!==domain.value)||(query&&!normalize(row.textContent||'').includes(query)));if(!row.hidden)visible++;}
  for(const group of groups)group.hidden=!Array.from(group.querySelectorAll             ('.risk-row')).some(row=>!row.hidden);
  riskRoot .querySelector('#risk-count') .textContent=`${visible} of ${rows.length} risks`;
  (riskRoot .querySelector('#risk-empty')               ).hidden=visible!==0;
 }
 function revealRiskLink()     {
  const target=rows.find(row=>'#'+row.id===location.hash);
  if(target){search.value='';domain.value='';filterRisks();target.scrollIntoView({block:'start'});}
 }
 riskRoot.querySelector('.risk-tools') .addEventListener('submit',event=>event.preventDefault());
 search.addEventListener('input',filterRisks);domain.addEventListener('change',filterRisks);
 riskRoot.querySelector('#risk-reset') .addEventListener('click',()=>{search.value='';domain.value='';filterRisks();search.focus();});
 (riskRoot.querySelector('.risk-tools')               ).hidden=false;
 window.addEventListener('hashchange',revealRiskLink);revealRiskLink();
}
