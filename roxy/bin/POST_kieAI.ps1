$api = $env:apiKIEAI_Roxy.Trim()

$headers = @{
    Authorization = "Bearer $api"
}

$prompt = Get-Content ".\prompt.txt" -Raw
$prompt = $prompt -replace '"', '\"'

$body = @{
    model = "nano-banana-2"
    callBackUrl = "https://webhook.site/cd31a6b8-450a-40a6-a8d9-a27c12803edd"
    input = @{
        prompt = "$prompt"
        image_input = @()
        aspect_ratio = "auto"
        resolution = "1K"
        output_format = "png"
    }
} | ConvertTo-Json -Depth 5

$response = Invoke-RestMethod 'https://api.kie.ai/api/v1/jobs/createTask' `
    -Method POST `
    -Headers $headers `
    -ContentType "application/json" `
    -Body $body

$response | ConvertTo-Json -Depth 5