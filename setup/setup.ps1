# PowerShell script to set up a virtual environment and install dependencies

$envName = ".venv"

# Create a virtual environment
python -m venv $envName

# Activate the virtual environment
& "$envName\Scripts\Activate.ps1"

# Install dependencies from requirements.txt
pip install -r requirements.txt

Write-Host "Setup complete! Virtual environment created and dependencies installed."