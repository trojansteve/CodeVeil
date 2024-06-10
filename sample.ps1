# This script demonstrates basic PowerShell syntax

# Variables
$serverIP = "192.168.1.100"
$filePath = "C:\Temp\log.txt"
$userName = "admin"

# Function definition
function Get-FileContent {
    param($path)
    $content = Get-Content -Path $path
    return $content
}

# Using cmdlets and variables
Write-Host "Reading file content from: $filePath"
$fileContent = Get-FileContent -path $filePath
Write-Host "File content: $fileContent"

# Conditional statement
if ($serverIP -eq "192.168.1.100") {
    Write-Host "Server IP is set to the default gateway."
}

# Loop structure
for ($i=0; $i -lt 10; $i++) {
    Write-Host "Current count: $i"
}

# Script block
$scriptBlock = {
    param($name)
    Write-Host "Hello, $name!"
}

# Invoking the script block
& $scriptBlock -name $userName
