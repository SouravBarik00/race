#!/bin/bash

# AWS Web Games Collection Deployment Script
# This script deploys the entire infrastructure and applications to AWS

set -e

# Configuration
PROJECT_NAME="web-games"
AWS_REGION="us-east-1"
ENVIRONMENT="prod"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        error "AWS CLI is not installed. Please install it first."
    fi
    
    # Check Terraform
    if ! command -v terraform &> /dev/null; then
        error "Terraform is not installed. Please install it first."
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install it first."
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        error "AWS credentials not configured. Please run 'aws configure'."
    fi
    
    success "All prerequisites met"
}

# Create S3 bucket for Terraform state
create_terraform_backend() {
    log "Setting up Terraform backend..."
    
    BUCKET_NAME="${PROJECT_NAME}-terraform-state-$(date +%s)"
    TABLE_NAME="terraform-state-lock"
    
    # Create S3 bucket
    aws s3 mb s3://${BUCKET_NAME} --region ${AWS_REGION} || true
    
    # Enable versioning
    aws s3api put-bucket-versioning \
        --bucket ${BUCKET_NAME} \
        --versioning-configuration Status=Enabled
    
    # Enable encryption
    aws s3api put-bucket-encryption \
        --bucket ${BUCKET_NAME} \
        --server-side-encryption-configuration '{
            "Rules": [
                {
                    "ApplyServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "AES256"
                    }
                }
            ]
        }'
    
    # Create DynamoDB table for state locking
    aws dynamodb create-table \
        --table-name ${TABLE_NAME} \
        --attribute-definitions AttributeName=LockID,AttributeType=S \
        --key-schema AttributeName=LockID,KeyType=HASH \
        --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
        --region ${AWS_REGION} || true
    
    # Update Terraform backend configuration
    sed -i "s/web-games-terraform-state/${BUCKET_NAME}/g" ../terraform/main.tf
    
    success "Terraform backend created: ${BUCKET_NAME}"
}

# Build and push Docker images
build_and_push_images() {
    log "Building and pushing Docker images..."
    
    # Get AWS account ID
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    ECR_REGISTRY="${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    
    # Create ECR repositories
    for service in bike-race temperature-dashboard db-viewer; do
        aws ecr create-repository \
            --repository-name ${PROJECT_NAME}/${service} \
            --region ${AWS_REGION} || true
    done
    
    # Login to ECR
    aws ecr get-login-password --region ${AWS_REGION} | \
        docker login --username AWS --password-stdin ${ECR_REGISTRY}
    
    # Build and push bike-race image
    log "Building bike-race image..."
    cd ../docker/bike-race
    docker build -t ${ECR_REGISTRY}/${PROJECT_NAME}/bike-race:latest .
    docker push ${ECR_REGISTRY}/${PROJECT_NAME}/bike-race:latest
    cd ../../scripts
    
    # Build and push temperature-dashboard image
    log "Building temperature-dashboard image..."
    cd ../docker/temperature-dashboard
    docker build -t ${ECR_REGISTRY}/${PROJECT_NAME}/temperature-dashboard:latest .
    docker push ${ECR_REGISTRY}/${PROJECT_NAME}/temperature-dashboard:latest
    cd ../../scripts
    
    # Build and push db-viewer image
    log "Building db-viewer image..."
    cd ../docker/db-viewer
    docker build -t ${ECR_REGISTRY}/${PROJECT_NAME}/db-viewer:latest .
    docker push ${ECR_REGISTRY}/${PROJECT_NAME}/db-viewer:latest
    cd ../../scripts
    
    success "All Docker images built and pushed"
}

# Deploy infrastructure with Terraform
deploy_infrastructure() {
    log "Deploying infrastructure with Terraform..."
    
    cd ../terraform
    
    # Initialize Terraform
    terraform init
    
    # Plan deployment
    terraform plan -var="aws_region=${AWS_REGION}" -var="environment=${ENVIRONMENT}"
    
    # Apply deployment
    terraform apply -var="aws_region=${AWS_REGION}" -var="environment=${ENVIRONMENT}" -auto-approve
    
    cd ../scripts
    
    success "Infrastructure deployed successfully"
}

# Deploy applications to ECS
deploy_applications() {
    log "Deploying applications to ECS..."
    
    # Get infrastructure outputs
    cd ../terraform
    VPC_ID=$(terraform output -raw vpc_id)
    PRIVATE_SUBNET_IDS=$(terraform output -json private_subnet_ids | jq -r '.[]' | tr '\n' ',' | sed 's/,$//')
    ECS_SECURITY_GROUP_ID=$(terraform output -raw security_group_ecs_id)
    RDS_ENDPOINT=$(terraform output -raw rds_endpoint)
    DB_SECRET_ARN=$(terraform output -raw db_secret_arn)
    cd ../scripts
    
    # Get AWS account ID
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    ECR_REGISTRY="${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    
    # Create ECS cluster
    aws ecs create-cluster \
        --cluster-name ${PROJECT_NAME}-cluster \
        --capacity-providers FARGATE FARGATE_SPOT \
        --default-capacity-provider-strategy capacityProvider=FARGATE,weight=1 capacityProvider=FARGATE_SPOT,weight=1 \
        --region ${AWS_REGION} || true
    
    # Create task execution role
    create_ecs_roles
    
    # Deploy bike-race service
    deploy_ecs_service "bike-race" "5001" "${ECR_REGISTRY}/${PROJECT_NAME}/bike-race:latest"
    
    # Deploy temperature-dashboard service
    deploy_ecs_service "temperature-dashboard" "5002" "${ECR_REGISTRY}/${PROJECT_NAME}/temperature-dashboard:latest"
    
    # Deploy db-viewer service
    deploy_ecs_service "db-viewer" "5003" "${ECR_REGISTRY}/${PROJECT_NAME}/db-viewer:latest"
    
    success "Applications deployed to ECS"
}

