const fs=require('fs'),os=require('os'),path=require('path'),cp=require('child_process');
const root=path.resolve(__dirname,'..'),stage=fs.mkdtempSync(path.join(os.tmpdir(),'essaint-preview-'));
const prepare='C:/Users/admin/.codex/plugins/cache/openai-bundled/sites/0.1.66/skills/sites-hosting/scripts/prepare-site-build.cjs';
cp.execFileSync(process.execPath,[prepare,root,path.join(stage,'dist')],{stdio:'inherit'});
cp.execFileSync('tar',['-C',stage,'-czf',path.join(root,'site-preview.tar.gz'),'dist'],{stdio:'inherit'});
const entries=cp.execFileSync('tar',['-tzf',path.join(root,'site-preview.tar.gz')],{encoding:'utf8'});
if(!entries.includes('dist/.openai/hosting.json')||!entries.includes('dist/index.html'))throw Error('Incomplete preview archive');
console.log('Validated static preview archive.');
