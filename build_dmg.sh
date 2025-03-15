#!/bin/bash
# Script to build the application and create a DMG

# Version management
VERSION="1.0.0"
DMG_NAME="PomodoroLab-${VERSION}.dmg"

echo "🔄 Building PomodoroLab version ${VERSION}"
echo "🧹 Cleaning previous builds and caches..."
rm -rf build dist .eggs *.egg-info
rm -f "${DMG_NAME}"  # Remove previous DMG if exists

# Clean macOS caches that might affect the app
defaults delete com.arturylab.pomodorolab 2>/dev/null || true

# Build the application
python3 setup.py py2app

# Verify if the build was successful
if [ ! -d "dist/PomodoroLab.app" ]; then
    echo "❌ Error: Application build failed"
    exit 1
fi

echo "✅ Application built successfully"
echo "📦 Creating DMG..."

# Create the DMG
create-dmg \
  --volname "PomodoroLab ${VERSION}" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "PomodoroLab.app" 175 190 \
  --hide-extension "PomodoroLab.app" \
  --app-drop-link 425 190 \
  "${DMG_NAME}" \
  "dist/PomodoroLab.app"

echo "✅ DMG created successfully: ${DMG_NAME}"

# Clean up build directories after DMG creation
echo "🧹 Cleaning up build directories..."
rm -rf build dist
echo "✅ Cleanup complete"