# Create ECS IAM roles
create_ecs_roles() {
    log "Creating ECS IAM roles..."
    
    # Task execution role
    aws iam create-role \
        --role-name ${PROJECT_NAME}-ecs-task-execution-role \
        --assume-role-policy-document '{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ecs-tasks.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }' || true
    
    # Attach policies to execution role
    aws iam attach-role-policy \
        --role-name ${PROJECT_NAME}-ecs-task-execution-role \
        --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
    
    # Task role
    aws iam create-role \
        --role-name ${PROJECT_NAME}-ecs-task-role \
        --assume-role-policy-document '{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ecs-tasks.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }' || true
    
    success "ECS IAM roles created"
}

# Deploy individual ECS service
deploy_ecs_service() {
    local SERVICE_NAME=$1
    local PORT=$2
    local IMAGE_URI=$3
    
    log "Deploying ${SERVICE_NAME} service..."
    
    # Get AWS account ID
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    
    # Create task definition
    cat > /tmp/${SERVICE_NAME}-task-definition.json << EOF
{
    "family": "${PROJECT_NAME}-${SERVICE_NAME}",
    "networkMode": "awsvpc",
    "requiresCompatibilities": ["FARGATE"],
    "cpu": "512",
    "memory": "1024",
    "executionRoleArn": "arn:aws:iam::${ACCOUNT_ID}:role/${PROJECT_NAME}-ecs-task-execution-role",
    "taskRoleArn": "arn:aws:iam::${ACCOUNT_ID}:role/${PROJECT_NAME}-ecs-task-role",
    "containerDefinitions": [
        {
            "name": "${SERVICE_NAME}",
            "image": "${IMAGE_URI}",
            "portMappings": [
                {
                    "containerPort": ${PORT},
                    "protocol": "tcp"
                }
            ],
            "essential": true,
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/${PROJECT_NAME}-${SERVICE_NAME}",
                    "awslogs-region": "${AWS_REGION}",
                    "awslogs-stream-prefix": "ecs"
                }
            },
            "environment": [
                {
                    "name": "FLASK_ENV",
                    "value": "production"
                },
                {
                    "name": "DATABASE_URL",
                    "value": "postgresql://webgames_admin:password@${RDS_ENDPOINT}:5432/webgames"
                }
            ],
            "healthCheck": {
                "command": ["CMD-SHELL", "curl -f http://localhost:${PORT}/health || exit 1"],
                "interval": 30,
                "timeout": 5,
                "retries": 3,
                "startPeriod": 60
            }
        }
    ]
}
EOF
    
    # Create CloudWatch log group
    aws logs create-log-group \
        --log-group-name "/ecs/${PROJECT_NAME}-${SERVICE_NAME}" \
        --region ${AWS_REGION} || true
    
    # Register task definition
    aws ecs register-task-definition \
        --cli-input-json file:///tmp/${SERVICE_NAME}-task-definition.json \
        --region ${AWS_REGION}
    
    # Create service
    aws ecs create-service \
        --cluster ${PROJECT_NAME}-cluster \
        --service-name ${SERVICE_NAME}-service \
        --task-definition ${PROJECT_NAME}-${SERVICE_NAME} \
        --desired-count 2 \
        --launch-type FARGATE \
        --network-configuration "awsvpcConfiguration={subnets=[${PRIVATE_SUBNET_IDS}],securityGroups=[${ECS_SECURITY_GROUP_ID}],assignPublicIp=DISABLED}" \
        --region ${AWS_REGION} || true
    
    success "${SERVICE_NAME} service deployed"
}

# Setup monitoring and alarms
setup_monitoring() {
    log "Setting up monitoring and alarms..."
    
    # Create CloudWatch dashboard
    aws cloudwatch put-dashboard \
        --dashboard-name "${PROJECT_NAME}-dashboard" \
        --dashboard-body '{
            "widgets": [
                {
                    "type": "metric",
                    "properties": {
                        "metrics": [
                            ["AWS/ECS", "CPUUtilization", "ServiceName", "bike-race-service", "ClusterName", "'${PROJECT_NAME}'-cluster"],
                            [".", "MemoryUtilization", ".", ".", ".", "."],
                            ["AWS/ApplicationELB", "TargetResponseTime", "LoadBalancer", "'${PROJECT_NAME}'-alb"]
                        ],
                        "period": 300,
                        "stat": "Average",
                        "region": "'${AWS_REGION}'",
                        "title": "Application Metrics"
                    }
                }
            ]
        }' \
        --region ${AWS_REGION}
    
    success "Monitoring setup complete"
}

# Main deployment function
main() {
    log "Starting AWS Web Games Collection deployment..."
    
    check_prerequisites
    create_terraform_backend
    build_and_push_images
    deploy_infrastructure
    deploy_applications
    setup_monitoring
    
    success "🎉 Deployment completed successfully!"
    log "Your Web Games Collection is now running on AWS!"
    log "Check the AWS Console for service endpoints and monitoring dashboards."
}

# Run main function
main "$@"
