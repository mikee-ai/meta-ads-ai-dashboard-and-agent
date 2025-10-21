# Meta Ads MCP Agent - Deployment Scripts

This directory contains automated deployment scripts and comprehensive documentation for installing the Meta Ads MCP Agent on Ubuntu servers.

## 🚀 Quick Start

### One-Command Installation (Recommended)

```bash
wget -O - https://raw.githubusercontent.com/mikee-ai/meta-ads-ai-dashboard-and-agent/main/deployment/install-fixed.sh | bash
```

This error-free installer will complete in ~3 minutes with zero errors.

## 📁 Files in This Directory

### Installation Scripts
- **`install-fixed.sh`** ⭐ - **RECOMMENDED** - Error-free installer with all fixes pre-applied
- **`install.sh`** - Standard installer
- **`update.sh`** - Update to newer versions
- **`test-installation.sh`** - Verify installation success

### Documentation
- **`README.md`** - Complete installation guide
- **`QUICKSTART.md`** - 5-minute setup guide
- **`DEPLOYMENT_NOTES.md`** - Technical details and troubleshooting
- **`DEPLOYMENT_SUMMARY.md`** - Executive summary
- **`INDEX.md`** - This file

### Other Files
- **`LICENSE`** - MIT License

## 🎯 What Gets Installed

- Meta Ads MCP Agent v1.0.15
- Python 3.x and pip
- All required dependencies
- Systemd service configuration
- Helper scripts (meta-ads-start, meta-ads-stop, meta-ads-status, meta-ads-logs)

## ✅ All Known Errors Fixed

The `install-fixed.sh` script automatically handles:
- ✅ Missing pip3 installation
- ✅ typing-extensions package conflicts
- ✅ Root user warnings
- ✅ Environment variable warnings
- ✅ File permission issues

## 📋 Post-Installation

After installation, you need to configure authentication:

1. Get your Pipeboard API token from https://pipeboard.co/api-tokens
2. Edit `/root/.meta-ads-mcp.env` and add your token
3. Load the environment: `source /root/.meta-ads-mcp.env`
4. Test: `meta-ads-mcp --version`

## 📚 Documentation

For detailed information, see:
- [Complete Guide](README.md) - Full documentation
- [Quick Start](QUICKSTART.md) - Fast setup
- [Technical Notes](DEPLOYMENT_NOTES.md) - All issues and solutions
- [Summary](DEPLOYMENT_SUMMARY.md) - Overview

## 🆘 Support

- **Repository**: https://github.com/mikee-ai/meta-ads-ai-dashboard-and-agent
- **Official MCP Docs**: https://github.com/pipeboard-co/meta-ads-mcp
- **Discord**: https://discord.gg/pipeboard
- **Email**: support@pipeboard.co

## 🔄 Updating

To update an existing installation:
```bash
cd /root/meta-ads-ai-dashboard-and-agent/deployment
./update.sh
```

## 🧪 Testing

To verify your installation:
```bash
cd /root/meta-ads-ai-dashboard-and-agent/deployment
./test-installation.sh
```

---

**Part of the Meta Ads AI Dashboard and Agent Project**

