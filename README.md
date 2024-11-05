### Virtuelle Python Umgebung einrichten

sudo apt-get install python3-venv
python3 -m venv sp500-venv


### Virtuelle Python Umgebung einrichten
. ./PFADzuENV/sp500-venv/bin/activate

#### Testen
python --version
Python 3.8.10

#### Pip Updaten
pip install --upgrade pip
...

pip --version
pip 21.3.1 from /home/user/my-virtual-env/lib/python3.8/site-packages/pip (python 3.8)

#### Mudole nachinstallieren
pip install pandas
pip install yfinance



### Chronjob dazu:
35 22 * * * /home/pi/sp500-venv/bin/python3 /home/pi/scripte/sp500ma200.py
