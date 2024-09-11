# README #

### What is this repository for? ###

This repository contains the code and resources for the "Efficient Test Data Prediction Using Amazon S3 Triggers, Lambda Functions, and SageMaker Endpoint" project. The project's primary goal is to guide users through the process of efficiently making predictions on test data using Amazon SageMaker, AWS Lambda functions, and Amazon S3 triggers. This serverless approach allows for seamless integration and automated model evaluation.

### Version ###

1.0

### How do I get set up? ###

**Summary of Set Up:**

To set up and run this project, follow the steps outlined below:

1. Clone the repository to your local machine.

2. Ensure you have an AWS account and configure the AWS CLI with your AWS credentials to enable the usage of AWS services.

3. Follow the provided guide to create an AWS Lambda function that integrates with an Amazon SageMaker endpoint to make predictions on data stored in an Amazon S3 bucket.

4. The Lambda function calculates the accuracy of these predictions using labels from the same CSV file and saves the results in a JSON file.

5. Configure Amazon S3 triggers to automate the process and upload the results to another specified Amazon S3 bucket.

For a detailed guide, please refer to "Efficient Test Data Prediction Using Amazon S3 Triggers, Lambda Functions, and SageMaker Endpoint.pdf" in this repository.

**Configuration:**

Ensure you have the following configuration set up:

- AWS account with appropriate permissions for AWS Lambda, Amazon S3, and Amazon SageMaker.
- AWS CLI configured with your AWS access key and secret key.

**Dependencies:**

The following dependencies are required to run this project:

- AWS CLI
- Python 3.x
- Amazon SageMaker
- AWS Lambda
- Amazon S3

**Database Configuration:**

This project does not involve a database. It focuses on efficient test data prediction and model evaluation using AWS services.

**How to Run Tests:**

Automated tests for this project are not provided. Testing is primarily manual and involves configuring and testing the Lambda function with SageMaker and S3 triggers.

**Deployment Instructions:**

Follow the project guide within the repository to set up and configure the Lambda function, SageMaker endpoint, and Amazon S3 triggers for efficient test data prediction.

### Contribution Guidelines ###

Contributions to this project are welcome. If you'd like to contribute, please follow these guidelines:

- Provide clear and detailed documentation.
- Ensure that your contributions align with the project's objectives and AWS best practices for serverless architecture.

If you have any suggestions or improvements, please submit a pull request or contact the project owner.

### Who do I talk to? ###

For questions or concerns related to this project, you can contact:

- Ganesamanian Kolappan 
- ganesamanian@advosense.com

Thank you for using this project, and we hope it helps you efficiently make predictions on test data using Amazon S3 triggers, Lambda functions, and SageMaker endpoints!