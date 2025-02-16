# 利用Promethuse和Telegraf创建集群可视化监控大盘

## 准备工作

### 一、主控机创建deploy_prometheus.yml文件
```yaml
# cat deploy_prometheus.yml
version: '3'
services:
  mysql8:
    image: registry.cn-guangzhou.aliyuncs.com/x86-registry/ops_mysql:8.0.41
    container_name: prom_mysql8
    environment:
      MYSQL_ROOT_PASSWORD: "@Sysadm1n"
      MYSQL_DATABASE: "devops_monitor"
      MYSQL_USER: "ops_monitor"
      MYSQL_PASSWORD: "@Sysadm1n"
    ports:
      - "53306:3306"
    volumes:
      - /data/mysql-data:/var/lib/mysql
    restart: always
    networks:
      - ops_monitor
    
  prometheus:
    image: registry.cn-guangzhou.aliyuncs.com/x86-registry/prometheus:latest
    container_name: prometheus
    ports:
      - "59090:9090"  # Prometheus Web UI
    volumes:
      - /data/etc/prometheus.yml:/etc/prometheus/prometheus.yml  # Mount Prometheus config
    environment:
      - PROMETHEUS_DB_HOST=prom_mysql8
      - PROMETHEUS_DB_PORT=53306
      - PROMETHEUS_DB_USER=ops_monitor
      - PROMETHEUS_DB_PASSWORD="@Sysadm1n"
    depends_on:
      - mysql8
    restart: always
    networks:
      - ops_monitor
      
  node_exporter:
    image: registry.cn-guangzhou.aliyuncs.com/x86-registry/node-exporter:latest
    container_name: node_exporter
    # ports:
    #   - "9100:9100"  # Node Exporter Port Is Not Required In host mode.
    restart: always
    network_mode: "host"  # Use host network to expose system metrics

  grafana:
    image: registry.cn-guangzhou.aliyuncs.com/x86-registry/grafana:latest
    container_name: grafana
    ports:
      - "53000:3000"  # Grafana Web UI
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=@Sysadm1n  # Set admin password for grafana
    depends_on:
      - prometheus
    restart: always
    networks:
      - ops_monitor
    
networks:
  ops_monitor:
    driver: bridge
```

### 二、被控机创建deploy_node_exporter.yml

```yaml
services:
  node_exporter:
    image: registry.cn-guangzhou.aliyuncs.com/x86-registry/node-exporter:latest
    container_name: node_exporter
    restart: always
    network_mode: "host"  # Use host network to expose system metrics
    networks:
      - ops_monitor
```

### 三、主控机创建prometheus.yml文件

```yaml
# cat /data/etc/prometheus.yml
global:
  scrape_interval: 30s
scrape_configs:
  - job_name: 'node_exporter'
    static_configs:
      - targets: ['86.105.132.169:9100','86.105.132.170:9100','86.105.132.171:9100','86.105.132.172:9100'] 
```

### 四、拉起prometheus和node_exporter

```shell
# 拉起主控节点的pormethuse和mysql8
docker-compose -f deploy_prometheus.yml up -d
# 拉起被控节点的的node_exporter
docker-compose -f deploy_node_exporter.yml up -d
```

## 个性化需求

> 如果node_exporter监控指标不满足要求，可自行搭建telegraf执行个性化监控脚本。
>
> telegraf可作为一个prometheus的node_exporter节点被抓取
>
> telegraf配合influxdb使用
>
> 也可直接结合deploy_prometheus.yml文件创建

### 一、主控机创建deploy_telegraf.yml文件

```yaml
# cat deploy_telegraf.yml
version: '3'
services:
  influxdb:
    image: registry.cn-guangzhou.aliyuncs.com/x86-registry/influxdb:latest
    container_name: influxdb
    ports:
      - "58086:8086"
    environment:
      INFLUXDB_ADMIN_USER: ops_monitor       # 管理员用户名
      INFLUXDB_ADMIN_PASSWORD: "@Sysadm1n"   # 管理员密码
      INFLUXDB_DB: telegraf            # 默认数据库
    volumes:
      - /data/influxdb_data:/var/lib/influxdb
    networks:
      - ops_monitor
    restart: always
      
  telegraf:
    image: registry.cn-guangzhou.aliyuncs.com/x86-registry/telegraf:latest
    environment:
      - TELEGRAF_CONFIG_PATH=/etc/telegraf/telegraf.conf
    volumes:
      - /data/etc/telegraf.conf:/etc/telegraf/telegraf.conf  # 你的 telegraf 配置文件路径
    networks:
      - ops_monitor
    depends_on:
      - influxdb
    restart: always
    
networks:
  ops_monitor:
    driver: bridge
```

### 二、主控机telegraf.conf文件

```ini
# cat /data/etc/telegraf.conf
[global_tags]
  # 可以在这里设置全局标签

[agent]
  interval = "10s"          # 收集数据的频率
  round_interval = true
  metric_batch_size = 1000
  metric_buffer_limit = 10000
  collection_jitter = "0s"
  flush_interval = "10s"    # 将数据推送到 InfluxDB 的间隔
  flush_jitter = "0s"

[[outputs.influxdb]]
  urls = ["http://influxdb:58086"]    # InfluxDB 服务的地址
  database = "telegraf"               # 默认数据库
  username = "ops_monitor"                  # InfluxDB 管理员用户名
  password = "@Sysadm1n"                  # InfluxDB 管理员密码

[[inputs.cpu]]
  percpu = true
  totalcpu = true
  collect_cpu_time = false
  report_active = false
  
[[inputs.mem]]
```

