import sys
sys.dont_write_bytecode = True

from website import app
app.run(port=5000, debug=True, host='0.0.0.0')