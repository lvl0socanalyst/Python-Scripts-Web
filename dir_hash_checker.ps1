$dir = Read-Host "dir path: "

Get-ChildItem -Path $dir -File -Recurse | ForEach-Object {
    $hashie = Get-FileHash $_.FullName -Algorithm SHA256
    [PSCustomObject]@{
        FileName = $_.Name
        Hash     = $hashie.Hash
    }
} | Format-Table -AutoSize

# TO RUN
# powershell -ExecutionPolicy Bypass -File .\dir_file_hashes.ps1
