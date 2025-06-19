# 🏗️ AWS Architecture Design - Web Games Collection

## 🎯 Architecture Overview

This architecture implements a secure, scalable, and highly available deployment of the Web Games Collection on AWS, excluding the snake game. The design follows AWS Well-Architected Framework principles with emphasis on security, reliability, and performance.

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                    INTERNET                                     │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              AWS CLOUDFRONT (CDN)                              │
│  • Global Content Delivery Network                                             │
│  • SSL/TLS Termination                                                         │
│  • DDoS Protection (AWS Shield Standard)                                       │
│  • Web Application Firewall (WAF)                                              │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        APPLICATION LOAD BALANCER (ALB)                         │
│  • SSL/TLS Termination                                                         │
│  • Health Checks                                                               │
│  • Target Group Routing                                                        │
│  • Security Groups                                                             │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
        ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
        │   AZ-1a (US)    │ │   AZ-1b (US)    │ │   AZ-1c (US)    │
        └─────────────────┘ └─────────────────┘ └─────────────────┘
                    │                   │                   │
                    ▼                   ▼                   ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              ECS FARGATE CLUSTER                               │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │  🏍️ BIKE RACE   │  │ 🌡️ TEMPERATURE  │  │ 📊 DB VIEWER    │                │
│  │   SERVICE       │  │   SERVICE       │  │   SERVICE       │                │
│  │                 │  │                 │  │                 │                │
│  │ • Auto Scaling  │  │ • Auto Scaling  │  │ • Auto Scaling  │                │
│  │ • Health Checks │  │ • Health Checks │  │ • Health Checks │                │
│  │ • Service Mesh  │  │ • Service Mesh  │  │ • Service Mesh  │                │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATABASE LAYER                                    │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        AMAZON RDS (PostgreSQL)                         │   │
│  │                                                                         │   │
│  │  ┌─────────────────┐              ┌─────────────────┐                  │   │
│  │  │   PRIMARY DB    │    ────────► │   READ REPLICA  │                  │   │
│  │  │   (AZ-1a)       │              │   (AZ-1b)       │                  │   │
│  │  │                 │              │                 │                  │   │
│  │  │ • Multi-AZ      │              │ • Read Scaling  │                  │   │
│  │  │ • Automated     │              │ • Backup        │                  │   │
│  │  │   Backups       │              │   Redundancy    │                  │   │
│  │  │ • Encryption    │              │ • Encryption    │                  │   │
│  │  └─────────────────┘              └─────────────────┘                  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              STORAGE LAYER                                     │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │   S3 BUCKET     │  │   S3 BUCKET     │  │   S3 BUCKET     │                │
│  │  (CODE REPO)    │  │  (STATIC WEB)   │  │   (BACKUPS)     │                │
│  │                 │  │                 │  │                 │                │
│  │ • Source Code   │  │ • HTML/CSS/JS   │  │ • DB Backups    │                │
│  │ • Docker Images │  │ • Game Assets   │  │ • Log Archives  │                │
│  │ • Versioning    │  │ • CDN Origin    │  │ • Versioning    │                │
│  │ • Encryption    │  │ • Encryption    │  │ • Encryption    │                │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            MONITORING & SECURITY                               │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │   CLOUDWATCH    │  │   AWS SECRETS   │  │      IAM        │                │
│  │                 │  │    MANAGER      │  │                 │                │
│  │ • Metrics       │  │                 │  │ • Roles         │                │
│  │ • Logs          │  │ • DB Passwords  │  │ • Policies      │                │
│  │ • Alarms        │  │ • API Keys      │  │ • MFA           │                │
│  │ • Dashboards    │  │ • Certificates  │  │ • Least Priv.   │                │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │   AWS CONFIG    │  │   CLOUDTRAIL    │  │   GUARDDUTY     │                │
│  │                 │  │                 │  │                 │                │
│  │ • Compliance    │  │ • API Logging   │  │ • Threat        │                │
│  │ • Config Rules  │  │ • Audit Trail   │  │   Detection     │                │
│  │ • Remediation   │  │ • Governance    │  │ • ML Security   │                │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🏗️ Detailed Component Architecture

### 1. **Frontend Layer**

#### **Amazon CloudFront (CDN)**
```yaml
Configuration:
  - Global Edge Locations: 400+ worldwide
  - SSL/TLS: AWS Certificate Manager (ACM)
  - Security Headers: HSTS, CSP, X-Frame-Options
  - Caching Strategy: Static assets (1 year), Dynamic content (5 min)
  - Compression: Gzip/Brotli enabled
  - Origin Shield: Enabled for better cache hit ratio
```

