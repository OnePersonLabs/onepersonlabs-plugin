import test from 'node:test'
import assert from 'node:assert/strict'
import { execFileSync } from 'node:child_process'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { pythonBin } from '../../../tools/runtime.mjs'
const repositoryRoot = fileURLToPath(new URL('../../../', import.meta.url))
const pluginRoot = join(repositoryRoot, 'plugins', 'onepersonlabs')
function runHookStatus(name, input, env = {}, root = pluginRoot) {
  try {
    const stdout = execFileSync(pythonBin(), ['-B', '-X', 'utf8', join(root, 'scripts', name)], {
      cwd: env.CODEX_PROJECT_DIR ?? pluginRoot,
      env: { ...process.env, NODE_BIN: process.execPath, CODEX_BIN: join(repositoryRoot, 'missing-test-codex'), ...env },
      input: JSON.stringify(input),
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe'],
    })
    return { status: 0, stdout, stderr: '' }
  } catch (error) {
    return {
      status: error.status,
      stdout: error.stdout?.toString() ?? '',
      stderr: error.stderr?.toString() ?? '',
    }
  }
}

test('dangerous shell blocks PowerShell root, home, parent, and glob removals', () => {
  for (const command of [
    'Remove-Item -LiteralPath "C:\\" -Recurse -Force',
    'Remove-Item -LiteralPath $HOME -Recurse -Force',
    'Remove-Item -LiteralPath "..\\shared" -Recurse -Force',
    'Remove-Item -Path "C:\\work\\*" -Recurse -Force',
    'rtk proxy powershell -Command "Remove-Item -LiteralPath $HOME -Recurse"',
    'git push origin main --force',
    'git push -f origin main',
  ]) {
    const result = runHookStatus('codex-dangerous-shell-gate.py', { tool_input: { command } })
    assert.equal(result.status, 2, `${command}\n${result.stderr}`)
  }
})

test('dangerous shell permits explicit repository cleanup in PowerShell', () => {
  const result = runHookStatus('codex-dangerous-shell-gate.py', {
    tool_input: { command: 'Remove-Item -LiteralPath "./build output" -Recurse -Force' },
  })
  assert.equal(result.status, 0, result.stderr)
})
