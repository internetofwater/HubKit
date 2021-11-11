from crontab import CronTab
import os
cron = CronTab(user='root')
command = "curl 'http://localhost:5000/v1/schedule' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  --data-raw '{\"config_file\":\"config (25).json\",\"source\":\"https://raw.githubusercontent.com/internetofwater/HubKit/main/examples/data/tests.csv\",\"interval\":\"15mins\"}' \
  --compressed"
job = cron.new(command=command)
job.minute.every(1)
cron.write()

os.system("service cron restart")