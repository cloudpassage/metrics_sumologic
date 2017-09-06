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
        url = "/v2/servers?group_id=%s&state=active,missing,deactivated,retired&descendants=true&group_by=state" % self.root_group["id"]
        servers = self.api.get(url)
        log = { 'os_types_summary': servers }
        data = { 'source': 'script', 'log': log, 'created_time': self.current_time }

        self.sumo.https_forwarder(data)

    def critical_issues_summary(self):
        url = "/v2/issues?group_id=%s&descendants=true&state=active,deactivated,missing&status=active&group_by=issue_type,critical" % self.root_group["id"]
        issues = self.api.get(url)
        log = { 'current_issues_by_criticality_summary': issues }
        data = { 'source': 'script', 'log': log, 'created_time': self.current_time }

        self.sumo.https_forwarder(data)

    def os_types_summary(self):
        url = "/v2/servers?group_id=%s&descendants=true&state=active&group_by=os_distribution,os_version" % self.root_group["id"]
        os_types = self.api.get(url)
        log = { 'os_types_summary': os_types }
        data = { 'source': 'script', 'log': log, 'created_time': self.current_time }

        self.sumo.https_forwarder(data)

    def sw_packages_summary(self):
        url = "/v2/servers?group_id=%s&descendants=true&state=active,missing,deactivated&group_by=os_type,package_name,package_version" % self.root_group["id"]
        sw_packages = self.api.get(url)
        log = { 'sw_packages_summary': sw_packages }
        data = { 'source': 'script', 'log': log, 'created_time': self.current_time }

        self.sumo.https_forwarder(data)

    def processes_summary(self):
        url = "/v2/servers?group_id=%s&descendants=true&state=active,missing,deactivated&group_by=os_type,process_name" % self.root_group["id"]
        processes = self.api.get(url)
        log = { 'processes_summary': processes }
        data = { 'source': 'script', 'log': log, 'created_time': self.current_time }

        self.sumo.https_forwarder(data)

    def local_accounts_summary(self):
        url = "/v1/local_accounts?group_id=%s&descendants=true&group_by=os_type,username&per_page=100" % self.root_group["id"]
        local_accounts = self.api.get(url)
        log = { 'local_accounts_summary': local_accounts }
        data = { 'source': 'script', 'log': log, 'created_time': self.current_time }

        self.sumo.https_forwarder(data)

    def sw_vuln_summary(self):
        url = "/v2/issues?group_id=%s&issue_type=sva&per_page=100&page=1&state=active,missing,deactivated&sort_by=critical.desc,count.desc&descendants=true&group_by=critical,issue_type,rule_key,name,policy_id&status=active" % self.root_group["id"]
        sw_vuln = self.api.get(url)
        log = { 'sw_vulnerability_summary': sw_vuln }
        data = { 'source': 'script', 'log': log, 'created_time': self.current_time }

        self.sumo.https_forwarder(data)
