from flask import Flask, request, render_template, jsonify
import subprocess

app = Flask(__name__)

current_command = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-command', methods=['POST'])
def generate_command():
    global current_command

    url = request.form.get('url')
    cookies = request.form.get('cookies')
    dbInputSection = request.form.get('dbInputSection')
    tableInputSection = request.form.get('tableInputSection')
    columnInputSection = request.form.get('columnInputSection')
    level = request.form.get('level')
    risk = request.form.get('risk')
    enumeration_option = request.form.get('enumeration_option')
    dbms = request.form.get('dbms')
    testparameter = request.form.get('testparameter')
    data = request.form.get('data')
    proxy = request.form.get('proxy')
    random_agent = request.form.get('random-agent')
    tor = request.form.get('tor')
    check_tor = request.form.get('check-tor')
    batch = request.form.get('batch')  
    enable_db = request.form.get('enableDb')  
    enable_table = request.form.get('enableTable')  
    enable_column = request.form.get('enableColumn') 
    db = request.form.get('db')  
    table = request.form.get('table')  
    column = request.form.get('column')  

    if not url:
        return jsonify({"error": "URL is required"}), 400

    command = ['sqlmap', '-u', url]
    if cookies:
        command.extend(['--cookie', cookies])
    if dbms:
        command.extend(['--dbms', dbms])
    if level!= 'off':
        command.extend(['--level', level]) 
    if risk!= 'off':
        command.extend(['--risk', risk]) 
    if enumeration_option != 'off':
        command.extend(['--'+enumeration_option])
    if testparameter:
        command.extend(['-p', testparameter])
    if data:
        command.extend(['--data', data])
    if proxy:
        command.extend(['--proxy', proxy])
    if random_agent== 'on':
        command.extend(['--random-agent'])
    if tor== 'on':
        command.extend(['--tor'])
    if check_tor== 'on':
        command.extend(['--check-tor'])
    if batch == 'on':
        command.append('--batch')
    if dbInputSection:
        command.extend(['-D', dbInputSection])
    if tableInputSection:
        command.extend(['-T', tableInputSection])
    if columnInputSection:
        command.extend(['-C', columnInputSection])
    if enable_db == 'on' and db:
        command.extend(['-D', db])
    if enable_table == 'on' and table:
        command.extend(['-T', table])
    if enable_column == 'on' and column:
        command.extend(['-C', column])

    current_command = " ".join(command)

    return jsonify({
        "command": current_command
    })

@app.route('/run-command', methods=['POST'])
def run_command():
    global current_command

    if not current_command:
        return jsonify({"error": "No command generated yet"}), 400

    try:
        print("Running command:", current_command)  
        result = subprocess.run(current_command.split(), capture_output=True, text=True)
        output = f"Command: {current_command}\n\n"
        output += f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        
        return jsonify({
            "output": output  
        })
    except Exception as e:
        print("Error:", str(e)) 
        return jsonify({"error": str(e)}), 500

@app.route('/respond-command', methods=['POST'])
def respond_command():
    global current_command

    response = request.json.get('response')  
    
    if response not in ['Y', 'N']:
        return jsonify({"error": "Invalid response. Must be 'Y' or 'N'"}), 400

    try:
        process = subprocess.Popen(
            current_command.split(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output, error = process.communicate(input=response + '\n')
        
        return jsonify({
            "output": output,
            "error": error
        })
    except Exception as e:
        print("Error:", str(e))  
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)