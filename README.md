# Transfer print-out maker

This program uses python's tkinter module and LaTeX (pdflatex required) to produce a transfer print (in pdf) used in traditional transfer orders - in polish and english.

![First picture](/readme-assets/first-pic.png?raw=true "First picture")

It was made originally for Linux, but it has been ported to Windows as well.

![Second picture](/readme-assets/sec-pic.png?raw=true "Second picture")

It supports dark mode and saving receivers/senders data on your drive (in csv formats)

![Third picture](/readme-assets/thir-pic.png?raw=true "Third picture")

The resulting transfer order print-out in pdf format:

![Fourth picture](/readme-assets/four-pic.png?raw=true "Fourth picture")

Please note that the transfer.tex file has to be in the same directory as trasfers.py for the program to work correctly.

To run the program clone the repository, move into the repository, and run the python script with below commands:

```shell
git clone https://github.com/marcsikor/transfer-producer
cd transfer-producer
python3 transfers.py
```

If any trouble with pdflatex occurs on your local machine, you can still use the generated newtransfer.tex file - for example with [Overleaf](https://www.overleaf.com)