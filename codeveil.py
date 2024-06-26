# Copyright 2024 Stephen Haruna

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
import random
import string
import re
import ipaddress
from datetime import datetime
import base64
import zlib
import binascii

# Function to generate a random string
def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Function to obfuscate comments in the PowerShell script
def obfuscate_comments(content):
    return re.sub(r'#.*', '#' + random_string(), content)

# Function to obfuscate variable names in the PowerShell script
def obfuscate_variables(content):
    def replace_var(match):
        return '$' + random_string()
    return re.sub(r'\$[a-zA-Z_][a-zA-Z0-9_]*', replace_var, content)

# Function to obfuscate string literals in the PowerShell script
def obfuscate_strings(content):
    def replace_string(match):
        return '"' + random_string() + '"'
    return re.sub(r'".*?"', replace_string, content)

# Function to hex encode IP addresses in the PowerShell script
def hex_encode_ip_addresses(content):
    def replace_ip(match):
        ip_hex = ''.join([f"{int(octet):02X}" for octet in match.group().split('.')])
        return f"0x{ip_hex}"
    return re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', replace_ip, content)

# Function to insert backticks into PowerShell keywords
def insert_backticks(content, keywords):
    for keyword in keywords:
        pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
        content = pattern.sub(lambda match: '`'.join(match.group()), content)
    return content

# Function to randomize the case of characters in the PowerShell script
def randomize_case(content):
    return ''.join(random.choice([c.upper(), c.lower()]) for c in content)

# Function to obfuscate variable names in the PowerShell script
def obfuscate_variables(content):
    variables = set(re.findall(r'\$[a-zA-Z_][a-zA-Z0-9_]*', content))
    var_mapping = {var: '$' + random_string() for var in variables}
    for var, obf_var in var_mapping.items():
        content = content.replace(var, obf_var)
    return content

# Function to obfuscate cmdlets and function calls
def obfuscate_cmdlets(content):
    cmdlets = ['Write-Host', 'Invoke-Expression', 'Get-Item', 'Set-Item']
    for cmdlet in cmdlets:
        obfuscated_cmdlet = ''.join(random.choice([c.upper(), c.lower()]) for c in cmdlet)
        content = re.sub(r'\b' + cmdlet + r'\b', obfuscated_cmdlet, content, flags=re.IGNORECASE)
    return content

# Function to Base64 encode string literals in the PowerShell script
def base64_encode_strings(content):
    def replace_string(match):
        encoded_string = base64.b64encode(match.group().encode()).decode()
        return f"[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('{encoded_string}'))"
    return re.sub(r'".*?"', replace_string, content)

# Function to Base64 encode entire script blocks or functions
def base64_encode_script_blocks(content):
    def encode_block(match):
        encoded_block = base64.b64encode(match.group().encode()).decode()
        return f"`$ExecutionContext.InvokeCommand.ExpandString([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('{encoded_block}')))"
    return re.sub(r'(?s)(function\s+.*?\{.*?\})', encode_block, content)

# Function to compress the script and decompress it at runtime
def compress_script(content):
    compressed_data = zlib.compress(content.encode())
    encoded_compressed_data = base64.b64encode(compressed_data).decode()
    decompression_script = f"$compressed = '{encoded_compressed_data}'; $decompressed = [System.Text.Encoding]::UTF8.GetString([System.IO.Compression.GZipStream]::new([System.IO.MemoryStream][System.Convert]::FromBase64String($compressed), [System.IO.Compression.CompressionMode]::Decompress)); Invoke-Expression $decompressed"
    return decompression_script

# Function to obfuscate Base64 encoded strings
def obfuscate_base64_constructs(content):
    def replace_base64(match):
        encoded_string = match.group().strip('"')
        # Split the Base64 string into chunks
        chunks = [encoded_string[i:i+4] for i in range(0, len(encoded_string), 4)]
        # Shuffle the chunks to obfuscate
        random.shuffle(chunks)
        # Create a PowerShell array to join the chunks at runtime
        ps_array = ','.join(f'"{chunk}"' for chunk in chunks)
        # PowerShell command to concatenate the chunks and decode the Base64 string at runtime
        return f"(-join @({ps_array})).TrimEnd('=') | ForEach-Object {{ [System.Convert]::FromBase64String($_) }}"
    return re.sub(r'"[A-Za-z0-9+/=]{4,}"', replace_base64, content)

# Function to obfuscate Base64 encoded strings by converting them to a byte array
def obfuscate_base64_identifiers(content):
    def replace_base64(match):
        # Decode the Base64 string to bytes
        b64_bytes = base64.b64decode(match.group().strip('"'))
        # Convert bytes to a list of byte values
        byte_values = [str(b) for b in b64_bytes]
        # Create a PowerShell command to convert from byte values to a string at runtime
        ps_command = f"[System.Text.Encoding]::UTF8.GetString([byte[]]({','.join(byte_values)}))"
        return ps_command
    return re.sub(r'"[A-Za-z0-9+/=]{4,}"', replace_base64, content)

