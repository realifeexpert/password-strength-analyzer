# web_demo.py
from flask import Flask, request, render_template_string
from analyzer import analyze

app = Flask(__name__)

HTML = """
<!doctype html>
<title>Password Analyzer</title>
<h2>Password Strength Analyzer</h2>
<form method=post>
  <input type=password name=pw placeholder="Enter password" style="width:300px">
  <input type=submit value=Check>
</form>
{% if res %}
  <p>Entropy: {{res.entropy_bits}} bits<br>
  Score: {{res.score}} / 100 ({{res.category}})</p>
  <ul>
  {% for s in res.suggestions %}
    <li>{{s}}</li>
  {% endfor %}
  </ul>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    res = None
    if request.method == "POST":
        pw = request.form.get("pw","")
        res = analyze(pw)
    return render_template_string(HTML, res=res)

if __name__ == "__main__":
    app.run(debug=True)
