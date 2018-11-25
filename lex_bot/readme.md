# Deploying a Lex Bot via Python and AWS SDK

[API-Reference Lex](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html)
[API-Reference Lambda](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html)

## Requirements 

* Python 2.7+
* Pip libraries: boto3
* AWS-CLI installed and configured 

## Usage 
Create the lex infrastructure on AWS:
```
$ ./deploy.py create
```
Destroy the lex infrastructure on AWS:
```
$ ./deploy.py destroy
```
