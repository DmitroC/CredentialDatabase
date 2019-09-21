## BreachCompilationDatabase

Multithreaded script to insert the BreachCompilation credentials into a postgresql database

## Usage
insert subsequent command to run this script completely in background
<pre><code>
nohup ./BreachCompilationDatabase --host localhost --port 5432 --user christian --password test1234 --schema breachcompilation --path /home/christian/Downloads/BreachCompilation &>/dev/null &
</code></pre>

## Database structure
creates for each number/letter (0-9,a-z) a table in defined schema (--schema argument) <br>

elements in database: 
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

<pre><code>
tail -F trace_log.log
</code></pre>