## REST API for the leaked BreachCompilation credentials

**BreachCompilation** includes billion clear text credentials discovered in a single database
(file size: ~42GB). The aim of this repo is to create a REST API interface similar to the [ghostproject](https://ghostproject.fr/)<br>

- [Application BreachCompilationRestAPI](https://github.com/bierschi/BreachCompilationRestAPI#installation)
- [BreachCompilation structure and usage](https://github.com/bierschi/BreachCompilationRestAPI#breachcompilation-structure-and-usage)
- [Download BreachCompilation via transmission software](https://github.com/bierschi/BreachCompilationRestAPI#download-breachcompilation-via-transmission-software)
- [Database settings for the BreachCompilation credentials](https://github.com/bierschi/BreachCompilationRestAPI#database-settings-for-the-breachcompilation-credentials)

<br>
<hr>
<br>

## Installation
installation from source

<pre><code>
sudo python3 setup.py release install
</code></pre>

execute command line script
<pre><code>
BreachCompilationApp
</code></pre>

or use the systemd service file
<pre><code>
sudo systemctl status BreachCompilationApp.service
</code></pre>

<hr>

or build a rpm file to deploy it on a server
<pre><code>
sudo apt install rpm alien
</code></pre>

create a release rpm package with setup.py
<pre><code>
sudo python3 setup.py release bdist_rpm
</code></pre>

change into folder `dist`
<pre><code>
sudo alien -i BreachCompilationRestAPI-1.0.0-1.noarch.rpm
</code></pre>

copy the rpm file to target server and install the rpm package with the alien tool  
<pre><code>
sudo alien -i BreachCompilationRestAPI-1.0.0-1.noarch.rpm
</code></pre>

or create first a debian package and install with `dpkg -i`
<pre><code>
sudo alien BreachCompilationRestAPI-1.0.0-1.noarch.rpm
sudo dpkg -i breachcompilationrestapi_1.0.0-2_all.deb
</code></pre>

execute command line script
<pre><code>
BreachCompilationApp
</code></pre>

or use the systemd service file
<pre><code>
sudo systemctl status BreachCompilationApp.service
</code></pre>

<br>
<hr>
<br>

### BreachCompilation structure and usage
<pre><code>
BreachCompilation/
    data/
        0/
            0
            1
            .
            z
        1/
        .
        9/
        a/
            0
            .
            b (example)
            .
            z
        .
        z/
    old/
    count_total.sh
    imported.log
    query.sh
    README
    sorter.sh
    splitter.sh
</code></pre>

each file includes email adresses and passwords(email and password are seperated with `:`) starting with a specific letter. Example entry in folder
**a/** and file **b**. 
<pre><code>
AB-HK@hotmail.com:apple1
</code></pre>

<br>
<hr>
<br>

### Download BreachCompilation via transmission software

you can obtain this large dataset with this **magnet link**
<pre><code>
magnet:?xt=urn:btih:7ffbcd8cee06aba2ce6561688cf68ce2addca0a3&dn=BreachCompilation&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fglotorrents.pw%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337
</code></pre>

but first install transmission software collection
<pre><code>
sudo apt-get install transmission-cli  transmission-common transmission-daemon
</code></pre>

stop the transmission daemon when changing the configuration file
<pre><code>
sudo systemctl stop transmission-daemon.service
</code></pre>

edit `setting.json` in `/etc/transmission-daemon`

this must be changed for remote access (192.168 have to match your private ip address range)

<pre><code>
"rpc-whitelist": "127.0.0.1,192.168.*.*",
</code></pre>

this parameter has to be changed that the account user have full access to files/folders created by Transmission (default 18).
<pre><code>
"umask": 2,
</code></pre>

add your prefered download directory
<pre><code>
"download-dir": "/home/christian/Downloads/BreachCompilation",
</code></pre>

<pre><code>
"incomplete-dir": "/home/christian/Downloads/BreachCompilation",
</code></pre>

after configuration change, restart the transmission daemon
<pre><code>
sudo systemctl restart transmission-daemon.service
</code></pre>


Open your browser and add the magnet link

<pre><code>
http://server-ip:9091/transmission/web/
</code></pre>

default username: transmission <br>
default password: transmission

finally insert the magnet link in the url field
<div align="left">
  <br>
  <img src="res/transmission_enter_magnet_url.png" alt="example" width="900" height="115">
</div>

<br>
<hr>
<br>




