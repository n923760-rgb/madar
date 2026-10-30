// Logic-only regression checks. This stub does not qualify DOM/browser/device behavior.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync(require('node:path').join(__dirname, '../index.html'), 'utf8');
const script = source.match(/<script>([\s\S]*?)<\/script>/)[1];
const elements = new Map();
const element = id => {
  if (!elements.has(id)) elements.set(id, {
    value: '', textContent: '', innerHTML: '', dataset: {}, style: {},
    classList: {add(){}, remove(){}, toggle(){return true}},
    focus(){}, setAttribute(){}, click(){}, listeners:{},
    addEventListener(type, handler){this.listeners[type]=handler},
    setPointerCapture(){}, insertAdjacentHTML(){},
  });
  return elements.get(id);
};
const context = vm.createContext({
  document: {getElementById: element, addEventListener(){}, querySelector(){return null}, querySelectorAll(){return []}},
  location: {reload(){}}, setInterval(){return 1}, clearInterval(){}, setTimeout(){}, clearTimeout(){},
});
vm.runInContext(script, context);
const run = expression => vm.runInContext(expression, context);
const route = () => run('state.route');
const screen = () => element('screen').innerHTML;
assert.equal(route(), 'home');
for (const screenName of ['welcome','onboarding','home','expanded','voice','file','processing','clarify','saved','inbox','calendar','things','timeline','ask','settings','asset','source','edit','text','privacy']) {
  run(`move('${screenName}')`);
  assert.ok(screen().length > 40, screenName);
  assert.ok(!screen().includes('undefined'), screenName);
}
run("state.scenario='reminder';move('processing');act('finish-processing')");
assert.equal(route(), 'saved', 'clear low-risk capture bypasses clarification');
run("act('undo')");
assert.equal(run('state.saved'), null);
run("state.scenario='oil';move('processing');act('finish-processing')");
assert.equal(route(), 'clarify');
element('odometer').value = '-1';
run("act('confirm-detail')");
assert.equal(route(), 'clarify', 'invalid odometer stays unresolved');
element('odometer').value = '86000';
run("act('confirm-detail')");
assert.equal(route(), 'saved');
assert.ok(run('state.saved.next').includes('91,000'));
run("act('source-oil');act('edit-source')");
element('correction').value = 'العداد 86,500 كم';
run("act('save-correction')");
assert.equal(run('state.revision'), true);
run("act('undo')");
assert.equal(run('state.revision'), false);
assert.ok(run('state.saved.detail').includes('86,000'));
run("act('duplicate');act('existing')");
assert.equal(route(), 'asset');
assert.equal(run('state.duplicate'), false);
run("act('fail-processing');act('offline');act('retry')");
assert.equal(route(), 'inbox', 'offline retry must not pretend to process');
run("act('online');act('retry')");
assert.equal(route(), 'processing');
run("move('ask');act('ask-example')");
assert.equal(run('state.answer'), true);
assert.ok(screen().includes('عرض المصدر'));
run("state.transcript='<img src=x onerror=alert(1)>';move('processing')");
assert.ok(screen().includes('&lt;img'));
assert.ok(!screen().includes('<img src=x'));
run("move('home');move('things');back()");
assert.equal(route(), 'home');
// Exercise the same controller that the Home pointer/keyboard handlers bind.
let pending;context.setTimeout=fn=>{pending=fn;return 1};context.clearTimeout=()=>{pending=null};
run("var events=[];var c=holdController({reset(){events.push('reset')},listen(){events.push('listen')},cancelHint(v){events.push(v?'cancel-zone':'recording')},cancelled(){events.push('cancel')},send(){events.push('send')},navigate(r){events.push(r)},hint(){events.push('hint')}})");
const tick=()=>{const fn=pending;pending=null;if(fn)fn()};
for(const [x,y,d] of [[100,0,'things'],[-100,0,'inbox'],[0,-100,'calendar'],[0,100,'ask']]){run(`events=[];c.down(0,0);c.move(${x},${y});c.up(${x},${y})`);assert.equal(run('events.at(-1)'),d);tick();assert.ok(!run("events.includes('listen')"));}
run('events=[];c.down(0,0)');tick();assert.equal(run('c.active'),true);run('c.up(0,0)');assert.equal(run("events.filter(e=>e==='send').length"),1);run('c.up(0,0)');assert.equal(run("events.filter(e=>e==='send').length"),1);
run('events=[];c.down(0,0);c.up(0,0)');tick();assert.ok(!run("events.includes('send')||events.includes('listen')"));
run('events=[];c.down(0,0)');tick();run('c.move(0,-100);c.up(0,-100)');assert.ok(run("events.includes('cancel')&&!events.includes('send')&&!events.includes('calendar')"));
run('events=[];c.down(0,0)');tick();run('c.cancel();c.up(0,0)');assert.ok(!run("events.includes('send')"));
run('events=[];c.down(0,0)');tick();run('c.move(0,-100);c.move(0,0);c.up(0,0)');assert.ok(run("events.includes('send')"));
run("move('home');$('orb').onpointerdown({clientX:0,clientY:0,pointerId:1,isPrimary:true,button:0})");tick();run("$('orb').onpointerup({clientX:0,clientY:0,preventDefault(){}})");assert.equal(route(),'processing');
assert.ok(!/(fetch\(|XMLHttpRequest|localStorage|sessionStorage|getUserMedia|https?:\/\/)/.test(script));
console.log('PASS: 20 templates and fixture journeys; hold threshold/release-once; four fast swipes; short tap; slide cancel and return; OS cancellation; actual Home release to processing. Node DOM stub only.');
