param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$PassThru
)

if (Test-Path .env) {
    Get-Content .env | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith('#') -or $line.IndexOf('=') -lt 0) { return }
        $parts = $line.Split('=', 2)
        $name = $parts[0].Trim()
        $value = $parts[1].Trim().Trim('"').Trim("'")
        if (-not [string]::IsNullOrWhiteSpace($name) -and -not [Environment]::GetEnvironmentVariable($name)) {
            [Environment]::SetEnvironmentVariable($name, $value)
        }
    }
}

if (-not $env:OMNIROUTE_BASE_URL) { $env:OMNIROUTE_BASE_URL = 'http://localhost:20128/v1' }
if (-not $env:OMNIROUTE_API_KEY) { $env:OMNIROUTE_API_KEY = '' }
if (-not $env:OMNIROUTE_MODEL) { $env:OMNIROUTE_MODEL = 'auto/best-fast' }
if (-not $env:OMNIROUTE_API_PATH) { $env:OMNIROUTE_API_PATH = '/chat/completions' }

$env:ANTHROPIC_BASE_URL = $env:OMNIROUTE_BASE_URL
$env:ANTHROPIC_API_KEY = $env:OMNIROUTE_API_KEY
$env:ANTHROPIC_MODEL = $env:OMNIROUTE_MODEL
$env:OPENAI_BASE_URL = $env:OMNIROUTE_BASE_URL
$env:OPENAI_API_KEY = $env:OMNIROUTE_API_KEY
$env:OPENAI_MODEL = $env:OMNIROUTE_MODEL

$npmBin = Join-Path $env:APPDATA 'npm'
if (Test-Path $npmBin) {
    $env:Path = "$npmBin;$env:Path"
}

$claudeCommand = $null
$claudeCandidates = @('claude', 'claude.exe', 'claude.cmd')
foreach ($candidate in $claudeCandidates) {
    $claudeCommand = Get-Command $candidate -ErrorAction SilentlyContinue
    if ($claudeCommand) { break }
}

if (-not $claudeCommand) {
    Write-Error "Claude Code CLI was not found on PATH. Install Claude Code or add its executable to PATH, then rerun this script."
    exit 1
}

& $claudeCommand.Source @PassThru
exit $LASTEXITCODE
