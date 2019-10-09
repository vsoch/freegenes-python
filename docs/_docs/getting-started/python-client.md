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
  	base                    create_composite_part() create_institution()     
  	cache                   create_container()      create_module()          
  	create_author()         create_distribution()   create_operation()      >
  	create_collection()     create_entity()         create_order()     
```

These are endpoints, explained in further detail below.

## Get Endpoints

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

## Delete Endpoints

Each of models has a delete function, and it's also required to be staff or 
superuser user to use it. 

```python
> client.delete_distributions(uuid)
> client.delete_collections(uuid)
> client.delete_compositeparts(uuid)
> client.delete_institutions(uuid)
> client.delete_modules(uuid)
> client.delete_operations(uuid)
> client.delete_orders(uuid)
> client.delete_organisms(uuid)
> client.delete_parts(uuid)
> client.delete_plans(uuid)
> client.delete_plates(uuid)
> client.delete_protocols(uuid)
> client.delete_robots(uuid)
```

Note that you are required to provide a unique id for the model 
to delete. A response with status 204 (no content) indicates success.


## Update and Patch Endpoints

An update coincides with "POST" and requires that you provide all of the model's
required fields. If you want to update only a substet of fields, then you
want to use the patch functions, which coincide with "PATCH." Patch
endpoints include:

```python
> client.patch_distributions(uuid, data)
> client.patch_collections(uuid, data)
> client.patch_compositeparts(uuid, data)
> client.patch_institutions(uuid, data)
> client.patch_modules(uuid, data)
> client.patch_operations(uuid, data)
> client.patch_orders(uuid, data)
> client.patch_organisms(uuid, data)
> client.patch_parts(uuid, data)
> client.patch_plans(uuid, data)
> client.patch_plates(uuid, data)
> client.patch_protocols(uuid, data)
> client.patch_robots(uuid, data)
```

For each function above, "data" should be a dictionary of parameters that you
want to update.  See the examples below for how to use patch.


## Errors

If you get a bad request, try looking at the json response to determine why:


```python
collection = client.create_collection(name=name, description=description)                                   
ERROR Error with /api/collections/, return value 400: Bad Request

> collection.reason                                                                                           
# 'Bad Request'

> collection.json()
# {'name': ['collection with this name already exists.']}
```

If you get a 400 family of errors, this indicates Permission denied,
and typically results because you need to be staff or superuser to
use endpoints that modify data.


## Examples

### Create an Author

You can create an author as follows:

```python
name = "Big Bird"
email = "yellowisgreat@bird.dev"
affiliation = "Sesame Street"

author = client.create_author(name=name, email=email, affiliation=affiliation)
```

Here is a successful response, and note that you can also provide an orcid id,
although it's not required.

```python
> author
{'uuid': 'e246f6bb-5cc4-4cc3-bd41-73d24567c0f4',
 'name': 'Big Bird',
 'email': 'yellowisgreat@bird.dev',
 'affiliation': 'Sesame Street',
 'orcid': None,
 'tags': [],
 'label': 'author'}
```

### Update an Author

Oh no, we make a mistake! Let's update the author we just made. Since we don't
want to provide all fields, we are going to use patch.

```python
author = client.patch_author(uuid=author['uuid'], data={"name": "Notsobig Bird"})
{'uuid': 'f176b56a-bd27-42d5-8867-0d53f09e54e3',
 'name': 'Notsobig Bird',
 'email': 'yellowisgreat@bird.dev',
 'affiliation': 'Sesame Street',
 'orcid': None,
 'tags': [],
 'label': 'author'}
```

### Create a Container

```python
name = "Crayon Box"
container_type = "trash"
description = "This is a crayon trash box?"
parent_id = "1ca52bd5-05e6-4f4f-913b-6760bed611f2"

container = client.create_container(name=name, container_type=container_type, description=description, parent_id=parent_id)
```

Note that since the top level parent container is the lab (only one per instance), you are required to provide
a parent id. Here is the created container:

```python
> container
{'uuid': 'a5541413-b002-4914-8d17-c2d8a30bc962',
 'time_created': '2019-10-06T11:47:39.464202-05:00',
 'time_updated': '2019-10-06T11:47:39.464250-05:00',
 'name': 'Crayon Box',
 'container_type': 'trash',
 'description': 'This is a crayon trash box?',
 'estimated_temperature': None,
 'x': None,
 'y': None,
 'z': None,
 'parent': '1ca52bd5-05e6-4f4f-913b-6760bed611f2',
 'plates': [],
 'label': 'container'}
