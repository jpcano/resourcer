# Resourcer

GUI tool to resource candidates using BigQuery

## Run

```
bash run.sh
```

## Run tests

```
bash run_tests.sh
```

## Create package to distribute in Mac

```
bash dist_mac.sh
```

## Install Reasourcer in Mac

- Put the zip package in ~/Downloads
- Open a terminal and execute the next command:

```
unzip ~/Downloads/Resourcer-v1.1.0.zip -d ~/Downloads > /dev/null 2>&1 && bash ~/Downloads/Resourcer-v1.1.0/install-update-resourcer.sh && rm -r ~/Downloads/Resourcer-v1.1.0 && echo "Resourcer-v1.1.0 was succesfully installed"
```

- The app is now installed in your Launchpad
