# Monitoring 

In order to prevent or fix issues, we need to monitor our app
- System metrics (CPU, RAM, disk, network)
- App health (is it reachable? response time?)
- SSL expiry / uptime (blackbox checks)
- Confirm access to Hetzner server (SSH / root), app domain or local IP, docker installed on the server

## Setup Monitoring Stack with Docker Compose 

- Create a monitoring/ folder in the project
- Add a docker-compose.yml with: Prometheus, Node Exporter, Blackbox Exporter, Grafana
- Configure service ports and volumes.

## Configure Grafana

- Launch Grafana container and log in.
- Add Prometheus as a data source.
- Import or create dashboards:
    - System metrics (Node Exporter)
    - Uptime & latency (Blackbox Exporter)

## Configure Prometheus

- Create prometheus.yml with scrape targets (Node Exporter (for system metrics), Blackbox Exporter (for probing the app))
- Define scrape intervals and job labels.

## Configure Alerting

- Add Alertmanager container
- Write simple alerting rules in Prometheus: High CPU, App unreachable, SSL about to expire
- Route alerts to email.

## Validate Everything

- Ensure all containers are running.
- Visit Grafana and confirm dashboards display real metrics.
- Test probes by stopping the app (trigger a failure).


## Step 1: Setup Monitoring Stack with Docker Compose 

Folder structure:
```sh
project-root/
└── monitoring/
    ├── docker-compose.yml
    ├── prometheus/
    │   └── prometheus.yml
    ├── blackbox/
    │   └── blackbox.yml
    └── grafana/  # for dashboard provisioning later
```
Once the .yml files are ready, we move to the server where we make the following setup:
```sh
# 1. SSH into your server
ssh root@your-server-ip

# 2. Install Docker if not already installed
curl -fsSL https://get.docker.com | bash

# 3. Upload the monitoring folder from local to server
# (use VS Code Remote-SSH or WinSCP or scp)
# Example using scp from PowerShell or Git Bash:
scp -r monitoring root@your-server-ip:/opt/

# 4. Start the monitoring stack
cd /opt/monitoring
docker compose up -d
```
- one issue I ran into: the user user running the GitHub Actions SSH session didn't had permissions to access the Docker socket
- had to log into the root account, and give permission to access it without a password:

```sh
sudo visudo

# add these permissions for the respective username
USERNAME ALL=(ALL) NOPASSWD: /usr/bin/docker, /usr/local/bin/docker-compose
```

## Step 2: Configure Grafana

- test on the server if monitoring container is up and running.
```sh
docker ps
```
- if successful, we can login into Grafana, typing the following in the browser:
```
http://your-server-ip:3000
```
- login using credentials `admin/admin`, we'll be prompted to change them
- next we add Prometheus as a new data source (Administration -> Plugins -> Prometheus -> Add new data source)
- we test it using this link in the URL field:
```
http://prometheus:9090
```
- click `Save & Test`
- we can import usefull dashboards (e.g. `Node Exporter Full` - code 1860), by clicking the top right `+` button on the home page. We introduce the dashboard code there and link it to our prometheus data source
- we can verify prometheus targets:
```sh
http://your-server-ip:9090/targets
```
