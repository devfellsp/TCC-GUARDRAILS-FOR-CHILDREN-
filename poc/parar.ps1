$ErrorActionPreference = 'Stop'
$connections = Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort 8765 -State Listen -ErrorAction SilentlyContinue
foreach ($connection in $connections) {
    $serverProcessId = $connection.OwningProcess
    $serverProcess = Get-CimInstance Win32_Process -Filter "ProcessId = $serverProcessId"
    if ($serverProcess.CommandLine -match 'uvicorn app:app.*8765') {
        Stop-Process -Id $serverProcessId
        Write-Output 'GuardKids encerrado.'
    } else {
        throw 'A porta está sendo usada por outro processo; nenhuma alteração foi feita.'
    }
}
