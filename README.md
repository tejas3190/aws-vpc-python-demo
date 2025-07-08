# aws-vpc-python-demo
This is an demo repo to test AWS VPC &amp; Subnet creation through Flask

## Dependencies
python ~3.10
boto3 ~1.39.x
flask ~3.1.x

## How to run 

The project is dependent on few environment variable

1. USERNAME -> User name for authentication REQUIRED
2. PASSWORD -> Password for authentication REQUIRED
3. APP_SECRET -> Secret for encode/decode of JWT token REQUIRED
4. AWS_ACCESS_KEY_ID OPTIONAL if you have set in /home/<user>/.aws
5. AWS_SECRET_ACCESS_KEY OPTIONAL if you have set in /home/<user>/.aws

After setting the above environment variable execute the following command to start the Flask Application running on http://locahost:5000

-> python server.py

APIs 

There are three API provisioned in this app 

1. Login or Authentication
   API -> POST http://localhost:5000/login
   In body you need to provide username & password. Use the same which you have provided during environment variable setup for USERNAME & PASSWORD. The API return a n JWT token valid for 1 hour. 
   Example:

   Request:
   curl -XPOST -H "Content-type: application/json" -d '{
    "username": "tejas",
    "password": "password"}' 'http://localhost:5000//login'

   Response:
   {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozMTMxLCJleHAiOjE3NTE5ODI4MjV9.xS70L5DGsUSADj507avUEmnhHsumRbZqTwEYigZhEUs"
   }

2. Create VPC & Subnet
   API -> http://localhost:5000/aws/api/v1/create-vpc
   In body you need to provide cidr_block, region & number of subnet to create. You also need to provide Authorization header with Bearer token received from Authentication API

   Request:
   curl -XPOST -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozMTMxLCJleHAiOjE3NTE5ODI4MjV9.xS70L5DGsUSADj507avUEmnhHsumRbZqTwEYigZhEUs' -H "Content-type: application/json" -d '{
    "cidr_block": "192.168.0.0/24",
    "region": "ap-south-1",
    "num_subnets": 2
  }' 'http://localhost:5000/aws/api/v1/create-vpc'

     Response:
     {
       "subnets": [
         {
           "AvailabilityZone": "ap-south-1b",
           "CidrBlock": "192.168.0.0/25",
           "SubnetId": "subnet-066afc5507ee2a54d"
         },
         {
           "AvailabilityZone": "ap-south-1b",
           "CidrBlock": "192.168.0.128/25",
           "SubnetId": "subnet-02884ff9a23c59132"
         }
       ],
       "vpc_id": "vpc-0a31061e38bc70016"
     }

3. Get VPC details
   API -> http://localhost:5000/aws/api/v1/<region>/vpc/<vpc-id>
   In URL you need to provide region & vpc id. ou also need to provide Authorization header with Bearer token received from Authentication API

   Request:
   curl -XGET -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozMTMxLCJleHAiOjE3NTE5ODI4MjV9.xS70L5DGsUSADj507avUEmnhHsumRbZqTwEYigZhEUs' 'http://localhost:5000/aws/api/v1/ap-south-1/vpc/vpc-0a31061e38bc70016'

   Response:
   {
  "subnets": [
    {
      "AssignIpv6AddressOnCreation": false,
      "AvailabilityZone": "ap-south-1b",
      "AvailabilityZoneId": "aps1-az3",
      "AvailableIpAddressCount": 123,
      "BlockPublicAccessStates": {
        "InternetGatewayBlockMode": "off"
      },
      "CidrBlock": "192.168.0.0/25",
      "DefaultForAz": false,
      "EnableDns64": false,
      "Ipv6CidrBlockAssociationSet": [],
      "Ipv6Native": false,
      "MapCustomerOwnedIpOnLaunch": false,
      "MapPublicIpOnLaunch": false,
      "OwnerId": "531160786080",
      "PrivateDnsNameOptionsOnLaunch": {
        "EnableResourceNameDnsAAAARecord": false,
        "EnableResourceNameDnsARecord": false,
        "HostnameType": "ip-name"
      },
      "State": "available",
      "SubnetArn": "arn:aws:ec2:ap-south-1:531160786080:subnet/subnet-066afc5507ee2a54d",
      "SubnetId": "subnet-066afc5507ee2a54d",
      "Tags": [
        {
          "Key": "vpc-id",
          "Value": "vpc-0a31061e38bc70016"
        }
      ],
      "VpcId": "vpc-0a31061e38bc70016"
    },
    {
      "AssignIpv6AddressOnCreation": false,
      "AvailabilityZone": "ap-south-1b",
      "AvailabilityZoneId": "aps1-az3",
      "AvailableIpAddressCount": 123,
      "BlockPublicAccessStates": {
        "InternetGatewayBlockMode": "off"
      },
      "CidrBlock": "192.168.0.128/25",
      "DefaultForAz": false,
      "EnableDns64": false,
      "Ipv6CidrBlockAssociationSet": [],
      "Ipv6Native": false,
      "MapCustomerOwnedIpOnLaunch": false,
      "MapPublicIpOnLaunch": false,
      "OwnerId": "531160786080",
      "PrivateDnsNameOptionsOnLaunch": {
        "EnableResourceNameDnsAAAARecord": false,
        "EnableResourceNameDnsARecord": false,
        "HostnameType": "ip-name"
      },
      "State": "available",
      "SubnetArn": "arn:aws:ec2:ap-south-1:531160786080:subnet/subnet-02884ff9a23c59132",
      "SubnetId": "subnet-02884ff9a23c59132",
      "Tags": [
        {
          "Key": "vpc-id",
          "Value": "vpc-0a31061e38bc70016"
        }
      ],
      "VpcId": "vpc-0a31061e38bc70016"
    }
  ],
  "vpc": {
    "BlockPublicAccessStates": {
      "InternetGatewayBlockMode": "off"
    },
    "CidrBlock": "192.168.0.0/24",
    "CidrBlockAssociationSet": [
      {
        "AssociationId": "vpc-cidr-assoc-03a9a148e9066d75d",
        "CidrBlock": "192.168.0.0/24",
        "CidrBlockState": {
          "State": "associated"
        }
      }
    ],
    "DhcpOptionsId": "dopt-0423948317767b37a",
    "InstanceTenancy": "default",
    "IsDefault": false,
    "OwnerId": "531160786080",
    "State": "available",
    "Tags": [
      {
        "Key": "Region",
        "Value": "ap-south-1"
      }
    ],
    "VpcId": "vpc-0a31061e38bc70016"
  }
}

   


   


