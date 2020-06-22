Write-Host "$(skipLogTime)"

#Configurations

$WorkspaceId = "$(WorkspaceId)"
$PrimaryKey = "$(PrimaryKey)"
$LogType = "$(LogType)"
$CurrentTime = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
# Create log entiry for starting or ending time.
$json = @"
[
  {
    "DeploymentID": "$(Release.DeploymentID)",
    "ReleaseName": "$(Release.DefinitionName)",
    "AgentName": "$(Agent.Name)",
    "Time":"$CurrentTime",
    "Action":"$(Action)",
    "StoreName": "$(StoreName)"
  }
]
"@

# Create the function to create the authorization signature
Function Build-Signature ($workspaceId, $sharedKey, $date, $contentLength, $method, $contentType, $resource)
{
    $xHeaders = "x-ms-date:" + $date
    $stringToHash = $method + "`n" + $contentLength + "`n" + $contentType + "`n" +
    $xHeaders + "`n" + $resource
    $bytesToHash = [Text.Encoding]::UTF8.GetBytes($stringToHash)
    $keyBytes = [Convert]::FromBase64String($sharedKey)
    $sha256 = New-Object System.Security.Cryptography.HMACSHA256
    $sha256.Key = $keyBytes
    $calculatedHash = $sha256.ComputeHash($bytesToHash)
    $encodedHash = [Convert]::ToBase64String($calculatedHash)
    $authorization = 'SharedKey {0}:{1}' -f $workspaceId,$encodedHash
    return $authorization
}

# Create the function to create and post the request
Function Post-LogAnalyticsData($workspaceId, $primaryKey, $body, $logType)
{
    $method = "POST"
    $contentType = "application/json"
    $resource = "/api/logs"
    $rfc1123date = [DateTime]::UtcNow.ToString("r")
    $contentLength = $body.Length
    $signature = Build-Signature `
        -workspaceId $workspaceId `
        -sharedKey $primaryKey `
        -date $rfc1123date `
        -contentLength $contentLength `
        -method $method `
        -contentType $contentType `
        -resource $resource
    $uri = "https://" + $workspaceId + ".ods.opinsights.azure.com" + $resource + "?api-version=2016-04-01"

    $headers = @{
        "Authorization" = $signature;
        "Log-Type" = $logType;
        "x-ms-date" = $rfc1123date;
    }

    $response = Invoke-WebRequest -Uri $uri -Method $method -ContentType $contentType -Headers $headers -Body $body -UseBasicParsing
    return $response.StatusCode
}

# Submit the data to the API endpoint
Post-LogAnalyticsData -WorkspaceId $WorkspaceId -PrimaryKey $PrimaryKey -body ([System.Text.Encoding]::UTF8.GetBytes($json)) -logType $logType