# SentinelAI Deployment Guide - Step by Step

## Prerequisites
- EC2 instance running Amazon Linux 2023
- SSH key file: `~/Downloads/na.pem`
- EC2 IP: `16.176.229.177`

## Step 1: Upload Application Files

### 1.1 Upload Frontend
```bash
rsync -avz --exclude 'node_modules' --exclude '.git' --exclude '.next' \
-e "ssh -i ~/.ssh/na.pem" \
frontend/ ec2-user@16.176.229.177:/tmp/frontend/
```

### 1.2 Upload Compliance Agent
```bash
rsync -avz --exclude '__pycache__' --exclude '*.pyc' --exclude '.git' --exclude 'venv' \
-e "ssh -i ~/.ssh/na.pem" \
my_compliance_agent/ ec2-user@16.176.229.177:/tmp/my_compliance_agent/
```

## Step 2: Connect to EC2 Instance
```bash
ssh -i ~/.ssh/na.pem ec2-user@16.176.229.177
```

## Step 3: Setup Application Directories
```bash
# Create directories
sudo mkdir -p /opt/sentinelai /opt/compliance-agent

# Change ownership
sudo chown -R ec2-user:ec2-user /opt/sentinelai /opt/compliance-agent

# Move uploaded files
cp -r /tmp/frontend/* /opt/sentinelai/
cp -r /tmp/my_compliance_agent/* /opt/compliance-agent/
```

## Step 4: Install System Dependencies

### 4.1 Update System
```bash
sudo yum update -y
```

### 4.2 Clean Node.js Conflicts (if needed)
```bash
# Remove conflicting packages
sudo yum remove -y nodejs npm nodejs-npm nodejs-docs nodejs-libs nodejs-full-i18n

# Clean yum cache
sudo yum clean all
```

### 4.3 Install Node.js via NodeSource
```bash
# Add NodeSource repository
curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -

# Install Node.js and other dependencies
sudo yum install -y nodejs python3 python3-pip git jq
```

### 4.4 Verify Node.js Installation
```bash
node --version
npm --version
```

## Step 5: Install PM2 Process Manager
```bash
sudo npm install -g pm2
```

## Step 6: Setup Frontend Application

### 6.1 Install Dependencies
```bash
cd /opt/sentinelai
npm install
```

### 6.2 Build Application
```bash
npm run build
```

## Step 7: Setup Python Environment for Compliance Agent

### 7.1 Create Virtual Environment
```bash
cd /opt/compliance-agent
python3 -m venv venv
```

### 7.2 Activate and Install Dependencies
```bash
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 7.3 Test Python Environment
```bash
# Verify installation
source venv/bin/activate
python -c "import anthropic, boto3; print('Dependencies installed successfully')"
deactivate
```

## Step 8: Create PM2 Configuration

### 8.1 Create PM2 Config File
```bash
cat > /opt/sentinelai/ecosystem.config.js << 'EOF'
module.exports = {
  apps: [
    {
      name: 'sentinelai-frontend',
      script: 'npm',
      args: 'start',
      cwd: '/opt/sentinelai',
      instances: 1,
      exec_mode: 'fork',
      env: {
        NODE_ENV: 'production',
        PORT: 3000
      },
      log_file: '/var/log/pm2/frontend-combined.log',
      out_file: '/var/log/pm2/frontend-out.log',
      error_file: '/var/log/pm2/frontend-error.log',
      restart_delay: 4000,
      max_restarts: 10,
      min_uptime: '10s',
      max_memory_restart: '500M'
    },
    {
      name: 'compliance-agent',
      script: '/opt/compliance-agent/venv/bin/python',
      args: '/opt/compliance-agent/main.py',
      cwd: '/opt/compliance-agent',
      instances: 1,
      exec_mode: 'fork',
      env: {
        PYTHONPATH: '/opt/compliance-agent',
        VIRTUAL_ENV: '/opt/compliance-agent/venv'
      },
      log_file: '/var/log/pm2/agent-combined.log',
      out_file: '/var/log/pm2/agent-out.log',
      error_file: '/var/log/pm2/agent-error.log',
      restart_delay: 4000,
      max_restarts: 10,
      min_uptime: '10s',
      max_memory_restart: '1G'
    }
  ]
};
EOF
```

## Step 9: Setup PM2 Logging
```bash
sudo mkdir -p /var/log/pm2
sudo chown -R ec2-user:ec2-user /var/log/pm2
```

## Step 10: Start Services with PM2

### 10.1 Stop Any Existing PM2 Processes
```bash
pm2 delete all || true
```

### 10.2 Start Applications
```bash
cd /opt/sentinelai
pm2 start ecosystem.config.js
```

### 10.3 Save PM2 Configuration
```bash
pm2 save
```

### 10.4 Setup PM2 Auto-start
```bash
pm2 startup systemd -u ec2-user --hp /home/ec2-user
# Follow the instructions printed by the command above
```

## Step 11: Configure Firewall

### 11.1 Open Port 3000 (Frontend)
```bash
# Using firewall-cmd (if available)
sudo firewall-cmd --permanent --add-port=3000/tcp
sudo firewall-cmd --reload

