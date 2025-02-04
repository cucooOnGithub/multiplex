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

def run_command(command_to_execute):
    """Execute a shell command and return its output (stdout & stderr)"""
    try:
        p = subprocess.Popen(command_to_execute, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate()

        result = []
        if output:
            result.append(output.decode())
        if err:
            result.append(err.decode())

        return result
    except Exception as e:
        return [f"Error executing command '{' '.join(command_to_execute)}': {str(e)}\n"]

def process_input(input_lines, command):
    """Process input lines and execute the command(s) in interleaved order"""
    processed_lines = []
    
    # Split multiple commands by ";"
    commands = [cmd.strip() for cmd in command.split(";") if cmd.strip()]

    for line in input_lines:
        line = line.strip()
        if not line:
            continue  # Skip empty lines

        arguments = line.split(" ")

        for cmd in commands:
            if has_positional_arguments(cmd):
                command_to_execute = shlex.split(cmd.format(*arguments))
            else:
                command_to_execute = shlex.split(cmd)

            output_lines = run_command(command_to_execute)
            
            # Append output for this specific input
            processed_lines.append(f"Command: {cmd}\n")
            processed_lines.extend(output_lines)
            processed_lines.append("\n")  # Ensure spacing between commands

    return processed_lines

if __name__ == "__main__":
    # Get command-line argument
    command = sys.argv[1] if len(sys.argv) > 1 else None

    # Read input lines from stdin
    input_lines = sys.stdin.readlines()

    # Process input lines and execute commands
    processed_lines = process_input(input_lines, command)

    # Print the result to stdout
    print("".join(processed_lines), flush=True)




