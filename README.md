# Amino Acids API 

This Amino Acids API is capable of the following: 
- Transcribing DNA sequences
- Translating mRNA sequences
- Providing information on codons (abbreviations, full names etc.)
- Searching amino acid database by select criteria
- Adding food sources to amino acids

## Tools Used
- Python
- Flask
- Docker
- AWS DynamoDB
- AWS Lightsail

## Usage

The API can be accessed at: 
https://flask-service.qqoeeb8dkba36.ca-central-1.cs.amazonlightsail.com/

## Amino Acids API Routes
### Transcribe DNA Sequence
Transcribes DNA sequence to mRNA sequence.
#### Request 
` GET /transcribe`
```sh 
curl https://flask-service.qqoeeb8dkba36.ca-central-1.cs.amazonlightsail.com/transcribe?dna=AGTCTAGC
```
#### Response
```sh
StatusCode        : 200
StatusDescription : OK
Content           : "UCAGAUCG"
```

### Translate mRNA Sequence
Searches mRNA sequence for start and stop codons, and translates codons into amino acids. Start and stop codons must be present in sequence.
#### Request
`GET /translate`
```sh 
curl https://flask-service.qqoeeb8dkba36.ca-central-1.cs.amazonlightsail.com/translate?mRNA=CCAAUGGUAACAUUUUGAACA
```
#### Response
```sh
StatusCode        : 200
StatusDescription : OK
Content           : [
    "MET",
    "VAL",
    "THR",
    "PHE",
    "Stop"
]
```

### Get All Codons
#### Request
` GET /codons`
```sh 
curl https://flask-service.qqoeeb8dkba36.ca-central-1.cs.amazonlightsail.com/codons
```
#### Response
```sh
StatusCode        : 200
StatusDescription : OK
Content           : [
    {
        "AminoAcid": {
            "S": "Proline"
        },
        "AminoAcidAbb": {
            "S": "PRO"
        },
        "Codon": {
            "S": "CCA"
        },
        "Essential": {
            "S": "Conditionally Essential"
        },
        "FoodSource": {
            "SS": [
                "Asparagus"...
```

### Get Information on One or More Codons
#### Request
`GET /codons`
```sh
curl https://flask-service.qqoeeb8dkba36.ca-central-1.cs.amazonlightsail.com/codons?seq=AUGCCA
```
#### Response
```sh
StatusCode        : 200
StatusDescription : OK
Content           : [
    [
        {
            "AminoAcid": {
                "S": "Methionine"
            },
            "AminoAcidAbb": {
                "S": "MET"
            },
            "Codon": {
                "S": "AUG"
            },
            "Essential": {
                "S": "Essential"
            },
            "FoodSource": {
                "SS": [
                    "Eggs"...
```

### Search Codons by Essentiality and/or Food Source
Searches amino acid database for all codons that meet search requirements (essentiality, available in specified food source, or both conditions)
| Essentiality | Query Parameter |
| ------ | ------ |
| Essential | ?essential=essential |
| Non-Essential | ?essential=nonessential |
| Conditionally Essential | ?essential=condessential |
#### Request 
`GET /search`
```sh
curl https://flask-service.qqoeeb8dkba36.ca-central-1.cs.amazonlightsail.com/search?essential=essential"&"food=chicken
```
#### Response
```sh
StatusCode        : 200
StatusDescription : OK
Content           : [
    [
        {
            "AminoAcid": {
                "S": "Threonine"
            },
            "AminoAcidAbb": {
                "S": "THR"
            },
            "Codon": {
                "S": "ACA"
            },
            "Essential": {
                "S": "Essential"
            },
            "FoodSource": {
                "SS": [
                    "Beef",
                    "Cheese",
                    "Chicken"...
```

### Add Food Source to Database 
Provide the amino acid abbreviation and food source to add food item to database. 
#### Request
`POST \food`
```sh
curl --location -request POST 'https://flask-service.qqoeeb8dkba36.ca-central-1.cs.amazonlightsail.com/food' --header 'Content-Type: application/json' --data-raw '{ "aminoAcid" : "LEU","food" : "Beef"}'
```
#### Response
```sh
StatusCode        : 200
StatusDescription : OK
Content           : {
    "message": "Food added successfully to database. Thank you for your contribution!",
    "response": {
        "CUA": [
            "Beef",
            "Cheese",
            "Chicken",
            "Fish",
            "Nuts",
            "Pork"
        ],
        "CUC": [
            "Beef",
            "Cheese",
            "Chicken"...
```
##
#### Source Code on GitHub: 
https://github.com/VerinaG/Amino-Acids-API/
##