```

### Update a Container

Let's update the container above.

```python
container = client.patch_container(uuid=container['uuid'], data={'name': 'Marker Box'})
{'uuid': '6f39b0ae-ca9c-4b7c-8d71-071283349852',
 'time_created': '2019-10-09T09:38:30.590297-05:00',
 'time_updated': '2019-10-09T09:39:14.051493-05:00',
 'name': 'Marker Box',
 'container_type': 'trash',
 'description': 'This is a crayon trash box?',
 'estimated_temperature': None,
 'x': None,
 'y': None,
 'z': None,
 'parent': '763221b0-8bdd-4b23-8da0-95eedce877ba',
 'plates': [],
 'label': 'container'}
```

### Create a Distribution

A distribution requires a name and description

```python
name = "Send out the hounds"
description = "So many hounds"
plateset_ids = ["37d895e3-eaf1-48f5-ad3d-9a7571e4434c"]

dist = client.create_distribution(name=name, description=description, plateset_ids=plateset_ids)
```

Here is the created distribution:

```python
> dist
{'uuid': '418f1e66-7f3b-46cf-b707-40bad407f202',
 'time_created': '2019-10-06T11:53:20.121227-05:00',
 'time_updated': '2019-10-06T11:53:20.121277-05:00',
 'name': 'Send out the hounds',
 'description': 'So many hounds',
 'platesets': ['37d895e3-eaf1-48f5-ad3d-9a7571e4434c'],
 'label': 'distribution'}
```

Note that you can provide a list of plateset ids, or a single id for platesets.

### Update a Distribution

Update the distribution as follows:

```python
dist = client.patch_distribution(uuid=dist['uuid'], data={"name": "Send in the hounds"})
{'uuid': '418f1e66-7f3b-46cf-b707-40bad407f202',
 'time_created': '2019-10-06T11:53:20.121227-05:00',
 'time_updated': '2019-10-06T11:53:20.121277-05:00',
 'name': 'Send in the hounds',
 'description': 'So many hounds',
 'platesets': ['37d895e3-eaf1-48f5-ad3d-9a7571e4434c'],
 'label': 'distribution'}
```


### Create a Collection

A collection requires a name and description, and a parent_id is required.

```python
name="dinosaur-collection"                                                                                  
description="This is the description"
parent_id = '763221b0-8bdd-4b23-8da0-95eedce877ba'                      

collection = client.create_collection(name=name, description=description, parent_id=parent_id)
```

If you are superuser or admin, the created collection will be returned.

```python
{'uuid': 'ec624409-26cb-4882-969e-f0d7c1c1aa44',
 'time_created': '2019-10-06T10:01:36.935007-05:00',
 'time_updated': '2019-10-06T10:01:36.935073-05:00',
 'name': 'dinosaur-collection',
 'description': 'This is the description',
 'parent': None,
 'tags': [],
 'label': 'collection'}
```

You can also provide a parent collection id with `parent_id` or a list of
tag ids with "tag_ids".


### Update a Collection

To update a collection:

```python
collection = client.patch_collection(uuid=collection['uuid'], data={"name": "avocado-collection"})
{'uuid': 'ec624409-26cb-4882-969e-f0d7c1c1aa44',
 'time_created': '2019-10-06T10:01:36.935007-05:00',
 'time_updated': '2019-10-06T10:01:36.935073-05:00',
 'name': 'avocado-collection',
 'description': 'This is the description',
 'parent': None,
 'tags': [],
 'label': 'collection'}
```

### Create a Module

To create a module, you need to provide more fields:

```python
name = "Dinosaur module"
notes = "This is a module for dinosaurs."
model_id = "dino-raptor-3000"
module_type = "pipette"
container_id = "1ca52bd5-05e6-4f4f-913b-6760bed611f2"

module = client.create_module(name=name, notes=notes, model_id=model_id, module_type=module_type, container_id=container_id)
```

Note that the container id is the uuid for an existing container in the database.
A successful response looks like the following:

```python
> module
{'uuid': '1b46bb05-09c9-401c-9f32-b1a17240a3ba',
 'time_created': '2019-10-06T11:34:26.698264-05:00',
 'time_updated': '2019-10-06T11:34:26.698314-05:00',
 'name': 'Dinosaur module',
 'container': '1ca52bd5-05e6-4f4f-913b-6760bed611f2',
 'notes': 'This is a module for dinosaurs.',
 'model_id': 'dino-raptor-3000',
 'module_type': 'pipette',
 'data': {},
 'label': 'module'}
