## CredentialDatabase
[![Build Status](https://travis-ci.org/bierschi/CredentialDatabase.png?branch=master)](https://travis-ci.org/bierschi/CredentialDatabase) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Create a massive credential database with collections like **BreachCompilation** or with credentials
from password files

**Features** of CredentialDatabase:
- develop awesome brute-force/credstuffer attacks which are based on CredentialDatabase
- build up a huge hash table for SHA1, SHA256, SHA512 and md5 hashes
- create a REST API interface similar to the [ghostproject](https://ghostproject.fr/)
- create a massive password database
- multithreaded database scripts

**BreachCompilation** includes billion clear text credentials discovered in a single database
(file size: ~42GB) <br>


## Content 

- [Installation](https://github.com/bierschi/CredentialDatabase#installation)
- [Usage and Examples](https://github.com/bierschi/CredentialDatabase#usage-and-examples)
- [Postgresql Database Settings](https://github.com/bierschi/CredentialDatabase#postgresql-database-settings)
- [Logs](https://github.com/bierschi/CredentialDatabase#logs)
- [Troubleshooting](https://github.com/bierschi/CredentialDatabase#troubleshooting)
- [Changelog](https://github.com/bierschi/CredentialDatabase#changelog)
- [License](https://github.com/bierschi/CredentialDatabase#license)

<br>

## Installation
installation with pip 
<pre><code>
pip3 install CredentialDatabase
</code></pre>

or from source
<pre><code>
sudo python3 setup.py install
</code></pre>

or create a wheel for installing the package with pip
<pre><code>
sudo python3 setup.py bdist_wheel
</code></pre>

install the package with pip
<pre><code>
pip3 install CredentialDatabase-1.0.0-py3-none-any.whl
</code></pre>

uninstall the package with pip 
<pre><code>
pip3 uninstall CredentialDatabase
</code></pre>

### Usage and Examples

#### BreachCompilationDatabase.py

execute the console script `BreachCompilationDatabase`
<pre><code>
BreachCompilationDatabase --host 192.168.1.2 --port 5432 --user john --password test1234 --dbname breachcompilation --breachpath /path/to/BreachCompilation
</code></pre>

insert subsequent command to run the script completely in background
<pre><code>
nohup BreachCompilationDatabase --host 192.168.1.2 --port 5432 --user john --password test1234 --dbname breachcompilation --breachpath /path/to/BreachCompilation &>/dev/null &
</code></pre>
or use a tool like [screen](https://wiki.ubuntuusers.de/Screen/)

#### Database structure

**schemas**: 0-9, a-z, symbols (first character from email) <br>
**tables**:  0-9, a-z, symbols (second character from email)

<pre><code>
id | email | password | username | provider | sh1 | sh256 | sh512 | md5 
</code></pre>

- script runtime about 8 days
- needs disk space for about 569 GB 

#### PasswordDatabase.py 

execute the console script `PasswordDatabase` with `--breachpath`
<pre><code>
PasswordDatabase --host 192.168.1.2 --port 5432 --user john --password test1234 --dbname passwords --breachpath /path/to/BreachCompilation
</code></pre>
or with `--filepath`
<pre><code>
PasswordDatabase --host 192.168.1.2 --port 5432 --user john --password test1234 --dbname passwords --filepath /path/to/CredentialFile --proc 10
</code></pre>

insert subsequent command to run the script completely in background
<pre><code>
nohup PasswordDatabase --host 192.168.1.2 --port 5432 --user john --password test1234 --dbname breachcompilation --breachpath /path/to/BreachCompilation &>/dev/null &
</code></pre>
or use a tool like [screen](https://wiki.ubuntuusers.de/Screen/)

#### Database structure

**schemas**: 0-9, a-z, symbols (first character from password) <br>
**tables**:  0-9, a-z, symbols (second character from password)

<pre><code>
password | length | isnumber | issymbol | ts
</code></pre>


## Postgresql Database Settings

install PostgreSQL dependencies via apt

<pre><code>
sudo apt-get install postgresql libpq-dev postgresql-client postgresql-client-common
</code></pre>

Follow this [tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04) to set up a 
postgresql environment. For graphical visualization install [pgAdmin4](https://www.pgadmin.org/download/).
<br>

### Postgresql Advanced

create an index only scan for columns `email` and `password`
<pre><code>
CREATE index idx_pass_email on "a"."d"(email, password);
</code></pre>

vacuum the table, so that the visibility map to be up-to-date
<pre><code>
VACUUM "a"."d";
</code></pre>

Delete a table completely with
<pre><code>
drop table "a"."d" cascade
</code></pre>


Settings for tuning your postgresql server are [here](http://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server)

## Logs

logs can be found in `/var/log/CredentialDatabase`

## Troubleshooting
add your current user to group `syslog`, this allows the application/scripts to create a folder in
`/var/log`. Replace `<user>` with your current user
<pre><code>
sudo adduser &lt;user&gt; syslog
</code></pre>
to apply this change, log out and log in again and check with the terminal command `groups`

## Changelog
All changes and versioning information can be found in the [CHANGELOG](https://github.com/bierschi/CredentialDatabase/blob/master/CHANGELOG.rst)

## License
Copyright (c) 2019 Bierschneider Christian. See [LICENSE](https://github.com/bierschi/CredentialDatabase/blob/master/LICENSE)
for details


