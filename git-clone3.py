#!/usr/bin/env python

import os
import sys
import requests

class Checkout(object):

    def __init__(self, ssh_url, rest_url, oauth, *users):
        self.ssh_url = ssh_url
        self.rest_url = rest_url
        self.users = users
        self.oauth = oauth

    def rest(self, resource, process=lambda x: x):
        url = '{}/{}'.format(self.rest_url, resource)
        headers = {'Authorization': 'token {self.oauth}'.format(self=self)}
        response = requests.get(url, headers=headers)
        return process(response.json())

    @classmethod
    def select(cls, choices):
        for i, e in enumerate(choices):
            print('{}. {}'.format(i, e))
        try:
           choice = int(input())
        except ValueError:
           return cls.select(choices)
        return choices[choice]

    @staticmethod
    def remove_existing(repo):
        while True:
            print('Overwrite {} y/n?'.format(repo))
            choice = input()
            if choice == 'y':
                cmd = 'rm -rf {}'.format(repo)
                os.system(cmd)
                break
            elif choice == 'n':
                exit()

    def git_clone(self, branch, user, repo):
        cmd = 'git clone -b {} {}:{}/{}.git'.format(branch, self.ssh_url, user, repo)
        rc = os.system(cmd)
        if not rc:
            pass
        elif rc == 32768:
            self.remove_existing(repo)
            self.git_clone(branch, user, repo)
        else:
            raise Exception('{} nonzero exit: {}'.format(cmd, rc))

    def checkout(self):
        user = self.select(self.users)
        repo_query = 'users/{}/repos?page=1&per_page=100'.format(user)
        repos = self.rest(repo_query, lambda x: [i['name'] for i in x])
        repo = self.select(repos)
        branch_query = 'repos/{}/{}/branches?page=1&per_page=100'.format(user, repo)
        branches = self.rest(branch_query, lambda x: [i['name'] for i in x])
        branch = self.select(branches)
        self.git_clone(branch, user, repo)

def main():
    checkout = Checkout(*sys.argv[1:])
    checkout.checkout()

if __name__ == '__main__':
    main()
