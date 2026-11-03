$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (!(Test-Path -LiteralPath $python)) { throw 'Ambiente não encontrado. Consulte LEIA-ME.md.' }
try {
    $existing = Invoke-RestMethod -Uri 'http://127.0.0.1:8765/api/status' -TimeoutSec 3
    if ($existing.model -eq 'qwen3:8b') {
        Write-Output 'O GuardKids já está disponível em http://127.0.0.1:8765.'
        exit 0
    }
} catch { }
& $python -m uvicorn app:app --host 127.0.0.1 --port 8765