# Function to obfuscate the 'FromBase64String' method call in PowerShell
def obfuscate_from_base64_string(content):
    # Generate a random function name to replace 'FromBase64String'
    random_func_name = random_string()

    # Define the custom function that decodes a Base64 string
    custom_decoder_func = f"""
function {random_func_name}([string]$value) {{
    $data = [System.Convert]::FromBase64String($value)
    return [System.Text.Encoding]::UTF8.GetString($data)
}}
"""

    # Replace the 'FromBase64String' method call with the custom function call
    content = re.sub(r'\[System\.Convert\]::FromBase64String\((.*?)\)', f'{random_func_name}($1)', content)

    # Prepend the custom function definition to the script content
    content = custom_decoder_func + content
    return content

# Function to obfuscate individual tokens like operators and punctuation
def obfuscate_tokens(content):
    tokens = {'=': '`=', '+': '`+', '-': '`-', '*': '`*', '/': '`/'}
    for token, obfuscated_token in tokens.items():
        content = content.replace(token, obfuscated_token)
    return content

# Function to add extra whitespaces and newlines
def manipulate_whitespace(content):
    return content.replace('\n', '\n' + ' ' * random.randint(1, 5))

# Function to generate dynamic variable names at runtime
def dynamic_variable_names(content):
    # Replace static variable names with dynamic expressions
    def replace_var(match):
        var_name = match.group()[1:]  # Exclude the '$' from the match
        dynamic_var = f"$(New-Variable -Name ('{var_name}'[0..({len(var_name)}-1)] -join '') -Value 'value' -PassThru).Value"
        return dynamic_var
    return re.sub(r'\$[a-zA-Z_][a-zA-Z0-9_]*', replace_var, content)

# Function to rename functions and parameters to non-descriptive names
def rename_functions_and_parameters(content):
    # Find all function names and parameters
    function_matches = re.findall(r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
    param_matches = re.findall(r'param\s*\((.*?)\)', content, re.DOTALL)

    # Generate new names for functions and parameters
    function_mapping = {name: 'Func_' + random_string() for name in function_matches}
    param_mapping = {param: 'Param_' + random_string() for params in param_matches for param in params.split(',') if param}

    # Replace function names and parameters in the content
    for original, new_name in function_mapping.items():
        content = re.sub(r'\b' + original + r'\b', new_name, content)
    for original, new_name in param_mapping.items():
        content = re.sub(r'\b' + original.strip() + r'\b', new_name, content)

    return content

# Function to insert special characters that are ignored by PowerShell
def insert_special_characters(content):
    # Insert zero-width spaces into strings
    def replace_string(match):
        string_content = match.group()
        # Insert a zero-width space after each character
        return ''.join(ch + '\u200B' for ch in string_content[:-1]) + string_content[-1]
    return re.sub(r'".+?"', replace_string, content)


# Main function to handle the obfuscation process
def main(input_file, output_file):
    try:
        # Read the input PowerShell script
        with open(input_file, 'r') as file:
            content = file.read()

        # Perform obfuscation techniques
        content = obfuscate_comments(content)
        content = obfuscate_variables(content)
        content = obfuscate_strings(content)
        content = hex_encode_ip_addresses(content)
        content = insert_backticks(content, ['function', 'param', 'begin', 'process', 'end'])
        content = randomize_case(content)
        content = base64_encode_strings(content)
        content = obfuscate_base64_constructs(content)
        content = base64_encode_script_blocks(content)
        content = obfuscate_base64_identifiers(content)
        content = obfuscate_from_base64_string(content)
        content = obfuscate_cmdlets(content)
        content = obfuscate_tokens(content)
        content = manipulate_whitespace(content)
        content = compress_script(content)
        content = dynamic_variable_names(content)
        content = rename_functions_and_parameters(content)
        content = insert_special_characters(content)

        # Write the obfuscated script to the output file
        with open(output_file, 'w') as file:
            file.write(content)

        print(f"Obfuscated script written to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Parse command-line arguments
parser = argparse.ArgumentParser(description='PowerShell script obfuscator for vulnerability research.')
parser.add_argument('-f', '--file', type=str, required=True, help='PowerShell file to obfuscate')
parser.add_argument('-o', '--output', type=str, help='Output file for the obfuscated script')
args = parser.parse_args()

# Generate a timestamped output filename if not provided
if not args.output:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    args.output = f"{args.file}-obfuscated-{timestamp}.ps1"

# Run the main function with the provided arguments
if __name__ == '__main__':
    main(args.file, args.output)
