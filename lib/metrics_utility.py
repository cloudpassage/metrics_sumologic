import datetime
import os
from sumologic import Sumologic
from config import CONFIG
from api_controller import ApiController


class MetricsUtility(object):
    def __init__(self):
        self.sumo_url = CONFIG['sumologic_https_url']
        self.current_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        self.api = ApiController()
        self.sumo = Sumologic()

        groups = self.api.get("/v2/groups")
        for group in groups["groups"]:
            if not group["parent_id"]:
                self.root_group = group

    def server_state_summary(self):
        servers = self.api.get_paginated('/v2/servers', group_id=self.root_group['id'],
                                                        state='active,missing,deactivated,retired',
                                                        descendants='true',
                                                        group_by='state')
        log = {'servers_by_state_summary': servers}
        data = {'source': 'script', 'log': log, 'created_time': self.current_time}

        self.sumo.https_forwarder(data)

    def critical_issues_summary(self):
        issues = self.api.get_paginated('/v2/issues', group_id=self.root_group['id'],
                                                      descendants='true',
                                                      state='active,deactivated,missing',
                                                      status='active',
                                                      group_by='issue_type,critical')
        log = {'current_issues_by_criticality_summary': issues}
        data = {'source': 'script', 'log': log, 'created_time': self.current_time}

        self.sumo.https_forwarder(data)

    def os_types_summary(self):
        os_types = self.api.get_paginated('/v2/servers', group_id=self.root_group['id'],
                                                         descendants='true',
                                                         state='active',
                                                         group_by='os_distribution,os_version')
        log = {'os_types_summary': os_types}
        data = {'source': 'script', 'log': log, 'created_time': self.current_time}

        self.sumo.https_forwarder(data)

    def sw_packages_summary(self):
        sw_packages = self.api.get_paginated('/v2/servers', group_id=self.root_group['id'],
                                                            descendants='true',
                                                            state='active,missing,deactivated',
                                                            group_by='os_type,package_name,package_version')
        log = {'sw_packages_summary': sw_packages}
        data = {'source': 'script', 'log': log, 'created_time': self.current_time}

        self.sumo.https_forwarder(data)

    def processes_summary(self):
        processes = self.api.get_paginated('/v2/servers', group_id=self.root_group['id'],
                                                          descendants='true',
                                                          state='active,missing,deactivated',
                                                          group_by='os_type,process_name')
        log = {'processes_summary': processes}
        data = {'source': 'script', 'log': log, 'created_time': self.current_time}

        self.sumo.https_forwarder(data)

    def local_accounts_summary(self):
        local_accounts = self.api.get_paginated('/v1/local_accounts', group_id=self.root_group['id'],
                                                                      descendants='true',
                                                                      group_by='os_type,username',
                                                                      per_page='100')
        log = {'local_accounts_summary': local_accounts}
        data = {'source': 'script', 'log': log, 'created_time': self.current_time}

        self.sumo.https_forwarder(data)

    def sw_vuln_summary(self):
        sw_vuln = self.api.get_paginated('/v2/issues', group_id=self.root_group['id'],
                                                       issue_type='sva',
                                                       per_page='100',
                                                       state='active,missing,deactivated',
                                                       sort_by='critical.desc,count.desc',
                                                       descendants='true',
                                                       group_by='critical,issue_type,rule_key,name,policy_id',
                                                       status='active')
        log = {'sw_vulnerability_summary': sw_vuln}
        data = {'source': 'script', 'log': log, 'created_time': self.current_time}

        self.sumo.https_forwarder(data)
