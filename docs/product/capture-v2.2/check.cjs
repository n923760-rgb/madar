// Specification fixture verifier only. No model, ingestion, storage or production executor.
// Implements only the JSON Schema keywords used by this adjacent schema; fails on others.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const read = name => JSON.parse(fs.readFileSync(path.join(__dirname, name), 'utf8'));
const schema = read('contract.schema.json');
const corpus = read('cases.json');
const fail = message => { throw new Error(message); };
const keywords = new Set(['$schema','$id','type','additionalProperties','required','properties','enum','const','items','minItems','maxItems','minLength']);
function supported(s) {
  for (const key of Object.keys(s)) if (!keywords.has(key)) fail('Unsupported schema keyword: '+key);
  for (const value of Object.values(s.properties || {})) supported(value);
  if (s.items) supported(s.items);
}
function shape(value, s, where='output') {
  const isType = type => type==='null' ? value===null : type==='array' ? Array.isArray(value) : type==='object' ? value!==null && typeof value==='object' && !Array.isArray(value) : type==='integer' ? Number.isSafeInteger(value) : typeof value===type;
  if (s.type && !(Array.isArray(s.type)?s.type:[s.type]).some(isType)) fail(where+': type');
  if ('const' in s && value!==s.const) fail(where+': const');
  if (s.enum && !s.enum.includes(value)) fail(where+': enum');
  if (typeof value==='string' && [...value].length<(s.minLength||0)) fail(where+': empty string');
  if (Array.isArray(value)) {
    if (value.length<(s.minItems||0) || value.length>(s.maxItems??Infinity)) fail(where+': array length');
    value.forEach((v,i)=>shape(v,s.items,where+'['+i+']'));
  } else if (value!==null && typeof value==='object') {
    for (const key of s.required||[]) if (!Object.hasOwn(value,key)) fail(where+': missing '+key);
    for (const [key,v] of Object.entries(value)) {
      if (!Object.hasOwn(s.properties||{},key)) {if (s.additionalProperties===false) fail(where+': unknown '+key);}
      else shape(v,s.properties[key],where+'.'+key);
    }
  }
}
const ints=new Set(['amount_minor','odometer','interval_km','next_odometer','warranty_months']);
const bools=new Set(['all_day','reminder_requested']);
const dateValid = value => /^\d{4}-\d{2}-\d{2}$/.test(value) && new Date(value+'T00:00:00Z').toISOString().slice(0,10)===value;
function verify(output, input) {
  shape(output,schema);
  assert.equal(output.capture_id,input.capture_id,'capture identity');
  const ids=new Set();
  for (const item of output.items) {
    assert.ok(!ids.has(item.item_id),'duplicate item ID');ids.add(item.item_id);
    const fields=new Map();
    for (const field of item.fields) {
      assert.ok(!fields.has(field.key),'duplicate field');fields.set(field.key,field);
      if (field.value!==null) {
        if (ints.has(field.key)) assert.ok(Number.isSafeInteger(field.value)&&field.value>=0,'integer minor units/readings');
        else if (bools.has(field.key)) assert.equal(typeof field.value,'boolean');
        else assert.equal(typeof field.value,'string');
        if (['date','expiry_date'].includes(field.key)) assert.ok(dateValid(field.value),'valid calendar date');
        if (field.key==='time') assert.match(field.value,/^([01]\d|2[0-3]):[0-5]\d$/);
        if (field.key==='currency') assert.match(field.value,/^[A-Z]{3}$/);
        if (field.key==='timezone') assert.doesNotThrow(()=>new Intl.DateTimeFormat('en',{timeZone:field.value}));
        if (field.key==='invoice_route') assert.ok(['expense','asset','document','source_only'].includes(field.value),'supported invoice route');
        if (field.key==='object_resolution') assert.ok(['matched','new_requested','unresolved','none'].includes(field.value),'object resolution');
      }
      if (field.confidence==='missing') {assert.equal(field.value,null);assert.equal(field.evidence.length,0);assert.equal(field.resolver,null);}
      else {
        assert.notEqual(field.value,null,'nonmissing value');
        if (field.confidence==='derived') {
          const result=input.resolver_results.find(r=>r.resolver_id===field.resolver);
          assert.ok(result,'known trusted resolver');assert.deepEqual(field.value,result.value,'matches trusted resolver result');
        } else {assert.ok(field.evidence.length,'source/uncertain field needs evidence');assert.equal(field.resolver,null);}
      }
      for (const evidence of field.evidence) {
        const source=input.sources.find(s=>s.source_id===evidence.source_id);
        assert.ok(source && source.text.includes(evidence.quote),'exact evidence from provided source');
      }
      if (field.key==='object_id'&&field.value!==null) assert.ok(input.authorized_objects.some(o=>o.id===field.value),'authorized object candidate');
    }
    const get=key=>fields.get(key)?.value;
    const requireField=key=>assert.ok(fields.has(key)&&['source','derived'].includes(fields.get(key).confidence)&&get(key)!==null,'ready '+item.intent+' requires '+key);
    if (item.status==='ready') {
      assert.ok(!item.fields.some(f=>['uncertain','missing'].includes(f.confidence)),'ready fields supported');
      if (['task','appointment','reminder','invoice','document','subscription','maintenance','odometer'].includes(item.intent)) requireField('title');
      if (item.intent==='appointment') {requireField('date');if(!get('all_day')){requireField('time');requireField('timezone');}}
      if (get('reminder_requested')===true&&['task','appointment','reminder'].includes(item.intent)) {requireField('date');requireField('time');requireField('timezone');}
      if (get('amount_minor')!==undefined&&get('amount_minor')!==null) requireField('currency');
      if (['maintenance','odometer'].includes(item.intent)) {requireField('object_id');requireField('odometer');}
      if (item.intent==='maintenance'&&get('reminder_requested')) requireField('interval_km');
      if (item.intent==='subscription') requireField('recurrence');
      if (item.intent==='invoice'&&['asset','document'].includes(get('invoice_route'))) {
        if(get('object_resolution')==='matched') requireField('object_id');
        else {assert.equal(get('invoice_route'),'asset');assert.equal(get('object_resolution'),'new_requested');requireField('object_name');}
      }
      if (item.intent==='note') requireField('content');
      if (item.intent==='retrieval') requireField('query');
      if(get('next_odometer')!==undefined) assert.equal(get('next_odometer'),get('odometer')+get('interval_km'),'mileage arithmetic');
    }
  }
  for(const q of output.questions) {
    const item=output.items.find(i=>i.item_id===q.item_id);
    assert.ok(item?.status==='needs_clarification','question target');
    assert.ok(item.fields.some(f=>f.key===q.field&&['uncertain','missing'].includes(f.confidence)),'question only unresolved field');
  }
  const statuses=output.items.map(i=>i.status);
  const intents=output.items.map(i=>i.intent);
  if(output.disposition==='ready') {assert.ok(statuses.every(s=>s==='ready'));assert.equal(output.questions.length,0);assert.ok(!intents.some(i=>['retrieval','correction','restricted','unsupported'].includes(i)));}
  if(output.disposition==='clarify') {assert.ok(statuses.includes('needs_clarification'));assert.ok(output.questions.length);for(const i of output.items.filter(i=>i.status==='needs_clarification')) assert.ok(output.questions.some(q=>q.item_id===i.item_id),'no unresolved item without question');}
  if(output.disposition==='retrieve') {assert.ok(intents.every(i=>i==='retrieval'));assert.equal(output.questions.length,0);}
  if(output.disposition==='keep_source') {assert.ok(statuses.every(s=>s==='source_only'));assert.equal(output.questions.length,0);}
  if(['restricted','unsupported'].includes(output.disposition)) {assert.ok(intents.every(i=>i===output.disposition));assert.ok(statuses.every(s=>s==='blocked'));assert.equal(output.questions.length,0);assert.ok(output.items.every(i=>i.fields.length===0),'do not echo restricted content into fields');}
  assert.ok(!/تم حفظ|تم حجز|بيوصلك التذكير/.test(output.user_message),'proposal must not claim execution');
}
supported(schema);
assert.equal(corpus.data,'synthetic');
assert.equal(new Set(corpus.cases.map(c=>c.id)).size,corpus.cases.length);
for(const c of corpus.cases) verify(c.expected,c.input);
const sample=id=>JSON.parse(JSON.stringify(corpus.cases.find(c=>c.id===id)));
const mutations=[
  ['schema version','task-undated',c=>c.expected.schema_version='wrong'],
  ['capture identity','task-undated',c=>c.expected.capture_id='another-user-capture'],
  ['unknown top-level field','task-undated',c=>c.expected.execute=true],
  ['unknown intent','task-undated',c=>c.expected.items[0].intent='transfer_money'],
  ['unknown field','task-undated',c=>c.expected.items[0].fields[0].key='password'],
  ['unsupported evidence','task-undated',c=>c.expected.items[0].fields[0].evidence[0].quote='not in source'],
  ['wrong source ID','task-undated',c=>c.expected.items[0].fields[0].evidence[0].source_id='other-user-source'],
  ['made-up resolver','task-date-only',c=>c.expected.items[0].fields[1].resolver='invented'],
  ['resolver value mismatch','task-date-only',c=>c.expected.items[0].fields[1].value='2026-11-02'],
  ['float amount','invoice-expense',c=>c.expected.items[0].fields.find(f=>f.key==='amount_minor').value=185.5],
  ['unauthorized object','maintenance-clear',c=>c.expected.items[0].fields.find(f=>f.key==='object_id').value='other-user-car'],
  ['appointment missing time','appointment-no-time',c=>{c.expected.disposition='ready';c.expected.items[0].status='ready';c.expected.questions=[];}],
  ['partial group pretend saved','mixed-group-clarification',c=>c.expected.disposition='ready'],
  ['impossible calendar date','appointment-explicit',c=>c.expected.items[0].fields.find(f=>f.key==='date').value='2026-02-30'],
  ['premature save wording','task-undated',c=>c.expected.user_message='تم حفظها'],
  ['duplicate item IDs','two-independent-tasks',c=>c.expected.items[1].item_id='i1'],
  ['restricted mixed with task','restricted-secret',c=>c.expected.items.push(sample('task-undated').expected.items[0])],
];
for(const [name,id,mutate] of mutations) {const c=sample(id);mutate(c);assert.throws(()=>verify(c.expected,c.input),undefined,name);}
const repo=path.resolve(__dirname,'../../..');
const manifest=JSON.parse(fs.readFileSync(path.join(repo,'docs/references/SOURCE-MANIFEST.json'),'utf8'));
for(const f of manifest.files) assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(repo,f.path))).digest('hex'),f.sha256);
console.log(`PASS: ${corpus.cases.length} golden output fixtures; ${mutations.length} invalid proposals rejected; original reference hashes unchanged.`);
console.log('NOT RUN: model accuracy, actual Arabic/date parsing, audio/OCR, persistence, authorization enforcement, Telegram or reminder delivery. This is a specification check, not a production validator.');
