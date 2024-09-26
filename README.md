# licenseValidity

**```licenseValidity```** - is a script that automatically checks ```.xml``` files and checks the validity of licenses.

## Installation

Install the current version with:

```shell
git clone https://github.com/imaonirvana/licenseValidity.git
```

Then install all requirements:

```shell
cd licenseValidity
```
```shell
pip3 install -r requirements.txt
```

___

*Note: If you already have **```licenseValidity```** on your device, download the latest version before using it:*

```shell
cd licenseValidity
```
```shell
git pull
```

## Usage

### How to run

To use the **```licenseValidity```** script, follow the format below in the command line:

```python3
python3 main.py user ip /remote/path /local/path
```

Replace *user* with the SSH login of server, where ```.xml``` file that you want to validate.
Replace *ip* with the IP address (or DNS) of the server.
Replace */remote/path* with the path to the ```.xml``` file on the server.
Replace */local/path* with the path to save the ```.xml``` file.

#### For example:

```python3
python3 main.py user dev-999.com /home/imaonirvana/file.xml ./file.xml
```

___

### Results

The results will be printed in an output to console:

![image](https://github.com/user-attachments/assets/e26a00c2-f0e7-4e88-883d-682dd8119c3a)

## Bug Reports and Feature Requests

If you encounter any bugs or have suggestions for new features, please feel free to contact me in Telegram or Teams. I appreciate your feedback and contributions to improve **```poChecker```**.

[Telegram](https://t.me/imaonirvana "Telegram") | [MS Teams](https://teams.microsoft.com/ "MS Teams") *(contact Dmytro Dudnyk)*
