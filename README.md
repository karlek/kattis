
## Kattis

Sublime package for submitting problems inside sublimes to kattis! 


## Installation

1. __Download package__

    ```sh
    $ cd "~/.config/sublime-text-3/Packages/"
    $ git clone "git@github.com:karlek/kattis.git"
    $ cd kattis
    $ # If you use open.kattis.com
    $ sed -i "s/kth.kattis/open.kattis/g" kattis.py
    ```

2. __Download config file__

    _kth.kattis.com_:  
    https://kth.kattis.com/download/kattisrc

    _open.kattis.com_:  
    https://open.kattis.com/download/kattisrc

    Save to ~/.kattisrc

## Usage

1. __Use kattis plugin in sublime to submit current file__

    `ctrl+shift+p` -> Kattis - Submit

    1b. __The file hasn't been submitted before.__

    Enter problem id.

2. __The file is submitted!__

    Ah yeah!

3. __Set/change problem id__

    `ctrl+shift+p` -> Kattis - Set Problem ID


## Public domain

I hereby release this code into the [public domain](https://creativecommons.org/publicdomain/zero/1.0/).
