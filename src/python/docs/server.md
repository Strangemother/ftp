## Install

You'll need macaroons and libsodiom.

Libsodium requires a GCC compiler on windows

### Linux


Libmacaroons should by built:

    sudo apt-get install devscripts debhelper build-essential
    wget https://download.libsodium.org/libsodium/releases/LATEST.tar.gz
    tar -xhf LATEST.tar.gz
    cd libsodium-1.0.3/
    ./configure
    sudo make
    sudo make install


### windows

1. Ensure you have a `makw` tool like WinMake or CygWin with `gcc` module
    a. Select 'devel' packages
2. download latest libsodium tar and extract
3. in the folder run:

    ./configure
    make && make install

**or**

mingw 32 or 64 bit compiled version will intergrate with the shared lib enviroment
really well. If the above is failing miserably, consider using mingw with base
GCC make compilers installed. 

1. Copy precompiled `lb`, `share`, `bin` to your Mingw share directory; install
pymacaroons and test.

## Usage

The server is ran on the machine providing the data. Running the server 
under basic config will provide a FTP server on 0.0.0.0:9044

A user will be provided a virtual directory of allowed drives, navigating
and selecting these drives will navigate the virtual directory.


## Authorized user

Settings Auth of a user binds them to allowed configurations
on their FTP service.

```python
    Auth: {
        user: {
            // can change dir
            chdir: true    
            // can make dir
            mkdir: true
            // can list a directory
            listdir: true
            // can remove a directory
            rmdir: true
            // can remove a file
            remove: true
            // can rename a file
            rename: true
            // can change a filemode
            chmod: true
        }
    }
```

## directories

A client connected via FTP can read a defined directory as root
folders to access. This is defined like a virutal directory, ensuring the
client is jailhoused to a specific folder or files structure.

A connected client can read a root folder noted as public - this is where shared
files can be maintained. An initial folder will be created in the destinaton
directory but this will be empty if the virtual folder structure is used.

An FTP client root folder will contain a list of virutal directories, allowing
a connecting client to read dirs the server configuration has named and specified.

In the FTP configuration, a user name - being their jailhouse - will defin a 
directory name and set to traverse. Normal FTP controls will navigate the
symbolic links of the associated drive. A FTP download sequence will provide
the file.

