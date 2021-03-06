#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64, hashlib, calendar, re, sys, platform, subprocess
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO
from pathlib import Path

def verify_password(password):
    RegexLength=re.compile(r'^\S{8,}$')
    RegexDigit=re.compile(r'\d')
    RegexLower=re.compile(r'[a-z]')
    if RegexLength.search(password) == None or RegexDigit.search(password) == None or RegexLower.search(password) == None: # or RegexUpper.search(password) == None :
        return False
    else:
        return True

def hash256(string):
    return hashlib.sha256(string.encode()).hexdigest()

def mk_timestamp():
    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())
    return unixtime

def to_base32(input):
    return base64.b32encode(bytearray(str(input), 'ascii')).decode('utf-8')

def to_hex(input):
    return input.encode("utf-8").hex()

def get_exec_sh():
    os = platform.platform().lower()
    executable = None
    if "darwin-19" in os:
        executable = "/bin/sh"
    elif "debian" in os:
        executable = "/bin/sh"

    return executable

def parse_yaml(input, file=False):
    if file is True:
        input = Path(input)
    yaml = YAML(typ='safe')
    data = yaml.load(input)
    return data

def date_crop(i):
    try:
        return i.split(".")[0].replace("-", "/").replace("T", " ")
    except:
        return i

def runcli(runstring, errorstring=None, raw=False, _parse=False):
    try:
        output = subprocess.check_output(
            str(runstring),
            shell=True,
            executable=get_exec_sh()
        ).decode()

        if output.find("failed to make a REST request") < -1:
            return
        if raw is True:
            return output

        if _parse is True:
            return parse_yaml(output)

        return output.replace("\n", "")

    except subprocess.CalledProcessError:
        if errorstring is None:
            print(f'Error running command: {runstring}\n')
        else:
            print(str(errorstring))

class Yaml(YAML):
    def dump(self, data, stream=None, **kw):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        if inefficient:
            return stream.getvalue()

    def parse(self, input, file=False):
        if file is True:
            input = Path(input)
        yaml = YAML(typ='safe')
        data = yaml.load(input)
        return data

    def save_file(self, input, location='config/settings.yaml'):
        _file = open(location, 'w')
        _file.write(self.dump(input))
        return
