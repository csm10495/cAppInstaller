'''
Home to common utils for cAppInstaller
'''
import queue
import shlex
import subprocess

def subprocess_call_live_output(output_queue: queue.Queue, cmd) -> int:
    '''
    Runs a given cmd via subprocess, and sends live output to the output_queue.

    Returns the process exit code.
    '''
    if isinstance(cmd, list):
        output_queue.put_nowait([f'>> {shlex.join(cmd)}'])
    else:
        output_queue.put_nowait([f'>> {cmd}'])

    process = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, shell=True)

    for stdout_line in process.stdout:
        output_queue.put_nowait(stdout_line.decode().splitlines())

    return process.wait()
