#------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------
#!/bin/bash
#--- Installing all the necessary packets ---
echo '------------------------ Installing all the necessary packets ------------------------'
sudo yum -y update
sudo yum install git mysql python36 mysql-devel python36-devel.x86_64 gcc -y
mkdir /home/ec2-user/project_repo
cd /home/ec2-user/project_repo
sudo git clone https://github.com/jjulianprin/FlaskProject.git
sudo cat /home/ec2-user/project_repo/FlaskProject/ormuco_rsa.pub >> /home/ec2-user/.ssh/authorized_keys
#
#
#'------------------------ Setting DB Up ------------------------' 
echo '------------------------ Configuring MySQL ------------------------'
#------- Table creation and configuration for first-time implementation
mysql -h  DatabaseEndpoint -P3306 -u admin -pqa12pl09 -e "CREATE DATABASE usersnpets"
#mysql -h DatabaseEndpoint -P3306 -u admin -pqa12pl09 -e "drop table if exists usersnpets.users;"
mysql -h DatabaseEndpoint -P3306 -u admin -pqa12pl09 -e "CREATE TABLE usersnpets.users (name VARCHAR(50), color VARCHAR(30), pet VARCHAR(5), PRIMARY KEY (name));"
export MYSQLHostAddress=DatabaseEndpoint
#
#
#
echo '------------------------ Setting Virtual Environment Up ------------------------'
#
cd /home/ec2-user/project_repo/FlaskProject
sudo chmod 777 /home/ec2-user/project_repo/FlaskProject
python3 -m venv venv
source venv/bin/activate
echo '------------------------ Inside Virtual Environment ------------------------'
pip3 install -r requirements.txt
python3 src/App.py &
#
echo '------------------------ Deployment Finished ------------------------'
#
#
#
#
