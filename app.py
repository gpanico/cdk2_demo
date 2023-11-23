#!/usr/bin/python3

import aws_cdk as cdk
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_dynamodb as dynamodb
import aws_cdk.aws_lambda as _lambda
import aws_cdk.aws_sqs as sqs
import aws_cdk.aws_ses as ses
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as rds

from constructs import Construct

class TwoStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
       
	# Create an S3 bucketsf1
        my_bucket = s3.Bucket(self, "MyS3Bucket-asd9asdasdasdsadasdsadad", # specify a unique bucket name
           versioned=True,
           encryption=s3.BucketEncryption.S3_MANAGED,
           removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Create a DynamoDB table
        dynamodb_table = dynamodb.Table(self, 'MyDynamoDBTable',
            partition_key={'name': 'id', 'type': dynamodb.AttributeType.STRING},
            point_in_time_recovery=True,
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Create a Lambda function
        my_lambda = _lambda.Function(self, 'MyLambdaFunction',
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler='my_lambda.handler',
            code =_lambda.Code.from_asset(r'./lambda_source.py'),
        )

        # Create an SQS queue
        my_queue = sqs.Queue(self, "MySQSQueue",
            visibility_timeout=cdk.Duration.seconds(300),
            encryption=sqs.QueueEncryption.KMS_MANAGED,
        )

        # Create an SES identity (email address or domain)
        email_identity = ses.CfnEmailIdentity(self, "SESEmailIdentity", email_identity="cdk2_demo@mailinator.com")
 
        # get vpc from existing resource
        instance_class=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO)
        vpc=ec2.Vpc.from_vpc_attributes(self, vpc_label, vpc_id=vpc_id, availability_zones=['us-east-1a'])

        # Create an RDS PostgreSQL database
        rds_instance = rds.DatabaseInstance(self, 'MyRDSInstance',
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_13
            ),
            instance_type=instance_class,
            credentials=rds.Credentials.username(
                username=db_username,
                password=cdk.SecretValue.plain_text(db_password)
            ),
            vpc=vpc,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