#### **Static Website Hosting (S3)**
```yaml
S3 Bucket Configuration:
  - Bucket Name: web-games-frontend-prod
  - Static Website Hosting: Enabled
  - Public Access: Blocked (CloudFront only)
  - Versioning: Enabled
  - Encryption: AES-256 (SSE-S3)
  - Lifecycle Policy: Delete old versions after 90 days
```

### 2. **Application Layer**

#### **Application Load Balancer (ALB)**
```yaml
Configuration:
  - Scheme: Internet-facing
  - IP Address Type: IPv4/IPv6 dual-stack
  - Security Groups: HTTPS (443), HTTP (80) → HTTPS redirect
  - SSL Policy: ELBSecurityPolicy-TLS-1-2-2017-01
  - Target Groups:
    - bike-race-tg: Port 5001
    - temperature-tg: Port 5002
    - db-viewer-tg: Port 5003
```

#### **Amazon ECS Fargate**
```yaml
Cluster Configuration:
  - Name: web-games-cluster
  - Capacity Providers: FARGATE, FARGATE_SPOT
  - Container Insights: Enabled
  - Service Discovery: AWS Cloud Map

Services:
  bike-race-service:
    - Task Definition: bike-race-task:latest
    - Desired Count: 2
    - Min Capacity: 1
    - Max Capacity: 10
    - CPU: 512 (0.5 vCPU)
    - Memory: 1024 MB
    - Auto Scaling: Target CPU 70%
    
  temperature-service:
    - Task Definition: temperature-task:latest
    - Desired Count: 2
    - Min Capacity: 1
    - Max Capacity: 5
    - CPU: 256 (0.25 vCPU)
    - Memory: 512 MB
    - Auto Scaling: Target CPU 70%
    
  db-viewer-service:
    - Task Definition: db-viewer-task:latest
    - Desired Count: 1
    - Min Capacity: 1
    - Max Capacity: 3
    - CPU: 256 (0.25 vCPU)
    - Memory: 512 MB
    - Auto Scaling: Target CPU 70%
```

### 3. **Database Layer**

#### **Amazon RDS PostgreSQL**
```yaml
Primary Database:
  - Engine: PostgreSQL 15.4
  - Instance Class: db.t3.medium
  - Multi-AZ: Enabled
  - Storage: 100 GB GP3 (Encrypted)
  - Backup Retention: 7 days
  - Maintenance Window: Sunday 03:00-04:00 UTC
  - Security Groups: Database access only from ECS
  
Read Replica:
  - Instance Class: db.t3.small
  - Cross-AZ: Yes
  - Read-only queries for analytics
  - Automated failover capability
```

### 4. **Storage Layer**

#### **Amazon S3 Buckets**
```yaml
Code Repository Bucket:
  - Name: web-games-code-repo-prod
  - Versioning: Enabled
  - Encryption: SSE-KMS
  - Access: Private (CodePipeline only)
  - Lifecycle: Archive to IA after 30 days
  
Static Assets Bucket:
  - Name: web-games-static-assets-prod
  - Versioning: Enabled
  - Encryption: SSE-S3
  - Access: CloudFront OAI only
  - CORS: Configured for web access
  
Backup Bucket:
  - Name: web-games-backups-prod
  - Versioning: Enabled
  - Encryption: SSE-KMS
  - Access: Backup services only
  - Lifecycle: Glacier after 30 days, Deep Archive after 90 days
```

## 🔒 Security Implementation

### 1. **Network Security**

#### **VPC Configuration**
```yaml
VPC:
  - CIDR: 10.0.0.0/16
  - DNS Hostnames: Enabled
  - DNS Resolution: Enabled
  
Public Subnets (ALB):
  - 10.0.1.0/24 (AZ-1a)
  - 10.0.2.0/24 (AZ-1b)
  - 10.0.3.0/24 (AZ-1c)
  
Private Subnets (ECS):
  - 10.0.11.0/24 (AZ-1a)
  - 10.0.12.0/24 (AZ-1b)
  - 10.0.13.0/24 (AZ-1c)
  
Database Subnets:
  - 10.0.21.0/24 (AZ-1a)
  - 10.0.22.0/24 (AZ-1b)
  - 10.0.23.0/24 (AZ-1c)
```