```

### Update a Module

To update a module:

```python
module = client.patch_module(uuid=module['uuid'], data={"name": "Avocado Module"})
```

```python
> module
{'uuid': '1b46bb05-09c9-401c-9f32-b1a17240a3ba',
 'time_created': '2019-10-06T11:34:26.698264-05:00',
 'time_updated': '2019-10-06T11:34:26.698314-05:00',
 'name': 'Avocado Module',
 'container': '1ca52bd5-05e6-4f4f-913b-6760bed611f2',
 'notes': 'This is a module for dinosaurs.',
 'model_id': 'dino-raptor-3000',
 'module_type': 'pipette',
 'data': {},
 'label': 'module'}
```


### Create an Institution

An institution only required a name, and a boolean to indicate if they have
signed a master MTA agreement (defaults to False):

```python
name = "Dinosaur College"
signed_master = True

institution = client.create_institution(name=name, signed_master=signed_master)
```

A successful response looks like the following:

```python
{'uuid': 'b8ebf93f-5418-4a19-b2ab-1b6737ba1142',
 'name': 'Dinosaur College',
 'signed_master': True,
 'label': 'institution'}
```

### Update an Institution

```python
institution = client.patch_institution(uuid=institution['uuid'], data={"name": "Lizard School"})
{'uuid': 'cf7176db-38ef-4188-8f99-27458da7558a',
 'name': 'Lizard School',
 'signed_master': True,
 'label': 'institution'}
```


### Create an Operation

An operation requires a name and description.

```python
name = "Operation Neptune"
description = "pew pew pew"

operation = client.create_operation(name=name, description=description)
```

A successful operation looks like the following:

```python
> operation

{'uuid': '9374b582-8237-4939-8ff6-0fbdce691724',
 'time_created': '2019-10-06T11:37:45.301572-05:00',
 'time_updated': '2019-10-06T11:37:45.301623-05:00',
 'name': 'Operation Neptune',
 'description': 'pew pew pew',
 'plans': [],
 'label': 'operation'}
```

Note that you can also provide a list of `plan_ids` to select plans.

### Update an Operation

```python
operation = client.patch_operation(uuid=operation['uuid'], data={"name": "Operation Venus"})
```


### Create an Order

Orders require a name and a description.

```python
name = "Buy Taco Genes"
notes = "Extra avocado please"

order = client.create_order(name=name, notes=notes)
```

A successful response looks like the following:

```python
> order
{'uuid': 'b43a53e8-d957-434d-8553-ab7384e0db1f',
 'time_created': '2019-10-06T11:40:39.715394-05:00',
 'time_updated': '2019-10-06T11:40:39.715426-05:00',
 'name': 'Buy Taco Genes',
 'notes': 'Extra avocado please',
 'distributions': [],
 'label': 'order'}
```

You can also provide `distribution_ids` to add one or more distributions to
the order (a list).

### Update an Order

```python
order = client.patch_order(uuid=order['uuid'], data={'notes': 'Extra avocado AND beans'})
```

### Create an Organism

An organism requires a name, description, and genotype.

```python
name = "Vanessasaurus"
description = "A soon to be extinct dinosaur."	
genotype = "Gaaattaagaataata"

organism = client.create_organism(name=name, description=description, genotype=genotype)
```

Here is a successful response:

```python
> organism
{'uuid': 'bafb3e9a-7bd0-40fc-a402-f17793e4ff05',
 'time_created': '2019-10-06T12:29:24.371688-05:00',
 'time_updated': '2019-10-06T12:29:24.371721-05:00',
 'name': 'Vanessasaurus',
 'description': 'A soon to be extinct dinosaur.',
 'genotype': 'Gaaattaagaataata',
 'label': 'organism'}
```

### Update an Organism

```python
organism = client.patch_organism(uuid=organism['uuid'], data={"description": "An extinct dinosaur"})
```


### Create a Part

A part requires the following fields:

```python
kwargs = {
    "name": "Thread",
    "description": "a piece of twine",
    "gene_id": "twiney-123",
    "part_type": "plasmid",
    "primer_forward": "AATG",
    "primer_reverse": "TGAA",	
    "author_id": "c9d9237b-c4f7-48a9-9ac1-33c2393cfbf1"
}

