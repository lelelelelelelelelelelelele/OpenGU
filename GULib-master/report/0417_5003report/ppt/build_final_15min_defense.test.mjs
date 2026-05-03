import test from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const scriptPath = path.join(__dirname, 'build_final_15min_defense.js');

function makeOutputDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'defense-deck-test-'));
}

test('build script generates the planned defense deck and companion script', { concurrency: false }, () => {
  const outputDir = makeOutputDir();
  const pptxPath = path.join(outputDir, 'final_15min_defense.pptx');
  const scriptMdPath = path.join(outputDir, 'final_15min_script.md');

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
  assert.match(scriptText, /## Slide 8: Main Finding: Family Spectrum/);
  assert.match(scriptText, /Estimated Time: 1:50/);
  assert.match(scriptText, /## Slide 13: Limitations And Future Work/);
  assert.match(scriptText, /completed MSc project/i);
  assert.match(scriptText, /future work/i);
  assert.doesNotMatch(scriptText, /Next step 1/i);
  assert.doesNotMatch(scriptText, /## Slide 13: Limitations And Next Steps/);

  fs.rmSync(outputDir, { recursive: true, force: true });
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

test('build script rebalances slide 1 thesis block and replaces the cramped single-line roadmap', () => {
  const generatorText = fs.readFileSync(scriptPath, 'utf8');

  assert.match(generatorText, /card\(s,7\.08,1\.3,2\.15,1\.8,'Thesis'/i, 'slide 1 thesis card should be moved down and resized');
  assert.match(generatorText, /\[\['Problem',7\.12,3\.45/i, 'slide 1 should use compact roadmap chips');
  assert.doesNotMatch(generatorText, /Problem -> Method -> Results -> Takeaway/i, 'old single-line roadmap should be removed');
});

test('build script rebalances slide 2 with dedicated layout geometry', () => {
  const generatorText = fs.readFileSync(scriptPath, 'utf8');

  assert.match(generatorText, /const slide2=\{/i, 'slide 2 should use a dedicated layout object');
  assert.match(generatorText, /headline:\{x:\.65,y:\.84,w:6,h:\.58,fontSize:17\.2\}/i, 'slide 2 headline geometry should be compressed');
  assert.match(generatorText, /cards:\{x:\.65,y:1\.48,w:2\.7,h:2\.48,gap:\.3\}/i, 'slide 2 cards should use the rebalanced row geometry');
  assert.match(generatorText, /callout:\{x:7\.18,y:4\.18,w:2\.12,h:\.82\}/i, 'slide 2 callout should be enlarged and aligned');
});

test('build script adds an attack selection logic page between pipeline and metrics', () => {
  const generatorText = fs.readFileSync(scriptPath, 'utf8');

  assert.match(generatorText, /frame\(s,6,'Attack Selection Logic'\)/i, 'generator should insert the attack selection logic page');
  assert.match(generatorText, /TracIn \/ IF-style/i, 'selection logic page should explain model-aware selection');
  assert.match(generatorText, /IM','Graph-structural logic/i, 'selection logic page should explain graph-structural selection');
  assert.match(generatorText, /score\(v\) ≈ I_train\(v\)/i, 'selection logic page should include the IF shorthand formula');
  assert.match(generatorText, /score\(S\) = spread\(S\)/i, 'selection logic page should include the IM shorthand formula');
  assert.match(generatorText, /score\(v\) = α·z_IF\(v\) \+ \(1-α\)·z_IM\(v\)/i, 'selection logic page should include the hybrid shorthand formula');
  assert.match(generatorText, /frame\(s,7,'Metrics Framework'\)/i, 'metrics page should shift after the selection logic page');
});

test('generated script explains the k=5 baseline design on the metrics framework page', { concurrency: false }, () => {
  const outputDir = makeOutputDir();
  const scriptMdPath = path.join(outputDir, 'final_15min_script.md');
  execFileSync(process.execPath, [scriptPath, '--output-dir', outputDir], {
    cwd: path.resolve(__dirname, '..', '..', '..'),
    stdio: 'pipe',
  });

  const scriptText = fs.readFileSync(scriptMdPath, 'utf8');
  assert.match(scriptText, /## Slide 6: Attack Selection Logic/);
  assert.match(scriptText, /## Slide 7: Metrics Framework/);
  assert.match(scriptText, /Structured attacks include TracIn, IM, and Hybrid\./);
  assert.doesNotMatch(scriptText, /IM-v4|Hybrid-v4/);
  assert.match(scriptText, /relative_f1_drop = F1_after\(k=5, random\) - F1_after\(attack\)/i);
  assert.match(scriptText, /use a tiny random-trigger baseline/i);
  assert.match(scriptText, /k equals 5, and use that post-unlearning F1 as the baseline/i);
  assert.match(scriptText, /## Slide 9: Ratio Sensitivity And Ablation/);
  assert.doesNotMatch(scriptText, /## Slide 7: What Was Built In OpenGU/);

  fs.rmSync(outputDir, { recursive: true, force: true });
});

test('generator source encodes the metrics-led results storyline', () => {
  const generatorText = fs.readFileSync(scriptPath, 'utf8');

  assert.match(generatorText, /Metrics Framework/i, 'generator should include the metrics page');
  assert.match(generatorText, /relative_f1_drop = F1_after\(k=5, random\) - F1_after\(attack\)/i, 'generator should encode the k=5 baseline formula');
  assert.match(generatorText, /tiny random-trigger baseline/i, 'generator should explain why the relative metric is needed');
  assert.match(generatorText, /the k=5 relative baseline is the cleaner comparison lens/i, 'generator should defend the shard-based baseline design');
  assert.match(generatorText, /frame\(s,12,'Statistical Support And Effect Size'\)/i, 'generator should move figure 4 into the main body');
  assert.match(generatorText, /frame\(s,15,'Backup Appendix: Full Strategy Spectrum'\)/i, 'generator should move the full figure 3 view to the appendix');
});

test('slide 11 includes a compact collateral evidence table to anchor the attribution logic', { concurrency: false }, () => {
  const outputDir = makeOutputDir();
  const scriptMdPath = path.join(outputDir, 'final_15min_script.md');
  execFileSync(process.execPath, [scriptPath, '--output-dir', outputDir], {
    cwd: path.resolve(__dirname, '..', '..', '..'),
    stdio: 'pipe',
  });

  const generatorText = fs.readFileSync(scriptPath, 'utf8');
  const scriptText = fs.readFileSync(scriptMdPath, 'utf8');

  assert.match(generatorText, /Collateral evidence/i, 'slide 11 should add a small evidence-table header');
  assert.match(generatorText, /Method\s*\|\s*Avg Gap\s*\|\s*Pred Shift \/ Flip/i, 'slide 11 should encode the evidence table columns');
  assert.match(generatorText, /GNNDelete\s*\|\s*9\.74%\s*\|\s*0\.245 \/ 26\.2%/i, 'slide 11 should surface the GNNDelete collateral evidence row');

  assert.match(scriptText, /small evidence table/i, 'speaker notes should acknowledge the new evidence table');
  assert.match(scriptText, /GNNDelete also has the largest retrain gap and the strongest retained-node disturbance/i, 'speaker notes should explain how to read the table');

  fs.rmSync(outputDir, { recursive: true, force: true });
});

test('generated pptx does not keep content-type overrides for missing parts', { concurrency: false }, () => {
  const outputDir = makeOutputDir();
  const pptxPath = path.join(outputDir, 'final_15min_defense.pptx');
  const unpackDir = path.join(outputDir, 'unpacked');
  const zipPath = path.join(outputDir, 'final_15min_defense.zip');

  execFileSync(process.execPath, [scriptPath, '--output-dir', outputDir], {
    cwd: path.resolve(__dirname, '..', '..', '..'),
    stdio: 'pipe',
  });

  fs.copyFileSync(pptxPath, zipPath);
  execFileSync('powershell', ['-NoProfile', '-Command', `Expand-Archive -LiteralPath '${zipPath}' -DestinationPath '${unpackDir}' -Force`], {
    cwd: path.resolve(__dirname, '..', '..', '..'),
    stdio: 'pipe',
  });

  const contentTypesPath = path.join(unpackDir, '[Content_Types].xml');
  const xml = fs.readFileSync(contentTypesPath, 'utf8');
  const overrides = [...xml.matchAll(/<Override PartName="([^"]+)" ContentType="([^"]+)"\/>/g)];
  for (const [, partName] of overrides) {
    const rel = partName.replace(/^\//, '').split('/').join(path.sep);
    const fullPath = path.join(unpackDir, rel);
    assert.equal(fs.existsSync(fullPath), true, `override should point to an existing part: ${partName}`);
  }

  fs.rmSync(outputDir, { recursive: true, force: true });
});
