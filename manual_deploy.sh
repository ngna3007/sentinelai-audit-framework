#!/bin/bash

# Manual Deployment Script for SentinelAI
# Usage: ./manual_deploy.sh 3.107.179.60 ~/Downloads/na.pem

set -e

EC2_IP=$1
KEY_PATH=$2
EC2_USER="ec2-user"

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <EC2_IP> <KEY_PATH>"
    exit 1
fi

echo "🚀 Manual SentinelAI deployment to $EC2_IP"

# Function to run commands on EC2
run_remote() {
    ssh -i "$KEY_PATH" -o StrictHostKeyChecking=no "$EC2_USER@$EC2_IP" "$1"
}

echo "Step 1: Uploading files..."
# Upload frontend
rsync -avz --exclude 'node_modules' --exclude '.git' --exclude '.next' \
-e "ssh -i $KEY_PATH -o StrictHostKeyChecking=no" \
frontend/ "$EC2_USER@$EC2_IP:/tmp/frontend/"

# Upload compliance agent
rsync -avz --exclude '__pycache__' --exclude '*.pyc' --exclude '.git' --exclude 'venv' \
-e "ssh -i $KEY_PATH -o StrictHostKeyChecking=no" \
my_compliance_agent/ "$EC2_USER@$EC2_IP:/tmp/my_compliance_agent/"

echo "Step 2: Setting up directories..."
run_remote "sudo mkdir -p /opt/sentinelai /opt/compliance-agent"
run_remote "sudo chown -R $EC2_USER:$EC2_USER /opt/sentinelai /opt/compliance-agent"
run_remote "cp -r /tmp/frontend/* /opt/sentinelai/"
run_remote "cp -r /tmp/my_compliance_agent/* /opt/compliance-agent/"

echo "Step 3: Installing Node.js via NodeSource (latest stable)..."
run_remote "curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -"
run_remote "sudo yum install -y nodejs python3 python3-pip git jq"

echo "Step 4: Installing PM2..."
run_remote "sudo npm install -g pm2"

echo "Step 5: Building frontend..."
run_remote "cd /opt/sentinelai && npm install && npm run build"

echo "Step 6: Setting up Python environment..."
run_remote "cd /opt/compliance-agent && python3 -m venv venv"
run_remote "cd /opt/compliance-agent && source venv/bin/activate && pip install -r requirements.txt"

echo "Step 7: Creating PM2 config..."
cat > /tmp/ecosystem.config.js << 'EOF'
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
      }
    },
    {
      name: 'compliance-agent',
      script: '/opt/compliance-agent/venv/bin/python',
      args: '/opt/compliance-agent/main.py',
      cwd: '/opt/compliance-agent',
      instances: 1,
      exec_mode: 'fork',
      env: {
        PYTHONPATH: '/opt/compliance-agent'
      }
    }
  ]
};
EOF

scp -i "$KEY_PATH" -o StrictHostKeyChecking=no /tmp/ecosystem.config.js "$EC2_USER@$EC2_IP:/opt/sentinelai/"

echo "Step 8: Starting services..."
run_remote "pm2 delete all || true"
run_remote "cd /opt/sentinelai && pm2 start ecosystem.config.js"
run_remote "pm2 save"
run_remote "pm2 startup systemd -u $EC2_USER --hp /home/$EC2_USER | grep 'sudo' | bash || true"

echo "Step 9: Opening firewall..."
run_remote "sudo firewall-cmd --permanent --add-port=3000/tcp 2>/dev/null || echo 'Firewall cmd not available'"
run_remote "sudo firewall-cmd --reload 2>/dev/null || echo 'Firewall cmd not available'"

echo "✅ Deployment completed!"
echo "🌐 Access your app at: http://$EC2_IP:3000"
echo ""
echo "📋 Check status:"
echo "  ssh -i $KEY_PATH $EC2_USER@$EC2_IP 'pm2 status'"
echo "  ssh -i $KEY_PATH $EC2_USER@$EC2_IP 'pm2 logs'" 