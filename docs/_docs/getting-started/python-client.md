---
title: Getting Started with the Python Client
tags: 
 - python
 - install
description: How to interact with FreeGenes via Python
---

## Environment Variables

Make sure that you've [installed FreeGenes]({{ site.baseurl }}/docs/getting-started/install)
before moving forward.

### Token

First you need to find your token! If you login to FreeGenes and go to your user
profile (usually located at `https://<freegenes-node>/u/profile` you'll see your
API token. Before you open an interactive shell (or run a script) you can export your
token to the environment:

```bash
export FREEGENES_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Base

By default, since we only have a development server running, FreeGenes will be 
looked for at `https://freegenes.dev`. When production is deployed, we might change this
to `https://freegenes.org`, and then you would need to optionally specify the development
server. For local development, you might want to change this to `http://127.0.0.1`. 
You can do that easily by exporting `FREEGENES_BASE`:

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
will have more fields exposed than the listing. For example:

```python
# Get a list, or single author
> client.get_authors()
> client.get_authors(uuid="xxxxxxxxxxx")

> client.get_containers()
> client.get_containers(uuid="xxxxxxxxxxx")
```

The above works for all of the following:

```python
> client.get_distributions()
> client.get_collections()
> client.get_compositeparts()
> client.get_institutions()
> client.get_modules()
> client.get_operations()
> client.get_orders()
> client.get_organisms()
> client.get_parts()
> client.get_plans()
> client.get_plates()
> client.get_protocols()
> client.get_robots()
```

## Functions

### Create Composite Part

You can define a new composite part based on a new sequence, which should
be a combination of parts (in forward or reverse directions) from the current
database. You are required to provide a name, and sequence. For example,
here is a composite part derived from two parts, one forward, and one reversed:

```python
name = "Dinosaur Part"
sequence = 'ATGGCTGCAAATAATAAAAAGTATTTTCTGGAGAGCTTTAGCCCGCTGGGTTATGTTAAGAACAACTTTCAGGGTAATCTGCGTAGCGTTAATTGGAATCTGGTTGACGACGAAAAAGATCTGGAGGTGTGGAATCGCATCGTGCAGAATTTCTGGCTGCCGGAAAAAATTCCGGTTAGCAATGACATCCCGAGCTGGAAGAAACTGAGCAAAGACTGGCAGGATCTGATCACCAAAACCTTTACCGGCCTGACCCTGCTGGACACCATCCAGGCGACGATTGGTGACATCTGCCAAATCGATCACGCGCTGACCGATCACGAACAAGTTATCTACGCGAACTTTGCCTTCATGGTCGGTGTGCACGCACGTTCCTACGGTACCATCTTTAGCACCTTGTGCACGTCAGAGCAAATCAATGCCGCGCACGAATGGGTGGTCAACACCGAGAGCCTGCAAAAGCGCGCTAAGGCACTGATTCCTTACTACACTGGTAACGACCCACTGAAATCCAAAGTCGCGGCGGCGCTGATGCCGGGCTTCTTGCTGTATGGTGGTTTCTATCTGCCGTTTTACCTGTCCAGCCGTAAGCAGCTCCCGAACACGTCGGACATCATTCGTCTGATCCTGCGTGATAAGGTTATCCATAATTACTATAGCGGTTATAAATACCAACGCAAGCTGGAAAAACTGCCTCTTGCAAAACAAAAAGAGATGAAGGCCTTCGTTTTTGAGCTGATGTATCGCCTGATTGAGCTGGAGAAAGATTATCTGAAGGAACTGTACGAGGGTTTCGGCATCGTGGACGACGCCATCAAGTTCAGCGTTTATAATGCTGGTAAATTTCTGCAGAATCTGGGCTACGATAGCCCGTTTACGGCAGCGGAAACCCGTATCAAACCGGAGATCTTCGCGCAACTGAGCGCGCGTGCAGACGAGAACCACGACTTCTTTTCCGGTAATGGTTCTTCGTACGTTATGGGCGTTTCTGAGGAAACGAACGATGACGACTGGAATTTTTGAAGTCCGGTTCTCAAGGTTTAGGAATGCTTAGTTCAAGAGAAAGAACTATTTTTAGAACAGAAAAAAGTAAAGGTATTTGCAGCCTTACAATCGTTTGTCCCAGTAGTCGTCCTAACGGTGCATCGAGTCTCTTTTCGGGTGTTACTTGTGGTCAACGCCTAGCGATAACGAGTCTAACTCTTTCCAGCGTTGCAAGAACATGAGTGGTAAGCAGGTCAGCGAGCGGTCCTATGGTCACCATAACGGCCATTAAACTGGGAATTTCTGGCTTTGGTAATTACGGTGCATCCTCTTTATCTAGTCGCGCTTTTGCACCTACATCTTTTTTCTTTAGTCCGACTTCGTCAATAGGGTGTCCTACTAGCGGTCCGAGTGGTCGTCCCTGTCCTTCACGTAGTACTTTATCTAAACCAATAACGGCCATGGTTGTTTTTATTTCAACTGTTACAGAACGAGTAACTGGCCCCATTTCTAGTCGAGTGGTTTGTCGCACTGGTCGCGCGGCTTGTCTGGTTTTTGGCGGTCGTGTGGTCTTTAAAAGAAGACGAAGTCCTTTTGCTTTTGGCCTCGTTAGTGCCGTTTCTTACCCGTGTCCAGGTTGTCTTTCTACGCCGAGTCTGCGTCCGATAGGTCTAAAACCGACGAGACCGATAAAACTGGTATCTGTAGTCCTTTGTCTATTTATTAGACCGCCGGCTTTTTCTGCATCTGTTTGTCCTGCTACCGGTCCTGAACTTAGTTTATTTTTGCTTAGAAGTCGAACGCCTGGTCGCCGCATTTGCGGTCCTGCGATTATTGTGGCCGCTATTAGTCCTATTAGTGTTCTATTAAGTCGCAAACGTA'
> composite_part = client.create_composite_part(name=name, sequence=sequence)
Caching parts for future requests...
```

The way this works, the client caches all parts from the server at the onset,
that way you can do it once and then use the cache as many times as you need.
We first look for all forward and reverse sequences for each part in your new part,
and then from those results we find a "best answer" with a scheduling algorithm:

 1. The list of matching parts (and directions) is sorted based on length
 2. We create a queue, and process it by popping one off the end (longest) until the queue is empty.
 3. For each new element, we check it against a list of selected_sequence items (which starts empty) to look for any overlap.
 4. If there isn't overlap, we add to selected sequences.

The final result will include an ordered list of the longest parts. If there are other
combinations, the client could remove the first match (the longest) and repeat the algorithm again -
however in practice the first result is the "right answer" and subsequent results turn out to 
be repeats of incredibly tiny optimized sequences (e.g., TGA). This isn't implemented, but could
be - please open an issue to discuss if this is needed.

Once we have an ordered list of part ids, directions, and the name, we can make the
request to the server to create the Composite Part. If the create or update is successful you'll get the complete part back:

```python
{'uuid': '9c4b6c9a-b929-4bc8-8b96-38064f9ecbd9',
 'time_created': '2019-09-28T09:52:56.871439-05:00',
 'time_updated': '2019-09-28T09:52:56.871491-05:00',
 'name': 'Dinosaur Part',
 'description': None,
 'composite_id': None,
 'composite_type': None,
 'direction_string': '><',
 'sequence': 'ATGGCTGCAAATAATAAAAAGTATTTTCTGGAGAGCTTTAGCCCGCTGGGTTATGTTAAGAACAACTTTCAGGGTAATCTGCGTAGCGTTAATTGGAATCTGGTTGACGACGAAAAAGATCTGGAGGTGTGGAATCGCATCGTGCAGAATTTCTGGCTGCCGGAAAAAATTCCGGTTAGCAATGACATCCCGAGCTGGAAGAAACTGAGCAAAGACTGGCAGGATCTGATCACCAAAACCTTTACCGGCCTGACCCTGCTGGACACCATCCAGGCGACGATTGGTGACATCTGCCAAATCGATCACGCGCTGACCGATCACGAACAAGTTATCTACGCGAACTTTGCCTTCATGGTCGGTGTGCACGCACGTTCCTACGGTACCATCTTTAGCACCTTGTGCACGTCAGAGCAAATCAATGCCGCGCACGAATGGGTGGTCAACACCGAGAGCCTGCAAAAGCGCGCTAAGGCACTGATTCCTTACTACACTGGTAACGACCCACTGAAATCCAAAGTCGCGGCGGCGCTGATGCCGGGCTTCTTGCTGTATGGTGGTTTCTATCTGCCGTTTTACCTGTCCAGCCGTAAGCAGCTCCCGAACACGTCGGACATCATTCGTCTGATCCTGCGTGATAAGGTTATCCATAATTACTATAGCGGTTATAAATACCAACGCAAGCTGGAAAAACTGCCTCTTGCAAAACAAAAAGAGATGAAGGCCTTCGTTTTTGAGCTGATGTATCGCCTGATTGAGCTGGAGAAAGATTATCTGAAGGAACTGTACGAGGGTTTCGGCATCGTGGACGACGCCATCAAGTTCAGCGTTTATAATGCTGGTAAATTTCTGCAGAATCTGGGCTACGATAGCCCGTTTACGGCAGCGGAAACCCGTATCAAACCGGAGATCTTCGCGCAACTGAGCGCGCGTGCAGACGAGAACCACGACTTCTTTTCCGGTAATGGTTCTTCGTACGTTATGGGCGTTTCTGAGGAAACGAACGATGACGACTGGAATTTTTGAAGTCCGGTTCTCAAGGTTTAGGAATGCTTAGTTCAAGAGAAAGAACTATTTTTAGAACAGAAAAAAGTAAAGGTATTTGCAGCCTTACAATCGTTTGTCCCAGTAGTCGTCCTAACGGTGCATCGAGTCTCTTTTCGGGTGTTACTTGTGGTCAACGCCTAGCGATAACGAGTCTAACTCTTTCCAGCGTTGCAAGAACATGAGTGGTAAGCAGGTCAGCGAGCGGTCCTATGGTCACCATAACGGCCATTAAACTGGGAATTTCTGGCTTTGGTAATTACGGTGCATCCTCTTTATCTAGTCGCGCTTTTGCACCTACATCTTTTTTCTTTAGTCCGACTTCGTCAATAGGGTGTCCTACTAGCGGTCCGAGTGGTCGTCCCTGTCCTTCACGTAGTACTTTATCTAAACCAATAACGGCCATGGTTGTTTTTATTTCAACTGTTACAGAACGAGTAACTGGCCCCATTTCTAGTCGAGTGGTTTGTCGCACTGGTCGCGCGGCTTGTCTGGTTTTTGGCGGTCGTGTGGTCTTTAAAAGAAGACGAAGTCCTTTTGCTTTTGGCCTCGTTAGTGCCGTTTCTTACCCGTGTCCAGGTTGTCTTTCTACGCCGAGTCTGCGTCCGATAGGTCTAAAACCGACGAGACCGATAAAACTGGTATCTGTAGTCCTTTGTCTATTTATTAGACCGCCGGCTTTTTCTGCATCTGTTTGTCCTGCTACCGGTCCTGAACTTAGTTTATTTTTGCTTAGAAGTCGAACGCCTGGTCGCCGCATTTGCGGTCCTGCGATTATTGTGGCCGCTATTAGTCCTATTAGTGTTCTATTAAGTCGCAAACGTA',
 'parts': ['81a92bdc-2b71-48de-bdfc-fafcf9bf26ed',
  'e7d46d00-e32e-417b-8628-0f5287d55840'],
 'label': 'compositepart'}
```

See [this original issue](https://github.com/vsoch/freegenes/issues/63) for discussion
about this endpoint function.