#### **Security Groups**
```yaml
ALB Security Group:
  Inbound:
    - Port 443 (HTTPS): 0.0.0.0/0
    - Port 80 (HTTP): 0.0.0.0/0 (redirect to HTTPS)
  Outbound:
    - All traffic to ECS Security Group

ECS Security Group:
  Inbound:
    - Port 5001-5003: ALB Security Group only
  Outbound:
    - Port 443: 0.0.0.0/0 (HTTPS)
    - Port 5432: Database Security Group

Database Security Group:
  Inbound:
    - Port 5432: ECS Security Group only
  Outbound:
    - None
```

### 2. **Identity and Access Management (IAM)**

#### **Service Roles**
```yaml
ECS Task Execution Role:
  Policies:
    - AmazonECSTaskExecutionRolePolicy
    - Custom policy for Secrets Manager access
    - Custom policy for CloudWatch Logs
    
ECS Task Role:
  Policies:
    - Custom policy for RDS access
    - Custom policy for S3 access (read-only)
    - Custom policy for Secrets Manager access

CodePipeline Role:
  Policies:
    - AWSCodePipelineFullAccess
    - Custom policy for S3 and ECR access
    - Custom policy for ECS deployment
```

### 3. **Data Encryption**

#### **Encryption at Rest**
```yaml
RDS:
  - Encryption: AWS KMS (Customer Managed Key)
  - Key Rotation: Annual
  - Backup Encryption: Enabled
  
S3:
  - Default Encryption: SSE-KMS
  - Bucket Key: Enabled (cost optimization)
  - Access Logging: Enabled
  
ECS:
  - Task Definition: Encryption in transit
  - Secrets: AWS Secrets Manager
  - Logs: CloudWatch Logs encryption
```

#### **Encryption in Transit**
```yaml
CloudFront:
  - Minimum TLS Version: 1.2
  - Cipher Suite: TLSv1.2_2021
  - HSTS: max-age=31536000; includeSubDomains
  
ALB:
  - SSL Policy: ELBSecurityPolicy-TLS-1-2-2017-01
  - Certificate: AWS Certificate Manager (ACM)
  - HTTP to HTTPS Redirect: Enabled
  
RDS:
  - SSL/TLS: Required
  - Certificate Verification: Enabled
```

### 4. **Web Application Firewall (WAF)**

#### **AWS WAF Rules**
```yaml
Managed Rule Groups:
  - AWSManagedRulesCommonRuleSet
  - AWSManagedRulesKnownBadInputsRuleSet
  - AWSManagedRulesSQLiRuleSet
  - AWSManagedRulesLinuxRuleSet
  - AWSManagedRulesUnixRuleSet

Custom Rules:
  - Rate Limiting: 2000 requests per 5 minutes per IP
  - Geographic Blocking: Block high-risk countries
  - IP Reputation: Block known malicious IPs
  - Size Restrictions: Limit request body size
```

## 📊 Monitoring and Observability

### 1. **Amazon CloudWatch**

#### **Metrics and Alarms**
```yaml
Application Metrics:
  - ECS CPU Utilization > 80%
  - ECS Memory Utilization > 85%
  - ALB Target Response Time > 2 seconds
  - ALB HTTP 5xx Error Rate > 5%
  - RDS CPU Utilization > 80%
  - RDS Database Connections > 80%

Custom Metrics:
  - Game Session Duration
  - User Registration Rate
  - Database Query Performance
  - API Response Times
```

#### **Log Aggregation**
```yaml
Log Groups:
  - /aws/ecs/bike-race-service
  - /aws/ecs/temperature-service
  - /aws/ecs/db-viewer-service
  - /aws/rds/postgresql/error
  - /aws/lambda/functions

Log Retention:
  - Application Logs: 30 days
  - Security Logs: 1 year
  - Audit Logs: 7 years
```

### 2. **AWS X-Ray**
```yaml
Distributed Tracing:
  - Service Map: End-to-end request flow
  - Performance Analysis: Latency bottlenecks
  - Error Analysis: Root cause identification
  - Sampling Rate: 10% of requests
```

## 🚀 CI/CD Pipeline

### 1. **AWS CodePipeline**

#### **Pipeline Stages**
```yaml
Source Stage:
  - GitHub Integration
  - Webhook Triggers
  - Branch: main
  
Build Stage:
  - AWS CodeBuild
  - Docker Image Build
  - Security Scanning (Snyk)
  - Unit Tests
  - Push to ECR
  
Deploy Stage:
  - ECS Service Update
  - Blue/Green Deployment
  - Health Checks
  - Rollback Capability
```

