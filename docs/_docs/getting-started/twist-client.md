---
title: Getting Started with the Twist Client
tags: 
 - python
 - install
description: How to interact with Twist via Python
---

## Environment Variables

Make sure that you've [installed FreeGenes]({{ site.baseurl }}/docs/getting-started/install)
before moving forward.

### Token and End User Token

I was only able to obtain these directly from the Twist maintainers / team, and
you might need to do the same:

```bash
export FREEGENES_TWIST_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export FREEGENES_TWIST_EUTOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Base

The default endpoint is the staging server, and you can also change that
to the production server. Both can be done like this:

```bash
export FREEGENES_TWIST_BASE=https://twist-api.twistdna.com
export FREEGENES_TWIST_BASE=https://twist-api.twistbioscience-staging.com/
```

## Instantiate Client

Once in python, you can import the Client.

```python
from freegenes.main.twist import Client
```

If you use the defaults and have
exported your token, no additional input variables are required - the token
will be discovered.


```python
> client = Client()
```

If you need to provide the base and/or tokens to the client, you can do as follows:

```python
> client = Client(token='xxxxxxxxxxxxxx', eutoken='xxxxxxxxxxxxxx')
```

When you create it, you can inspect it to see the version:

```python
> client                                                                  
[client][twist]
```

## Client Shell

The command line FreeGenes also offers a "twist" command that will get you
started with a client. You again need to export the environment variables
that you might need. If you don't:

```bash
$ freegenes twist
ERROR You must export FREEGENES_TWIST_TOKEN or FREEGENES_TWIST_LOGIN and FREEGENES_TWIST_PASSWORD
```

You can also load a default email for the client to discover:

```bash
export FREEGENES_TWIST_EMAIL=me@domain.com
```

When you do, you'll load the shell

```bash
$ freegenes twist

Python 3.7.3 (default, Mar 27 2019, 22:11:17) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.4.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: client                                                                  
Out[1]: [client][twist]
```

You can use tab completion (with ipython) to see all the functions provided by 
the client:

```bash
In [1]: client. 
   account()          accounts()         get()              orders()            
   account_contacts() base               headers            token               
   account_prices()   catalog_items()    healthcheck()      user()             >
   account_users()    eutoken            is_alive()         user_addresses()
```

These are endpoints, with details available at the [Twist API Docs](https://twistapi.docs.apiary.io/#).

## Basic Endpoints

### Whoami

You can check that everything works with the whoami endpoint:

```python
> client.whoami()
{'username': 'company_api',
 'email': 'you@institution.edu',
 'account_admin': True}
```

### Orders

You might start out by getting a list of orders:

```python
> orders = client.orders()
```

### Order Items

Let's grab a random order from the list. There are a lot of fields, but the primary one
we are interested in is `sfdc_id` that we can use to look up order items:

```python
> order_id = orders[3]["sfdc_id"]
> items = client.order_items(sfdc_id)
```

### Order PlateMap by Barcode

Now let's say we have an order we are interested in - we've obtained details for it via the
items endpoint above, we can see associated shipments under "shipments" - it's a list:

```python
{'id': '53485054-5d15-390f-3a55-671c2396ce05',
 'sfdc_id': 'a4g5A000000LWZVQA4',
 'tracking_number': '1101111111111',
 'carrier': 'FEDEX',
 'carrier_detail': None,
 'shipped_date': '2019-06-27T21:45:51.538706+00:00',
 'type': 'dry_ice',
 'status': 'received',
 'status_detail': {'provider_detail': 'arrived_at_destination',
  'provider_status': 'delivered'},
 'last_location': 'SOMEWHERE, CA US',
 'last_updated_at': '2019-06-28T18:33:05+00:00',
 'estimated_delivery_date': '2019-06-28T22:00:00+00:00',
 'received_at': '2019-06-28T19:00:07.744280+00:00',
 'tracking_url': 'https://track.easypost.com/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
 'containers': [{'barcode': 'pSHPs000000000000000',
   'size': 96,
   'wells': [{'location': 'A1',
     'order_item_id': 'OI_xxxxxxxxxxxxxxxxxxxxxx',
     'type': 'shippable_plasmid',
     'name': 'BBF10K_000000',
     'qc_summary': {'ngs': True, 'yield': True},
     'yield': {'value': 2000, 'details': 'not_applicable'}}]},
  {'barcode': 'pSHPs111111111111',
   'size': 96,
   'wells': [{'location': 'A1',
     'order_item_id': 'OI_xxxxxxxxxxxxxxx',
     'type': 'shippable_glycerol',
     'name': 'BBF10K_00000',
     'qc_summary': {'ngs': True},
     'yield': {'value': 'not_applicable', 'details': 'not_applicable'}}]}]}
```

Under shipments you will see containers, and each has a barcode. We can 
now request a platemap based on the barcode from the shipment and
the order if (sfdc_id):

```python

> sfdc_id= '8015A000002uHggQAE'
> barcode='pSHPs0627B165998SH'  # items["shipments"][0]

rows = client.order_platemaps_by_barcode(sfdc_id=sfdc_id, barcode=barcode)
```

The output will be rows of a parsed csv for the order, with the first row being
the header row, and the remaining content in the csv.

### Order PlateMaps

But actually, having to parse through that data structure is not ideal. It would
be better to retrieve a compiled set of rows for all containers across a shipment,
and add the extra metadata to the table from the container object. We can do that too:

```python
rows = client.order_platemaps(sfdc_id=sfdc_id)
```

The client handles obtaining the barcodes on the backend, and in addition,
adds the metadata from the container in case there are differences between them.
