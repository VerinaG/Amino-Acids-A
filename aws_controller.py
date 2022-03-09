import boto3, json, flask
from flask import Response
from botocore.exceptions import ClientError

# Read in credentials
with open('credentials.json', 'r') as f:
    credentials = json.load(f)

dynamo_client = boto3.client(
    'dynamodb',
    aws_access_key_id = credentials['aws_access_key_id'],
    aws_secret_access_key = credentials['aws_secret_access_key'],
    region_name = credentials['region_name']
)

# Return all items
def get_items():
    response = dynamo_client.scan(
        TableName = 'AminoAcids'
    )

    return response['Items']

# Return translated protein from mRNA
def translate(mRNA):
    protein = []

    #Find start codon and translate
    if mRNA.find('AUG') == -1:
        return "Error: No start codon found.", 400
    elif (mRNA.find('UAG') and mRNA.find('UAA') and mRNA.find('UGA')) == -1:
        return "Error: No stop codon found.", 400
    else:
        pos = mRNA.find('AUG')
        # Keep looping until you hit end of sequence or reach stop codon
        while (pos <= (len(mRNA) - 3)):
            currCodon = dynamo_client.query(
                TableName='AminoAcids',
                KeyConditionExpression='Codon = :Codon',
                ExpressionAttributeValues={
                    ':Codon': {'S': mRNA[pos:pos+3]}
                },
                ProjectionExpression = 'AminoAcidAbb'
            )
            protein.append(currCodon['Items'][0]['AminoAcidAbb']['S'])
            if currCodon['Items'][0]['AminoAcidAbb']['S'] == 'Stop':
                break
            else:
                pos += 3

    return protein

# Return all information about codon(s)
def codons(seq):
    codonInfo = []

    pos = 0
    while (pos <= (len(seq) - 3)):
        currCodon = dynamo_client.query(
            TableName='AminoAcids',
            KeyConditionExpression='Codon = :Codon',
            ExpressionAttributeValues={
                ':Codon': {'S': seq[pos:pos+3]}
            },
        )
        codonInfo.append(currCodon['Items'])
        pos += 3

    return codonInfo

# Return all codons that meet search criteria
def search(essential, food):
    codonInfo = []

    # Scan database by essential, food or both
    if not essential:
        currInfo = dynamo_client.scan(
            TableName='AminoAcids',
            FilterExpression='contains(FoodSource, :FoodSource)',
            ExpressionAttributeValues={
                ':FoodSource': {'S': food}
            }
        )
    elif not food:
        currInfo = dynamo_client.scan(
            TableName='AminoAcids',
            FilterExpression='Essential = :Essential',
            ExpressionAttributeValues={
                ':Essential': {'S': essential}
            }
        )
    else:
        currInfo = dynamo_client.scan(
            TableName='AminoAcids',
            FilterExpression='contains(FoodSource, :FoodSource) and Essential = :Essential',
            ExpressionAttributeValues={
                ':FoodSource': {'S': food},
                ':Essential': {'S': essential}
            }
        )

    codonInfo.append(currInfo['Items'])

    return codonInfo

# Add food to database
def addFood(aminoAcid, food):
    # Find all codons associated with amino acid
    allCodons = dynamo_client.scan(
        TableName='AminoAcids',
        FilterExpression='AminoAcidAbb = :aminoAcid',
        ExpressionAttributeValues={
            ':aminoAcid': {'S': aminoAcid}
        },
        ProjectionExpression='Codon'
    )

    # Return error if no codons match amino acid abbreviation
    if not allCodons['Items']:
        return "Error: Amino Acid Abbreviation \"{}\" does not exist. Please enter correct amino acid.".format(aminoAcid), 400

    response = {}
    # Update item in database if amino acid is valid
    for c in allCodons['Items']:
        currResponse = dynamo_client.update_item(
            TableName='AminoAcids',
            Key={
                'Codon': c['Codon'],
                'AminoAcidAbb': {"S": aminoAcid}
            },
            UpdateExpression='ADD #FS :f',
            ExpressionAttributeNames={
                '#FS': 'FoodSource'
            },
            ExpressionAttributeValues={
                ':f': {"SS": [food]},
            },
            ReturnValues="ALL_NEW"
        )
        response[currResponse['Attributes']['Codon']['S']] = currResponse['Attributes']['FoodSource']['SS']
    return {
        'message': 'Food added successfully to database. Thank you for your contribution!',
        'response': response
    }, 200
