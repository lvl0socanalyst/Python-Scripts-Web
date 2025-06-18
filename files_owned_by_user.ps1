# Ask user for input
$user = Read-Host "Enter the username to search for (e.g., MYPC\walter)"
$path = Read-Host "Enter the directory to scan (e.g., C:\Windows)"
$outputPath = Read-Host "Enter txt file name"

Write-Host "`nScanning files in $path owned by '$user'..." -ForegroundColor Cyan

# Initialize array for matching files
$matches = @()

# Search for files
Get-ChildItem -Path $path -Recurse -Force -ErrorAction SilentlyContinue |
ForEach-Object {
    try {
        $owner = (Get-Acl $_.FullName).Owner
        if ($owner -eq $user) {
            $matches += $_.FullName
        }
    } catch {
        # Ignore errors (e.g., permission denied)
    }
}

# Save results
if ($matches.Count -eq 0) {
    "No files found owned by '$user'." | Out-File -FilePath $outputPath
    Write-Host "`nNo files found. Output written to: $outputPath" -ForegroundColor Yellow
} else {
    $matches | Out-File -FilePath $outputPath -Encoding UTF8
    Write-Host "`nFound $($matches.Count) files. Output written to: $outputPath" -ForegroundColor Green
}
