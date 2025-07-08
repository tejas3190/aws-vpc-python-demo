from flask import Flask, request, jsonify
import jwt
import datetime
import os
import boto3
import ipaddress
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('APP_SECRET')

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

def check_token(token):
    try:
        token = token.split(" ")[1]
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return False, "Valid Token"
    except jwt.ExpiredSignatureError:
        return True, 'Token expired'
    except jwt.InvalidTokenError:
        return True, 'Invalid token'

def create_subnets(ec2, vpc_id, vpc_cidr, number_of_subnet):
    vpc_network = ipaddress.IPv4Network(vpc_cidr)
    required_bits = math.ceil(math.log(number_of_subnet,2))
    #print(required_bits)
    new_prefix = vpc_network.prefixlen + required_bits
    #print(vpc_network.prefixlen)
    #print(new_prefix)
    subnet_size = ipaddress.IPv4Network(f'0.0.0.0/{new_prefix}')
    #print(subnet_size)
    #print("********")
    subnets_cidr = vpc_network.subnets(new_prefix=new_prefix)
    subnets = []
    tags = [
        { "Key": "vpc-id", "Value": vpc_id }
    ]
    for scidr in subnets_cidr:
        #print(scidr)
        subnet_response = ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock=str(scidr),
            TagSpecifications=[{'ResourceType': 'subnet','Tags':tags}]
        )
        subnets.append({"SubnetId":subnet_response["Subnet"]["SubnetId"],\
        "CidrBlock": subnet_response["Subnet"]["CidrBlock"], "AvailabilityZone":subnet_response["Subnet"]["AvailabilityZone"]})
    return subnets

def create_vpc_with_subnets(cidr_block, num_subnets, region="ap-south-1"):
    # Initialize boto3 client
    ec2 = boto3.client("ec2", region_name=region)

    # Create VPC
    tags = [
        {"Key": "Region", "Value": region},
    ]
    vpc_response = ec2.create_vpc(CidrBlock=cidr_block, InstanceTenancy="default", TagSpecifications=[{'ResourceType': 'vpc','Tags':tags}])
    vpc_id = vpc_response["Vpc"]["VpcId"]
    # Create subnets
    subnets = create_subnets(ec2, vpc_id, cidr_block, num_subnets)
    return {"vpc_id": vpc_id, "subnets": subnets}

@app.route("/aws/api/v1/<region>/vpc/<vpc_id>", methods=["GET"])
def get_vpc(region, vpc_id):
    ec2 = boto3.client("ec2", region_name=region)
    vpc_details = ec2.describe_vpcs(VpcIds=[vpc_id])["Vpcs"][0]
    print(vpc_details)
    subnets = ec2.describe_subnets(Filters=[{"Name": "vpc-id", "Values": [vpc_id]}])["Subnets"]
    return jsonify({"vpc": vpc_details, "subnets": subnets}), 200

@app.route("/aws/api/v1/create-vpc", methods=["POST"])
def create_vpc():
    token = request.headers.get('Authorization')
    if token:
        err, msg = check_token(token)
        if err:
            return jsonify({'message': msg}), 401
        data = request.get_json()
        #print(data)
        vpc_info = create_vpc_with_subnets(**data)
        return jsonify(vpc_info), 201
    else:
        return jsonify({'message': 'Token not provided'}), 401

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username == USERNAME and password == PASSWORD:
        payload = {
            'user_id': 3131,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
