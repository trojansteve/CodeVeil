# CodeVeil
CodeVeil is a versatile obfuscation tool designed to enhance the security testing of scripts by employing a variety of advanced obfuscation techniques. It transcends traditional PowerShell obfuscation, offering support for multiple scripting languages and providing a robust solution for researchers and penetration testers to challenge and improve detection systems.

## Features
- Multi-language support for script obfuscation
- Advanced techniques including Base64 encoding, dynamic variable names, and control flow alteration
- Customizable obfuscation levels to suit different testing scenarios
- User-friendly command-line interface for ease of use
- Extensible architecture to add new obfuscation methods

## Installation
To install CodeVeil, clone the repository and set up a Python environment:
- git clone https://github.com/trojansteve/CodeVeil.git
- cd CodeVeil
- python -m venv venv
- source venv/bin/activate  # For Unix or MacOS
- venv\Scripts\activate  # For Windows
- pip install -r requirements.txt

## Usage
python codeveil.py -f input_script.ps1 -o obfuscated_script.ps1

For additional options and help, use the -h flag:
python codeveil.py -h

## Contributing
Contributions to CodeVeil are welcome! Please read our CONTRIBUTING.md for guidelines on how to submit pull requests, report issues, and suggest enhancements.

## License
CodeVeil is released under the Apache 2.0 License. See the LICENSE file for more details.

## Disclamer
CodeVeil is intended for educational and security testing purposes only. The developers are not responsible for any misuse or damage caused by this tool. Always have explicit permission before testing systems that you do not own.

## Acknowledgments
- Inspired by the legacy of Chimera
- Thanks to the Python community for their invaluable resources


