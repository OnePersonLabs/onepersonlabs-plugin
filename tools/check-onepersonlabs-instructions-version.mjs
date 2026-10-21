#!/usr/bin/env node

import { execFileSync, spawnSync } from 'node:child_process'

const path = 'plugins/onepersonlabs/AGENTS.md'

function git(...args) {
  return execFileSync('git', args, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] })
}

function hasHead() {
  return spawnSync('git', ['rev-parse', '--verify', 'HEAD'], { stdio: 'ignore' }).status === 0
}

function normalize(text) {
  return text.replace(/^\uFEFF/, '').replace(/\r\n/g, '\n')
}

function version(text, { allowMissing = false, previous = false } = {}) {
  const markerName = previous ? '[a-z][a-z0-9-]*-instructions-version' : 'onepersonlabs-instructions-version'
  const occurrences = [...text.matchAll(new RegExp(markerName, 'g'))]
  if (allowMissing && occurrences.length === 0) return null
  const markers = [...text.matchAll(new RegExp(`^<!-- ${markerName}: ([1-9]\\d*) -->$`, 'gm'))]
  if (occurrences.length !== 1 || markers.length !== 1) {
    throw new Error('OnePersonLabs AGENTS.md must contain exactly one valid <!-- onepersonlabs-instructions-version: N --> marker with a positive integer revision.')
  }
  return { value: BigInt(markers[0][1]), marker: markers[0][0] }
}

try {
  const stagedChanges = git('diff', '--cached', '--name-only', '--', path).trim()
  if (stagedChanges) {
    if (!git('ls-files', '--stage', '--', path).trim()) {
      throw new Error('OnePersonLabs AGENTS.md is deleted from the index. Restore and stage the versioned instruction file before committing.')
    }
    const staged = normalize(git('show', `:${path}`))
    const stagedVersion = version(staged)
    const existingHead = hasHead()
    // Follow the staged rename so a package rename retains its instruction
    // revision instead of being mistaken for first-time version adoption.
    const renamed = existingHead ? git('diff', '--cached', '--name-status', '--find-renames', '--diff-filter=R')
      .trim().split('\n').map((line) => line.split('\t')).find((fields) => fields[2] === path) : undefined
    const previousPath = renamed?.[1] ?? path
    const previousEntry = existingHead ? git('ls-tree', 'HEAD', '--', previousPath).trim() : ''
    const previous = previousEntry ? normalize(git('show', `HEAD:${previousPath}`)) : ''
    const previousVersion = version(previous, { allowMissing: true, previous: true })
    if (!previousVersion) {
      if (existingHead && stagedVersion.value !== 1n) throw new Error('Initial OnePersonLabs instruction version adoption must use revision 1.')
    } else {
      if (stagedVersion.value < previousVersion.value) throw new Error('OnePersonLabs instruction revision must not decrease. Restore or increment the revision, stage the file, and retry.')
      const changedContent = staged.replace(stagedVersion.marker, '') !== previous.replace(previousVersion.marker, '')
      if (changedContent && stagedVersion.value <= previousVersion.value) {
        throw new Error(`Instruction content changed without a staged revision bump. Increment to at least ${previousVersion.value + 1n}, stage only the intended changes, and retry.`)
      }
    }
  }
} catch (error) {
  const detail = error.stderr?.toString().trim()
  process.stderr.write(`${detail || error.message}\n`)
  process.exitCode = 1
}
