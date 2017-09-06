#### Python code collect Halo metrics and forward them to Sumo Logic.


#### Required Configuration
Please fill in the following information, 

1. Halo api key id
2. Halo api secret key
3. Sumologic http source.

Location: configs/portal.yml
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
This will pull information from Halo Api and feed them to Sumologic.

`python halo_metrics_to_sumologic.py` 
