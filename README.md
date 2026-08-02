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

## Claude Code launchers

You can launch Claude Code through the gateway from either shell:

```powershell
.\claude-omniroute.ps1
```

or:

```cmd
claude-omniroute.cmd
```

These wrappers set the gateway environment so Claude Code will route through the local OmniRoute server.

## Environment variables

- `OMNIROUTE_BASE_URL`
- `OMNIROUTE_API_KEY`
- `OMNIROUTE_MODEL`
- `OMNIROUTE_API_PATH`

## Expected behavior

The probe makes a POST request to the OpenAI-style chat completions endpoint and prints the model response when the gateway is reachable.