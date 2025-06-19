# 🚀 AWS Deployment Guide - Web Games Collection

## 🏗️ Architecture Overview

This deployment creates a production-ready, secure, and scalable AWS infrastructure for the Web Games Collection (excluding snake game) with the following components:

### 🌐 **Frontend & CDN**
- **Amazon CloudFront**: Global CDN with SSL/TLS termination
- **AWS WAF**: Web Application Firewall for security
- **S3 Static Hosting**: Frontend assets and static content

### 🖥️ **Application Layer**
- **Application Load Balancer**: Traffic distribution and SSL termination
- **Amazon ECS Fargate**: Containerized applications (serverless containers)
- **Auto Scaling**: Automatic scaling based on demand
- **Service Discovery**: AWS Cloud Map for service communication

### 🗄️ **Database Layer**
- **Amazon RDS PostgreSQL**: Multi-AZ primary database
- **Read Replica**: Read scaling and backup redundancy
- **Encryption**: At-rest and in-transit encryption
- **Automated Backups**: Point-in-time recovery

### 📦 **Storage & Code**
- **Amazon S3**: Code repository, static assets, backups
- **Amazon ECR**: Docker container registry
- **Versioning**: Code and asset versioning

### 🔒 **Security & Monitoring**
- **AWS Secrets Manager**: Secure credential storage
- **CloudWatch**: Comprehensive monitoring and logging
- **AWS Config**: Compliance and configuration management
- **GuardDuty**: Threat detection and security monitoring

---

## 🛠️ Prerequisites

### 1. **AWS Account Setup**
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS credentials
aws configure
# Enter your AWS Access Key ID, Secret Access Key, Region (us-east-1), and output format (json)
```

### 2. **Install Required Tools**
```bash
# Install Terraform
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Install Docker
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Install jq (JSON processor)
sudo apt install jq
```

### 3. **Verify Prerequisites**
```bash
aws --version
terraform --version
docker --version
jq --version
```

---

## 🚀 Deployment Steps

### **Option 1: Automated Deployment (Recommended)**

```bash
# Navigate to deployment directory
cd aws-deployment/scripts

# Run automated deployment
./deploy.sh
```

The automated script will:
1. ✅ Check all prerequisites
2. 🏗️ Create Terraform backend (S3 + DynamoDB)
3. 🐳 Build and push Docker images to ECR
4. 🌐 Deploy infrastructure with Terraform
5. 🚀 Deploy applications to ECS Fargate
6. 📊 Setup monitoring and alarms

### **Option 2: Manual Step-by-Step Deployment**

#### **Step 1: Setup Terraform Backend**
```bash
# Create S3 bucket for Terraform state
aws s3 mb s3://web-games-terraform-state-$(date +%s) --region us-east-1

# Create DynamoDB table for state locking
aws dynamodb create-table \
    --table-name terraform-state-lock \
    --attribute-definitions AttributeName=LockID,AttributeType=S \
    --key-schema AttributeName=LockID,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --region us-east-1
```

#### **Step 2: Deploy Infrastructure**
```bash
cd aws-deployment/terraform

# Initialize Terraform
terraform init

# Plan deployment
terraform plan

# Apply deployment
terraform apply
```

#### **Step 3: Build and Push Docker Images**
```bash
# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REGISTRY="${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com"

# Create ECR repositories
aws ecr create-repository --repository-name web-games/bike-race --region us-east-1
aws ecr create-repository --repository-name web-games/temperature-dashboard --region us-east-1
aws ecr create-repository --repository-name web-games/db-viewer --region us-east-1

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_REGISTRY

# Build and push images
cd aws-deployment/docker/bike-race
docker build -t $ECR_REGISTRY/web-games/bike-race:latest .
docker push $ECR_REGISTRY/web-games/bike-race:latest
```

#### **Step 4: Deploy Applications to ECS**
```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name web-games-cluster --region us-east-1

# Deploy services (use provided task definitions)
aws ecs create-service --cli-input-json file://bike-race-service.json
```

---

## 🌐 Access Your Applications

After successful deployment, your applications will be available at:

### **Production URLs**
- **🏍️ Bike Race Game**: `https://your-cloudfront-domain.cloudfront.net/bike-race`
- **🌡️ Temperature Dashboard**: `https://your-cloudfront-domain.cloudfront.net/temperature`
- **📊 Database Viewer**: `https://your-cloudfront-domain.cloudfront.net/db-viewer`

### **Direct ALB URLs** (for testing)
- **Application Load Balancer**: `https://your-alb-dns-name.us-east-1.elb.amazonaws.com`

### **API Endpoints**
- **Database API**: `https://your-domain/api/database-data`
- **Bike Race API**: `https://your-domain/api/bike-race`
- **Temperature API**: `https://your-domain/api/temperature`

---

## 📊 Monitoring and Management

### **AWS Console Access**
1. **ECS Console**: Monitor container health and scaling
2. **RDS Console**: Database performance and backups
3. **CloudWatch**: Metrics, logs, and alarms
4. **CloudFront**: CDN performance and caching

