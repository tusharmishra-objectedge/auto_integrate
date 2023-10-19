# auto-integrate

## Setting up the environment
Run the following commands to set up the environment:
```
source venv/bin/activate
pip3 install -r requirements.txt
```

## Running the program
The program needs to be run from the root directory of the repository. The following arguments are required:
- `-i` or `--input`: The path to the input file
- `-o` or `--output`: The path to the output file

The program can hence be run as follows:
```
python3 -m auto_integrate_cli -i <input_file> -o <output_file>
```

For example:
```
python3 -m auto_integrate_cli -i inputs/mockAPI1.json -o outputs/o.txt
```