# OR using iptables (if firewall-cmd not available)
sudo iptables -A INPUT -p tcp --dport 3000 -j ACCEPT
sudo service iptables save || echo "iptables service not available"
```

### 11.2 Ensure SSH Port is Open
```bash
sudo firewall-cmd --permanent --add-port=22/tcp || sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

## Step 12: Verify Deployment

### 12.1 Check PM2 Status
```bash
pm2 status
```

### 12.2 Check Application Logs
```bash
# View all logs
pm2 logs

# View specific service logs
pm2 logs sentinelai-frontend
pm2 logs compliance-agent
```

### 12.3 Test Frontend Access
```bash
# Check if frontend is responding
curl http://localhost:3000

# Check from external
curl http://3.107.179.60:3000
```

## Step 13: Access Your Application
Open your browser and navigate to:
```
http://3.107.179.60:3000
```

## Useful Management Commands

### Monitor Services
```bash
pm2 monit
```

### Restart Services
```bash
pm2 restart sentinelai-frontend
pm2 restart compliance-agent
pm2 restart all
```

### Stop Services
```bash
pm2 stop sentinelai-frontend
pm2 stop compliance-agent
pm2 stop all
```

### View Logs
```bash
pm2 logs --lines 50
pm2 logs sentinelai-frontend --lines 50
```

### Check System Resources
```bash
htop
df -h
free -h
```

## Troubleshooting

### If Frontend Won't Start
```bash
cd /opt/sentinelai
npm run build
pm2 restart sentinelai-frontend
pm2 logs sentinelai-frontend
```

### If Compliance Agent Won't Start
```bash
cd /opt/compliance-agent
source venv/bin/activate
python main.py  # Test manually
pm2 restart compliance-agent
pm2 logs compliance-agent
```

### If Port 3000 Not Accessible
```bash
# Check if service is listening
sudo netstat -tulpn | grep :3000

# Check firewall status
sudo firewall-cmd --list-all
# OR
sudo iptables -L
```

### Check EC2 Security Groups
Make sure your EC2 security group allows:
- Port 22 (SSH) from your IP
- Port 3000 (HTTP) from 0.0.0.0/0 or your IP

## Environment Variables (If Needed)
If your applications need environment variables, create `.env` files:

### For Frontend
```bash
cat > /opt/sentinelai/.env.local << 'EOF'
NODE_ENV=production
PORT=3000
# Add other environment variables as needed
EOF
```

### For Compliance Agent
```bash
cat > /opt/compliance-agent/.env << 'EOF'
# Add your environment variables here
# ANTHROPIC_API_KEY=your_key_here
# AWS_ACCESS_KEY_ID=your_key_here
# AWS_SECRET_ACCESS_KEY=your_secret_here
EOF
```

Then restart the services:
```bash
pm2 restart all
``` 