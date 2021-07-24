import subprocess
width=5
def main(w=5,d=1,v=False):
    try:
        response = "\n".join(subprocess.check_call(f"python3 astarsolver.py -w={w} -d={d} -N", shell=True).decode(encoding="utf-8").split("\n")[0:width])
        return(response)
    except (subprocess.CalledProcessError,AttributeError):
        pass