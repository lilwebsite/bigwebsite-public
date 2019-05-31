import subprocess
import shutil
from io import BytesIO as bytesio
from os import(
	remove,
	rename,
	mkdir
)
from os.path import (
	isfile,
	isdir,
	basename
)
import re
