#!/bin/bash

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║      🛡️ Deteksi Judol Online - Setup & Deploy Script       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Function untuk print messages
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[i]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check Python installation
print_info "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    exit 1
fi
print_status "Python 3 found: $(python3 --version)"

# Check Docker installation
print_info "Checking Docker installation..."
if command -v docker &> /dev/null; then
    print_status "Docker found: $(docker --version)"
else
    print_warn "Docker not found (optional for containerized deployment)"
fi

# Create virtual environment
print_info "Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_warn "Virtual environment already exists"
fi

# Activate venv
print_info "Activating virtual environment..."
source venv/bin/activate
print_status "Virtual environment activated"

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
print_status "Pip upgraded"

# Install dependencies
print_info "Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    print_status "Dependencies installed successfully"
else
    print_error "Failed to install dependencies"
    exit 1
fi

# Check list_web.txt
print_info "Checking list_web.txt..."
if [ ! -f "list_web.txt" ]; then
    print_error "list_web.txt not found"
    print_info "Creating example list_web.txt..."
    cat > list_web.txt << EOF
https://www.pertanian.go.id/
https://csirt.pertanian.go.id/
https://ditjenpkh.pertanian.go.id/
EOF
    print_status "Example list_web.txt created"
else
    LINES=$(wc -l < list_web.txt)
    print_status "list_web.txt found with $LINES URLs"
fi

# Create scan_results directory
print_info "Creating results directory..."
mkdir -p scan_results
print_status "Results directory ready"

# Run tests
print_info "Running tests..."
echo ""
python3 test_detection.py

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Setup completed successfully!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo ""

print_info "Next steps:"
echo "  1. Run scanner:"
echo "     python3 deteksi_judol.py"
echo ""
echo "  2. Run Streamlit app:"
echo "     streamlit run app.py"
echo ""
echo "  3. Deploy with Docker:"
echo "     docker-compose up"
echo ""

# Option untuk deploy dengan Docker
echo ""
read -p "$(echo -e ${BLUE}Do you want to setup Docker compose? (y/n):${NC} )" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Setting up Docker..."
    
    if command -v docker &> /dev/null; then
        print_info "Building Docker image..."
        docker build -t judol-detector .
        
        if [ $? -eq 0 ]; then
            print_status "Docker image built successfully"
            
            read -p "$(echo -e ${BLUE}Start Docker container now? (y/n):${NC} )" -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                print_info "Starting Docker container..."
                docker-compose up -d
                print_status "Container started"
                print_info "Access the app at http://localhost:8501"
            fi
        else
            print_error "Failed to build Docker image"
        fi
    else
        print_error "Docker is not installed"
    fi
fi

echo ""
print_status "Setup complete! Happy scanning! 🛡️"
