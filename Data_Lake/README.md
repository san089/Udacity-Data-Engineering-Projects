


## Deployement

If you are using local as your development environemnt - Moving project directory from local to EMR 


 

     scp -i <.pem-file> <Local-Path> <username>@<EMR-MasterNode-Endpoint>:~<EMR-path>

Running spark job (Before running job make sure EMR Role have access to s3)

    spark-submit etl.py --master yarn --deploy-mode client --driver-memory 4g --num-executors 2 --executor-memory 2g --executor-core 2

