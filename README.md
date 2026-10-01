# Virtual Crosshair

A sleek, premium, and lightweight crosshair overlay app for Windows, built with Python and PyQt6.

note that the crosshair (as far as i tested) was NOT detected by anticheats but not too sure, use it at your own risks

## Features

- **Transparent Overlay**: High-performance, click-through crosshair that stays on top of all windows.
- **Customizable**: Adjust shape, size, color, thickness, and opacity.
- **Premium UI**: Modern dark-themed settings dashboard.
- **System Tray Integration**: Run in the background and access settings via the system tray.
- **Multi-Monitor Ready**: Automatically centers on the primary screen and handles resolution changes.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/lucykamerad/Windows-VirtualCrosshair.git
   cd Windows-VirtualCrosshair
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application**:
   ```bash
   python main.py
   ```
2. **Configure**: Use the settings window to customize your crosshair.
3. **Minimize**: Closing the settings window will hide it to the system tray.
4. **Exit**: Right-click the system tray icon and select "Exit App" or use the "Exit App" button in settings.

## Configuration

Standard configuration is stored in `crosshair_config.json`. This file is created automatically on the first run.

## License

MIT License - feel free to use and modify for your own projects!
