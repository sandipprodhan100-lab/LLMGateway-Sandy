# LLMGateway-Sandy

This repository now includes a minimal VS Code-ready scaffold for connecting to an OmniRoute-compatible LLM gateway.

## What was added

- A sample environment file at [.env.example](.env.example)
- A Python probe script at [connect_omniroute.py](connect_omniroute.py)
- VS Code workspace settings at [.vscode/settings.json](.vscode/settings.json)

## Quick start

1. Copy [.env.example](.env.example) to `.env`.
2. Keep the base URL as `http://localhost:20128/v1` for your local OmniRoute endpoint.
3. If your gateway requires auth, add the key in `OMNIROUTE_API_KEY`.
4. Run the probe:

```powershell
python .\connect_omniroute.py
```

## Claude Code via OmniRoute

This repo no longer uses wrapper scripts for Claude Code. Configure your Claude client or the Claude CLI to use OmniRoute directly by setting the appropriate gateway environment variables.

### For Claude client / GUI

Set these environment variables in your shell or inside the Claude interface if it supports custom gateway settings:

```powershell
$env:OMNIROUTE_BASE_URL = 'http://localhost:20128/v1'
$env:OMNIROUTE_API_KEY = '<your-key-if-required>'
$env:OMNIROUTE_MODEL = 'auto/best-fast'
$env:OMNIROUTE_API_PATH = '/chat/completions'
```

### For Claude CLI (route through OmniRoute without Anthropic login)

Use `--bare` so the CLI relies only on the `ANTHROPIC_*` environment variables and does not read the Anthropic keychain/OAuth login.

```powershell
$env:ANTHROPIC_BASE_URL = 'http://localhost:20128/v1'
$env:ANTHROPIC_API_KEY = '<your-omniroute-key>'
$env:ANTHROPIC_MODEL = 'auto/best-fast'
claude --bare
```

If you want to keep the same `.env` style settings, export both the `OMNIROUTE_*` and `ANTHROPIC_*` values, since the Claude CLI reads `ANTHROPIC_*`.

## Environment variables

- `OMNIROUTE_BASE_URL`
- `OMNIROUTE_API_KEY`
- `OMNIROUTE_MODEL`
- `OMNIROUTE_API_PATH`

## Expected behavior

The probe makes a POST request to the OpenAI-style chat completions endpoint and prints the model response when the gateway is reachable.

## Notes

- Do not commit real API keys or `.env` files.
- Keep secrets in local environment variables or a private `.env` file that is ignored by Git.