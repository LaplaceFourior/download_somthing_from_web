if (!(Test-Path venv)) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
    Write-Host "Virtual environment created."
} else {
    Write-Host "Virtual environment already exists."
}

Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1
Write-Host "Virtual environment activated."

# Check if required packages are already installed
$required_packages = Get-Content requirements.txt
$installed_packages = pip freeze
$missing_packages = $required_packages | Where-Object { $_ -notin $installed_packages }
if ($missing_packages) {
    Write-Host "Installing required packages..."
    pip install -r requirements/Win.txt
} else {
    Write-Host "Required packages already installed."
}

Write-Host "Packages installed."
Write-Host "Starting application..."

Start-Process python -ArgumentList "${PSScriptRoot}\main.py"