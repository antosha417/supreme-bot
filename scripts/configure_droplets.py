"""Script for configuring droplets."""

import pickle
from time import sleep

import digitalocean
import paramiko

import app.models as models
from scripts import token


def configure(_ip):
    """Configure droplet using its _ip."""
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(_ip, username='root',
                key_filename='/home/antosha/.ssh/id_rsa.pub')

    sftp = ssh.open_sftp()
    print sftp.put('droplet/order_data.py', 'order_data.py')
    print sftp.put('droplet/config.sh', 'config.sh')
    print sftp.put('droplet/pyconfig.py', 'pyconfig.py')
    print sftp.put('droplet/script.py', 'script.py')
    sftp.close()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username='root',
                key_filename='/home/antosha/.ssh/id_rsa.pub')
    command = "nohup bash /root/config.sh </dev/null >config_log 2>&1 &"
    ssh.exec_command(command)


with open('droplet/config.sh', 'w') as f:
    f.write('apt-get update --fix-missing\n')
    f.write('apt-get -y install python-pip\n')
    f.write('pip install python-crontab\n')
    f.write('pip install requests\n')
    f.write('apt-get -y install python-bs4\n')
    f.write('python pyconfig.py\n')

with open('droplet/pyconfig.py', 'w') as f:
    f.write('from crontab import CronTab\ncron = CronTab(user=True)\n')
    f.write('job = cron.new(command="python /root/script.py")\n')
    f.write('job.setall("0","*","*","*","*")\njob.enable()\ncron.write()\n')

manager = digitalocean.Manager(token=token)
keys = manager.get_all_sshkeys()
orders = models.Order.query.all()

for order in orders:
    droplet = digitalocean.Droplet(token=token,
                                   name=str(order.order_id),
                                   image='ubuntu-16-04-x64',
                                   size_slug='512mb',
                                   region='fra1',
                                   ssh_keys=keys,
                                   backups=False)
    droplet.create()


for order in orders:
    user = models.User.query.get(order.user_id)
    name = order.name
    email = order.email

    card = order.card
    u_cards = user.cards.all()
    for _card in u_cards:
        if _card.type[:4] == card[:4] and _card.cnb[-9:] == card[-9:]:
            _type = _card.type
            cnb = _card.cnb
            month = _card.month
            year = _card.year
            vval = _card.vval

    adr = order.adr
    u_addresses = user.addresses.all()
    for _adr in u_addresses:
        if adr == _adr.address:
            address = _adr.address
            city = _adr.city
            _zip = _adr.zip
            country = _adr.country
    clothes_name = order.clothes_name
    clothes_name = '.*'.join(clothes_name.split(' '))
    clothes_colors = str(pickle.loads(order.clothes_colors))
    size = order.size
    tel = order.tel

    with open('droplet/order_data.py', 'w') as f:
        f.write('# -*- coding: utf-8 -*-\n')
        f.write('clothes_name = "' + clothes_name + '"\n')
        f.write('clothes_colors = ' + clothes_colors + '\n')
        f.write('order_size = "' + size + '"\n')

        f.write('billing_name = "' + name.encode('utf8') + '"\n')
        f.write('email = "' + email + '"\n')
        f.write('tel = "' + tel + '"\n')
        f.write('billing_address = "' + address + '"\n')
        f.write('billing_city = "' + city + '"\n')
        f.write('billing_zip = "' + _zip + '"\n')
        f.write('billing_country = "' + country + '"\n')
        f.write('credit_card_type = "' + _type + '"\n')
        f.write('credit_card_cnb = "' + cnb + '"\n')
        f.write('credit_card_month = "' + month + '"\n')
        f.write('credit_card_year = "' + year + '"\n')
        f.write('credit_card_vval = "' + vval + '"\n')

    print 'order: |', order.order_id, '|'
    with open('droplet/order_data.py', 'r') as f:
        print f.read()

    print 'getting ready'

    _sleep = False
    while not _sleep:
        sleep(1)
        actions = droplet.get_actions()
        for action in actions:
            action.load()
            # Once it shows complete, droplet is up and running
            _sleep = (action.status == 'completed')

    print 'sleeping'

    sleep(60)

    my_droplets = manager.get_all_droplets()

    print 'configuring'

    for curr_droplet in enumerate(my_droplets):
        if curr_droplet[1].name == str(order.order_id):
            print curr_droplet[0] + 1, '/', len(my_droplets)
            ip = curr_droplet[1].networks['v4'][0]['ip_address']
            print ip
            configure(ip)

    print '\ndone'
