[Work in Progress]

This document describes how to define your own Metadata schemas, which can be published in the Data Discovery Engine.

### How to define a metadata schema?

 * Why should we define our schemas in a standardized way?
 
   - To better share schemas
     
     Any application involves particular data types will most likely need to define your own data schema. Unless you expect to keep your data structure hidden from your users (either general users or developer users), it's always a good practice to share your data schema with your users. Often we see three scenarios below.
     
     |    |                           |     |
     | -- | ------------------------- | --- |
     | #1 | Not sharing schema at all | ❌ |
     | #2 | Sharing schema in a non-computable form (e.g. word, pdf, html files) | ❌ |
     | #3 | Sharing schema in a computable form | ✔ |
   
     We obviously want to prompt the scenario #3 above, and make the process easier with the schema tools from the Data Discovery Engine.

   - To better reuse schemas for interoperabilities.
   
### How schema.org is defined?
Schema.org defines schemas as a set of 'types', each associated with a set of properties. The types or classes (as they are referred to in the DDE) are arranged in a hierarchy. Schema.org is extremely flexible and has only a few constraints. 
 1. Properties and classes should follow the appropriate naming conventions. 
 2. Properties belonging to a class can be inherited by child classes. Eg- All properties of Thing can also be inherited by CreativeWork, a derivative class of Thing
 3. Properties have an expected type (ie- the value of the property is expected to be constrained to a specific class or set of classes). For example, the value of `name` is expected to be `Text`; hence, a date/time value would not be expected.

Schema.org does not define cardinality/marginality; however, since these constraints are usually important in the biomedical research space, they can be defined within the DDE when creating your own schema by adding JSON-Schema based validation rules. More about schema.org can be found at https://schema.org/docs/documents.html

### How to create your own schema by extending a schema.org class?
A quickstart guide for selecting a schema.org class and extending it can be found at https://discovery.biothings.io/faq#what-is-schema-playground

### Add the JSON-Schema based validation rules 
Since schema.org classes do not have marginality/cardinality constraints, the schema.org classes do not include validation rules. Instead, the Schema Playground has a validation editor which consists of several pre-defined validation rules, a validation rule editor, and a drag-and-drop interface. To add a validation rule to a property, drag it from the validation rules listing and drop it on the applicable property. 

### How to and why extend from a class in the schema registry?
Many consortia and projects are already using the DDE Schema Playground and registry. This means that they may already have custom schema that are more relevant for biomedical research use. For example, the Dataset schema from the NAIAD Data Portal is available in the DDE Schema Playground. This Dataset schema includes a minimal set of properties that should be included for a Dataset in the Allergy, Immunology, and Infectious Disease research space. It defines the cardinality and marginality constraints for each property and the validation rules in this schema are already set. If you have a dataset in this research space, and would like to further tailor the schema for your dataset, re-using/extending from this class will allow you to inherit those validation rules. The validation rules can then be tweaked for individual properties using the schema editor
