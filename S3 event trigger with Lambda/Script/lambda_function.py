import json
import boto3
import pandas as pd
import datetime
import pytz

# Function to convert microseconds to datetime objects
def convert_microseconds_to_datetime(timestamp_microseconds):
    """
    Converts a timestamp in microseconds to a datetime object in a specified timezone.

    Args:
        timestamp_microseconds (int): A timestamp in microseconds.

    Returns:
        str: A datetime string in the format 'YYYY-MM-DD HH:MM:SS' with the desired timezone applied.
             Microseconds are removed.

    
    """
    
    timestamp_seconds = int(timestamp_microseconds) / 1_000_000
    timestamp_datetime = datetime.datetime.fromtimestamp(timestamp_seconds)
    desired_timezone = pytz.timezone('US/Eastern')  # Replace with your desired time zone, currently it's -5
    timestamp_datetime = timestamp_datetime.astimezone(desired_timezone)
    timestamp_datetime = timestamp_datetime.replace(microsecond=0)  # Remove microseconds
    timestamp_datetime = timestamp_datetime.strftime('%Y-%m-%d %H:%M:%S')  # Format without milliseconds
    return timestamp_datetime

# Function to split date and time
def formatting_datetime(df, remove_microseconds = True, split_datetime = True):
    """
    Formats a DataFrame with timestamp data, optionally removing microseconds and 
    splitting datetime into separate Date and Time columns.

    Args:
        df (DataFrame): A DataFrame containing a 'tag_timestamp' column with timestamp data.
        remove_microseconds (bool, optional): A boolean flag to remove microseconds 
                                              from the timestamp (default is True).
        split_datetime (bool, optional): A boolean flag to split the timestamp into separate 
                                         'Date' and 'Time' columns (default is True).

    Returns:
        DataFrame: A modified DataFrame with 'Date' and 'Time' columns based on the specified flags.

    
    """
        
    if remove_microseconds:
        # Apply the conversion function to the DataFrame column
        df['tag_timestamp'] = df['tag_timestamp'].apply(convert_microseconds_to_datetime)
    if split_datetime:
        # Split 'Data and Time' column into 'Date' and 'Time' columns
        df[['Date', 'Time']] = df['tag_timestamp'].str.split(pat=' ', n=1, expand=True)

        # Drop the original 'Data and Time' column
        df.drop(columns=['tag_timestamp'], inplace=True)

        # Reorder columns with 'Date' and 'Time' at the start
        new_column_order = ['Date', 'Time'] + [col for col in df.columns if col not in ['Date', 'Time']]
        df = df[new_column_order]
        df['Time'] = df['Time'].str.split('.').str[0].str[:8]
        
    dropped_columns = df.columns[df.isnull().all()]
    df = df.dropna(axis=1, how='all')
    print("\nDropped Columns:")
    print(dropped_columns)
    return df
    

#Fucntion to convert data from
#JSON to CSV
def json2dataframe(data):
    tags = []
    
    for message in data:
        if 'messages' in message:
            for nested_message in message['messages']:
                if 'payload' in nested_message:
                    payload = json.loads(nested_message['payload'])
                    if "tags" in payload:
                        for fields in payload["tags"]:
                            tag = {
                                'reader_name': payload.get('rfidReaderName', ''),
                                'reader_serial': payload.get('rfidReaderSerialNumber', ''),
                                'reader_internal_serial': payload.get('rfidReaderInternalSerialNumber', ''),
                                'reader_timezone': payload.get('timeZone', ''),
                                'tag_pc': fields.get('pc', ''),
                                'tag_epc': fields.get('epc', ''),
                                'tag_tidBank': fields.get('tidBank', ''),
                                'tag_timestamp': fields.get('timeStampOfRead', ''),
                                'tag_rssi': fields.get('rssi', ''),
                                'tag_phase': fields.get('phase', ''),
                                'tag_antennaport': fields.get('antennaPort', '')
                            }
                            tags.append(tag)

    df = pd.DataFrame(tags)
    
    df = df[['reader_name', 'reader_serial', 'reader_internal_serial', 'reader_timezone', 'tag_pc', 'tag_epc', 'tag_tidBank', 'tag_timestamp', 'tag_rssi', 'tag_phase', 'tag_antennaport']]
    
    return df

def lambda_handler(event, context):
    # Define the source and destination bucket names
    source_bucket_name = 'bucket-inputdata'
    destination_bucket_name = 'bucket-processedata'
    copied_file_record_key = 'copied_files.json'  # Key to store the record of copied files
    preprocess_data = True

    # Initialize the S3 client
    s3 = boto3.client('s3')

    # List objects in the source bucket
    response = s3.list_objects_v2(Bucket=source_bucket_name)
    
    # Load the record of copied files from S3 if it exists
    copied_files = set()
    try:
        copied_files_obj = s3.get_object(Bucket=destination_bucket_name, Key=copied_file_record_key)
        copied_files = set(json.loads(copied_files_obj['Body'].read().decode('utf-8')))
    except Exception as e:
        # If the record doesn't exist, it's okay; start with an empty set
        pass

    # Iterate through the files in the source bucket, copy only if not in the record
    if 'Contents' in response:
        for obj in response['Contents']:
            source_key = obj['Key']
            destination_key = source_key.rsplit('.', 1)[0] + '.csv'
            if destination_key not in copied_files:
                
                # Read the JSON data 
                s3_response = s3.get_object(Bucket=source_bucket_name, Key=source_key)
                json_data = json.loads(s3_response['Body'].read().decode('utf-8'))
                
                if preprocess_data:
                    df = json2dataframe(json_data)
                    df = formatting_datetime(df)
                else:
                    df = json2dataframe(json_data)
               
                # Save the DataFrame as a CSV file
                csv_bytes = df.to_csv(index=False).encode('utf-8')
                s3.put_object(Bucket=destination_bucket_name, Key=destination_key, Body=csv_bytes)
                
                # s3.copy_object(CopySource={'Bucket': source_bucket_name, 'Key': source_key},
                            #   Bucket=destination_bucket_name, Key=destination_key)
                copied_files.add(destination_key)  # Add the copied file to the record

    # Update the record of copied files in S3
    s3.put_object(Bucket=destination_bucket_name, Key=copied_file_record_key, Body=json.dumps(list(copied_files)))

    return {
        'statusCode': 200,
        'body': 'Recent uncopied files copied successfully!'
    }

