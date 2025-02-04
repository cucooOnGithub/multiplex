#-------------------------------------------------------------------------------------
# multiplex - Utility to apply a shell command to a list
#-------------------------------------------------------------------------------------
# Author    : cucoo 
# Twitter   : @cucooOnX    
# Github    : cucooOnGitHub#
#-------------------------------------------------------------------------------------
# Description : multiplex is a simple utility in python that pipe a input to a shell command.
#               You can for instance, have a list of IP addresses and execute a shell command 
#               on each one of them and pipe the results into other files
#
# Example :
#           cat list_of_ips.txt | multiplex "whois"
#-------------------------------------------------------------------------------------
import subprocess
import sys
import shlex

def has_positional_arguments(command):
    """Check if the command contains placeholders {0}, {1}, ..., {9}"""
    return any("{" + str(i) + "}" in command for i in range(10))

def process_input(input_lines, command):
    """Process input lines and execute the command(s) accordingly"""
    processed_lines = []
    
    # Split multiple commands by ";"
    commands = command.split(";")

    for cmd in commands:
        cmd = cmd.strip()
        if not cmd:
            continue  # Skip empty commands

        # Check if the command needs input (i.e., contains {0}, {1}, etc.)
        needs_input = has_positional_arguments(cmd)

        if needs_input:
            for line in input_lines:
                line = line.strip()
                if not line:
                    continue  # Skip empty lines

                arguments = line.split(" ")
                command_to_execute = shlex.split(cmd.format(*arguments))

                processed_lines.extend(run_command(command_to_execute, cmd))
        else:
            # Execute command without appending input
            command_to_execute = shlex.split(cmd)
            processed_lines.extend(run_command(command_to_execute, cmd))

    return processed_lines

def run_command(command_to_execute, cmd):
    """Execute a shell command and return its output (stdout & stderr)"""
    processed_output = []
    try:
        p = subprocess.Popen(command_to_execute, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate()

        if output:
            processed_output.append(output.decode())
        if err:
            processed_output.append(err.decode())

    except Exception as e:
        processed_output.append(f"Error executing command '{cmd}': {str(e)}\n")

    return processed_output

if __name__ == "__main__":
    # Get command-line argument
    command = sys.argv[1] if len(sys.argv) > 1 else None

    # Read input lines from stdin
    input_lines = sys.stdin.readlines()

    # Process input lines and execute commands
    processed_lines = process_input(input_lines, command)

    # Print the result to stdout
    print("".join(processed_lines), flush=True)


