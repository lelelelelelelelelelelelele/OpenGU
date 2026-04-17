import test from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const scriptPath = path.join(__dirname, 'build_final_15min_defense.js');
const outputDir = path.join(__dirname, 'out-test');
const pptxPath = path.join(outputDir, 'final_15min_defense.pptx');
const scriptMdPath = path.join(outputDir, 'final_15min_script.md');

function cleanup() {
  fs.rmSync(outputDir, { recursive: true, force: true });
}

test('build script generates the planned defense deck and companion script', () => {
  cleanup();

  let buildError;
  try {
    execFileSync(process.execPath, [scriptPath, '--output-dir', outputDir], {
      cwd: path.resolve(__dirname, '..', '..', '..'),
      stdio: 'pipe',
    });
  } catch (error) {
    buildError = error;
  }

  assert.equal(buildError, undefined, buildError?.stderr?.toString() || buildError?.message || 'build failed');
  assert.equal(fs.existsSync(pptxPath), true, 'pptx should be generated');
  assert.equal(fs.existsSync(scriptMdPath), true, 'speech script should be generated');

  const scriptText = fs.readFileSync(scriptMdPath, 'utf8');
  assert.match(scriptText, /# EE5003 Final Presentation Speech Script/);
  assert.match(scriptText, /## Slide 7: Main Finding: Vulnerability Spectrum/);
  assert.match(scriptText, /Estimated Time: 1:40/);
  assert.match(scriptText, /## Slide 12: Limitations And Future Work/);
  assert.match(scriptText, /completed MSc project/i);
  assert.match(scriptText, /future work/i);
  assert.doesNotMatch(scriptText, /Next step 1/i);
  assert.doesNotMatch(scriptText, /## Slide 12: Limitations And Next Steps/);
});

test('build script uses the approved navy-led palette instead of the old maroon-gold theme', () => {
  const generatorText = fs.readFileSync(scriptPath, 'utf8');

  assert.doesNotMatch(generatorText, /7C1730/i, 'old maroon primary should be removed');
  assert.doesNotMatch(generatorText, /4C0E1C/i, 'old dark maroon should be removed');
  assert.doesNotMatch(generatorText, /C8A96B/i, 'old gold accent should be removed');

  assert.match(generatorText, /223A5E/i, 'new navy primary should be present');
  assert.match(generatorText, /16263F/i, 'new dark navy should be present');
  assert.match(generatorText, /A6404B/i, 'new red accent should be present');
});

test('build script uses Times New Roman throughout the deck typography', () => {
  const generatorText = fs.readFileSync(scriptPath, 'utf8');

  assert.match(generatorText, /Times New Roman/i, 'Times New Roman should be present');
  assert.doesNotMatch(generatorText, /Georgia/i, 'legacy heading font should be removed');
  assert.doesNotMatch(generatorText, /Calibri/i, 'legacy body font should be removed');
});

test('build script rebalances slide 2 with dedicated layout geometry', () => {
  const generatorText = fs.readFileSync(scriptPath, 'utf8');

  assert.match(generatorText, /const slide2=\{/i, 'slide 2 should use a dedicated layout object');
  assert.match(generatorText, /headline:\{x:\.65,y:\.84,w:6,h:\.58,fontSize:17\.2\}/i, 'slide 2 headline geometry should be compressed');
  assert.match(generatorText, /cards:\{x:\.65,y:1\.48,w:2\.7,h:2\.48,gap:\.3\}/i, 'slide 2 cards should use the rebalanced row geometry');
  assert.match(generatorText, /callout:\{x:7\.18,y:4\.18,w:2\.12,h:\.82\}/i, 'slide 2 callout should be enlarged and aligned');
});
