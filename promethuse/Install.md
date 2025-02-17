# 利用Promethuse和Telegraf创建集群可视化监控大盘

## 准备工作

### 一、主控机创建deploy_prometheus.yml文件
```yaml
# cat deploy_prometheus.yml
services:
  prometheus:
    image: registry.cn-guangzhou.aliyuncs.com/x86-registry/prometheus:latest
    container_name: prometheus
    ports:
      - "59090:9090"  # Prometheus Web UI
    volumes:
      - /data/etc/prometheus.yml:/etc/prometheus/prometheus.yml  # Mount Prometheus config
      - /data/prometheus-data:/prometheus
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
      
  - job_name: 'telegraf_exporter'
    static_configs:
      - targets: ['86.105.132.172:9273']
storage:
  tsdb:
    retention:
      time: 30d
      size: 1GB
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
> telegraf可作为一个prometheus的node_exporter节点被抓取或者配合influxdb使用，作为grafana的数据源
>
> telegraf也可直接结合deploy_prometheus.yml文件一并创建

### 一、主控机创建deploy_telegraf.yml文件

> 带influxdb

```yaml
# cat deploy_telegraf.yml
# influxdb:2.7.11-alpine => 轻量化alpine容器
services:
  influxdb_v2:
    image: registry.cn-guangzhou.aliyuncs.com/x86-registry/influxdb:2.7.11-alpine
    container_name: influxdb_v2
    ports:
      - "58086:8086"
    environment:
      - DOCKER_INFLUXDB_INIT_MODE=setup  # 启用初始化模式
      - DOCKER_INFLUXDB_INIT_USERNAME=admin  # 管理员用户名
      - DOCKER_INFLUXDB_INIT_PASSWORD=@Sysadm1n  # 管理员密码
      - DOCKER_INFLUXDB_INIT_ORG=ops_monitor  # 组织名称
      - DOCKER_INFLUXDB_INIT_BUCKET=telegraf  # 默认 Bucket
      - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN="@Sysadm1n"  # 自定义Token
    volumes:
      - /data/influxdb_data:/var/lib/influxdb2
    networks:
      - ops_monitor
    restart: always
    # 添加influxdb健康检查
    healthcheck:  
      test: ["CMD", "influx", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3
      
  telegraf:
    image: registry.cn-guangzhou.aliyuncs.com/x86-registry/telegraf:latest
    container_name: telegraf
    environment:
      - TELEGRAF_CONFIG_PATH=/etc/telegraf/telegraf.conf
    volumes:
      - /data/etc/telegraf.conf:/etc/telegraf/telegraf.conf  # 你的 telegraf 配置文件路径
      - /data/telegraf/script:/data/telegraf/script
    # ports:
    #   - "9273:9273"  不作为node_exproter被实时抓取，通过influshdb入库
    networks:
      - ops_monitor
    depends_on:
      - influxdb_v2
    restart: always
    
networks:
  ops_monitor:
    driver: bridge
```

> 不带influxdb

```yaml
services:
  telegraf:
    image: registry.cn-guangzhou.aliyuncs.com/x86-registry/telegraf:latest
    container_name: telegraf
    environment:
      - TELEGRAF_CONFIG_PATH=/etc/telegraf/telegraf.conf
    volumes:
      - /data/etc/telegraf.conf:/etc/telegraf/telegraf.conf  # 你的 telegraf 配置文件路径
      - /data/telegraf/script:/data/telegraf/script
    ports:
      - "9273:9273"  # 为node_exproter被实时抓取，通过influshdb入库
    networks:
      - ops_monitor
    restart: always
    
networks:
  ops_monitor:
    name: ops_monitor
    driver: bridge
```

### 二、主控机telegraf.conf文件

```ini
# cat /data/etc/telegraf.conf

[global_tags]

[agent]
interval = "5m" # 采集（拨测）间隔
round_interval = false
metric_batch_size = 1000
metric_buffer_limit = 10000
collection_jitter = "1s"
flush_interval = "20s"
flush_jitter = "1s"
precision = "4s"
debug = true
quiet = false
logtarget = ""
logfile_rotation_interval = "1d"
logfile_rotation_max_archives = 5
hostname = ""
omit_hostname = true

# [[outputs.influxdb_v2]]
#  urls = ["http://influxdb_v2:8086"]
#  token = "@Sysadm1n"
#  organization = "ops_monitor"
#  bucket = "telegraf"

[[inputs.exec]]
  commands = ["bash /data/ssh/check.sh"]
  timeout = "250s"
  data_format = "prometheus"

[[outputs.prometheus_client]]
  # Prometheus 输出插件配置
  listen = ":9273"  # 配置Telegraf监听的端口
  metric_version = 2  # Prometheus的版本，通常选择2
  # 设置暴露的URL路径
  path = "/metrics" 
```

### 三、插入数据到influxDB的格式

```shell
tianxun,ip=$IP,name=$NAME,uptime=$UP_TIME,cpu1=$CPU1,cpu5=$CPU5,cpu15=$CPU15 ssh_connect=0

from(bucket: "telegraf")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "tianxun" and r["_field"] == "ssh_connect")
  |> group(columns: ["name"]) 
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "status")
  
  
SELECT "name","ssh_connect"
FROM "tianxun"
WHERE time >= now()-30m AND time <= now()
GROUP BY "name"
limit 1

```

### 四、 自定义telegraf扩展脚本

```shell

```

