const {chromium}=require('playwright');const fs=require('fs');
const font=fs.readFileSync('node_modules/@fontsource/gloock/files/gloock-latin-400-normal.woff2').toString('base64');
const C='#3b1d3a';
// nón lá: cone tilted, apex up-left, rim stripe
const hat=`<svg class="hat" viewBox="0 0 120 60"><g transform="rotate(-4 60 40)">
<path d="M4 44 L52 6 Q56 3 60 6 L116 40 Q60 58 4 44 Z" fill="${C}"/>
<path d="M10 42 Q60 52 110 39" stroke="#f3e9c6" stroke-width="2.4" fill="none" opacity=".55"/>
<path d="M30 28 Q62 34 92 27" stroke="#f3e9c6" stroke-width="1.6" fill="none" opacity=".35"/>
</g></svg>`;
const acute=`<svg class="ac" viewBox="0 0 40 60"><path d="M6 58 Q8 40 24 4 Q30 0 36 4 Q30 30 12 58 Z" fill="${C}"/></svg>`;
const E=`<span class="e">e${hat}${acute}</span>`;
const html=(bg)=>`<style>@font-face{font-family:G;src:url(data:font/woff2;base64,${font})}
html,body{margin:0;background:${bg}}#w{display:inline-block;padding:160px 120px 120px}
.t{font-family:G;font-size:400px;color:${C};line-height:1;white-space:nowrap;letter-spacing:-4px}
.e{position:relative;display:inline-block}
.hat{position:absolute;width:175px;left:8px;top:40px}
.ac{position:absolute;width:40px;left:182px;top:20px}
.sp{display:inline-block;width:70px}</style>
<div id="w"><div class="t">B${E}p<span class="sp"></span>N${E}p</div></div>`;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:2600,height:900}});
for(const [n,bg] of [['bep-nep-logo-transparent.png','transparent'],['bep-nep-logo-cream.png','#f3e9c6']]){
await p.setContent(html(bg));await p.waitForTimeout(300);await p.locator('#w').screenshot({path:n,omitBackground:bg==='transparent'});}
await b.close()})();
