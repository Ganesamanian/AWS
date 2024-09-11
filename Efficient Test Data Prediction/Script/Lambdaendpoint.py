import json
import boto3
import csv
import tempfile
import os
import pandas as pd

def calculate_accuracy(predictions, labels):
    correct_predictions = 0
    total_predictions = len(predictions)
    
    for pred, label in zip(predictions, labels):
        if pred == label:
            correct_predictions += 1
    
    return correct_predictions / total_predictions

def lambda_handler(event, context):
    # Initialize SageMaker runtime and S3 client
    sm_runtime = boto3.client('sagemaker-runtime')
    s3_client = boto3.client('s3')

    # Specify the SageMaker endpoint name
    endpoint_name = 'tuned-svm-endpoint'
    
    # Define S3 bucket and file paths
    input_bucket = 'bucket-inputdata'
    input_file_key = 'test.csv'
    output_bucket = 'bucket-processedata'
    output_file_key = 'predictions.json'

    # Download the input CSV file from S3 to a temporary directory
    temp_dir = tempfile.mkdtemp()
    input_file_path = os.path.join(temp_dir, 'input.csv')
    s3_client.download_file(input_bucket, input_file_key, input_file_path)

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_file_path)

    # Extract the label column for accuracy calculation
    labels = df['label']  # Assuming 'label' is the name of your label column

    # Remove the label column before making predictions
    data = df.drop(columns=['label'])

    # Make a prediction request to the SageMaker endpoint
    response = sm_runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='text/csv',
        Body=data.to_csv(index=False, header=False)
    )

    # Extract the prediction result
    prediction_result = json.loads(response['Body'].read())

    # Calculate accuracy manually
    accuracy = calculate_accuracy(prediction_result, labels)

    # Save the predictions and accuracy to a JSON file
    output_data = {
        "predictions": prediction_result,
        "accuracy": accuracy
    }
    output_json = json.dumps(output_data)

    # Upload the JSON file to the output S3 bucket
    s3_client.put_object(
        Bucket=output_bucket,
        Key=output_file_key,
        Body=output_json,
        ContentType='application/json'
    )

    return {
        'statusCode': 200,
        'body': json.dumps("Predictions and accuracy saved to S3")
    }

