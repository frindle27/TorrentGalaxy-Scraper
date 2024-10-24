# How to Install a qBittorrent Plugin that Uses Third-Party Libraries

You can either use a virtual environment to avoid installing these libraries globally (recommended for advanced users), or install them directly into your main Python environment (recommended for beginners).

## Option 1: Using a Virtual Environment (Recommended for Advanced Users)

**1. Create a virtual environment**
- In the same folder as the `requirements.txt` file, run the following command to create a virtual environment:
```bash
python -m venv venv
```
**2. Activate the virtual environment**
- On Windows, run:
```bash
venv\Scripts\activate.bat
```

- On macOS/Linux, run:
```bash
source venv/bin/activate
```

**3. Install the required libraries**
```bash
pip install -r requirements.txt
```
Here, it is assumed that all the libraries required for the plugin to work are present in `requirements.txt`, as is the case for this plugin.

**4. Create a .bat file to launch qBittorrent with the virtual environment activated**
```bat
@echo off
call .\venv\Scripts\activate.bat
qbittorrent.exe
exit
```
- This script will automatically activate the virtual environment and then launch qBittorrent.
- You can create a shortcut to the .bat file for convenient launching.

**5. Install the plugin**
- Open qBittorrent and navigate to View > Search Engine.
- Click Install a new search plugin, and select the `torrentgalaxy.py` file.
- Your plugin is now installed and should work with the required dependencies.

## Option 2: Install Libraries Globally (Recommended for Beginners)

**1. Install the required libraries**
```bash
pip install -r requirements.txt
```
Here, it is assumed that all libraries required for the plugin to work are present in `requirements.txt`, as is the case for this plugin

**2. Install the plugin**
- Open qBittorrent and navigate to View > Search Engine.
- Click Install a new search plugin, and select the `torrentgalaxy.py` file.
- Your plugin is now installed and should work with the required dependencies.
