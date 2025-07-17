#!/bin/bash

# SentinelAI Audit Framework - Full Deployment Script
# Usage: ./deploy_full.sh [EC2_IP] [KEY_PATH]
# Example: ./deploy_full.sh 3.107.179.60 ~/Downloads/na.pem

set -e

# Check arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <EC2_IP> <KEY_PATH>"
    echo "Example: $0 3.107.179.60 ~/Downloads/na.pem"
    exit 1
fi

EC2_IP=$1
KEY_PATH=$2
EC2_USER="ec2-user"
APP_DIR="/opt/sentinelai"
AGENT_DIR="/opt/compliance-agent"

echo "🚀 Starting SentinelAI Full Stack deployment to $EC2_IP..."

# Function to run commands on EC2
run_remote() {
    ssh -i "$KEY_PATH" -o StrictHostKeyChecking=no "$EC2_USER@$EC2_IP" "$1"
}

# Function to copy files to EC2 using rsync
copy_to_ec2() {
    rsync -avz -e "ssh -i $KEY_PATH -o StrictHostKeyChecking=no" "$1" "$EC2_USER@$EC2_IP:$2"
}

echo "📦 Preparing deployment package..."

# Create temporary deployment directory
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Copy frontend files
echo "📂 Copying frontend files..."
cp -r frontend/ "$TEMP_DIR/frontend/"

# Copy compliance agent files
echo "🤖 Copying compliance agent files..."
cp -r my_compliance_agent/ "$TEMP_DIR/my_compliance_agent/"

# Copy configuration files
cp ecosystem.config.js "$TEMP_DIR/" 2>/dev/null || true
cp package.json "$TEMP_DIR/" 2>/dev/null || true
cp next.config.ts "$TEMP_DIR/" 2>/dev/null || true

echo "🌐 Setting up EC2 instance..."

# Install system dependencies
run_remote "sudo yum update -y"
run_remote "sudo yum install -y nodejs npm python3 python3-pip git jq"

# Install PM2 globally
run_remote "sudo npm install -g pm2"

# Install Python package manager
run_remote "sudo pip3 install virtualenv"

echo "📤 Uploading files to EC2..."

# Upload each directory separately
copy_to_ec2 "$TEMP_DIR/frontend" "/tmp/"
copy_to_ec2 "$TEMP_DIR/my_compliance_agent" "/tmp/"

# Upload config files if they exist
[ -f "$TEMP_DIR/ecosystem.config.js" ] && copy_to_ec2 "$TEMP_DIR/ecosystem.config.js" "/tmp/"
[ -f "$TEMP_DIR/package.json" ] && copy_to_ec2 "$TEMP_DIR/package.json" "/tmp/"
[ -f "$TEMP_DIR/next.config.ts" ] && copy_to_ec2 "$TEMP_DIR/next.config.ts" "/tmp/"

echo "🏗️ Setting up application directories..."

# Create application directories
run_remote "sudo mkdir -p $APP_DIR $AGENT_DIR"
run_remote "sudo chown -R $EC2_USER:$EC2_USER $APP_DIR $AGENT_DIR"

# Move files to proper locations
run_remote "cp -r /tmp/frontend/* $APP_DIR/"
run_remote "cp -r /tmp/my_compliance_agent/* $AGENT_DIR/"
run_remote "cp /tmp/ecosystem.config.js $APP_DIR/" 2>/dev/null || true

echo "📦 Installing frontend dependencies..."

# Install and build frontend
run_remote "cd $APP_DIR && npm install"
run_remote "cd $APP_DIR && npm run build"

echo "🐍 Setting up Python environment for compliance agent..."

# Setup Python virtual environment
run_remote "cd $AGENT_DIR && python3 -m venv venv"
run_remote "cd $AGENT_DIR && source venv/bin/activate && pip install --upgrade pip"

# Install Python dependencies
run_remote "cd $AGENT_DIR && source venv/bin/activate && pip install -r requirements.txt"

echo "🔧 Setting up PM2 configuration..."

