import subprocess

def install(module):
    subprocess.check_call(['python3.11', '-m' 'pip', 'install', module])
    print(f"The module {module} was installed")

def setup():
  install('nltk')
    