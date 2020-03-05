## Data Orchestration Pipeline Using Amazon EMR and Apache Livy
## Setting up Airflow using AWS CloudFormation script

![Airflow_Livy_Architecture](https://github.com/san089/Data_Engineering_Projects/blob/master/airflow_livy.png)

Script is available publically and can be imported from - https://s3.amazonaws.com/aws-bigdata-blog/artifacts/airflow.livy.emr/airflow.yaml 

**This requires access to an Amazon EC2 key pair in the AWS Region you’re launching your CloudFormation stack. Please make sure to create a key-pair in the AWS Region first. Follow : [create-your-key-pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#having-ec2-create-your-key-pair)** 

Steps to import:
1. Go to AWS Console -> Search for CloudFormation Service and open it.
2. Click on create stack -> Select **Template is Ready**
3. In the Amazon S3 URL paste the URL mentioned above.
4. This will load a template from `airflow.yaml`
5. Click Next -> Specify DBPassword and KeyName(the already existing key-pair) and S3BucketName (bucket should not be exisiting, it will automatically create a new bucket).
6. Click Next -> Next to run the stack. 

After the stack run is successfully completed, got to EC2 and you will see a new instance launched. Connect to instance using ssh connection. You can use putty or can connect using command line using ssh. 

[Connect to EC2 using putty](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html)

**Connect using ssh from command line**

    chmod  400 airflow_key_pair.pem 
    ssh  -i "airflow_key_pair.pem" ec2-user@ec2-your-public-ip.your-region.compute.amazonaws.com

After you are logged in: 
Run Command: 

    # sudo as the root user  
    sudo  su  
    
    export AIRFLOW_HOME=~/airflow
    # Navigate to the airflow directory which was created by the cloudformation template – Look at the user-data section.
    cd  ~/airflow 
    source  ~/.bash_profile

#### Airflow initialization and running webserver

    # initialise the SqlLite database, 
    # below command will pick changes from airflow.cfg
    airflow initdb
    
  Open two new terminals. One to start the web server (you can set the port as well) and the other for a scheduler
  

	# Run the webserver on the custom port you can specify
	# MAKE SURE THIS PORT IS SPECIFIED IN YOUR SECURITY GROUP FOR INBOUND TRAFFIC. READ BELOW ARTICLE FOR MORE DETAILS.
	
    airflow webserver --port=<your port number>
    
    # RUN THE SCHEDULER
    airflow scheduler


[Authorizing Access To An Instance](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/authorizing-access-to-an-instance.html)

#### Once the scheduler is running you can access airflow UI using your brower. 
To see the Airflow webserver, open any browser and type in the 

    <EC2-public-dns-name>:<your-port-number>


REFERENCES: 

[Build-a-concurrent-data-orchestration-pipeline-using-amazon-emr-and-apache-livy](https://aws.amazon.com/blogs/big-data/build-a-concurrent-data-orchestration-pipeline-using-amazon-emr-and-apache-livy/)

[Airflow Installation Steps](https://limitlessdatascience.wordpress.com/2019/10/01/apache-airflow-installation-steps/)
