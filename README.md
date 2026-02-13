# CLI Server

A lightweight, command-line based file server built with Flask for serving files over your local network or WAN. Designed specifically for easy file transfers using tools like `wget` and `curl`.

## Overview

CLI Server is a simple HTTP file server that allows you to quickly share files from your local machine over the network. It features optional HTTP Basic Authentication to secure your files and is particularly useful for transferring files between machines on the same network or over the internet.

### Key Features

-  **Simple Setup** - Start serving files with a single command
-  **Optional Authentication** - Built-in HTTP Basic Authentication support
-  **Network Accessible** - Binds to all network interfaces (0.0.0.0) for easy access
-  **Directory Traversal Protection** - Prevents access to files outside the base directory
-  **Configurable** - Customizable password or no-password mode
-  **wget Compatible** - Designed to work seamlessly with wget and curl

## Installation

1. Clone or download this repository:
```bash
git clone <repository-url>
cd cli_server
```

2. Create a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate  # On Windows
```

3. Install the required dependencies:
```bash
pip install flask flask-httpauth werkzeug
```

## Usage

### Basic Usage

Start the server with default settings (password: "dingus"):
```bash
python main.py
```

The server will start on `http://0.0.0.0:8888` and serve files from the current working directory.

### Command-Line Arguments

#### Custom Password

Set a custom password for authentication:
```bash
python main.py --password mysecretpass
# or using short form
python main.py -ps mysecretpass
```

#### Disable Authentication

Run the server without any authentication (use with caution):
```bash
python main.py --no-password
# or using short form
python main.py -no
```

## Accessing Files

Once the server is running, you can access your files from any device on the network.

### Finding Your Server IP

Get your local IP address:
```bash
# Linux/Mac
ip addr show | grep inet
# or
ifconfig | grep inet

# Windows
ipconfig
```

### Downloading Files with wget

**With Authentication (default):**
```bash
# Download a single file
wget --user=any --password=dingus http://SERVER_IP:8888/path/to/file.txt

# Download with custom password
wget --user=any --password=mysecretpass http://SERVER_IP:8888/file.pdf

# Recursive directory download
wget -r --user=any --password=dingus http://SERVER_IP:8888/directory/
```

**Without Authentication:**
```bash
# If server started with --no-password
wget http://SERVER_IP:8888/path/to/file.txt
```

### Downloading Files with curl

**With Authentication:**
```bash
# Download a single file
curl -u any:dingus http://SERVER_IP:8888/path/to/file.txt -O

# With custom password
curl -u any:mysecretpass http://SERVER_IP:8888/file.pdf -O
```

**Without Authentication:**
```bash
curl http://SERVER_IP:8888/path/to/file.txt -O
```

## Examples

### Example 1: Share Files on Local Network

1. Start the server on your computer:
```bash
python main.py --password myfiles123
```

2. On another device, download files:
```bash
wget --user=any --password=myfiles123 http://192.168.1.100:8888/document.pdf
```

### Example 2: Transfer Files Between Servers

1. On the source server (10.0.0.5):
```bash
cd /data/backups
python main.py --password backup2024
```

2. On the destination server:
```bash
wget --user=any --password=backup2024 http://10.0.0.5:8888/database_backup.sql
```

### Example 3: Quick Public Share (Caution!)

For quick, temporary file sharing without authentication:
```bash
python main.py --no-password
```

Then share: `http://YOUR_IP:8888/filename.ext`

⚠️ **Warning:** Only use `--no-password` on trusted networks!

## Security Considerations

1. **Password Protection**: Always use a strong password when serving files over untrusted networks
2. **Directory Traversal**: The server has built-in protection against directory traversal attacks
3. **Network Exposure**: The server binds to `0.0.0.0`, making it accessible from all network interfaces
4. **Firewall**: Consider using firewall rules to restrict access to specific IP addresses
5. **HTTPS**: This server uses HTTP, not HTTPS. Avoid transmitting sensitive data over public networks
6. **Temporary Use**: This server is designed for temporary file transfers, not production use

## Building Executable (Optional)

The project includes a `main.spec` file for building a standalone executable using PyInstaller:

```bash
pip install pyinstaller
pyinstaller main.spec
```

The executable will be in the `dist/` directory.

## Troubleshooting

### Port Already in Use
If port 8888 is already in use, you can modify the port in [main.py](main.py#L57) (line 57).

### Connection Refused
- Ensure your firewall allows connections on port 8888
- Check that the server is running and listening on `0.0.0.0:8888`
- Verify you're using the correct IP address

### Authentication Failed
- Double-check your password
- The username can be anything when using HTTP Basic Auth (e.g., "any", "user", etc.)
- Ensure the server has authentication enabled (not started with `--no-password`)

## Technical Details

- **Framework**: Flask
- **Authentication**: HTTP Basic Auth (username ignored, password validated)
- **Port**: 8888
- **Host**: 0.0.0.0 (all interfaces)
- **Base Directory**: Current working directory where the script is executed

## License

This project is provided as-is for personal and educational use.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.