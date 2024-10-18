# Telephone
The program prints the geography zone of italy related to home telephone numbers, original operators of mobile telephone numbers or service related to a special number.
It requires several dependencies, that you can install using this bash command:
```bash
pip3 install colorama termcolor csv
```
or
```bash
pip3 install -r requirements.txt
```
To run the server in a Docker container, you need to type the following commands on terminal:
```bash
docker build -t username/app .
docker run -it username/app
```
with:<br>
**-t tagname** to specify a tagname to identify the container<br>
**-it** only to type the number on stdin and see the results