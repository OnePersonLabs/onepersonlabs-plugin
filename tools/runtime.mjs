import process from 'node:process'
import { codexCommand } from '../plugins/onepersonlabs/skills/refresh-local-plugins/scripts/codex-command.mjs'

export { codexCommand }

export function pythonBin(env = process.env, platform = process.platform) {
  return env.PYTHON_BIN || (platform === 'win32' ? 'python' : 'python3')
}