part = client.create_part(**kwargs)
```

A successful response looks like the following:

```python
> part
{'uuid': 'e0fd70fe-3c82-4b48-83f2-ac2425a9e177',
 'time_created': '2019-10-06T12:42:35.703039-05:00',
 'time_updated': '2019-10-06T12:42:35.703081-05:00',
 'name': 'Thread',
 'description': 'a piece of twine',
 'status': 'null',
 'gene_id': 'twiney-123',
 'part_type': 'plasmid',
 'genbank': {},
 'original_sequence': None,
 'optimized_sequence': None,
 'synthesized_sequence': None,
 'full_sequence': None,
 'vector': None,
 'primer_forward': 'AATG',
 'primer_reverse': 'TGAA',
 'barcode': None,
 'label': 'part',
 'translation': None,
 'tags': [],
 'collections': [],
 'author': 'c9d9237b-c4f7-48a9-9ac1-33c2393cfbf1'}
```

### Update a Part

```python
part = client.patch_part(uuid=part['uuid'], data={'name': 'Thimble'})
```

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

We assume that the sequence provided is circular, but if it's not, you should set circular
to False:

```python
> composite_part = client.create_composite_part(name=name, sequence=sequence, circular=False)
```

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

### Update a Composite Part

This is the one slightly different patch function, because if you provide a sequence
it will calculate updated parts, and if you provide just parts, you are also required to
provide the corresponding sequence. The circular argument is also provided as a boolean.

```python
composite_part = client.patch_composite_part(uuid=composite_part['uuid'], data={'sequence': sequence}, circular=False)
```

### Create a Plan

```python
name = "Dr. Evil's Plan"
description = "One hundred... billion dollars!"
status = "Planned"
operation_id = '9374b582-8237-4939-8ff6-0fbdce691724'

plan = client.create_plan(name=name, description=description, status=status, operation_id=operation_id)
```

The successful response looks like the following:

```python
> plan
{'uuid': '1f9bf6ab-0871-4d70-948f-533df87914af',
 'time_created': '2019-10-06T12:49:58.534434-05:00',
 'time_updated': '2019-10-06T12:49:58.534480-05:00',
 'name': "Dr. Evil's Plan",
 'description': 'One hundred... billion dollars!',
 'parent': None,
 'operation': '9374b582-8237-4939-8ff6-0fbdce691724',
 'status': 'Planned',
 'label': 'plan'}
```

Note you can also provide a `parent_id`  if relevant.

### Update a Plan

```python
plan = client.patch_plan(uuid=plan['uuid'], data={"name": "Austin Power's Plan"})
```

### Create a Plate

The following fields are required:

```python
kwargs = {
    "plate_type": "culture",
    "plate_form": "standard96",
    "status": "Planned",
    "name": "Broccoli Fingers",
    "notes": "Broccolini or broccoli?",
    "container_id": "1ca52bd5-05e6-4f4f-913b-6760bed611f2"
}

plate = client.create_plate(**kwargs)
```

Note that you can also provide `well_ids` and `protocol_id`, along with `length` and `width`. 
Here is the created object:

```python
> plate
{'uuid': '8463b8b7-3726-4919-8dac-e8f71c445280',
 'time_created': '2019-10-06T12:56:40.314493-05:00',
 'time_updated': '2019-10-06T12:56:40.314532-05:00',
 'plate_type': 'culture',
 'plate_form': 'standard96',
 'status': 'Planned',
 'name': 'Broccoli Fingers',
 'thaw_count': 0,
 'notes': 'Broccolini or broccoli?',
 'height': 16,
 'length': 24,
 'container': '1ca52bd5-05e6-4f4f-913b-6760bed611f2',
 'protocol': None,
 'wells': [],
 'label': 'plate'}
```

### Update a Plate

```python
plate = client.patch_plate(uuid=plate['uuid'], data={"notes": "Asparagus"})
```

### Create a PlateSet

You are required to provide one or more plates to create a plateset.

```python
description = "The best plates"
name = "My Plates"
plate_ids = ['8463b8b7-3726-4919-8dac-e8f71c445280']

plateset = client.create_plateset(description=description, name=name, plate_ids=plate_ids)
```

The created object is shown below.

```python
> plateset
{'uuid': '6e12439e-2aff-4e16-9726-390e8d21b198',
 'description': 'The best plates',
 'name': 'My Plates',
 'time_created': '2019-10-06T12:59:11.632197-05:00',
 'time_updated': '2019-10-06T12:59:11.632245-05:00',
 'plates': ['8463b8b7-3726-4919-8dac-e8f71c445280'],
 'label': 'plateset'}
```

### Update a PlateSet

```python
plateset = client.patch_plateset(uuid=plateset['uuid'], data={"name": "Your Plates"})
```

### Create a Sample

You must provide wells and a part unique id:

```
part_id = "243611b6-124a-461f-bfba-bf745b131db3"
well_ids = ['565ab16f-4fb0-45ec-a296-a620a5cd0d24',
            '0740224f-34d5-45c4-a672-30b5ed6e1472']