# Create updated ecosystem config for both services
cat > "$TEMP_DIR/ecosystem.production.config.js" << EOF
module.exports = {
  apps: [
    {
      name: 'sentinelai-frontend',
      script: 'npm',
      args: 'start',
      cwd: '$APP_DIR',
      instances: 1,
      exec_mode: 'fork',
      env: {
        NODE_ENV: 'production',
        PORT: 3000
      },
      env_production: {
        NODE_ENV: 'production',
        PORT: 3000
      },
      log_file: '/var/log/pm2/frontend-combined.log',
      out_file: '/var/log/pm2/frontend-out.log',
      error_file: '/var/log/pm2/frontend-error.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      restart_delay: 4000,
      max_restarts: 10,
      min_uptime: '10s',
      max_memory_restart: '500M',
      watch: false,
      ignore_watch: ['node_modules', '.next', 'logs']
    },
    {
      name: 'compliance-agent',
      script: '$AGENT_DIR/venv/bin/python',
      args: '$AGENT_DIR/main.py',
      cwd: '$AGENT_DIR',
      instances: 1,
      exec_mode: 'fork',
      env: {
        PYTHONPATH: '$AGENT_DIR',
        VIRTUAL_ENV: '$AGENT_DIR/venv'
      },
      log_file: '/var/log/pm2/agent-combined.log',
      out_file: '/var/log/pm2/agent-out.log',
      error_file: '/var/log/pm2/agent-error.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      restart_delay: 4000,
      max_restarts: 10,
      min_uptime: '10s',
      max_memory_restart: '1G',
      watch: false
    }
  ]
};
EOF

# Upload updated PM2 config
copy_to_ec2 "$TEMP_DIR/ecosystem.production.config.js" "$APP_DIR/"

echo "🚀 Starting services..."

# Setup PM2 directories
run_remote "sudo mkdir -p /var/log/pm2"
run_remote "sudo chown -R $EC2_USER:$EC2_USER /var/log/pm2"

# Stop existing PM2 processes
run_remote "pm2 delete all || true"

# Start services with PM2
run_remote "cd $APP_DIR && pm2 start ecosystem.production.config.js --env production"

# Save PM2 configuration
run_remote "pm2 save"

# Setup PM2 startup script
run_remote "pm2 startup systemd -u $EC2_USER --hp /home/$EC2_USER | grep 'sudo' | bash || true"

echo "🔒 Setting up firewall rules..."

# Open necessary ports (using firewall-cmd if available, otherwise iptables)
run_remote "sudo firewall-cmd --permanent --add-port=3000/tcp || sudo iptables -A INPUT -p tcp --dport 3000 -j ACCEPT || true"
run_remote "sudo firewall-cmd --permanent --add-port=22/tcp || sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT || true"
run_remote "sudo firewall-cmd --reload || sudo service iptables save || true"

echo "🏥 Health check..."

sleep 10

# Check if services are running
FRONTEND_STATUS=$(run_remote "pm2 jlist | jq -r '.[] | select(.name==\"sentinelai-frontend\") | .pm2_env.status' 2>/dev/null || echo 'unknown'")
AGENT_STATUS=$(run_remote "pm2 jlist | jq -r '.[] | select(.name==\"compliance-agent\") | .pm2_env.status' 2>/dev/null || echo 'unknown'")

echo "📊 Deployment Status:"
echo "Frontend: $FRONTEND_STATUS"
echo "Compliance Agent: $AGENT_STATUS"

if [ "$FRONTEND_STATUS" = "online" ]; then
    echo "✅ Frontend deployed successfully!"
    echo "🌐 Frontend URL: http://$EC2_IP:3000"
else
    echo "❌ Frontend deployment failed"
    echo "🔍 Check logs with: ssh -i $KEY_PATH $EC2_USER@$EC2_IP 'pm2 logs sentinelai-frontend'"
fi

if [ "$AGENT_STATUS" = "online" ]; then
    echo "✅ Compliance Agent deployed successfully!"
else
    echo "❌ Compliance Agent deployment failed"
    echo "🔍 Check logs with: ssh -i $KEY_PATH $EC2_USER@$EC2_IP 'pm2 logs compliance-agent'"
fi

echo ""
echo "🎉 SentinelAI Full Stack deployment completed!"
echo ""
echo "📋 Useful commands:"
echo "  Monitor services: ssh -i $KEY_PATH $EC2_USER@$EC2_IP 'pm2 monit'"
echo "  View logs: ssh -i $KEY_PATH $EC2_USER@$EC2_IP 'pm2 logs'"
echo "  Restart frontend: ssh -i $KEY_PATH $EC2_USER@$EC2_IP 'pm2 restart sentinelai-frontend'"
echo "  Restart agent: ssh -i $KEY_PATH $EC2_USER@$EC2_IP 'pm2 restart compliance-agent'"
echo "  Check status: ssh -i $KEY_PATH $EC2_USER@$EC2_IP 'pm2 status'"
echo ""
echo "🔗 Access your application at: http://$EC2_IP:3000" 