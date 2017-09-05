#### Python code collect Halo metrics and forward them to Sumo Logic.


#### Configuration
```
key_id: 'halo_key_id'
secret_key: 'halo_secret_key'
api_hostname : api.cloudpassage.com
api_port: 443
sumologic_https_url: 'sumologic_https_url'
```
#### System Requirements

Mac OSX and Linux only

Must have python 2.7+

Must have cloudpassage module installed
`pip install cloudpassage`

#### Run instructions

`python halo_metrics_to_sumologic.py`
