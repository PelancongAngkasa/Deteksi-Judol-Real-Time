@echo off
setlocal enabledelayedexpansion

:: Color setup (requires Windows 10 or later with ANSI support)
cls

echo.
echo =====================================================================
echo      ^!^! Deteksi Judol Online - Setup ^& Deploy Script [Windows]
echo =====================================================================
echo.

:: Check Python installation
echo [*] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python is not installed or not in PATH
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VER=%%i
echo [OK] %PYTHON_VER% found
echo.

:: Check Docker installation
echo [*] Checking Docker installation...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [!] Docker not found (optional)
) else (
    for /f "tokens=*" %%i in ('docker --version') do set DOCKER_VER=%%i
    echo [OK] !DOCKER_VER! found
)
echo.

:: Create virtual environment
echo [*] Creating Python virtual environment...
if not exist "venv\" (
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [!] Virtual environment already exists
)
echo.

:: Activate venv
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

:: Upgrade pip
echo [*] Upgrading pip...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
echo [OK] Pip upgraded
echo.

:: Install dependencies
echo [*] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [X] Failed to install dependencies
    exit /b 1
)
echo [OK] Dependencies installed successfully
echo.

:: Check list_web.txt
echo [*] Checking list_web.txt...
if not exist "list_web.txt" (
    echo [!] Creating example list_web.txt...
    (
        echo https://www.pertanian.go.id/
        echo https://csirt.pertanian.go.id/
        echo https://ditjenpkh.pertanian.go.id/
    ) > list_web.txt
    echo [OK] Example list_web.txt created
) else (
    for /f "usebackq" %%A in (`find /c /v "" ^< list_web.txt`) do set LINES=%%A
    echo [OK] list_web.txt found with !LINES! URLs
)
echo.

:: Create scan_results directory
echo [*] Creating results directory...
if not exist "scan_results\" mkdir scan_results
echo [OK] Results directory ready
echo.

:: Run tests
echo [*] Running tests...
echo.
python test_detection.py
echo.

echo =====================================================================
echo [OK] Setup completed successfully!
echo =====================================================================
echo.

echo [i] Next steps:
echo     1. Run scanner:
echo        python deteksi_judol.py
echo.
echo     2. Run Streamlit app:
echo        streamlit run app.py
echo.
echo     3. Deploy with Docker:
echo        docker-compose up
echo.

:: Optional Docker setup
set /p DOCKER_SETUP="[?] Do you want to setup Docker compose? (y/n): "
if /i "%DOCKER_SETUP%"=="y" (
    echo.
    echo [*] Setting up Docker...
    
    docker --version >nul 2>&1
    if errorlevel 1 (
        echo [X] Docker is not installed
    ) else (
        echo [*] Building Docker image...
        docker build -t judol-detector .
        
        if errorlevel 1 (
            echo [X] Failed to build Docker image
        ) else (
            echo [OK] Docker image built successfully
            echo.
            
            set /p START_CONTAINER="[?] Start Docker container now? (y/n): "
            if /i "!START_CONTAINER!"=="y" (
                echo [*] Starting Docker container...
                docker-compose up -d
                echo [OK] Container started
                echo [i] Access the app at http://localhost:8501
            )
        )
    )
)

echo.
echo [OK] Setup complete! Happy scanning! [Shield]
echo.
pause
