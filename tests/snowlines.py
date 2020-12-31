import os
import boto3
import urllib.request
import json
from botocore.exceptions import NoCredentialsError, ClientError
from netcdf2geotiff import rgb_geotiff, singleband_geotiff


def upload_to_s3(local_file, bucket, s3_file, access_key, secret_key):
    print("Uploading output to S3 Bucket...")
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    if exists_in_s3(s3, bucket, s3_file):
        try:
            s3.upload_file(local_file, bucket, s3_file)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False
    else:
        return True


def exists_in_s3(s3, bucket, s3_file):
    try:
        s3.head_object(Bucket=bucket, Key=s3_file)
        print("File already exists in S3")
        return False
    except ClientError as e:
        return True
    return True


def date_from_file(file):
    return file.split("____")[1].split("T")[0]


def update_geotiff_json(file, bucket, access_key, secret_key):
    date = date_from_file(file)
    try:
        with urllib.request.urlopen(
                "https://snowlines-database.s3.eu-central-1.amazonaws.com/geotiff/"+date+".json") as url:
            data = json.loads(url.read().decode())["data"]
    except:
        data = []

    if file not in data:
        data.append(file)
        with open('temp.json', 'w') as outfile:
            json.dump(data, outfile)
        upload_to_s3("temp.json", bucket, "geotiff/"+date+".json", access_key, secret_key)
        os.remove("temp.json")
    else:
        print("File already in database")


with open('config.json', 'r') as config_file:
    config = json.load(config_file)
input_folder = "/home/jamesrunnalls/git/snowline/netcdf-files"
output_folder = "/media/jamesrunnalls/JamesSSD/Snowline/Geotiffs"

for file in os.listdir(input_folder):
    if "S3" in file:
        outfile_rgb = os.path.join(output_folder, "RGB_" + file.replace(".nc", ".tif"))
        outfile_snow = os.path.join(output_folder, "SNOW_" + file.replace(".nc", ".tif"))
        if not os.path.isfile(outfile_rgb):
            rgb_geotiff(os.path.join(input_folder, file), outfile_rgb, "RED", "GREEN", "BLUE", "lat", "lon")
        if upload_to_s3(outfile_rgb, "snowlines-geotiff", os.path.basename(outfile_rgb), config["aws_access"],
                        config["aws_secret"]):
            update_geotiff_json(os.path.basename(outfile_rgb), "snowlines-database", config["aws_access"], config["aws_secret"])
        if not os.path.isfile(outfile_snow):
            singleband_geotiff(os.path.join(input_folder, file), outfile_snow, "IDEPIX_SNOW_ICE", "lat", "lon")
        if upload_to_s3(outfile_snow, "snowlines-geotiff", os.path.basename(outfile_snow), config["aws_access"],
                        config["aws_secret"]):
            update_geotiff_json(os.path.basename(outfile_snow), "snowlines-database", config["aws_access"], config["aws_secret"])



