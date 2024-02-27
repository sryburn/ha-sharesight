# ha-sharesight
A Home Assistant custom component for Sharesight. 

Currently only provides a `sharesight.send_price` service to update custom investment prices. This can be used in conjunction with [yahoofinance](https://github.com/iprak/yahoofinance) or other data source to maintain investments that are not available directly within Sharesight.

In future this component could be extended to support other use-cases, for example displaying portfolio data on a Home Assistant dashboard.

## To install
1. Copy the `sharesight` folder to `config\custom_components` in Home Assistant.
1. Restart Home Assistant.
1. Click "Add Integration" (under _Settings > Devices & Services_) and add the Sharesight integration from the search list.
1. Enter your Sharesight API credentials (`client_id` and `client_secret`).

## Usage example
```
service: sharesight.send_price
data:
  investment_id: 123456
  last_traded_price: 1.23
  last_traded_on: 2024-02-01
```  
## Automation example
```
alias: send IBIT price to Sharesight
description: ""
trigger:
  - platform: time
    at: "12:00:00"
condition: []
action:
  - service: sharesight.send_price
    data:
      investment_id: 123456
      last_traded_price: "{{ states('sensor.yahoofinance_ibit') }}"
      last_traded_on: "{{ (now().date() }}"
mode: single
```
## Obtaining Sharesight API credentials
Contact Sharesight support and ask for API access to your account (you must be on a paid plan).

## To obtain the investment_id
In Sharesight click _Account > Custom Investments_, click on the relevant custom investment and copy the ID from the URL.
