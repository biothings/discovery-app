# Schemas

## What is a schema and why do we need one?
The term *schema* refers to the organization of data as a blueprint of how the database is constructed.
Schemas allow for data to be completely understood by different interfaces and let computers access, exchange, integrate data in a uniform manner. 
We use [Schema.org](https://schema.org/) as a stable source for generic definitions we can build from. 

## Schema.org
[Schema.org](https://schema.org/) is a collaborative, community activity with a mission to create, maintain, and promote schemas for structured data on the Internet, on web pages, in email messages, and beyond.
If we apply this standard to biomedical data we believe we can speed up the processing and discovery of new biomedical data within the research community.

# How to extend an existing schema definition step-by-step


## 1 - Find a Structure
From [Schema.org](https://schema.org/) you can find anything from the most generic type (Thing) to more specific types (Dataset, Patient, Organization, etc). From any of those types you can branch off to create a more specific version of that particular type. Each type is represented by a **Class** and each class has **properties** associated with it.

Example:
**A** (Thing[**name, description...**]) --> **B** (CreativeWork) --> **C** (Dataset) --> **D** [**YourDataset**]

Here we have a Class Thing that has properties name and description. Any Class derived from Thing will inherit those properties, meaning that Class **B**, **C**, and **D** will have access to those properties and you do not need to redefine them. This makes your job easier as you only need to define what makes Class **D** different from Class **C** and not inherited from any of its parents. 

## 2-  Schema Set Up

A schema is represented in [JSON-LD](https://json-ld.org/) and these are the fields that make it up:

 1. **@context** - contains all the prefixes used in the schema, and the values that replace such prefixes when the schema is compacted. 
 2. **@id** - unique identifier/location of this schema.
 3. **@graph** - a list of objects, each represents all the classes and properties included in this schema

```
    {
	    "@context": {
		    "schema" : "https://schema.org/",
		    "myprefix" : "https://mywesbite.com/view/"
	    },
	    "@id": "https://mywesbite.com/view/",
	    "@graph": [{...},{...}],
    }
```

## 3- Your Extended New Class
**A** (Thing) --> **B** (CreativeWork) --> **C** (Dataset) --> **D** [**MyDataset**]

In this example, we decided that we want to extend **C** [Dataset](https://schema.org/Dataset) from schema.org. 
Following the [style guides](https://schema.org/docs/styleguide.html) provided name it something meaningful. but in this example we'll call it **MyDataset**.


This is how a Class should be structured:
 1. **@id** - prefix : ClassName
 2. **@type** - since it's a class it should always be **rdfs:Class**
 3. **rdfs:label** - ClassName only
 4. **rdfs:comment** - comment or description
 5. **rdfs:subClassOf - This is where you specify where you are extending from**
 6. **schema:isPartOf** - url of origin of this Class, where it is/will be hosted

```
    {
	    "@context": {
		    "schema" : "https://schema.org/",
		    "myprefix" : "https://mywesbite.com/view/"
	    },
	    "@id": "https://mywesbite.com/view/",
	    "@graph": [
		    {
			    "@id": "myprefix:MyDataset",
			    "@type": "rdfs:Class",
			    "rdfs:label": "MyDataset",
			    "rdfs:comment": "Comment about this Class",
			    "rdfs:subClassOf": {"@id": "schema:Dataset"},
			    "schema:isPartOf": {"@id": "https://mywesbite.com/view/"},
		    }
	    ],
    }
```

## 4- Custom Properties
**A** (Thing) --> **B** (CreativeWork) --> **C** (Dataset) --> **D** [**MyDataset**]

We know that Class **D** will inherit all properties of its parents (**A, B and C**). So we only need to define those properties that you need but are non existent. 
Let's say we need to include a property that lets us know if the dataset contains PHI (Private Health information). But this property is not included in schema.org.
Following the [style guides](https://schema.org/docs/styleguide.html) provided name it something meaningful. but in this example we'll call it **contain_phi**.


This is how a property should be structured:
 1. **@id** - prefix : propertyName
 2. **@type** - since it's a property it should always be **rdf:Property**
 3. **rdfs:label** - propertyName only
 4. **rdfs:comment** - comment or description
 5. **schema:domainIncludes - What Class does this belong to, in this case our Class**
 6. **schema:rangeIncludes** - The type of value this property holds, based on an existing or new Class.

```
    {
	    "@context": {
		    "schema" : "https://schema.org/",
		    "myprefix" : "https://mywesbite.com/view/"
	    },
	    "@id": "https://mywesbite.com/view/",
	    "@graph": [
		    {
			    "@id": "myprefix:MyDataset",
			    "@type": "rdfs:Class",
			    "rdfs:label": "MyDataset",
			    "rdfs:comment": "Comment about this Class",
			    "rdfs:subClassOf": {"@id": "schema:Dataset"},
			    "schema:isPartOf": {"@id": "https://mywesbite.com/view/"},
		    },
		    {
			    "@id": "myprefix:contain_phi",
			    "@type": "rdf:Property",
			    "rdfs:comment": "Does the dataset contains Protected health information (PHI)?",
			    "rdfs:label": "contain_phi",
			    "schema:domainIncludes": {"@id": "myprefix:MyDataset"},
			    "schema:rangeIncludes": {"@id": "schema:Boolean"}
			}
	    ],
    }
```


## 5- Validation
Validation is defined as [json schema validation](https://json-schema.org/draft/2019-09/json-schema-validation.html) to help us make assertions about what a valid document must look like.
Now that we know what our new Class is (**MyDataset**), its inherited properties (**eg. name, description**), and its custom properties (**contain_phi**) we can define some validation rules for our schema:


A new key **$validation** will be added to our custom Class and this is how the validation should be structured:
 1. **$schema** - json schema validation version to be used. See  [json schema validation](https://json-schema.org/draft/2019-09/json-schema-validation.html).
 2. **type** - Overall data type structure, since it's an object > **object**.
 3. **properties** - object of all properties that you want to represent your MyDataset data, including inherited and custom properties. Each with its [validation rules](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.6). Each key represents a property defined in our schema.
 4.  **required** - A list of properties that you want to enforce as required.

```
    {
	    "@context": {
		    "schema" : "https://schema.org/",
		    "myprefix" : "https://mywesbite.com/view/"
	    },
	    "@id": "https://mywesbite.com/view/",
	    "@graph": [
		    {
			    "@id": "myprefix:MyDataset",
			    "@type": "rdfs:Class",
			    "rdfs:label": "MyDataset",
			    "rdfs:comment": "Comment about this Class",
			    "rdfs:subClassOf": {"@id": "schema:Dataset"},
			    "schema:isPartOf": {"@id": "https://mywesbite.com/view/"},
			    "$validation":{
				    "$schema": "http://json-schema.org/draft-07/schema#",
				    "type": "object",
				    "properties":{
					    "name": {
						    "description": "Name of the dataset",
						    "type": "string"
						 },
						 "description": {
							 "description": "Description of what is contained in the dataset",
							 "type": "string"
						},
						"contain_phi": {
							 "description": "Contains PHI?",
							 "type": "boolean"
						}
				    },
				    "required": ['contain_phi', 'name']
			    }
		    },
		    {
			    "@id": "myprefix:contain_phi",
			    "@type": "rdf:Property",
			    "rdfs:comment": "Does the dataset contains Protected health information (PHI)?",
			    "rdfs:label": "contain_phi",
			    "schema:domainIncludes": {"@id": "myprefix:MyDataset"},
			    "schema:rangeIncludes": {"@id": "schema:Boolean"}
			}
	    ],
    }
```

Now we have a schema even more applicable than the original schema.org version since it's tailored to your needs and it includes custom validation to make sure the data ingested by your system is compliant by your own custom rules.


Given this schema, valid data will look like this:

```
{
	"name": "Some Title".
	"description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s",
	"contain_phi": false
}
```

This is just a very simple example of what you can do! With json schema you can define rules for:
format, length, lists,  custom definitions, nested structures, enumerations, constants, max, min, reuse definitions, etc. [Learn more](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.6).

## For more documentation on how to write validation rules in json schema [click here](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.6).




## FAQ

Still have questions or issues? Create an issue [here](https://github.com/biothings/discovery-app/issues).

|Question        |Answer                         |
|----------------|-------------------------------|
|Can I define multiple Classes at once?|Yes, but you must maintain the schema hierarchy. Meaning each Class must be a subClass of an existing Class in your schema.           |
|What is a prefix?         |In the context of a schema it is a short name used to replace a reused part of a URL.  Eg. All schemas in [Schema.org](https://schema.org/) follow the same pattern --> "http://schema.org/"+**ClassName**/**propName** so we can create a prefix "**schema**" in our context --> ```{"schema": "http://schema.org/"}``` that when compacted resolves to the full URL. Ideally the prefix you choose and its value will resolve to a working URI. [Learn more](https://www.w3.org/ns/json-ld).       |
|Is the validation required?          |Validation is not required in terms of being compatible with schema.org, that's why it is annotated with a "**$**" (Used internally only by DDE, you'll benefit from additional functionality). However, including this makes your schema more robust and ensures the data your system ingests is consistent and follows your structure. Both schema and validation are based on reliable and stable markup languages so you can rest assured they work. |
|A property exists but it's not exactly what I need, do I need to redefine it?          |Properties, much like Classes can also be expanded. Maybe the range (input) it takes is not enough or it's too generic.  In such case you can define a new property with a different name that indicates its meaning, see [style guides](https://schema.org/docs/styleguide.html)  for more info on naming conventions.|
|What are the benefits of defining my schema in this format?          | [FAIR](https://www.go-fair.org/fair-principles/) data-sharing principles recommend using Findable, Accessible, Interoperable and Reusable methods to generate data.  We use [Schema.org](https://schema.org/) which is founded by Google, Microsoft, Yahoo and Yandex. You are using a format already in use and widely accepted. We can reuse this structure to tailor it to our needs and inject additional [json-schema validation](https://json-schema.org/draft/2019-09/json-schema-validation.html) to make it even more applicable. The result is validated data that can be understood by different interfaces and computers can access, exchange, integrate in a uniform manner.   Additionally, if you register your schema on the [Data Discovery Engine](https://discovery.biothings.io/) you will benefit from additional web documentation automatically generated from your schema and validation and the ability to share your schema so others can reuse your custom schema as well.|


