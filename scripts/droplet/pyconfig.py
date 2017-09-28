from crontab import CronTab
cron = CronTab(user=True)
job = cron.new(command="python /root/script.py")
job.setall("0", "*", "*", "*", "*")
job.enable()
cron.write()
