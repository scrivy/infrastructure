#!/usr/bin/env python
#
# Dynamic inventory script for getting infrastructure information from hcloud

import argparse
import json
import yaml
import sys

from hcloud import Client

from misc.get_key import load_vault


def parse_args():
    parser = argparse.ArgumentParser(description="Hcloud dynamic inventory script")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true')
    group.add_argument('--host')
    return parser.parse_args()


def list_running_hosts(client):
    return [server.name for server in client.servers.get_all()]


def get_host_details(client, host):
    server = client.servers.get_by_name(host)
    return {'ansible_ssh_host': server.public_net.ipv4.ip,
            'ansible_ssh_port': 22,
            'ansible_ssh_user': "root"}


def main():
    args = parse_args()
    loaded = load_vault('misc/vault_hetzner.yml')
    client = Client(token=loaded["hetzner_cloud_api_key"])

    if args.list:
        hosts = list_running_hosts(client=client)
        json.dump({'hcloud': hosts}, sys.stdout)
    else:
        details = get_host_details(client, args.host)
        json.dump(details, sys.stdout)


if __name__ == '__main__':
    main()