sample = client.create_sample(part_id=part_id, well_ids=well_ids)
```

Here is a successful response:

```
> sample
{'uuid': 'da03fed5-0d67-498d-9071-22485f479d4f',
 'outside_collaborator': True,
 'sample_type': None,
 'status': None,
 'evidence': None,
 'vendor': None,
 'time_created': '2019-10-06T13:16:53.029585-05:00',
 'time_updated': '2019-10-06T13:16:53.029633-05:00',
 'derived_from': None,
 'part': '243611b6-124a-461f-bfba-bf745b131db3',
 'index_forward': None,
 'index_reverse': None,
 'label': 'sample',
 'wells': ['0740224f-34d5-45c4-a672-30b5ed6e1472',
  '565ab16f-4fb0-45ec-a296-a620a5cd0d24']}
```

### Update a Sample

```python
sample = client.patch_sample(uuid=sample['uuid'], data={"vendor": "Meatball"})
```

### Create a Protocol

You only are required to add a description for a protocol.

```python
description = "What is a Protocol, Protocol"

protocol = client.create_protocol(description=description)
```

If you want to add "data" (a dictionary) for it, you can specify `protocol_data`
or a schema with `schema_id`. Here is a response from the above:

```python
> protocol
{'uuid': '9c0dea2c-07fd-4697-86b9-02f7f84647e1',
 'time_created': '2019-10-06T13:00:30.479923-05:00',
 'time_updated': '2019-10-06T13:00:30.479962-05:00',
 'data': {},
 'description': 'What is a Protocol, Protocol',
 'label': 'protocol',
 'schema': None}
```

### Update a Protocol

```python
protocol = client.patch_protocol(uuid=protocol['uuid'], data={'description': 'Over there!'})
```

### Create a Robot

Here is how to create a robot:

```python
kwargs = {
    "container_id": "1ca52bd5-05e6-4f4f-913b-6760bed611f2",
    "name": "Dinobot",
    "robot_id": "dinobot-3000",
    "notes": "This is the dinobot.",
    "server_version": "1.0.0",
    "right_mount_id": '1b46bb05-09c9-401c-9f32-b1a17240a3ba',
    "left_mount_id": '3443ba88-a75e-4f1b-be96-eb185745528e'
}	

robot = client.create_robot(**kwargs)
```

You can also provide an optional `robot_type`. Here is the successful response:

```python
> robot
{'uuid': '89d360ed-211b-4a27-8a54-601e4d0ec8ed',
 'time_created': '2019-10-06T13:07:21.996704-05:00',
 'time_updated': '2019-10-06T13:07:21.996914-05:00',
 'container': '1ca52bd5-05e6-4f4f-913b-6760bed611f2',
 'name': 'Dinobot',
 'robot_id': 'dinobot-3000',
 'robot_type': 'OT2',
 'notes': 'This is the dinobot.',
 'server_version': '1.0.0',
 'right_mount': '1b46bb05-09c9-401c-9f32-b1a17240a3ba',
 'left_mount': '3443ba88-a75e-4f1b-be96-eb185745528e',
 'label': 'robot'}
```

### Update a Robot

```python
robot = client.patch_robot(uuid=robot['uuid'], data={"name": "TVBot"})
```

### Create a Schema

Here is how to create a schema:

```python
name = "Robot Schema"
description = "This is the schema for a robot"	
schema_version = "1.0.0"

schema = client.create_schema(name=name, description=description, schema_version=schema_version)
```

Here is the successful response:

```python
> schema
{'uuid': '0764da51-7ecc-466d-a488-b12a31924162',
 'time_created': '2019-10-06T13:19:05.715045-05:00',
 'time_updated': '2019-10-06T13:19:05.715099-05:00',
 'name': 'Robot Schema',
 'description': 'This is the schema for a robot',
 'schema': {},
 'schema_version': '1.0.0',
 'label': 'schema'}
```

### Update a Schema

```python
schema = client.patch_schema(uuid=schema['uuid'], data={'description': "This is not a schema for a robot"})
```

### Create a Tag

Creating a tag simply requires a tag!

```python
tag = client.create_tag(tag="bogey")

> tag
{'uuid': 'd600c0f6-9ff8-4e3b-9c27-07f5476f54be',
 'tag': 'bogey',
 'label': 'tag'}
```

### Update a Tag

```python
tag = client.patch_tag(uuid=tag['uuid'], data={'tag': 'down-now'})
```
