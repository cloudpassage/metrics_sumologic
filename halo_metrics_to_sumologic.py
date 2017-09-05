from lib.metrics_utility import MetricsUtility


class HaloMetrics():
    def __init__(self):
        self.metrics_utility = MetricsUtility()

    def run(self):
        self.metrics_utility.server_state_summary()
        self.metrics_utility.critical_issues_summary()
        self.metrics_utility.os_types_summary()
        self.metrics_utility.sw_packages_summary()
        self.metrics_utility.processes_summary()
        self.metrics_utility.local_accounts_summary()
        self.metrics_utility.sw_packages_summary()

def main():
    HaloMetrics().run()

if __name__ == "__main__":
    main()
