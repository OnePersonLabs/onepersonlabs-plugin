import assert from 'node:assert/strict'
import { execFileSync, spawnSync } from 'node:child_process'
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'
import test from 'node:test'

const guard = fileURLToPath(new URL('../../../tools/check-opl-instructions-version.mjs', import.meta.url))
const instructionPath = 'plugins/opl/AGENTS.md'
const instructions = (revision, body = '# Instructions\n') => `<!-- opl-instructions-version: ${revision} -->\n${body}`

function check(t, { before = instructions(1), staged, working }) {
  const root = mkdtempSync(join(tmpdir(), 'opl-version-'))
  t.after(() => rmSync(root, { recursive: true, force: true }))
  const git = (...args) => execFileSync('git', args, { cwd: root, stdio: 'pipe' })
  git('init', '--quiet')
  git('config', 'user.name', 'Test')
  git('config', 'user.email', 'test@example.invalid')
  git('config', 'core.autocrlf', 'false')
  mkdirSync(join(root, 'plugins', 'opl'), { recursive: true })
  writeFileSync(join(root, instructionPath), before)
  git('add', instructionPath)
  git('-c', 'core.hooksPath=/dev/null', 'commit', '--quiet', '-m', 'baseline')
  if (staged === null) {
    git('rm', instructionPath)
  } else if (staged !== undefined) {
    writeFileSync(join(root, instructionPath), staged)
    git('add', instructionPath)
  } else {
    writeFileSync(join(root, 'unrelated.txt'), 'unrelated')
    git('add', 'unrelated.txt')
  }
  if (working !== undefined) writeFileSync(join(root, instructionPath), working)
  const indexBefore = git('write-tree').toString().trim()
  const workBefore = staged === null ? null : readFileSync(join(root, instructionPath))
  const result = spawnSync(process.execPath, [guard], { cwd: root, encoding: 'utf8' })
  assert.equal(git('write-tree').toString().trim(), indexBefore, 'validation must preserve the index')
  if (workBefore !== null) assert.deepEqual(readFileSync(join(root, instructionPath)), workBefore, 'validation must preserve working edits')
  return result
}

test('accepts a staged revision bump with instruction changes', (t) => {
  assert.equal(check(t, { staged: instructions(2, '# Updated\n') }).status, 0)
})

test('accepts an inherited revision in an unborn repository', (t) => {
  const root = mkdtempSync(join(tmpdir(), 'opl-extraction-version-'))
  t.after(() => rmSync(root, { recursive: true, force: true }))
  const git = (...args) => execFileSync('git', args, { cwd: root, stdio: 'pipe' })
  git('init', '--quiet')
  mkdirSync(join(root, 'plugins', 'opl'), { recursive: true })
  writeFileSync(join(root, instructionPath), instructions(10))
  git('add', instructionPath)
  const result = spawnSync(process.execPath, [guard], { cwd: root, encoding: 'utf8' })
  assert.equal(result.status, 0, result.stderr)
})

test('rejects an unstaged revision bump without staging working edits', (t) => {
  const result = check(t, { staged: instructions(1, '# Updated\n'), working: instructions(2, '# Updated\n') })
  assert.equal(result.status, 1)
  assert.match(result.stderr, /staged revision bump/u)
})

test('unrelated staged changes do not inspect an unstaged instruction edit', (t) => {
  assert.equal(check(t, { working: 'invalid local work' }).status, 0)
})

test('normalizes BOM and CRLF but rejects unversioned content edits', (t) => {
  assert.equal(check(t, { staged: '\uFEFF' + instructions(1).replaceAll('\n', '\r\n') }).status, 0)
  const result = check(t, { staged: instructions(1, '# Instructions \n'), working: instructions(2, '# Instructions \n') })
  assert.equal(result.status, 1)
  assert.match(result.stderr, /staged revision bump/u)
})

test('accepts initial unversioned adoption only as revision 1', (t) => {
  assert.equal(check(t, { before: '# Previous\n', staged: instructions(1) }).status, 0)
  assert.equal(check(t, { before: '# Previous\n', staged: instructions(2) }).status, 1)
})

test('rejects missing, duplicate, and malformed markers', (t) => {
  for (const staged of ['# Missing\n', instructions(1) + instructions(2), instructions(0), instructions('1.1'), instructions('01'), instructions('-1')]) {
    assert.equal(check(t, { staged }).status, 1, staged)
  }
})

test('rejects a deleted instruction file with an actionable error', (t) => {
  const result = check(t, { staged: null })
  assert.equal(result.status, 1)
  assert.match(result.stderr, /Restore and stage the versioned instruction file/)
})

test('rejects version-only decreases and permits version-only increases', (t) => {
  assert.equal(check(t, { before: instructions(2), staged: instructions(1) }).status, 1)
  assert.equal(check(t, { staged: instructions(2) }).status, 0)
})
