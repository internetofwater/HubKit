from crontab import CronTab
cron = CronTab(user='root')
job = cron.new(command='curl http://localhost:5000')
job.minute.every(1)
cron.write()
