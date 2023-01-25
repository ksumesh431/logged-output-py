import csv
import boto3
import logging
from datetime import datetime
now = datetime.now()
date_st = now.strftime("%d%m%y_%H%M%S")
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(filename="logfilename_{}.log".format(date_st), level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
#Supress boto3 logging 
logging.getLogger("boto3").setLevel(logging.ERROR)
logging.getLogger("botocore").setLevel(logging.ERROR)

ami_list = []
with open("./amilist.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    ami_list.append(row[0])

boto3.setup_default_session()
# Connect to EC2
ec2 = boto3.client('ec2', region_name = "us-east-1")
try:
    for ami in ami_list:
        try:
            #logging.info(ami)
            snapshot_ids = ec2.describe_images(ImageIds=[ami])['Images'][0]['BlockDeviceMappings']
            logging.info("Deregistering the AMI : {}".format(ami))
            ec2.deregister_image(ImageId=ami)
            for snapshot in snapshot_ids:
                # Delete the snapshot
                logging.info("Deleting the snapshot : {}".format(snapshot['Ebs']['SnapshotId']))
                ec2.delete_snapshot(SnapshotId=snapshot['Ebs']['SnapshotId'])
        except Exception as e:
            logging.warning("error in exception : {}".format(e))
except Exception as f:
    logging.warning("error in exception : {}".format(f))
