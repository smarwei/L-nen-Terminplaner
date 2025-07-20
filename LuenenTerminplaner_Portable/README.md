# Lünen Terminplaner - Portable Version

## 🚀 Quick Start

### Windows:
1. Double-click `LuenenTerminplaner.bat`
2. Browser opens automatically on http://localhost:5000

### Linux:
1. Run `./LuenenTerminplaner.sh` in terminal
2. Browser opens automatically on http://localhost:5000

## 📦 Installation (Optional)

### Windows Auto-Installation:
1. Double-click `install.bat`
2. Follow the instructions
3. Desktop shortcut will be created

### Manual Installation:
1. Extract all files to a folder
2. Run the launcher from that folder

## 🔧 Requirements

- **Python 3.8+** (Download from https://python.org)
- **Internet connection** (for downloading meeting data)
- **100 MB free space**

## 📋 Features

- ✅ **Meeting Scraper**: Automatically downloads Lünen council meetings
- ✅ **PDF Processing**: Extracts and summarizes meeting documents
- ✅ **Smart Filtering**: Filter by committees and date ranges
- ✅ **Multiple Exports**: Markdown, HTML, PDF, JSON formats
- ✅ **Detail Views**: Comprehensive meeting summaries
- ✅ **Responsive Design**: Works on all screen sizes

## 🎯 Usage

1. **Start the application** (see Quick Start above)
2. **Select date range** for meetings to search
3. **Choose committees** you're interested in
4. **Click "Termine laden"** to search for meetings
5. **Browse results** and view detailed summaries
6. **Export data** in your preferred format

## 🛠️ Troubleshooting

### "Python is not installed"
- Download Python from https://python.org/downloads/
- ⚠️ **Important**: Check "Add Python to PATH" during installation
- Restart computer after installation

### "Dependencies failed to install"
- Run as Administrator (Windows) or with sudo (Linux)
- Check internet connection
- Temporarily disable antivirus/firewall

### "Browser doesn't open automatically"
- Manually open http://localhost:5000 in your browser
- Keep the console window open

### "Port already in use"
- Close other applications using port 5000
- Or edit `main_standalone.py` and change the port number

### "No meetings found"
- Check internet connection
- Try different date ranges
- Select more committees

## 📁 File Structure

```
LuenenTerminplaner/
├── LuenenTerminplaner.bat    # Windows launcher
├── LuenenTerminplaner.sh     # Linux launcher
├── main_standalone.py        # Main application
├── app.py                    # Flask web app
├── scraper.py               # Web scraping logic
├── pdf_processor.py         # PDF processing
├── export_manager.py        # Export functionality
├── requirements_minimal.txt  # Python dependencies
├── templates/               # Web interface
├── downloads/              # PDF cache
└── exports/               # Exported files
```

## 🌐 Web Interface

Once started, the application runs a local web server accessible at:
**http://localhost:5000**

The interface includes:
- Date range selector
- Committee filter checkboxes
- Real-time search progress
- Meeting cards with summaries
- Export buttons for different formats
- Detailed meeting view pages

## 📄 Data Sources

This application extracts data from:
- **Lünen Council Information System** (official public data)
- **Meeting PDFs** for detailed summaries
- **Committee listings** for filtering options

## 🔒 Privacy

- All data processing happens **locally** on your computer
- No data is sent to external servers (except for downloading public meeting data)
- PDF files are cached locally for faster access
- No personal information is collected or stored

## 📞 Support

For technical issues:
1. Check this README for common solutions
2. Verify Python installation: `python --version`
3. Check console output for error messages
4. Ensure internet connectivity for data downloads

## 📈 Version Information

**Version**: 1.0.3  
**Build**: Portable Python Distribution  
**Compatibility**: Windows 10+, Linux (Ubuntu 18.04+)  
**Python**: 3.8+ required  

---

🎉 **Thank you for using Lünen Terminplaner!**

This tool helps make local government more transparent and accessible.
