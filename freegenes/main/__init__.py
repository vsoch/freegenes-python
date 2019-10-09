'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from freegenes.version import __version__
from freegenes.logger import bot

from .helpers import derive_parts
from .cache import cache_parts

import requests
import os
import re

class Client(object):

    def __init__(self, token=None, base="https://freegenes.dev", validate=True):
 
        self.validate = validate
        self._set_base(base)
        self._set_token(token)
        self._set_headers()
        self._test_token()
        self.cache = {}

    def __repr__(self):
        return "[client][freegenes][%s]" % __version__

    def __str__(self):
        return "[client][freegenes][%s]" % __version__

    def _set_token(self, token):
        '''ensure that token provided, or FREEGENES_TOKEN is defined in environ
        '''
        self.token = os.environ.get('FREEGENES_TOKEN', token)
        if not self.token:
            if self.validate:
                bot.exit("You must provide a token or export FREEGENES_TOKEN.")
            bot.warning("No token provided, API will not function as expected.")

    def _set_base(self, base):
        '''look for FREEGENES_BASE defined in environ
        '''
        self.base = os.environ.get('FREEGENES_BASE', base)
        if self.base:
            self.base = self.base.strip('/')

    def _set_headers(self):
        '''set the headers to the default, meaning we provide an
           authorization token.
        '''
        self.headers = {
          "Accept": "application/json",
          "Authorization": "Token %s" % self.token
        }

    def _prepare_url(self, url):
        '''add the given url to a base url, also ensure that it ends in a slash
        '''
        fullurl = "%s%s" %(self.base, url)

        if not fullurl.endswith('/'):
            fullurl = "%s/" % fullurl
        return fullurl

    def _test_token(self):
        '''test that the token works - this function also ensures
           that the base is correct.
        '''
        if self.validate:
            if requests.head("%s" % self.base, headers=self.headers).status_code != 200:
                bot.exit('Provided token is invalid.')

    # Specific API calls

    def get(self, url, headers=None, paginate=True, limit=1000):
        '''the default get, will use default headers if custom aren't defined.
           we take a partial url (e.g., /api/authors) and then add the base.

           Parameters
           ==========
           url: the url endpoint to query (without the http/s or domain)
           headers: if defined, don't use default headers.
           paginate: obtain all pages after query (default is True)
           limit: number of responses per query (default 1000)
        '''
        heads = headers or self.headers

        # A second call will already provide a complete url
        fullurl = "%s?limit=%s" %(self._prepare_url(url), limit)
        if url.startswith('http'):
            fullurl = url

        response = requests.get(fullurl, headers=heads)

        # Return a successful response
        if response.status_code == 200:
 
            response = response.json()
            results = response

            # Listings will have results, single entity not
            if "results" in response:
                results = response['results']

            # Are there pages (but the user doesn't want a specific one)
            if paginate:
                next_url = response.get('next')
                if next_url is not None:
                    return results + self.get(next_url, headers)
            return results

        bot.error("Error with %s, return value %s: %s" %(url, response.status_code, response.reason))
        return response

    def patch(self, url, data, headers=None):
        '''a patch request is used for a partial update.
        '''
        return self._create(url, requests.patch, data, headers, "patch")

    def post(self, url, data=None, headers=None):
        '''a wrapper to create, providing requests.post as the function
        '''
        return self._create(url, requests.post, data, headers)

    def put(self, url, data=None, headers=None):
        '''a wrapper to create, providing requests.put as the function
        '''
        return self._create(url, requests.put, data, headers)

    def _create(self, url, func, data=None, headers=None, name="create"):
        '''create is a base method that can handle a put or post, and
           the caller is required to provide a function handle.
           Uses default headers if custom aren't defined.
           we take a partial url (e.g., /api/authors) and then add the base.

           Parameters
           ==========
           url: the url endpoint to query (without the http/s or domain)
           data: data to add to the request.
           headers: if defined, don't use default headers.
        '''
        heads = headers or self.headers

        # Get the full url, must end in slash
        fullurl = self._prepare_url(url)

        # Remove empty / None fields from data (not booleans!)
        if data:
            data = {k:v for k,v in data.items() if v not in [None, ""]}

        # POST indicates create or update, we need at least one field
        if not data:
            bot.exit("At least one parameter must be provided for a %s" % name)

        response = func(fullurl, headers=heads, data=data)

        # Return a successful response
        if response.status_code in [200, 201]: 
            return response.json()

        bot.error("Error with %s, return value %s: %s" %(url, 
                                                         response.status_code, 
                                                         response.reason))
        return response

    def delete(self, url, headers=None):
        '''data is required (typically with a unique id in the url to identify 
           the object to delete)

           Parameters
           ==========
           url: the url endpoint to query (without the http/s or domain)
        '''
        heads = headers or self.headers
        fullurl = self._prepare_url(url)
        response = requests.delete(fullurl, headers=heads)

        if response.status_code not in [204]: 
            bot.error("Error with %s, return value %s: %s" %(url, response.status_code, response.reason))

        return response

    def create_entity(self, name, data=None):
        '''create an entity with a POST request.

           Parameters
           ==========
           name: the name of the endpoint to post to.
           data: key word arguments to include.
        '''
        return self.post('/api/%s/' % name, data=data)


    # UPDATE Endpoints

    def update_entity(self, name, uuid, data):
        '''delete an entity with a DELETE request. For all entities,
           we take the uuid, and the name of the delete endpoint.
        '''
        if not uuid:
            bot.exit("A unique id (uuid) is required to update.")
        return self.put('/api/%s/%s/' % (name, uuid), data)


    # PATCH (partial update) Endpoints

    def patch_entity(self, name, uuid, data):
        '''A partial update performs a patch, allowing for update of just
           a single (or not all required) fields.
        '''
        return self.patch('/api/%s/%s' % (name, uuid), data)

    def patch_author(self, uuid, data):
        return self.patch_entity('authors', uuid, data)

    def patch_collection(self, uuid, data):
        return self.patch_entity('collections', uuid, data)

    def patch_composite_part(self, uuid, data, circular=True):

        # The user is allowed to update a composite part based on a new sequence
        if "sequence" in data:

            # [(uuid, direction, start, end),
            selected_parts = self._derive_parts(data['sequence'], circular)
            data['part_ids'] = [x[0] for x in selected_parts]
            data['direction_string'] = "".join([x[1] for x in selected_parts])

        # If part ids is in data, we also require sequence
        if "part_ids" in data and "sequence" not in data:
            bot.exit("If updating part_ids, a sequence must also be provided.")

        return self.patch_entity('compositeparts', uuid, data)

    def patch_container(self, uuid, data):
        return self.patch_entity('containers', uuid, data)

    def patch_distribution(self, uuid, data):
        return self.patch_entity('distributions', uuid, data)

    def patch_institution(self, uuid, data):
        return self.patch_entity('institutions', uuid, data)

    def patch_module(self, uuid, data):
        return self.patch_entity('modules', uuid, data)

    def patch_operation(self, uuid, data):
        return self.patch_entity('operations', uuid, data)

    def patch_order(self, uuid, data):
        return self.patch_entity('orders', uuid, data)

    def patch_organism(self, uuid, data):
        return self.patch_entity('organisms', uuid, data)

    def patch_part(self, uuid, data):
        return self.patch_entity('parts', uuid, data)

    def patch_plan(self, uuid, data):
        return self.patch_entity('plans', uuid, data)

    def patch_plate(self, uuid, data):
        return self.patch_entity('plates', uuid, data)

    def patch_plateset(self, uuid, data):
        return self.patch_entity('platesets', uuid, data)

    def patch_protocol(self, uuid, data):
        return self.patch_entity('protocols', uuid, data)

    def patch_robot(self, uuid, data):
        return self.patch_entity('robots', uuid, data)

    def patch_sample(self, uuid, data):
        return self.patch_entity('samples', uuid, data)

    def patch_schema(self, uuid, data):
        return self.patch_entity('schemas', uuid, data)

    def patch_tag(self, uuid, data):
        return self.patch_entity('tags', uuid, data)

    # DELETE Endpoints

    def delete_entity(self, name, uuid):
        '''delete an entity with a DELETE request. For all entities,
           we take the uuid, and the name of the delete endpoint.
        '''
        return self.delete('/api/%s/%s' % (name, uuid))

    def delete_author(self, uuid):
        return self.delete_entity('authors', uuid)

    def delete_collection(self, uuid):
        return self.delete_entity('collections', uuid)

    def delete_composite_part(self, uuid):
        return self.delete_entity('compositeparts', uuid)

    def delete_container(self, uuid):
        return self.delete_entity('containers', uuid)

    def delete_distribution(self, uuid):
        return self.delete_entity('distributions', uuid)

    def delete_institution(self, uuid):
        return self.delete_entity('institutions', uuid)

    def delete_module(self, uuid):
        return self.delete_entity('modules', uuid)

    def delete_operation(self, uuid):
        return self.delete_entity('operations', uuid)

    def delete_order(self, uuid):
        return self.delete_entity('orders', uuid)

    def delete_organism(self, uuid):
        return self.delete_entity('organisms', uuid)

    def delete_part(self, uuid):
        return self.delete_entity('parts', uuid)

    def delete_plan(self, uuid):
        return self.delete_entity('plans', uuid)

    def delete_plate(self, uuid):
        return self.delete_entity('plates', uuid)

    def delete_plateset(self, uuid):
        return self.delete_entity('platesets', uuid)

    def delete_protocol(self, uuid):
        return self.delete_entity('protocols', uuid)

    def delete_robot(self, uuid):
        return self.delete_entity('robots', uuid)

    def delete_sample(self, uuid):
        return self.delete_entity('samples', uuid)

    def delete_schema(self, uuid):
        return self.delete_entity('schemas', uuid)

    def delete_tag(self, uuid):
        return self.delete_entity('tags', uuid)


    # GET Endpoints

    def get_entity(self, name, uuid=None):
        '''return a single entity if a uuid is provided, otherwise a list

           Parameters
           ==========
           uuid: the unique resource identifier of the entity
        '''
        if uuid:
            return self.get('/api/%s/%s/' % (name, uuid))
        return self.get('/api/%s/' % name)


    def get_authors(self, uuid=None):
        return self.get_entity('authors', uuid)

    def get_collections(self, uuid=None):
        return self.get_entity('collections', uuid)

    def get_composite_parts(self, uuid=None):
        return self.get_entity('compositeparts', uuid)

    def get_containers(self, uuid=None):
        return self.get_entity('containers', uuid)

    def get_distributions(self, uuid=None):
        return self.get_entity('distributions', uuid)

    def get_institutions(self, uuid=None):
        return self.get_entity('institutions', uuid)

    def get_modules(self, uuid=None):
        return self.get_entity('modules', uuid)

    def get_operations(self, uuid=None):
        return self.get_entity('operations', uuid)

    def get_orders(self, uuid=None):
        return self.get_entity('orders', uuid)

    def get_organisms(self, uuid=None):
        return self.get_entity('organisms', uuid)

    def get_parts(self, uuid=None):
        return self.get_entity('parts', uuid)

    def get_plans(self, uuid=None):
        return self.get_entity('plans', uuid)

    def get_plates(self, uuid=None):
        return self.get_entity('plates', uuid)

    def get_platesets(self, uuid=None):
        return self.get_entity('platesets', uuid)

    def get_protocols(self, uuid=None):
        return self.get_entity('protocols', uuid)

    def get_robots(self, uuid=None):
        return self.get_entity('robots', uuid)

    def get_samples(self, uuid=None):
        return self.get_entity('samples', uuid)

    def get_schemas(self, uuid=None):
        return self.get_entity('schemas', uuid)

    def get_tags(self, uuid=None):
        return self.get_entity('tags', uuid)


    # POST and PUT Endpoints (create and update) require same fields

    # Authors

    def create_author(self, name, 
                            email, 
                            affiliation, 
                            uuid=None, 
                            orcid=None,
                            tag_ids=None, update=False):
        '''create a new author using the FreeGenes API. Must be superuser
           or staff, and provide required fields in data.
        '''
        data = {"name": name,
                "email": email,
                "affiliation": affiliation,
                "orcid": orcid,
                "tags": tag_ids}

        if update:
            return self.update_entity("authors", uuid, data)
        return self.create_entity("authors", data)

    def update_author(self, uuid, name, email, affiliation, orcid=None, tag_ids=None):
        return self.create_author(name, email, affiliation, uuid, orcid, tag_ids, update=True)


    # Containers

    def create_container(self, name, 
                               container_type, 
                               description, 
                               parent_id,
                               uuid=None,
                               estimated_temperature=None, 
                               x=None, y=None, z=None, update=False):
        '''create a new container using the FreeGenes API. Must be superuser
           or staff, and provide required fields in data.
        '''
        data = {"name": name,
                "parent": parent_id,
                "container_type": container_type,
                "description": description,
                "estimated_temperature": estimated_temperature,
                "x": x, "y": y, "z": z}

        if update:
            return self.update_entity("containers", uuid, data)
        return self.create_entity("containers", data)

    def update_container(self, uuid, name, container_type, description, parent_id,
                         estimated_temperature=None, x=None, y=None, z=None):
        return self.create_container(name, container_type, description, parent_id,
                                     uuid, estimated_temperature, x, y, z, update=True)


    # Collections

    def create_collection(self, name, 
                                description,
                                parent_id,
                                uuid=None,
                                tag_ids=None, update=False):
        '''create a new collection using the FreeGenes API. Must be superuser
           or staff, and provide required fields in data.
        '''
        data = {"name": name, 
                "description": description,
                "parent": parent_id,
                "tags": tag_ids}

        if update:
            return self.update_entity("collections", uuid, data)
        return self.create_entity("collections", data)

    def update_collection(self, uuid, name, description, parent_id, tag_ids=None):
        return self.create_collection(name, description, parent_id, uuid, tag_ids, update=True)


    # Distributions

    def create_distribution(self, name, 
                                  description,
                                  plateset_ids, 
                                  uuid=None, update=False):
        '''create a new distribution using the FreeGenes API. Must be superuser
           or staff, and provide required fields in data.
        '''
        data = {"name": name,
                "description": description,
                "platesets": plateset_ids}

        if update:
            return self.update_entity("distributions", uuid, data)
        return self.create_entity("distributions", data)

    def update_distribution(self, uuid, name, description, plateset_ids):
        return self.create_distribution(name, description, plateset_ids, uuid, update=True)


    # Modules

    def create_module(self, name, 
                            container_id, 
                            notes, 
                            model_id, 
                            module_type,
                            uuid=None, 
                            module_data=None, update=False):
        '''create a new module using the FreeGenes API. Must be superuser
           or staff, and provide required fields in data.
        '''
        data = {"name": name,
                "notes": notes,
                "container": container_id,
                "model_id": model_id,
                "module_type": module_type,
                "data": module_data}

        if update:
            return self.update_entity("modules", uuid, data)
        return self.create_entity("modules", data)

    def update_module(self, uuid, name, container_id, notes, model_id, module_type, module_data=None):
        return self.create_module(name, container_id, notes, model_id, module_type, uuid, module_data, update=True)


    # Institutions

    def create_institution(self, name, uuid=None, signed_master=False, update=False):
        '''create a new institution using the FreeGenes API. Must be superuser
           or staff, and provide required fields in data.
        '''
        data = {"name": name, "signed_master": signed_master}

        if update:
            return self.update_entity("institutions", uuid, data)
        return self.create_entity("institutions", data)

    def update_institution(self, uuid, name, signed_master=False):
        return self.create_institution(name, uuid, signed_master, update=True)


    # Operations

    def create_operation(self, name, description, uuid=None, plan_ids=None, update=False):
        '''create a new operation using the FreeGenes API. Must be superuser
           or staff, and provide required fields in data.
        '''
        data = {"name": name,
                "description": description,
                "plans": plan_ids}

        if update:
            return self.update_entity("operations", uuid, data)
        return self.create_entity("operations", data)

    def update_operation(self, uuid, name, description, plan_ids):
         return self.create_operation(name, description, uuid, plan_ids, update=True)


    # Orders

    def create_order(self, name, notes, uuid=None, distribution_ids=None, update=False):
        '''create a new order using the FreeGenes API. Must be superuser
           or staff, and provide required fields in data.
        '''
        data = {"name": name,
                "notes": notes,
                "distributions": distribution_ids}

        if update:
            return self.update_entity("orders", uuid, data)
        return self.create_entity("orders", data)


    def update_order(self, uuid, name, notes, distribution_ids=None):
        return self.create_order(name, notes, uuid, distribution_ids, update=True)


    # Organisms

    def create_organism(self, name, description, genotype, uuid=None, update=False):
        '''create a new organism using the FreeGenes API. Must be superuser
           or staff, and provide required fields in data.
        '''
        data = {"name": name,
                "description": description,
                "genotype": genotype}

        if update:
            return self.update_entity("organisms", uuid, data)
        return self.create_entity("organisms", data)

    def update_organism(self, uuid, name, description, genotype):
        return self.create_organism(name, description, genotype, uuid, update=True)


    # Plans

    def create_plan(self, name, 
                          description,
                          status,
                          operation_id,
                          uuid=None,
                          parent_id=None, update=False):
        '''create a new plan using the FreeGenes API. Must be superuser
           or staff, and provide required fields in data.
        '''
        data = {"name": name,
                "operation": operation_id,
                "parent": parent_id,
                "description": description,
                "status": status}

        if update:
            return self.update_entity("plans", uuid, data)
        return self.create_entity("plans", data)

    def update_plan(self, uuid, name, description, status, operation_id, parent_id=None):
        return self.create_plan(name, description, status, operation_id, uuid, parent_id, update=True)


    # Parts

    def create_part(self, name, 
                          gene_id, 
                          author_id, 
                          part_type,
                          primer_forward,
                          primer_reverse, 
                          uuid=None,
                          genbank=None,
                          original_sequence=None,
                          optimized_sequence=None, 
                          synthesized_sequence=None, 
                          full_sequence=None, 
                          vector=None,
                          description=None, 
                          status=None, 
                          barcode=None,
                          translation=None,
                          tag_ids=None,
                          collection_ids=None, update=False):
        '''create a new part using the FreeGenes API. Must be superuser
           or staff, and provide required fields in data.
        '''
        data = {"name": name,
                "gene_id": gene_id,
                "author": author_id,
                "part_type": part_type,
                "primer_forward": primer_forward,
                "primer_reverse": primer_reverse,
                "genbank": genbank,
                "original_sequence": original_sequence,
                "optimized_sequence": optimized_sequence,
                "synthesized_sequence": synthesized_sequence,
                "full_sequence": full_sequence,
                "vector": vector,
                "barcode": barcode,
                "translation": translation,
                "tags": tag_ids,
                "collections": collection_ids,
                "description": description,
                "status": status}

        if update:
            return self.update_entity("parts", uuid, data)
        return self.create_entity("parts", data)

    def update_part(self, uuid,
                          name, 
                          gene_id, 
                          author_id, 
                          part_type,
                          primer_forward,
                          primer_reverse, 
                          genbank=None,
                          original_sequence=None,
                          optimized_sequence=None, 
                          synthesized_sequence=None, 
                          full_sequence=None, 
                          vector=None,
                          description=None, 
                          status=None, 
                          barcode=None,
                          translation=None,
                          tag_ids=None,
                          collection_ids=None):
        return self.create_part(name, gene_id, author_id, part_type, primer_forward, primer_reverse, 
                                uuid, genbank, original_sequence, optimized_sequence, synthesized_sequence, 
                                full_sequence, vector, description, status, barcode, translation, tag_ids,
                                collection_ids, update=True)


    # Protocols

    def create_protocol(self, description, uuid=None, protocol_data=None, schema_id=None, update=False):
        '''create a new protocol using the FreeGenes API. Must be superuser
           or staff, and provide required fields in data.
        '''
        data = {"description": description,
                "schema": schema_id,
                "data": protocol_data}

        if update:
            return self.update_entity("protocols", uuid, data)
        return self.create_entity("protocols", data)

    def update_protocol(self, uuid, description, protocol_data=None, schema_id=None, update=False):
        return self.create_protocol(description, uuid, protocol_data, schema_id, update=True)


    # Plates

    def create_plate(self, name, 
                           container_id, 
                           plate_type, 
                           plate_form, 
                           status, 
                           notes,
                           uuid=None,
                           protocol_id=None,
                           well_ids=None,
                           thaw_count=None,
                           height=None,
                           length=None, update=False):
        '''create a new plate using the FreeGenes API. Must be superuser
           or staff, and provide required fields in data.
        '''
        data = {"plate_type": plate_type,
                "plate_form": plate_form,
                "container": container_id,
                "status": status,
                "name": name,
                "wells": well_ids,
                "notes": notes,
                "thaw_count": thaw_count,
                "protocol": protocol_id,
                "height": height,
                "length": length}

        if update:
            return self.update_entity("plates", uuid, data)
        return self.create_entity("plates", data)

    def update_plate(self, uuid, name, container_id, plate_type, plate_form, status, notes,
                     protocol_id=None, well_ids=None, thaw_count=None, height=None, length=None):
        return self.create_plate(name, container_id, plate_type, plate_form, status, notes, uuid,
                     protocol_id, well_ids, thaw_count, height, length, update=True)


    # Platesets

    def create_plateset(self, name, description, plate_ids, uuid=None, update=False):
        '''create a new plateset using the FreeGenes API. Must be superuser
           or staff, and provide required fields in data.
        '''
        data = {"description": description,
                "name": name,
                "plates": plate_ids}

        if update:
            return self.update_entity("platesets", uuid, data)
        return self.create_entity("platesets", data)

    def update_plateset(self, uuid, name, description, plate_ids):
        return self.create_plateset(name, description, plate_ids, uuid, update=True)


    # Robots

    def create_robot(self, name,
                           robot_id,
                           container_id,
                           notes,
                           server_version,
                           left_mount_id,
                           right_mount_id, 
                           uuid=None,
                           robot_type=None, update=False):
        '''create a new robot using the FreeGenes API. Must be superuser
           or staff, and provide required fields in data.
        '''
        data = {"name": name,
                "container": container_id,
                "left_mount": left_mount_id,
                "right_mount": right_mount_id,
                "robot_id": robot_id,
                "robot_type": robot_type,
                "notes": notes,
                "server_version": server_version}

        if update:
            return self.update_entity("robots", uuid, data)
        return self.create_entity("robots", data)

    def update_robot(self, uuid, name, robot_id, container_id, notes, server_version, left_mount_id, right_mount_id, robot_type=None):
        return self.create_robot(name, robot_id, container_id, notes, server_version, left_mount_id, right_mount_id, uuid, robot_type, update=True)
    

    # Samples

    def create_sample(self, part_id,
                            well_ids,
                            uuid=None,
                            status=None,
                            evidence=None,
                            outside_collaborator=True,
                            vendor=None,
                            sample_type=None,
                            index_forward=None,
                            index_reverse=None, update=False):
        '''create a new sample using the FreeGenes API. Must be superuser
           or staff, and provide required fields in data.
        '''
        data = {"part": part_id,
                "status": status,
                "evidence": evidence,
                "wells": well_ids,
                "outside_collaborator": outside_collaborator,
                "vendor": vendor,
                "sample_type": sample_type,
                "index_forward": index_forward,
                "index_reverse": index_reverse}

        if update:
            return self.update_entity("samples", uuid, data)
        return self.create_entity("samples", data)

    def update_sample(self, uuid, part_id, well_ids, status=None, evidence=None,
                      outside_collaborator=True, vendor=None, sample_type=None,
                      index_forward=None, index_reverse=None):
        return self.create_sample(self, part_id, well_ids, uuid, status, evidence,
                      outside_collaborator, vendor, sample_type,
                      index_forward, index_reverse, update=True)



    # Schema


    def create_schema(self, name, description, 
                      uuid=None, schema=None,
                      schema_version=None, update=False):
        '''create a new schema using the FreeGenes API. Must be superuser
           or staff, and provide required fields in data.
        '''
        data = {"name": name,
                "description": description,
                "schema": schema,
                "schema_version": schema_version}

        if update:
            return self.update_entity("schemas", uuid, data)
        return self.create_entity("schemas", data)

    def update_schema(self, uuid, name, description, schema=None, schema_version=None):
        return self.create_schema(name, description, uuid, schema, schema_version, update=True)


    # Tag

    def create_tag(self, tag, uuid=None, update=False):
        '''create a new tag using the FreeGenes API. Must be superuser
           or staff, and provide required fields in data.
        '''
        if update:
            return self.update_entity("tags", uuid, {"tag": tag})
        return self.create_entity("tags", {"tag": tag})

    def update_tag(self, uuid, tag):
        return self.create_tag(tag, uuid, update=True)

    
    # Composite Parts

    def create_composite_part(self, name, 
                                    sequence,
                                    uuid=None,
                                    circular=True,
                                    part_ids=None,
                                    description=None,
                                    direction_string=None,
                                    composite_id=None,
                                    composite_type=None, update=False):
        '''create a new composite part from a sequence. If no parts are provided,
           then we search the provided sequence for all parts in FreeGenes, and
           make the association (and derive directions). The data for the parts
           is cached with the client so we only need to derive it once.
           
           Parameters
           ==========
           name: a name for the composite part (required)
           sequence: the new sequence (required)
           circular: is the sequence circular? (default True)
           part_ids: a list of one or more part ids (optional)
           description: a string description (optional)
           composite_id: a composite id (optional) (like gene_id for a part)
           composite_type: the type of composite part (optional)
        '''
        # If part ids not defined, we need to search sequence
        if not part_ids:

            # [(uuid, direction, start, end),
            selected_parts = self._derive_parts(sequence, circular)
            part_ids = [x[0] for x in selected_parts]
            direction_string = "".join([x[1] for x in selected_parts])

        data = {"name": name,
                "parts": part_ids,
                "sequence": sequence,
                "description": description,
                "direction_string": direction_string,
                "composite_id": composite_id,
                "composite_type": composite_type}
       
        if update:
            return self.update_entity("compositeparts", uuid, data)
        return self.create_entity("compositeparts", data)


    def update_composite_part(self, uuid,
                                    name, 
                                    sequence,
                                    circular=True,
                                    part_ids=None,
                                    description=None,
                                    direction_string=None,
                                    composite_id=None,
                                    composite_type=None, update=False):
        return self.create_composite_part(name, sequence, uuid, circular, part_ids, description,
                     direction_string, composite_id, composite_type, update=True)


# Helper and Caching Functions

Client._derive_parts = derive_parts
Client._cache_parts = cache_parts
