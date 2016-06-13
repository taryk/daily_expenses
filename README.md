# Daily Expenses

This project is my attempt to put my expenses in order.

I've been using Google SpreadSheet to keep track of my expenses for a few 
years now. It's fine as long as all you need is just to add your expenses in
and see how much you spent for some period of time (a day/week/month/year), to
sum your expenses up, etc. But it gets a bit difficult if you want to run
some arbitrary queries on the data, like "tell me how much I spent on food for
the last year".

I'd like the process of adding the expenses in and then querying them to be as
effortless as possible, hence I started prototyping the app. Ideally, there
should be an app for Android and iOS as well.


### Install dependencies

If you fancy to try it out, you'll need to install `python3`, `Qt5`, and 
`PyQt5` if you don't have them yet.

#### Mac OS X
```
$ brew install python3 qt5
$ pip3 install pyqt5 sqlalchemy pytest pytest-qt pytest-mock
```

### Generate the UI

Although the UI is already generated, if you make any changes to it, you'll
need to run:
```
$ pyuic5 ui/ui_dailyexpenses.ui -o ui/ui_dailyexpenses.py
```

### Run

```
$ ./daily_expenses.py
```

### Tests

```
$ python3.5 -m pytest tests
```