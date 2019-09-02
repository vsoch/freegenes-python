---
title: Getting Started with the Python Client
tags: 
 - python
 - install
description: How to interact with FreeGenes via Python
---

Make sure that you've [installed FreeGenes]({{ site.baseurl }}/docs/getting-started/install)
before moving forward.

## Environment Variables

### Token

First you need to find your token! If you login to FreeGenes and go to your user
profile (usually located at `https://<freegenes-node>/u/profile` you'll see your
API token. Before you open an interactive shell (or run a script) you can export your
token to the environment:

```bash
export FREEGENES_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Base

By default, FreeGenes will be looked for at https://freegenes.org. For local development,
you might want to change this to `http://127.0.0.1`, or for the development server,
`https://freegenes.dev`. You can do that easily by exporting `FREEGENES_BASE`:

```bash
export FREEGENES_BASE=http://127.0.0.1
```

Both the API token and base URL are tested on instantiation of the client, so
make sure you get them right!

## Instantiate Client

Once in python, you can import the Client.


```python
from freegenes.main import Client
```

If you use the defaults and have
exported your token, no additional input variables are required - the token
will be discovered.


```python
> client = Client()
```

If you need to provide the base and/or token to the client, you can do as follows:

```python
> client = Client(token='xxxxxxxxxxxxxx', base='https://freegenes.dev'
```

When you create it, you can inspect it to see the version:

```python
> client                                                                  
[client][freegenes][0.0.0]
```

## Client Shell

The command line FreeGenes also offers a "shell" command that will get you
started with a client. You again need to export the environment variables
that you might need. If you don't:

```bash
$ freegenes shell
ERROR You must provide a token or export FREEGENES_TOKEN.
```

When you do:

```bash
export FREEGENES_TOKEN=xxxxxxxxxxxx
export FREEGENES_BASE=http://127.0.0.1
$ freegenes shell

Python 3.7.3 (default, Mar 27 2019, 22:11:17) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.4.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: client                                                                                                                            
Out[1]: [client][freegenes][0.0.0]
```

You can use tab completion (with ipython) to see all the functions provided by 
the client:

```bash
In [1]: client. 
                base                get_containers()    get_modules()       get_parts()         get_protocols()    
                get()               get_distributions() get_operations()    get_plans()         get_robots()       
                get_authors()       get_entity()        get_orders()        get_plates()        headers            
                get_collections()   get_institutions()  get_organisms()     get_platesets()     token        
```

These are endpoints, explained in further detail below.

## Basic Endpoints

A basic endpoint is a function to get a single
or list of entities. This contrasts to a more complicated function that might perform
a specific task for the lab possibly using multiple endpoints, and performing additional tasks.
For functions, see [the functions section](#functions) below.

Let's explore all of the basic endpoints.  Generally, each model in FreeGenes (e.g., a Plate or Protocol) 
has an endpoint to get details for a single entity, or to list
many (paginated) entities. In the case of more complex models, the detail view
will have more fields exposed than the listing.

## Functions

**not yet written, need to get information from Keoni**
