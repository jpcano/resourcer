#!/usr/bin/env bash

SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_NAME="Resourcer"

# Checks if a command is available in the system
# args: param1 is the command to be checked
# returns: 0 if if command is available, otherwises 1
function commandP() {
    if hash $1 2>/dev/null; then
	return 0;
    else
	return 1;
    fi
}

# Checks if a particular brew package is installed
# args: param1 is the package to be checked
# returns: 0 if if command is available, otherwises 1
function brewPackageP() {
    if brew ls --versions $1 | read REPLY; then
	return 0;
    else
	return 1;
    fi
}

# Checks if a particular pip package is installed
# args: param1 is the package to be checked
# returns: 0 if if command is available, otherwises 1
function pipPackageP() {
    if pip list | grep -F $1 | read REPLY; then
	return 0;
    else
	return 1;
    fi
}

# Install Homebrew and/or PyQT if they are not installed
echo "Checking if brew is installed..."
if commandP "brew"; then
    echo "Checking if PyQt is installed..."
    if !(brewPackageP "pyqt";) then
	echo "Installing PyQt...";
	brew install pyqt
    fi
else
    echo "Installing Brew...";
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    echo "Installing PyQt..."Installing brew
    brew install pyqt
fi

# Install pip and/or google-api-python-client if they are not installed
echo "Checking if pip is installed..."
if commandP "pip"; then
    echo "Checking if google-api-python-client is installed..."
    if !(pipPackageP "google-api-python-client";) then
	echo "Installing google-api-python-client...";
	pip install google-api-python-client
    fi
else
    echo "Installing pip...";
    easy_install pip
    echo "Installing google-api-python-client...";
    pip install google-api-python-client
fi

# Make System Python to use homebrew libraries
mkdir -p ~/Library/Python/2.7/lib/python/site-packages
echo "import site; site.addsitedir('/usr/local/lib/python2.7/site-packages')" > ~/Library/Python/2.7/lib/python/site-packages/homebrew.pth

# Remove old .app if it is installed in Applications directory
if [ -d "/Applications/${APP_NAME}.app" ]; then
    rm -r "/Applications/${APP_NAME}.app";
fi

# Copy the new .app  in Applications directory
cp -r "${SCRIPT_PATH}/${APP_NAME}.app" /Applications
