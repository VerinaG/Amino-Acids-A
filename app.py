import flask
from flask import request, jsonify, current_app
import aws_controller

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return current_app.send_static_file('homepage.html')

# V2 - Route to return information about all or one codon
@app.route('/codons', methods=['GET'])
def get_codons():
    if 'seq' in request.args:
        seq = request.args['seq'].upper()
        return jsonify(aws_controller.codons(seq))

    return jsonify(aws_controller.get_items())

# V2 - Route to return codons by essential or food
@app.route('/search', methods=['GET'])
def search_codons():
    essential = ''
    food = ''

    # Read in and format params
    if 'essential' in request.args:
        essential = request.args['essential']
        if (essential == 'essential' or essential == 'nonessential'):
            essential = essential.capitalize()
        elif essential == 'condessential':
            essential = 'Conditionally Essential'
        else:
            return "Error. Invalid essential paramater. Valid values = \"essential\", \"nonessential\" or \"condessential\".", 400
    if 'food' in request.args:
        food = request.args['food']
        food = food.capitalize()

    return jsonify(aws_controller.search(essential, food))

# V2 - Route to return translated mRNA
@app.route('/translate', methods=["GET"])
def api_v2translate():
    # Read in mRNA sequence
    try:
        mRNA = request.args['mRNA'].upper()
        if any(c not in 'UAGC' for c in mRNA):
            return "Error: mRNA strand must only contain U, A, G or C."
    except KeyError:
        return "Error: No mRNA sequence provided. Please specify an mRNA sequence.", 400

    return jsonify(aws_controller.translate(mRNA))

@app.route('/food', methods=["POST"])
def api_v2food():
    # Read in food
    data = request.get_json()

    try:
        codon = data['aminoAcid']
        food = data['food']
    except KeyError:
        return "Missing Body Parameter. 'aminoAcid' and 'food' paramters must be included in request body.", 400

    response = aws_controller.addFood(codon.upper(), food.capitalize())

    return response

# V2 - A transcription
@app.route('/transcribe', methods=["GET"])
def api_v2transcribe():
    # Read in DNA sequence
    try:
        dna = request.args['dna'].upper()
    except KeyError:
        return "Error: No DNA sequence provided. Please specify a DNA sequence.", 400

    # Create string to hold mRNA sequence
    mRNA = ""
    # Iterate through DNA strand to transcribe to mRNA
    for nucleotide in dna:
        if nucleotide == 'A':
            mRNA += 'U'
        elif nucleotide == 'T':
            mRNA += 'A'
        elif nucleotide == 'G':
            mRNA += 'C'
        elif nucleotide == 'C':
            mRNA += 'G'
        else:
            return "Error. DNA sequence can only consist of 'A', 'T', 'C' and 'G'.", 400

    return jsonify(mRNA)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
