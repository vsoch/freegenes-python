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
