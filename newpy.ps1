param (
    [string]$ProjectName
)

if (-not $ProjectName) {
    Write-Host "Usage: newpy ProjectName"
    exit
}

# Create project folder
mkdir $ProjectName
cd $ProjectName

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install pygame automatically
python -m pip install --upgrade pip
python -m pip install pygame

# Create project structure
mkdir assets
mkdir sounds
New-Item main.py -ItemType File
New-Item requirements.txt -ItemType File
New-Item README.md -ItemType File

# Add starter Pygame code to main.py
Set-Content main.py @"
import pygame
import sys

# Initialize pygame
pygame.init()

# Window settings
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('$ProjectName')

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill screen with color (R, G, B)
    screen.fill((30, 30, 60))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
"@

Write-Host "Project $ProjectName created successfully!"
Write-Host "Virtual environment activated and pygame installed."
Write-Host "Starter Pygame window is ready in main.py!" 