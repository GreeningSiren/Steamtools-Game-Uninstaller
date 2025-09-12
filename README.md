# Steamtools Game Uninstaller

A Python application designed to help users clean up leftover files from games that were cracked using Steamtools but are no longer installed through Steam.

## Description

This tool helps remove residual files left behind by Steamtools-cracked games, specifically:
- `.lua` files in Steam's `stplug-in` directory
- Depot cache files (`.manifest` files) in Steam's `depotcache` directory

The application provides a user-friendly GUI to select games and safely remove associated files.

## Features

- **Game Discovery**: Automatically finds all games that have Steamtools files
- **Steam API Integration**: Fetches real game names from Steam's API for better identification
- **User-Friendly Interface**: Simple GUI built with Tkinter
- **File Preview**: Shows exactly which files will be deleted before confirmation

## Requirements

- Python 3.6+
- Windows OS (designed for Steam on Windows)
- Steam installed in default location

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd steamtools-uninstaller
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running from Source
```bash
python main.py
```

### Using the Executable
Simply run `Steamtools Game Uninstaller.exe`

### How to Use

1. **Find Games**: Click "Find Games" to scan for Steamtools-related files
2. **Select Game**: Choose a game from the list
3. **Find Files**: Click "Find Files" to see what will be deleted
4. **Delete Files**: Click "Delete All Files" to remove the selected files

## Building Executable

To create a standalone executable, use the provided build script:

```bash
build.bat
```

Or manually install PyInstaller and run:

```bash
pip install pyinstaller
```

Then run the PyInstaller command:

```bash
pyinstaller main.py -n "Steamtools Game Uninstaller" -y --collect-all pyfiglet -F
```

The executable will be created in the `dist/` directory and automatically copied to the root directory.

## File Structure

```
steamtools-uninstaller/
├── main.py                          # Main application file
├── requirements.txt                 # Python dependencies
├── Steamtools Game Uninstaller.spec # PyInstaller specification
├── build.bat                        # Build script
├── .gitignore                       # Git ignore file
└── README.md                        # This file
```

## How It Works

1. Scans `C:\Program Files (x86)\Steam\config\stplug-in\` for `.lua` files
2. Each `.lua` file represents a game that was processed by Steamtools
3. Parses `.lua` files to extract depot IDs using regex pattern `addappid\((\d+)`
4. Finds corresponding `.manifest` files in `C:\Program Files (x86)\Steam\config\depotcache\`
5. Verifies the game is not currently installed by checking for `appmanifest_{game_id}.acf`
6. Safely removes all associated files

## Safety Features

- **File Preview**: Shows all files that will be deleted before confirmation
- **Error Handling**: Graceful error handling for file operations
- **Steam Restart Warning**: Reminds users to restart Steam after cleanup

## Warnings

⚠️ **Important Warnings**:
- Restart Steam after using this tool to ensure changes take effect
- This tool modifies Steam configuration files - use at your own risk
- Always backup important data before using file deletion tools

## Dependencies

- `requests>=2.25.0` - For Steam API communication
- `pyfiglet>=0.8.0` - For ASCII art banner
- `tkinter` - For GUI (included with Python)

## Credits

Created by **GreeningSiren** and **𝓝1𝓰𝓱𝓽𝓜𝓪𝓻𝓮** (nikola_vslv)

Contact on Discord for more information.

## License

This project is provided as-is for educational and utility purposes. Use at your own risk.

## Troubleshooting

### Common Issues

1. **"No games found"**: 
   - Ensure Steamtools was used previously
   - Check if Steam is installed in the default location

2. **Permission errors**:
   - Run as administrator if needed
   - Ensure Steam is closed during cleanup

3. **API errors**:
   - Check internet connection
   - Steam API might be temporarily unavailable

### File Locations

- Steamtools files: `C:\Program Files (x86)\Steam\config\stplug-in\`
- Depot cache: `C:\Program Files (x86)\Steam\config\depotcache\`
- App manifests: `C:\Program Files (x86)\Steam\steamapps\`
