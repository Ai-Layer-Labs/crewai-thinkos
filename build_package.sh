#!/bin/bash
# Build script for CrewAI with ThinkOS integration

echo "🔧 Building CrewAI-ThinkOS Package..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Make sure you're in the crewai-thinkos directory."
    exit 1
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Install build tools if needed
echo "📦 Ensuring build tools are installed..."
pip install --quiet build wheel

# Build the package
echo "🏗️  Building package..."
python -m build

# Check if build was successful
if [ -d "dist" ] && [ -n "$(ls -A dist)" ]; then
    echo "✅ Build successful!"
    echo "📦 Built packages:"
    ls -la dist/
    echo ""
    echo "To install in ThinkOS, run:"
    echo "  cd ../backend"
    echo "  pip install ../crewai-thinkos/dist/crewai_thinkos-*.whl"
else
    echo "❌ Build failed. Check for errors above."
    exit 1
fi