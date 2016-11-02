#!/usr/bin/env bash

APPNAME="Resourcer";
VERSION=$(cat VERSION)
DISTNAME="${APPNAME}-v${VERSION}"

DIST_DIR="build/${DISTNAME}"
CONTENTS="${DIST_DIR}/${APPNAME}.app/Contents";
MACOS="${CONTENTS}/MacOS"
RESOURCES="${CONTENTS}/Resources"
RESOURCER="${MACOS}/rsc/"

# Remove build dir if needed
if [ -d "build/" ]; then
    rm -r "build/"
fi;

# Create .app directory tree
mkdir -p "${CONTENTS}";
mkdir -p "${MACOS}";
mkdir -p "${RESOURCES}";

mkdir -p "${MACOS}/ui";
mkdir -p "${MACOS}/share";
mkdir -p "${RESOURCER}";

cp share/Info.plist "${CONTENTS}";

# Copy the bash script that will serve as the entry point of the app
cp share/run_dist.sh "${MACOS}/${APPNAME}";
chmod +x "${MACOS}/${APPNAME}";

# Create resources for the app
cp share/group-512.png.icns "${RESOURCES}";

# ui files
cp ui/mainwindow.ui "${MACOS}/ui";

# client secret
cp share/CLIENTSECRET.json "${MACOS}/share";

# Version
cp VERSION "${MACOS}";

# Create the main files for the app
cd resourcer

cp resourcer.py "../${RESOURCER}";
# chmod +x "../${RESOURCER}/resourcer.py";
cp bigquery.py "../${RESOURCER}";
cp countries.py "../${RESOURCER}";
cp queries.py "../${RESOURCER}";
cp resourcer.py "../${RESOURCER}";
cp srcdplayground.py "../${RESOURCER}";
cp srcdrest.py "../${RESOURCER}";

cd ..

cp share/install-update-resourcer.sh ${DIST_DIR}

# zip package to be distributes
cd "build"; zip -r "${DISTNAME}.zip" "${DISTNAME}" > /dev/null 2>&1; cd ..

echo "Successfully builded"
echo "To install the program put ${DISTNAME}.zip in ~/Downloads and execute the following command in a console:"
echo ""
echo "unzip ~/Downloads/${DISTNAME}.zip -d ~/Downloads > /dev/null 2>&1 && bash ~/Downloads/${DISTNAME}/install-update-resourcer.sh && rm -r ~/Downloads/${DISTNAME} && echo \"${DISTNAME} was succesfully installed\""
