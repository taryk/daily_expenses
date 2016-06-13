# Daily Expenses

## Install dependencies

You'll need to install Qt5 and PyQt5 if you don't have them yet.

### Mac OS X
```
brew install python3 qt5
pip3 install pyqt5
```

## Generate the UI

Although it's already generated, if you make any changes to the .ui file, you'll
need to run:
```
pyuic5 ui/ui_dailyexpenses.ui -o ui/ui_dailyexpenses.py
```

## Run

./daily_expenses.py
