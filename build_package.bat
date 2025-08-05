@echo off
REM Build script for CrewAI with ThinkOS integration (Windows)

echo Building CrewAI-ThinkOS Package...

REM Check if we're in the right directory
if not exist "pyproject.toml" (
    echo Error: pyproject.toml not found. Make sure you're in the crewai-thinkos directory.
    exit /b 1
)

REM Clean previous builds
echo Cleaning previous builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"

REM Install build tools if needed
echo Ensuring build tools are installed...
pip install --quiet build wheel

REM Build the package
echo Building package...
python -m build

REM Check if build was successful
if exist dist (
    echo Build successful!
    echo Built packages:
    dir dist
    echo.
    echo To install in ThinkOS, run:
    echo   cd ..\backend
    echo   pip install ..\crewai-thinkos\dist\crewai_thinkos-*.whl
) else (
    echo Build failed. Check for errors above.
    exit /b 1
)