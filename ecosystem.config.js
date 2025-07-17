module.exports = {
  apps: [
    {
      name: 'sentinelai-audit-framework',
      script: 'npm',
      args: 'start',
      cwd: '/opt/sentinelai',
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
      // Logging
      log_file: '/var/log/pm2/sentinelai-combined.log',
      out_file: '/var/log/pm2/sentinelai-out.log',
      error_file: '/var/log/pm2/sentinelai-error.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      // Restart policy
      restart_delay: 4000,
      max_restarts: 10,
      min_uptime: '10s',
      // Resource limits
      max_memory_restart: '500M',
      // Health check
      health_check_grace_period: 10000,
      // Watch and ignore
      watch: false,
      ignore_watch: ['node_modules', '.next', 'logs'],
    }
  ]
};
