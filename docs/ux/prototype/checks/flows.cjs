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
    focus(){}, setAttribute(){}, click(){},
  });
  return elements.get(id);
};
const context = vm.createContext({
  document: {getElementById: element, addEventListener(){}, querySelector(){return null}},
  location: {reload(){}}, setInterval(){return 1}, clearInterval(){}, setTimeout(){},
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
assert.ok(!/(fetch\(|XMLHttpRequest|localStorage|sessionStorage|getUserMedia|https?:\/\/)/.test(script));
console.log('PASS: 20 screen renders; low-risk save; clarification; mileage validation; correction undo; duplicate; offline retry; sourced answer; escaping; Back; no network or media APIs. Browser/device QA NOT RUN.');