### **Key Metrics to Monitor**
- **ECS CPU/Memory Utilization**: Target < 80%
- **RDS Connections**: Monitor connection pool
- **ALB Response Time**: Target < 2 seconds
- **CloudFront Cache Hit Ratio**: Target > 85%

### **Log Locations**
```bash
# View ECS logs
aws logs describe-log-groups --log-group-name-prefix "/ecs/web-games"

# View specific service logs
aws logs get-log-events --log-group-name "/ecs/web-games-bike-race" --log-stream-name "ecs/bike-race/task-id"
```

---

## 🔒 Security Features Implemented

### **Network Security**
✅ **VPC with Private Subnets**: Applications isolated from internet
✅ **Security Groups**: Restrictive inbound/outbound rules
✅ **NAT Gateways**: Secure outbound internet access
✅ **SSL/TLS Everywhere**: End-to-end encryption

### **Data Security**
✅ **RDS Encryption**: KMS encryption at rest
✅ **S3 Encryption**: Server-side encryption
✅ **Secrets Manager**: Secure credential storage
✅ **IAM Least Privilege**: Minimal required permissions

### **Application Security**
✅ **WAF Protection**: SQL injection, XSS protection
✅ **DDoS Protection**: AWS Shield Standard
✅ **Container Security**: Non-root user, minimal base images
✅ **Health Checks**: Automatic unhealthy instance replacement

---

## 💰 Cost Optimization

### **Estimated Monthly Costs** (us-east-1)
- **ECS Fargate**: ~$50-100 (2-4 tasks)
- **RDS PostgreSQL**: ~$30-60 (db.t3.medium + replica)
- **Application Load Balancer**: ~$20
- **CloudFront**: ~$5-15 (depending on traffic)
- **S3 Storage**: ~$5-10
- **Data Transfer**: ~$10-20
- **Total**: ~$120-225/month

### **Cost Optimization Features**
✅ **Fargate Spot**: 50% cost reduction for non-critical workloads
✅ **RDS Reserved Instances**: Up to 60% savings
✅ **S3 Intelligent Tiering**: Automatic cost optimization
✅ **CloudFront Caching**: Reduced origin requests

---

## 🔧 Troubleshooting

### **Common Issues**

#### **1. ECS Tasks Not Starting**
```bash
# Check task definition
aws ecs describe-tasks --cluster web-games-cluster --tasks task-id

# Check logs
aws logs get-log-events --log-group-name "/ecs/web-games-bike-race"
```

#### **2. Database Connection Issues**
```bash
# Check RDS status
aws rds describe-db-instances --db-instance-identifier web-games-primary-db

# Test connectivity from ECS
aws ecs execute-command --cluster web-games-cluster --task task-id --container bike-race --interactive --command "/bin/bash"
```

#### **3. Load Balancer Health Check Failures**
```bash
# Check target group health
aws elbv2 describe-target-health --target-group-arn your-target-group-arn

# Check security group rules
aws ec2 describe-security-groups --group-ids sg-xxxxxxxxx
```

### **Useful Commands**
```bash
# Scale ECS service
aws ecs update-service --cluster web-games-cluster --service bike-race-service --desired-count 4

# View CloudWatch metrics
aws cloudwatch get-metric-statistics --namespace AWS/ECS --metric-name CPUUtilization

# Check Terraform state
terraform show
terraform state list
```

---

## 🔄 Updates and Maintenance

### **Application Updates**
```bash
# Build new image
docker build -t $ECR_REGISTRY/web-games/bike-race:v2.0 .
docker push $ECR_REGISTRY/web-games/bike-race:v2.0

# Update ECS service
aws ecs update-service --cluster web-games-cluster --service bike-race-service --force-new-deployment
```

### **Infrastructure Updates**
```bash
cd aws-deployment/terraform
terraform plan
terraform apply
```

### **Database Maintenance**
- **Automated Backups**: Daily backups with 7-day retention
- **Maintenance Window**: Sundays 3:00-4:00 AM UTC
- **Security Updates**: Automatic minor version updates

---

## 🆘 Support and Resources

### **AWS Documentation**
- [ECS Fargate Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html)
- [RDS PostgreSQL Guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html)
- [CloudFront Guide](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/)

### **Terraform Resources**
- [AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)

### **Emergency Contacts**
- **AWS Support**: Available through AWS Console
- **Infrastructure Issues**: Check CloudWatch alarms and logs
- **Application Issues**: Review ECS service logs

---

## 🎯 Next Steps

After successful deployment:

1. **🔗 Setup Custom Domain**: Configure Route 53 and SSL certificates
2. **📈 Performance Tuning**: Optimize based on CloudWatch metrics
3. **🔒 Security Hardening**: Regular security assessments
4. **📊 Advanced Monitoring**: Setup custom dashboards and alerts
5. **🚀 CI/CD Pipeline**: Implement automated deployments
6. **💾 Backup Strategy**: Test disaster recovery procedures

---

**🎉 Congratulations! Your Web Games Collection is now running securely and scalably on AWS!**