### 2. **AWS CodeBuild**
```yaml
Build Environment:
  - Image: aws/codebuild/amazonlinux2-x86_64-standard:3.0
  - Compute: BUILD_GENERAL1_MEDIUM
  - Privileged Mode: Enabled (for Docker)
  
Build Phases:
  - Pre-build: Install dependencies, login to ECR
  - Build: Docker build, run tests
  - Post-build: Push to ECR, update task definitions
```

## 💰 Cost Optimization

### 1. **Resource Optimization**
```yaml
ECS Fargate:
  - Spot Instances: 50% of capacity
  - Right-sizing: CPU/Memory optimization
  - Scheduled Scaling: Scale down during low usage
  
RDS:
  - Reserved Instances: 1-year term
  - Storage Optimization: GP3 instead of GP2
  - Read Replica: Scale based on read load
  
S3:
  - Intelligent Tiering: Automatic cost optimization
  - Lifecycle Policies: Archive old data
  - Request Optimization: CloudFront caching
```

### 2. **Cost Monitoring**
```yaml
AWS Cost Explorer:
  - Daily cost monitoring
  - Service-level cost breakdown
  - Forecasting and budgets
  
AWS Budgets:
  - Monthly budget alerts
  - Service-specific budgets
  - Cost anomaly detection
```

## 🔄 Disaster Recovery

### 1. **Backup Strategy**
```yaml
RDS Backups:
  - Automated Backups: 7 days retention
  - Manual Snapshots: Monthly
  - Cross-Region Replication: Enabled
  
S3 Backups:
  - Cross-Region Replication: Enabled
  - Versioning: 90 days retention
  - MFA Delete: Enabled for critical buckets
```

### 2. **Recovery Procedures**
```yaml
RTO (Recovery Time Objective): 4 hours
RPO (Recovery Point Objective): 1 hour

Failover Process:
  1. Promote Read Replica to Primary
  2. Update ECS service configuration
  3. Update DNS records
  4. Validate application functionality
```

## 📋 Implementation Checklist

### Phase 1: Infrastructure Setup (Week 1-2)
- [ ] Create VPC and networking components
- [ ] Set up RDS PostgreSQL with Multi-AZ
- [ ] Configure S3 buckets with proper policies
- [ ] Create IAM roles and policies
- [ ] Set up CloudFront distribution

### Phase 2: Application Deployment (Week 3-4)
- [ ] Containerize applications with Docker
- [ ] Create ECS task definitions
- [ ] Set up Application Load Balancer
- [ ] Configure ECS services with auto-scaling
- [ ] Implement health checks

### Phase 3: Security Hardening (Week 5)
- [ ] Configure WAF rules
- [ ] Set up Secrets Manager
- [ ] Enable encryption at rest and in transit
- [ ] Configure security groups and NACLs
- [ ] Set up GuardDuty and Config

### Phase 4: Monitoring and CI/CD (Week 6)
- [ ] Set up CloudWatch dashboards and alarms
- [ ] Configure X-Ray tracing
- [ ] Create CodePipeline for deployments
- [ ] Set up automated testing
- [ ] Configure backup and disaster recovery

### Phase 5: Testing and Go-Live (Week 7-8)
- [ ] Performance testing
- [ ] Security testing
- [ ] Load testing
- [ ] Disaster recovery testing
- [ ] Production deployment

## 💡 Best Practices Implemented

### Security
✅ **Defense in Depth**: Multiple security layers
✅ **Least Privilege**: Minimal required permissions
✅ **Encryption Everywhere**: Data at rest and in transit
✅ **Network Segmentation**: Private subnets for applications
✅ **Security Monitoring**: Real-time threat detection

### Reliability
✅ **Multi-AZ Deployment**: High availability
✅ **Auto Scaling**: Handle traffic spikes
✅ **Health Checks**: Automatic failure detection
✅ **Backup Strategy**: Multiple backup methods
✅ **Disaster Recovery**: Cross-region replication

### Performance
✅ **CDN**: Global content delivery
✅ **Caching**: Multiple caching layers
✅ **Database Optimization**: Read replicas
✅ **Container Optimization**: Right-sized resources
✅ **Load Balancing**: Traffic distribution

### Cost Optimization
✅ **Spot Instances**: Cost-effective compute
✅ **Reserved Instances**: Long-term savings
✅ **Storage Tiering**: Automatic cost optimization
✅ **Resource Monitoring**: Usage optimization
✅ **Scheduled Scaling**: Scale based on demand

This architecture provides a production-ready, secure, and scalable deployment of your Web Games Collection on AWS with comprehensive monitoring, automated deployments, and disaster recovery capabilities.
