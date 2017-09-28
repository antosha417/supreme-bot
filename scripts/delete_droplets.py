"""Deleting all droplets."""

import digitalocean

from scripts import token


def delete_all():
    """Delete all drplets exept Main ones."""
    manager_ = digitalocean.Manager(token=token)
    my_droplets = manager_.get_all_droplets()

    for droplet in my_droplets:
        if droplet.name != 'Main':
            droplet.destroy()


delete_all()
