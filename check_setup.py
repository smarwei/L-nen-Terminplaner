#!/usr/bin/env python3
"""
Check if the project setup is complete and ready for CI/CD
"""

import os
import sys
from pathlib import Path

def check_file(file_path, description):
    """Check if a file exists and print status"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (FEHLT)")
        return False

def check_directory(dir_path, description):
    """Check if a directory exists and print status"""
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        print(f"✅ {description}: {dir_path}/")
        return True
    else:
        print(f"❌ {description}: {dir_path}/ (FEHLT)")
        return False

def check_file_content(file_path, required_content, description):
    """Check if a file contains required content"""
    if not os.path.exists(file_path):
        print(f"❌ {description}: {file_path} (DATEI FEHLT)")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if required_content in content:
                print(f"✅ {description}: {file_path}")
                return True
            else:
                print(f"❌ {description}: {file_path} (INHALT FEHLT)")
                return False
    except Exception as e:
        print(f"❌ {description}: {file_path} (FEHLER: {e})")
        return False

def main():
    print("🔍 Lünen Terminplaner - Setup Check")
    print("=" * 40)
    
    all_good = True
    
    # Core application files
    print("\n📦 Core Application Files:")
    all_good &= check_file('app.py', 'Flask App')
    all_good &= check_file('scraper.py', 'Web Scraper')
    all_good &= check_file('pdf_processor.py', 'PDF Processor')
    all_good &= check_file('export_manager.py', 'Export Manager')
    all_good &= check_file('requirements.txt', 'Python Dependencies')
    
    # Templates and static files
    print("\n🎨 Templates & UI:")
    all_good &= check_directory('templates', 'HTML Templates')
    all_good &= check_file('templates/index.html', 'Main Template')
    all_good &= check_file('templates/meeting_detail.html', 'Detail Template')
    
    # Working directories
    print("\n📁 Working Directories:")
    all_good &= check_directory('downloads', 'PDF Downloads')
    all_good &= check_directory('exports', 'Export Files')
    all_good &= check_file('downloads/.gitkeep', 'Downloads gitkeep')
    all_good &= check_file('exports/.gitkeep', 'Exports gitkeep')
    
    # Documentation
    print("\n📖 Documentation:")
    all_good &= check_file('README.md', 'Main README')
    all_good &= check_file('spezifikation.md', 'Project Specification')
    all_good &= check_file('CI_CD_SETUP.md', 'CI/CD Documentation')
    
    # Git and CI/CD setup
    print("\n🔧 Git & CI/CD Setup:")
    all_good &= check_file('.gitignore', 'Git Ignore File')
    all_good &= check_directory('.github', 'GitHub Directory')
    all_good &= check_directory('.github/workflows', 'GitHub Workflows')
    all_good &= check_file('.github/workflows/build-releases.yml', 'Release Workflow')
    all_good &= check_file('.github/workflows/test-and-build.yml', 'Test Workflow')
    
    # Check .gitignore content
    print("\n🚫 .gitignore Content Check:")
    all_good &= check_file_content('.gitignore', '*.exe', 'Ignores EXE files')
    all_good &= check_file_content('.gitignore', '*.AppImage', 'Ignores AppImage files')
    all_good &= check_file_content('.gitignore', 'dist/', 'Ignores dist directory')
    all_good &= check_file_content('.gitignore', 'downloads/*.pdf', 'Ignores PDF downloads')
    
    # Check workflow content
    print("\n⚙️ Workflow Content Check:")
    all_good &= check_file_content('.github/workflows/build-releases.yml', 'pyinstaller', 'Contains PyInstaller build')
    all_good &= check_file_content('.github/workflows/build-releases.yml', 'AppImage', 'Contains AppImage build')
    all_good &= check_file_content('.github/workflows/build-releases.yml', 'windows-latest', 'Windows build job')
    all_good &= check_file_content('.github/workflows/build-releases.yml', 'ubuntu-latest', 'Linux build job')
    
    # Test files
    print("\n🧪 Test Setup:")
    all_good &= check_directory('tests', 'Tests Directory')
    all_good &= check_file('pytest.ini', 'Pytest Config')
    all_good &= check_file('local_build_test.py', 'Local Build Test')
    
    # Build files (created by build scripts)
    print("\n🏗️ Build Files (Optional):")
    check_file('main.py', 'Main Entry Point (auto-generated)')
    check_file('luenen_terminplaner.spec', 'PyInstaller Spec (auto-generated)')
    
    # Summary
    print("\n" + "=" * 40)
    if all_good:
        print("🎉 SETUP VOLLSTÄNDIG!")
        print("\n✅ Bereit für:")
        print("   • Git Commits")
        print("   • GitHub Push")
        print("   • Automatische Builds")
        print("   • Release Creation")
        
        print("\n🚀 Nächste Schritte:")
        print("   1. git add .")
        print("   2. git commit -m 'Complete CI/CD setup'")
        print("   3. git push origin main")
        print("   4. git tag v1.0.0")
        print("   5. git push origin v1.0.0")
        print("   6. 🎊 Automatische Builds starten!")
        
    else:
        print("❌ SETUP UNVOLLSTÄNDIG!")
        print("\n💡 Fehlende Dateien müssen erstellt werden.")
        print("   Führen Sie die Build-Scripts erneut aus.")
    
    print(f"\n📊 Status: {('READY' if all_good else 'INCOMPLETE')}")
    return 0 if all_good else 1

if __name__ == '__main__':
    sys.exit(main())