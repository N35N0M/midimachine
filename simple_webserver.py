import sys

from flask import Flask, redirect, url_for, request, jsonify
app = Flask(__name__)

@app.route('/deckLoaded/<deck>', methods=['POST', 'GET'])
def deckLoaded(deck):
   print(f"Update from deckLoaded: {deck}", file=sys.stderr)
   if request.method == 'POST':
      print("Got a POST!", file=sys.stderr)
      print(request.data, file=sys.stderr)
      return jsonify(success=True)
   else:
      print("Got a GET!", file=sys.stderr)
      return jsonify(success=True)

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

if __name__ == '__main__':
   app.run(debug = True)