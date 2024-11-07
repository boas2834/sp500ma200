#### Virtuelle Python Umgebung einrichten

sudo apt-get install python3-venv
python3 -m venv sp500-venv


#### Virtuelle Python Umgebung aktivieren
. ./PFADzuENV/sp500-venv/bin/activate

#### Testen
python --version
Python 3.8.10

#### Pip Updaten
pip install --upgrade pip

#### Pip Version anzeigen
pip --version
pip 21.3.1 from /home/user/my-virtual-env/lib/python3.8/site-packages/pip (python 3.8)

#### Module nachinstallieren
pip install pandas
pip install yfinance



### Chronjob dazu:
chrontab -e
22 22 * * * /PathTo/run.sh > /PathTo/sp500maillog.log 2>&1
