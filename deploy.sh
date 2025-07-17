#!/bin/bash

# SentinelAI Audit Framework - Production Deployment Script
# Usage: ./deploy.sh

set -e

echo "🚀 Starting SentinelAI Audit Framework deployment..."

# Variables
APP_DIR="/opt/sentinelai"
BACKUP_DIR="/opt/sentinelai-backup"
LOG_FILE="/var/log/sentinelai-deploy.log"

# Create log file
sudo mkdir -p $(dirname $LOG_FILE)
sudo touch $LOG_FILE

# Function to log messages
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | sudo tee -a $LOG_FILE
}

log "Starting deployment process..."

# Create application directory
log "Creating application directory..."
sudo mkdir -p $APP_DIR
sudo chown -R ec2-user:ec2-user $APP_DIR

# Backup existing deployment if it exists
if [ -d "$APP_DIR/.next" ]; then
    log "Backing up existing deployment..."
    sudo rm -rf $BACKUP_DIR
    sudo cp -r $APP_DIR $BACKUP_DIR
fi

# Copy new files
log "Copying application files..."
sudo cp -r /tmp/sentinelai-audit-framework-static-ui/* $APP_DIR/
sudo chown -R ec2-user:ec2-user $APP_DIR

# Install dependencies
log "Installing dependencies..."
cd $APP_DIR
npm install --production

# Build application
log "Building application..."
npm run build:prod

# Setup PM2 directories
log "Setting up PM2 directories..."
sudo mkdir -p /var/log/pm2
sudo chown -R ec2-user:ec2-user /var/log/pm2

# Start/Restart application with PM2
log "Starting application with PM2..."
pm2 delete sentinelai-audit-framework 2>/dev/null || true
pm2 start ecosystem.config.js --env production

# Save PM2 configuration
pm2 save

# Setup PM2 startup script
pm2 startup systemd | grep "sudo" | bash

log "✅ Deployment completed successfully!"
log "🌐 Application should be available at: http://$(curl -s ifconfig.me):3000"

echo ""
echo "🎉 SentinelAI Audit Framework deployed successfully!"
echo "📊 Monitor with: pm2 monit"
echo "📋 View logs with: pm2 logs sentinelai-audit-framework"
echo "🔄 Restart with: pm2 restart sentinelai-audit-framework"
