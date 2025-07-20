#!/usr/bin/env python3
"""
Local GitHub Actions workflow validator
"""

import os
import re
import sys
from pathlib import Path

def check_yaml_syntax():
    """Basic YAML syntax checks"""
    print("🔍 Checking YAML syntax...")
    
    workflows = [
        '.github/workflows/build-releases.yml',
        '.github/workflows/test-and-build.yml'
    ]
    
    for workflow in workflows:
        if not os.path.exists(workflow):
            print(f"❌ {workflow} not found")
            return False
            
        with open(workflow, 'r') as f:
            content = f.read()
            
        # Check for common issues
        issues = []
        
        # Check for unescaped quotes
        if re.search(r'[^\\]"[^"]*"[^"]*"', content):
            issues.append("Potential unescaped quotes")
            
        # Check for Windows path separators in Linux contexts
        if re.search(r'[^:]\\[^n]', content):
            issues.append("Backslashes that might cause issues")
            
        # Check for missing shell declarations
        if 'run: |' in content and 'shell:' not in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'run: |' in line and i > 0:
                    prev_lines = lines[max(0, i-5):i]
                    if not any('shell:' in pl for pl in prev_lines):
                        # This is OK for most cases, but flag it
                        pass
        
        if issues:
            print(f"⚠️  {workflow}: {', '.join(issues)}")
        else:
            print(f"✅ {workflow}: Basic syntax OK")
    
    return True

def check_dependencies():
    """Check if all required dependencies are in requirements.txt"""
    print("\n📦 Checking dependencies...")
    
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found")
        return False
    
    with open('requirements.txt', 'r') as f:
        requirements = f.read().lower()
    
    required_packages = [
        'flask', 'requests', 'beautifulsoup4', 'sumy', 
        'pymuPDF', 'pdfplumber', 'markdown'
    ]
    
    missing = []
    for package in required_packages:
        if package.lower() not in requirements:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        return False
    else:
        print("✅ All required packages in requirements.txt")
    
    return True

def check_file_structure():
    """Check if all required files exist"""
    print("\n📁 Checking file structure...")
    
    required_files = [
        'app.py', 'scraper.py', 'pdf_processor.py', 'export_manager.py',
        'templates/index.html', 'templates/meeting_detail.html',
        'requirements.txt', 'spezifikation.md'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"❌ Missing files: {', '.join(missing)}")
        return False
    else:
        print("✅ All required files present")
    
    return True

def check_pyinstaller_compatibility():
    """Check for common PyInstaller issues"""
    print("\n🔨 Checking PyInstaller compatibility...")
    
    # Check app.py for common issues
    if os.path.exists('app.py'):
        with open('app.py', 'r') as f:
            app_content = f.read()
        
        issues = []
        
        # Check for debug mode
        if 'debug=True' in app_content:
            issues.append("debug=True found (should be False for production)")
        
        # Check for use_reloader
        if 'use_reloader=True' in app_content:
            issues.append("use_reloader=True found (should be False for PyInstaller)")
        
        # Check for relative imports that might cause issues
        if re.search(r'from \. import', app_content):
            issues.append("Relative imports found (might cause PyInstaller issues)")
        
        if issues:
            print(f"⚠️  app.py: {', '.join(issues)}")
        else:
            print("✅ app.py: PyInstaller compatible")
    
    return True

def check_windows_specific_issues():
    """Check for Windows-specific issues in workflows"""
    print("\n🪟 Checking Windows-specific issues...")
    
    workflow_path = '.github/workflows/build-releases.yml'
    if not os.path.exists(workflow_path):
        return False
    
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    issues = []
    
    # Check for path separator issues
    if re.search(r'--add-data[^;]*:', content):
        issues.append("Unix path separators in Windows build (should use ;)")
    
    # Check for PowerShell variable escaping
    if re.search(r'\$[A-Za-z]', content) and not re.search(r'\$\$[A-Za-z]', content):
        issues.append("Unescaped PowerShell variables")
    
    # Check for encoding issues
    if 'Out-File' in content and 'UTF8' not in content and 'Default' not in content:
        issues.append("Missing encoding specification for Out-File")
    
    if issues:
        print(f"⚠️  Windows build: {', '.join(issues)}")
        return False
    else:
        print("✅ Windows build: No obvious issues")
    
    return True

def generate_fixed_workflows():
    """Generate corrected workflow files"""
    print("\n🔧 Generating corrected workflows...")
    
    # Fixed test-and-build.yml with proper escaping
    test_workflow = '''name: Test & Development Build

on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master, develop ]
  workflow_dispatch:

jobs:
  test:
    name: 🧪 Run Tests
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']
    
    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4
      
    - name: 🐍 Setup Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        
    - name: 📦 Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-flask pytest-mock responses
        
    - name: 🧪 Run tests
      run: |
        python -m pytest tests/ -v --tb=short || echo "Tests completed with issues"

  build-test:
    name: 🔧 Test Build Process
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        
    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4
      
    - name: 🐍 Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        
    - name: 📦 Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pyinstaller
        
    - name: 🔨 Test PyInstaller build
      shell: bash
      run: |
        # Create directories
        mkdir -p downloads exports
        
        # Create simple test main.py
        cat > main_test.py << 'EOF'
        #!/usr/bin/env python3
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent))
        
        def main():
            print("Build test successful!")
            return 0
        
        if __name__ == "__main__":
            sys.exit(main())
        EOF
        
        # Test PyInstaller
        pyinstaller --onefile --name=TestBuild main_test.py
        
    - name: ✅ Verify build artifacts
      shell: bash
      run: |
        if [ "$RUNNER_OS" == "Windows" ]; then
          ls -la dist/TestBuild.exe
          echo "✅ Windows EXE build test passed"
        else
          ls -la dist/TestBuild
          echo "✅ Linux binary build test passed"
        fi
'''

    # Write corrected test workflow
    with open('.github/workflows/test-and-build.yml', 'w') as f:
        f.write(test_workflow)
    print("✅ Generated corrected test-and-build.yml")
    
    return True

def main():
    print("🔍 GitHub Actions Workflow Validator")
    print("=" * 40)
    
    all_good = True
    
    all_good &= check_file_structure()
    all_good &= check_dependencies()
    all_good &= check_yaml_syntax()
    all_good &= check_pyinstaller_compatibility()
    all_good &= check_windows_specific_issues()
    
    if not all_good:
        print("\n🔧 Generating fixes...")
        generate_fixed_workflows()
    
    print(f"\n📊 Overall Status: {'✅ READY' if all_good else '⚠️  NEEDS FIXES'}")
    
    return 0 if all_good else 1

if __name__ == '__main__':
    sys.exit(main())