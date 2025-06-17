from flask import Flask, render_template, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-scraping', methods=['POST'])
def start_scraping():
    try:
        # Ensure the script path is correct
        script_path = os.path.join(os.getcwd(), 'F:\\python project\\cryptocurrency\\cryptocurrency\\spiders\\coinmarketcap.py')

        # Check if the script exists
        if not os.path.exists(script_path):
            return jsonify({"status": "error", "message": "Scraping script not found!"})

        # Run the Python scraping script synchronously
        result = subprocess.run(['python', script_path], capture_output=True, text=True)

        # Check if the scraping was successful
        if result.returncode == 0:
            return jsonify({"status": "success", "message": "Scraping has started successfully!"})
        else:
            return jsonify({"status": "error", "message": result.stderr})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
