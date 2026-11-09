param([ValidateSet('encrypt','decrypt')][string]$Mode)
$ErrorActionPreference = 'Stop'
try {
    Add-Type -AssemblyName System.Security
    $inputBytes = [Convert]::FromBase64String([Console]::In.ReadToEnd())
    $scope = [System.Security.Cryptography.DataProtectionScope]::CurrentUser
    if ($Mode -eq 'encrypt') {
        $outputBytes = [System.Security.Cryptography.ProtectedData]::Protect($inputBytes, $null, $scope)
    } else {
        $outputBytes = [System.Security.Cryptography.ProtectedData]::Unprotect($inputBytes, $null, $scope)
    }
    [Console]::Out.Write([Convert]::ToBase64String($outputBytes))
} catch {
    [Console]::Error.Write('Windows credential protection failed.')
    exit 1
}
