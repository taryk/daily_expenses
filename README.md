# Daily Expenses

## Install dependencies

You'll need to install Qt5 and PySide if you don't have them yet.

### Mac OS X
```
brew install python3 qt5
pip3 install pyside
pyside_postinstall.py -install
```

## Install DB
```
sqlite3 db/daily_expenses.db < db/daily_expenses.default.sql
```

## Run

./daily_expenses.py
