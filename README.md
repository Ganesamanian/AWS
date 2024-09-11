# Table of Contents

1. [AWS Projects](#aws-projects)
   - [S3 Event Trigger with Lambda](#s3-event-trigger-with-lambda)
   - [Amazon SageMaker Model Building](#amazon-sagemaker-model-building)
   - [Efficient Test Data Prediction Using Amazon S3 Triggers, Lambda Functions, and SageMaker Endpoint](#efficient-test-data-prediction-using-amazon-s3-triggers-lambda-functions-and-sagemaker-endpoint)
   
---

## AWS Projects

Welcome to the AWS Projects section! Here, you'll find a collection of small projects related to various AWS services and technologies.

### S3 Event Trigger with Lambda

In this project, we demonstrate how to automate data processing tasks by utilizing Amazon S3 triggers and AWS Lambda functions. We'll guide you through setting up the necessary configurations to trigger Lambda functions when new objects are created or updated in an S3 bucket.

- [Project Repository](https://bitbucket.org/advosense/aws/src/master/S3%20event%20trigger%20with%20Lambda/)
- [Readme](https://bitbucket.org/advosense/aws/src/master/S3%20event%20trigger%20with%20Lambda/README.md)

### Amazon SageMaker Model Building

Explore the world of machine learning with Amazon SageMaker. In this project, we'll walk you through the process of building and training machine learning models using AWS SageMaker. You'll learn how to create, train, and deploy models for various applications.

- [Project Repository](https://bitbucket.org/advosense/aws/src/master/Sagemaker/)
- [Readme](https://bitbucket.org/advosense/aws/src/master/Sagemaker/README.md)

### Efficient Test Data Prediction Using Amazon S3 Triggers, Lambda Functions, and SageMaker Endpoint

This project provides a comprehensive guide on using a serverless AWS Lambda function designed to seamlessly integrate with Amazon SageMaker, a machine learning service. Its main purpose is to make predictions on data stored in a CSV file located in an Amazon S3 bucket. This Lambda function downloads the input data, sends it to a pre-configured SageMaker endpoint, and receives the model's predictions. It then manually calculates the accuracy of these predictions using the labels from the same CSV file, providing a detailed evaluation of the model's performance. Finally, the Lambda function saves the predictions and accuracy results in a JSON file and uploads it to another specified Amazon S3 bucket. This approach ensures efficient and automated machine learning model evaluation while leveraging AWS serverless computing for enhanced scalability.

- [Project Repository](https://bitbucket.org/advosense/aws/src/master/Efficient%20Test%20Data%20Prediction/)
- [Readme](https://bitbucket.org/advosense/aws/src/master/Efficient%20Test%20Data%20Prediction/README.md)

