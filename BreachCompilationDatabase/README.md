## BreachCompilationDatabase

Multithreaded script to insert the BreachCompilation credentials into a postgresql database

## Usage
insert subsequent command to run this script completely in background
<pre><code>
nohup ./BreachCompilationDatabase --host 192.168.1.2 --port 5432 --user john --password test1234 --dbname credentials --schema breachcompilation --path /path/to/BreachCompilation &>/dev/null &
</code></pre>

or use a tool like [screen](https://wiki.ubuntuusers.de/Screen/)

<br>

## Database structure
creates for each number/letter (0-9,a-z) a table in defined schema (--schema argument) <br>

Columns in database: 
- id
- email
- password
- username
- provider
- sh1 
- sh256
- sh512
- md5

<div align="left">
  <br>
  <img src="res/" alt="example" width="900" height="115">
</div>

## check logs
trace logs
<pre><code>
tail -F trace.log
</code></pre>

insert fails
<pre><code>
tail -F insert_fail.log
</code></pre>

file viewer
<pre><code>
tail -F file.log
</code></pre>

<br>

## Postgresql database settings for the BreachCompilation credentials

install PostgreSQL dependencies via apt

<pre><code>
sudo apt-get install postgresql libpq-dev postgresql-client postgresql-client-common
</code></pre>

Follow this [tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04) to set up a 
postgresql environment. For graphical visualization install [pgAdmin4](https://www.pgadmin.org/download/).
<br>

Use the the script [BreachCompilationDatabase](BreachCompilationDatabase.py) 
to create the necessary database structure

<br>

## Execute an index only scan to increase query perfomance

create an index only scan for columns `email` and `password`
<pre><code>
CREATE index idx_pass_email on breachcompilation."d"(email, password);
</code></pre>

vacuum the table, so that the visibility map to be up-to-date
<pre><code>
VACUUM breachcompilation."d";
</code></pre>

Delete a table completely
<pre><code>
drop table breachcompilation."d" cascade
</code></pre>


Settings for tuning your postgresql server are [here](http://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server)