---
name: camoufox-setup
description: Set up an interactive CamoFox browser on Windows or WSL with pnpm, uBlock Origin, and a website whitelist when explicitly requested.
---

# Set up CamoFox

Create a usable browser installation, a visible window when requested, and local agent access. Preserve the selected platform and existing browser profiles. Read [whitelist guidance](references/whitelist.md) when configuring allowed websites.

## Select the installation

- Inspect existing installations before installing another copy. Identify the package, package version, native browser version, launcher, and configuration owner.
- Prefer `@askjo/camofox-browser` from [Jo](https://github.com/jo-inc/camofox-browser) for an interactive desktop on Windows or Linux. The separate [redfox package](https://github.com/redf0x1/camofox-browser), `camofox-browser`, has different launch options and platform support. Check its current documentation before selecting it for a visible Windows window.
- Use current official package documentation and installed source to establish supported environment variables and API routes. Pin the selected version in the installation project and retain the lockfile. Do not transfer configuration between the two packages without checking it.
- Use a dedicated installation directory and browser profile. Install with pnpm when available or requested. Approve only the required dependency build scripts through the configuration supported by the installed pnpm version. Native SQLite dependencies can require a compiler and Python.

## Choose the platform

On Windows, run the Windows Node.js executable and install the Windows browser binary. Use native paths in PowerShell. Keep background server windows hidden. Show the browser window when the user needs to interact with it.

On WSL, run Linux Node.js and install the Linux browser binary inside the distribution. Use Linux paths. Check `DISPLAY`, `WAYLAND_DISPLAY`, and WSLg availability before selecting desktop mode. WSLg can show a browser window on the Windows desktop. If it is unavailable, use a documented display or remote desktop option that fits the requested interaction.

Keep server and browser processes in the same selected environment. Check actual localhost connectivity before connecting a Windows client to a WSL server. Do not assume a particular WSL networking mode. Add bubblewrap or another sandbox only when requested or needed for the agreed scope.

## Configure local access and protection

1. Bind the browser API to loopback. Create a private random access key and configure the package's authentication mechanism. Keep the key out of command output, URLs, and committed files.
2. Select a persistent profile and dedicated paths for downloads and runtime data. Let the user sign in through the browser when needed.
3. Enable uBlock Origin through the browser's supported add-on mechanism. Check the extension manifest and launch configuration. Its Firefox extension ID is `uBlock0@raymondhill.net`.
4. Configure the website whitelist using the reference. Retain existing vendor policies. Use the real browser installation directory, not a temporary executable symlink directory.
5. Keep launch and stop commands for the selected environment. Stop through the authenticated browser API when available, then stop the owned server process. Preserve unrelated processes.

## Complete the setup

Start the service and open a visible blank tab when desktop interaction was requested. Confirm startup from the process and API response. If startup fails, inspect its logs and report the specific failure.

If the wrapper rejects an unknown fingerprint property, compare its generated configuration with the installed browser's `properties.json` and supported version pair. Keep configuration validation enabled. Apply a compatibility change only to the affected fields, or install a compatible pair. Do not make a past version workaround a permanent rule for future releases.

Provide the installation location, start and stop commands, whitelist location, and invocation method for the browser controller. Distinguish configured protection from observed behavior. Run behavioral checks only when requested or required by applicable instructions.
