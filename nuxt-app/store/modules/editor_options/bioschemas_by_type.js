export const most_used = [
  "Text",
  "URL",
  "PropertyValue",
  "CreativeWork",
  "DefinedTerm",
  "Organization",
  "Person",
  "Date",
  "BioChemEntity",
  "DateTime",
  "ImageObject",
  "Integer",
  "Product",
  "Taxon",
  "Place",
  "Boolean",
  "Language",
  "MedicalCondition",
  "Event",
  "Duration",
  "Gene",
  "PostalAddress",
  "SoftwareApplication",
  "Number",
];

export const bioschemas_by_type = [
  {
    _id: "extydq290bio",
    title: "Text",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyfl438bio",
    title: "Text",
    color: "#097969",
    validation: {
      oneOf: [
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyfj790bio",
    title: "URL",
    color: "#097969",
    validation: {
      type: "string",
      format: "uri",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyym302bio",
    title: "URL",
    color: "#097969",
    validation: {
      oneOf: [
        {
          type: "string",
          format: "uri",
        },
        {
          type: "array",
          items: {
            type: "string",
            format: "uri",
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyxl582bio",
    title: "PropertyValue",
    color: "#097969",
    validation: {
      "@type": "PropertyValue",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyyo163bio",
    title: "PropertyValue",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "PropertyValue",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "PropertyValue",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyeo182bio",
    title: "CreativeWork",
    color: "#097969",
    validation: {
      "@type": "CreativeWork",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybn831bio",
    title: "CreativeWork",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "CreativeWork",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "CreativeWork",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyfo202bio",
    title: "DefinedTerm",
    color: "#097969",
    validation: {
      "@type": "DefinedTerm",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extywq938bio",
    title: "DefinedTerm",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "DefinedTerm",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "DefinedTerm",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyfm451bio",
    title: "Organization",
    color: "#097969",
    validation: {
      "@type": "Organization",
      type: "object",
      properties: {
        description: {
          type: "string",
        },
        legalName: {
          type: "string",
        },
        name: {
          type: "string",
        },
        sameAs: {
          type: "string",
          format: "uri",
        },
        topic: {
          oneOf: [
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        type: {
          oneOf: [
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
      },
      required: ["description", "legalName", "name", "sameAs", "topic", "type"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyvq346bio",
    title: "Organization",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Organization",
          type: "object",
          properties: {
            description: {
              type: "string",
            },
            legalName: {
              type: "string",
            },
            name: {
              type: "string",
            },
            sameAs: {
              type: "string",
              format: "uri",
            },
            topic: {
              oneOf: [
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            type: {
              oneOf: [
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
          },
          required: [
            "description",
            "legalName",
            "name",
            "sameAs",
            "topic",
            "type",
          ],
        },
        {
          type: "array",
          items: {
            "@type": "Organization",
            type: "object",
            properties: {
              description: {
                type: "string",
              },
              legalName: {
                type: "string",
              },
              name: {
                type: "string",
              },
              sameAs: {
                type: "string",
                format: "uri",
              },
              topic: {
                oneOf: [
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              type: {
                oneOf: [
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
            },
            required: [
              "description",
              "legalName",
              "name",
              "sameAs",
              "topic",
              "type",
            ],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyak727bio",
    title: "Person",
    color: "#097969",
    validation: {
      "@type": "Person",
      type: "object",
      properties: {
        description: {
          type: "string",
        },
        mainEntityOfPage: {
          oneOf: [
            {
              type: "object",
              "@type": "CreativeWork",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        name: {
          type: "string",
        },
      },
      required: ["description", "mainEntityOfPage", "name"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyzq221bio",
    title: "Person",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Person",
          type: "object",
          properties: {
            description: {
              type: "string",
            },
            mainEntityOfPage: {
              oneOf: [
                {
                  type: "object",
                  "@type": "CreativeWork",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            name: {
              type: "string",
            },
          },
          required: ["description", "mainEntityOfPage", "name"],
        },
        {
          type: "array",
          items: {
            "@type": "Person",
            type: "object",
            properties: {
              description: {
                type: "string",
              },
              mainEntityOfPage: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "CreativeWork",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              name: {
                type: "string",
              },
            },
            required: ["description", "mainEntityOfPage", "name"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyvp710bio",
    title: "Date",
    color: "#097969",
    validation: {
      type: "string",
      format: "date",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyei859bio",
    title: "Date",
    color: "#097969",
    validation: {
      oneOf: [
        {
          type: "string",
          format: "date",
        },
        {
          type: "array",
          items: {
            type: "string",
            format: "date",
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybo550bio",
    title: "BioChemEntity",
    color: "#097969",
    validation: {
      "@type": "BioChemEntity",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extydo901bio",
    title: "BioChemEntity",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "BioChemEntity",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "BioChemEntity",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyej323bio",
    title: "DateTime",
    color: "#097969",
    validation: {
      "@type": "DateTime",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extycq398bio",
    title: "DateTime",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "DateTime",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "DateTime",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extycq705bio",
    title: "ImageObject",
    color: "#097969",
    validation: {
      "@type": "ImageObject",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyyq549bio",
    title: "ImageObject",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "ImageObject",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "ImageObject",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyvo111bio",
    title: "Integer",
    color: "#097969",
    validation: {
      type: "integer",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybq969bio",
    title: "Integer",
    color: "#097969",
    validation: {
      oneOf: [
        {
          type: "integer",
        },
        {
          type: "array",
          items: {
            type: "integer",
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyyk865bio",
    title: "Thing",
    color: "#097969",
    validation: {
      "@type": "Thing",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extywm897bio",
    title: "Thing",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Thing",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "Thing",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyfp538bio",
    title: "Product",
    color: "#097969",
    validation: {
      "@type": "Product",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyxl753bio",
    title: "Product",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Product",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "Product",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyzp914bio",
    title: "Taxon",
    color: "#097969",
    validation: {
      "@type": "Taxon",
      type: "object",
      properties: {
        name: {
          type: "string",
        },
        taxonRank: {
          oneOf: [
            {
              type: "object",
              "@type": "PropertyValue",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
      },
      required: ["name", "taxonRank"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybi877bio",
    title: "Taxon",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Taxon",
          type: "object",
          properties: {
            name: {
              type: "string",
            },
            taxonRank: {
              oneOf: [
                {
                  type: "object",
                  "@type": "PropertyValue",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
          },
          required: ["name", "taxonRank"],
        },
        {
          type: "array",
          items: {
            "@type": "Taxon",
            type: "object",
            properties: {
              name: {
                type: "string",
              },
              taxonRank: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "PropertyValue",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
            },
            required: ["name", "taxonRank"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyyi469bio",
    title: "Place",
    color: "#097969",
    validation: {
      "@type": "Place",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyzm512bio",
    title: "Place",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Place",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "Place",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyck927bio",
    title: "Boolean",
    color: "#097969",
    validation: {
      type: "boolean",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyxm458bio",
    title: "Boolean",
    color: "#097969",
    validation: {
      oneOf: [
        {
          type: "boolean",
        },
        {
          type: "array",
          items: {
            type: "boolean",
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyzj164bio",
    title: "Language",
    color: "#097969",
    validation: {
      "@type": "Language",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extywo256bio",
    title: "Language",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Language",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "Language",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyvl909bio",
    title: "MedicalCondition",
    color: "#097969",
    validation: {
      "@type": "MedicalCondition",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybm812bio",
    title: "MedicalCondition",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "MedicalCondition",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "MedicalCondition",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybk728bio",
    title: "Event",
    color: "#097969",
    validation: {
      "@type": "Event",
      type: "object",
      properties: {
        contact: {
          oneOf: [
            {
              type: "object",
              "@type": "Organization",
            },
            {
              type: "object",
              "@type": "Person",
            },
          ],
        },
        description: {
          type: "string",
        },
        endDate: {
          oneOf: [
            {
              type: "string",
              format: "date",
            },
            {
              type: "object",
              "@type": "DateTime",
            },
          ],
        },
        eventType: {
          type: "object",
          "@type": "EventType",
        },
        hostInstitution: {
          type: "object",
          "@type": "Organization",
        },
        location: {
          oneOf: [
            {
              type: "object",
              "@type": "Place",
            },
            {
              type: "object",
              "@type": "PostalAddress",
            },
            {
              type: "string",
            },
          ],
        },
        name: {
          type: "string",
        },
        startDate: {
          oneOf: [
            {
              type: "string",
              format: "date",
            },
            {
              type: "object",
              "@type": "DateTime",
            },
          ],
        },
      },
      required: [
        "contact",
        "description",
        "endDate",
        "eventType",
        "hostInstitution",
        "location",
        "name",
        "startDate",
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyzk154bio",
    title: "Event",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Event",
          type: "object",
          properties: {
            contact: {
              oneOf: [
                {
                  type: "object",
                  "@type": "Organization",
                },
                {
                  type: "object",
                  "@type": "Person",
                },
              ],
            },
            description: {
              type: "string",
            },
            endDate: {
              oneOf: [
                {
                  type: "string",
                  format: "date",
                },
                {
                  type: "object",
                  "@type": "DateTime",
                },
              ],
            },
            eventType: {
              type: "object",
              "@type": "EventType",
            },
            hostInstitution: {
              type: "object",
              "@type": "Organization",
            },
            location: {
              oneOf: [
                {
                  type: "object",
                  "@type": "Place",
                },
                {
                  type: "object",
                  "@type": "PostalAddress",
                },
                {
                  type: "string",
                },
              ],
            },
            name: {
              type: "string",
            },
            startDate: {
              oneOf: [
                {
                  type: "string",
                  format: "date",
                },
                {
                  type: "object",
                  "@type": "DateTime",
                },
              ],
            },
          },
          required: [
            "contact",
            "description",
            "endDate",
            "eventType",
            "hostInstitution",
            "location",
            "name",
            "startDate",
          ],
        },
        {
          type: "array",
          items: {
            "@type": "Event",
            type: "object",
            properties: {
              contact: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "Organization",
                  },
                  {
                    type: "object",
                    "@type": "Person",
                  },
                ],
              },
              description: {
                type: "string",
              },
              endDate: {
                oneOf: [
                  {
                    type: "string",
                    format: "date",
                  },
                  {
                    type: "object",
                    "@type": "DateTime",
                  },
                ],
              },
              eventType: {
                type: "object",
                "@type": "EventType",
              },
              hostInstitution: {
                type: "object",
                "@type": "Organization",
              },
              location: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "Place",
                  },
                  {
                    type: "object",
                    "@type": "PostalAddress",
                  },
                  {
                    type: "string",
                  },
                ],
              },
              name: {
                type: "string",
              },
              startDate: {
                oneOf: [
                  {
                    type: "string",
                    format: "date",
                  },
                  {
                    type: "object",
                    "@type": "DateTime",
                  },
                ],
              },
            },
            required: [
              "contact",
              "description",
              "endDate",
              "eventType",
              "hostInstitution",
              "location",
              "name",
              "startDate",
            ],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyyo590bio",
    title: "Duration",
    color: "#097969",
    validation: {
      "@type": "Duration",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyaj149bio",
    title: "Duration",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Duration",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "Duration",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyfp499bio",
    title: "Gene",
    color: "#097969",
    validation: {
      "@type": "Gene",
      type: "object",
      properties: {
        identifier: {
          oneOf: [
            {
              type: "object",
              "@type": "PropertyValue",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        name: {
          type: "string",
        },
      },
      required: ["identifier", "name"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyzp605bio",
    title: "Gene",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Gene",
          type: "object",
          properties: {
            identifier: {
              oneOf: [
                {
                  type: "object",
                  "@type": "PropertyValue",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            name: {
              type: "string",
            },
          },
          required: ["identifier", "name"],
        },
        {
          type: "array",
          items: {
            "@type": "Gene",
            type: "object",
            properties: {
              identifier: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "PropertyValue",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              name: {
                type: "string",
              },
            },
            required: ["identifier", "name"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybn551bio",
    title: "PostalAddress",
    color: "#097969",
    validation: {
      "@type": "PostalAddress",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyyk950bio",
    title: "PostalAddress",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "PostalAddress",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "PostalAddress",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyfq578bio",
    title: "SoftwareApplication",
    color: "#097969",
    validation: {
      "@type": "SoftwareApplication",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyco250bio",
    title: "SoftwareApplication",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "SoftwareApplication",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "SoftwareApplication",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyyn260bio",
    title: "Number",
    color: "#097969",
    validation: {
      type: "number",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybo753bio",
    title: "Number",
    color: "#097969",
    validation: {
      oneOf: [
        {
          type: "number",
        },
        {
          type: "array",
          items: {
            type: "number",
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybm287bio",
    title: "PublicationIssue",
    color: "#097969",
    validation: {
      "@type": "PublicationIssue",
      type: "object",
      properties: {
        issueNumber: {
          oneOf: [
            {
              type: "integer",
            },
            {
              type: "string",
            },
          ],
        },
      },
      required: ["issueNumber"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybq159bio",
    title: "PublicationIssue",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "PublicationIssue",
          type: "object",
          properties: {
            issueNumber: {
              oneOf: [
                {
                  type: "integer",
                },
                {
                  type: "string",
                },
              ],
            },
          },
          required: ["issueNumber"],
        },
        {
          type: "array",
          items: {
            "@type": "PublicationIssue",
            type: "object",
            properties: {
              issueNumber: {
                oneOf: [
                  {
                    type: "integer",
                  },
                  {
                    type: "string",
                  },
                ],
              },
            },
            required: ["issueNumber"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyyo978bio",
    title: "PublicationVolume",
    color: "#097969",
    validation: {
      "@type": "PublicationVolume",
      type: "object",
      properties: {
        url: {
          type: "string",
          format: "uri",
        },
        volumeNumber: {
          oneOf: [
            {
              type: "integer",
            },
            {
              type: "string",
            },
          ],
        },
      },
      required: ["url", "volumeNumber"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyym893bio",
    title: "PublicationVolume",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "PublicationVolume",
          type: "object",
          properties: {
            url: {
              type: "string",
              format: "uri",
            },
            volumeNumber: {
              oneOf: [
                {
                  type: "integer",
                },
                {
                  type: "string",
                },
              ],
            },
          },
          required: ["url", "volumeNumber"],
        },
        {
          type: "array",
          items: {
            "@type": "PublicationVolume",
            type: "object",
            properties: {
              url: {
                type: "string",
                format: "uri",
              },
              volumeNumber: {
                oneOf: [
                  {
                    type: "integer",
                  },
                  {
                    type: "string",
                  },
                ],
              },
            },
            required: ["url", "volumeNumber"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybl244bio",
    title: "ContactPoint",
    color: "#097969",
    validation: {
      "@type": "ContactPoint",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyyo270bio",
    title: "ContactPoint",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "ContactPoint",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "ContactPoint",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extywk362bio",
    title: "Journal",
    color: "#097969",
    validation: {
      "@type": "Journal",
      type: "object",
      properties: {
        identifier: {
          oneOf: [
            {
              type: "object",
              "@type": "PropertyValue",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        name: {
          type: "string",
        },
      },
      required: ["identifier", "name"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyep185bio",
    title: "Journal",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Journal",
          type: "object",
          properties: {
            identifier: {
              oneOf: [
                {
                  type: "object",
                  "@type": "PropertyValue",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            name: {
              type: "string",
            },
          },
          required: ["identifier", "name"],
        },
        {
          type: "array",
          items: {
            "@type": "Journal",
            type: "object",
            properties: {
              identifier: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "PropertyValue",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              name: {
                type: "string",
              },
            },
            required: ["identifier", "name"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybo275bio",
    title: "ComputerLanguage",
    color: "#097969",
    validation: {
      "@type": "ComputerLanguage",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyek194bio",
    title: "ComputerLanguage",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "ComputerLanguage",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "ComputerLanguage",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyaj875bio",
    title: "ScholarlyArticle",
    color: "#097969",
    validation: {
      "@type": "ScholarlyArticle",
      type: "object",
      properties: {
        identifier: {
          oneOf: [
            {
              type: "object",
              "@type": "PropertyValue",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        name: {
          type: "string",
        },
      },
      required: ["identifier", "name"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyvi987bio",
    title: "ScholarlyArticle",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "ScholarlyArticle",
          type: "object",
          properties: {
            identifier: {
              oneOf: [
                {
                  type: "object",
                  "@type": "PropertyValue",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            name: {
              type: "string",
            },
          },
          required: ["identifier", "name"],
        },
        {
          type: "array",
          items: {
            "@type": "ScholarlyArticle",
            type: "object",
            properties: {
              identifier: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "PropertyValue",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              name: {
                type: "string",
              },
            },
            required: ["identifier", "name"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyzl124bio",
    title: "Offer",
    color: "#097969",
    validation: {
      "@type": "Offer",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extycq274bio",
    title: "Offer",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Offer",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "Offer",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extycj711bio",
    title: "ProgramMembership",
    color: "#097969",
    validation: {
      "@type": "ProgramMembership",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extywl864bio",
    title: "ProgramMembership",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "ProgramMembership",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "ProgramMembership",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyvo697bio",
    title: "Audience",
    color: "#097969",
    validation: {
      "@type": "Audience",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyen868bio",
    title: "Audience",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Audience",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "Audience",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyaj154bio",
    title: "MediaObject",
    color: "#097969",
    validation: {
      "@type": "MediaObject",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyen686bio",
    title: "MediaObject",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "MediaObject",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "MediaObject",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyek292bio",
    title: "TaxonName",
    color: "#097969",
    validation: {
      "@type": "TaxonName",
      type: "object",
      properties: {
        name: {
          type: "string",
        },
      },
      required: ["name"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyvi734bio",
    title: "TaxonName",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "TaxonName",
          type: "object",
          properties: {
            name: {
              type: "string",
            },
          },
          required: ["name"],
        },
        {
          type: "array",
          items: {
            "@type": "TaxonName",
            type: "object",
            properties: {
              name: {
                type: "string",
              },
            },
            required: ["name"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyzj337bio",
    title: "Trip",
    color: "#097969",
    validation: {
      "@type": "Trip",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyyk642bio",
    title: "Trip",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Trip",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "Trip",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyvj263bio",
    title: "FormalParameter",
    color: "#097969",
    validation: {
      "@type": "FormalParameter",
      type: "object",
      properties: {
        name: {
          type: "string",
        },
      },
      required: ["name"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extydn600bio",
    title: "FormalParameter",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "FormalParameter",
          type: "object",
          properties: {
            name: {
              type: "string",
            },
          },
          required: ["name"],
        },
        {
          type: "array",
          items: {
            "@type": "FormalParameter",
            type: "object",
            properties: {
              name: {
                type: "string",
              },
            },
            required: ["name"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyyk417bio",
    title: "QuantitativeValue",
    color: "#097969",
    validation: {
      "@type": "QuantitativeValue",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyao391bio",
    title: "QuantitativeValue",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "QuantitativeValue",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "QuantitativeValue",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyxi979bio",
    title: "RNA",
    color: "#097969",
    validation: {
      "@type": "RNA",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extywq404bio",
    title: "RNA",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "RNA",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "RNA",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extywl674bio",
    title: "CategoryCode",
    color: "#097969",
    validation: {
      "@type": "CategoryCode",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyyi553bio",
    title: "CategoryCode",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "CategoryCode",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "CategoryCode",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extydj111bio",
    title: "DataDownload",
    color: "#097969",
    validation: {
      "@type": "DataDownload",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyzm105bio",
    title: "DataDownload",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "DataDownload",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "DataDownload",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyvn115bio",
    title: "DataCatalog",
    color: "#097969",
    validation: {
      "@type": "DataCatalog",
      type: "object",
      properties: {
        description: {
          type: "string",
        },
        keywords: {
          type: "string",
        },
        name: {
          type: "string",
        },
        provider: {
          oneOf: [
            {
              type: "object",
              "@type": "Organization",
            },
            {
              type: "object",
              "@type": "Person",
            },
          ],
        },
        url: {
          type: "string",
          format: "uri",
        },
      },
      required: ["description", "keywords", "name", "provider", "url"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybk806bio",
    title: "DataCatalog",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "DataCatalog",
          type: "object",
          properties: {
            description: {
              type: "string",
            },
            keywords: {
              type: "string",
            },
            name: {
              type: "string",
            },
            provider: {
              oneOf: [
                {
                  type: "object",
                  "@type": "Organization",
                },
                {
                  type: "object",
                  "@type": "Person",
                },
              ],
            },
            url: {
              type: "string",
              format: "uri",
            },
          },
          required: ["description", "keywords", "name", "provider", "url"],
        },
        {
          type: "array",
          items: {
            "@type": "DataCatalog",
            type: "object",
            properties: {
              description: {
                type: "string",
              },
              keywords: {
                type: "string",
              },
              name: {
                type: "string",
              },
              provider: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "Organization",
                  },
                  {
                    type: "object",
                    "@type": "Person",
                  },
                ],
              },
              url: {
                type: "string",
                format: "uri",
              },
            },
            required: ["description", "keywords", "name", "provider", "url"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyyq349bio",
    title: "DNA",
    color: "#097969",
    validation: {
      "@type": "DNA",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybo441bio",
    title: "DNA",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "DNA",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "DNA",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyap208bio",
    title: "SequenceMatchingModel",
    color: "#097969",
    validation: {
      "@type": "SequenceMatchingModel",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extydn131bio",
    title: "SequenceMatchingModel",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "SequenceMatchingModel",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "SequenceMatchingModel",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyxk519bio",
    title: "Study",
    color: "#097969",
    validation: {
      "@type": "Study",
      type: "object",
      properties: {
        author: {
          oneOf: [
            {
              type: "object",
              "@type": "Organization",
            },
            {
              type: "object",
              "@type": "Person",
            },
          ],
        },
        datePublished: {
          type: "string",
          format: "date",
        },
        description: {
          type: "string",
        },
        identifier: {
          oneOf: [
            {
              type: "object",
              "@type": "PropertyValue",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        name: {
          type: "string",
        },
        studyDomain: {
          oneOf: [
            {
              type: "object",
              "@type": "PropertyValue",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        studySubject: {
          oneOf: [
            {
              type: "object",
              "@type": "BioChemEntity",
            },
            {
              type: "object",
              "@type": "MedicalEntity",
            },
          ],
        },
      },
      required: [
        "author",
        "datePublished",
        "description",
        "identifier",
        "name",
        "studyDomain",
        "studySubject",
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extycp908bio",
    title: "Study",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Study",
          type: "object",
          properties: {
            author: {
              oneOf: [
                {
                  type: "object",
                  "@type": "Organization",
                },
                {
                  type: "object",
                  "@type": "Person",
                },
              ],
            },
            datePublished: {
              type: "string",
              format: "date",
            },
            description: {
              type: "string",
            },
            identifier: {
              oneOf: [
                {
                  type: "object",
                  "@type": "PropertyValue",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            name: {
              type: "string",
            },
            studyDomain: {
              oneOf: [
                {
                  type: "object",
                  "@type": "PropertyValue",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            studySubject: {
              oneOf: [
                {
                  type: "object",
                  "@type": "BioChemEntity",
                },
                {
                  type: "object",
                  "@type": "MedicalEntity",
                },
              ],
            },
          },
          required: [
            "author",
            "datePublished",
            "description",
            "identifier",
            "name",
            "studyDomain",
            "studySubject",
          ],
        },
        {
          type: "array",
          items: {
            "@type": "Study",
            type: "object",
            properties: {
              author: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "Organization",
                  },
                  {
                    type: "object",
                    "@type": "Person",
                  },
                ],
              },
              datePublished: {
                type: "string",
                format: "date",
              },
              description: {
                type: "string",
              },
              identifier: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "PropertyValue",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              name: {
                type: "string",
              },
              studyDomain: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "PropertyValue",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              studySubject: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "BioChemEntity",
                  },
                  {
                    type: "object",
                    "@type": "MedicalEntity",
                  },
                ],
              },
            },
            required: [
              "author",
              "datePublished",
              "description",
              "identifier",
              "name",
              "studyDomain",
              "studySubject",
            ],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyfl245bio",
    title: "Review",
    color: "#097969",
    validation: {
      "@type": "Review",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyvl905bio",
    title: "Review",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Review",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "Review",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyvi377bio",
    title: "PriceSpecification",
    color: "#097969",
    validation: {
      "@type": "PriceSpecification",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyai123bio",
    title: "PriceSpecification",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "PriceSpecification",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "PriceSpecification",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybj963bio",
    title: "SequenceAnnotation",
    color: "#097969",
    validation: {
      "@type": "SequenceAnnotation",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extywp735bio",
    title: "SequenceAnnotation",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "SequenceAnnotation",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "SequenceAnnotation",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyaj571bio",
    title: "Action",
    color: "#097969",
    validation: {
      "@type": "Action",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyzk467bio",
    title: "Action",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Action",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "Action",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyym622bio",
    title: "HowToStep",
    color: "#097969",
    validation: {
      "@type": "HowToStep",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybj911bio",
    title: "HowToStep",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "HowToStep",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "HowToStep",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybi774bio",
    title: "Periodical",
    color: "#097969",
    validation: {
      "@type": "Periodical",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyeq866bio",
    title: "Periodical",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Periodical",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "Periodical",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyfj503bio",
    title: "AggregateRating",
    color: "#097969",
    validation: {
      "@type": "AggregateRating",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyzl700bio",
    title: "AggregateRating",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "AggregateRating",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "AggregateRating",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extydl218bio",
    title: "AlignmentObject",
    color: "#097969",
    validation: {
      "@type": "AlignmentObject",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyai379bio",
    title: "AlignmentObject",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "AlignmentObject",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "AlignmentObject",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyvk582bio",
    title: "AnatomicalStructure",
    color: "#097969",
    validation: {
      "@type": "AnatomicalStructure",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyzo841bio",
    title: "AnatomicalStructure",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "AnatomicalStructure",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "AnatomicalStructure",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyap272bio",
    title: "AnatomicalSystem",
    color: "#097969",
    validation: {
      "@type": "AnatomicalSystem",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extycl788bio",
    title: "AnatomicalSystem",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "AnatomicalSystem",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "AnatomicalSystem",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyzm827bio",
    title: "BioSample",
    color: "#097969",
    validation: {
      "@type": "BioSample",
      type: "object",
      properties: {
        description: {
          type: "string",
        },
        identifier: {
          oneOf: [
            {
              type: "object",
              "@type": "PropertyValue",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        name: {
          type: "string",
        },
        url: {
          type: "string",
          format: "uri",
        },
      },
      required: ["description", "identifier", "name", "url"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyyq725bio",
    title: "BioSample",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "BioSample",
          type: "object",
          properties: {
            description: {
              type: "string",
            },
            identifier: {
              oneOf: [
                {
                  type: "object",
                  "@type": "PropertyValue",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            name: {
              type: "string",
            },
            url: {
              type: "string",
              format: "uri",
            },
          },
          required: ["description", "identifier", "name", "url"],
        },
        {
          type: "array",
          items: {
            "@type": "BioSample",
            type: "object",
            properties: {
              description: {
                type: "string",
              },
              identifier: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "PropertyValue",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              name: {
                type: "string",
              },
              url: {
                type: "string",
                format: "uri",
              },
            },
            required: ["description", "identifier", "name", "url"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyan847bio",
    title: "ChemicalSubstance",
    color: "#097969",
    validation: {
      "@type": "ChemicalSubstance",
      type: "object",
      properties: {
        identifier: {
          oneOf: [
            {
              type: "object",
              "@type": "PropertyValue",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        name: {
          type: "string",
        },
        url: {
          type: "string",
          format: "uri",
        },
      },
      required: ["identifier", "name", "url"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyfi998bio",
    title: "ChemicalSubstance",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "ChemicalSubstance",
          type: "object",
          properties: {
            identifier: {
              oneOf: [
                {
                  type: "object",
                  "@type": "PropertyValue",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            name: {
              type: "string",
            },
            url: {
              type: "string",
              format: "uri",
            },
          },
          required: ["identifier", "name", "url"],
        },
        {
          type: "array",
          items: {
            "@type": "ChemicalSubstance",
            type: "object",
            properties: {
              identifier: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "PropertyValue",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              name: {
                type: "string",
              },
              url: {
                type: "string",
                format: "uri",
              },
            },
            required: ["identifier", "name", "url"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyvq931bio",
    title: "Comment",
    color: "#097969",
    validation: {
      "@type": "Comment",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyxk364bio",
    title: "Comment",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Comment",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "Comment",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyfp486bio",
    title: "CorrectionComment",
    color: "#097969",
    validation: {
      "@type": "CorrectionComment",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyel479bio",
    title: "CorrectionComment",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "CorrectionComment",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "CorrectionComment",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyem680bio",
    title: "Course",
    color: "#097969",
    validation: {
      "@type": "Course",
      type: "object",
      properties: {
        description: {
          type: "string",
        },
        keywords: {
          oneOf: [
            {
              type: "object",
              "@type": "DefinedTerm",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        name: {
          type: "string",
        },
      },
      required: ["description", "keywords", "name"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extydn777bio",
    title: "Course",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Course",
          type: "object",
          properties: {
            description: {
              type: "string",
            },
            keywords: {
              oneOf: [
                {
                  type: "object",
                  "@type": "DefinedTerm",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            name: {
              type: "string",
            },
          },
          required: ["description", "keywords", "name"],
        },
        {
          type: "array",
          items: {
            "@type": "Course",
            type: "object",
            properties: {
              description: {
                type: "string",
              },
              keywords: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "DefinedTerm",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              name: {
                type: "string",
              },
            },
            required: ["description", "keywords", "name"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyvi689bio",
    title: "CourseInstance",
    color: "#097969",
    validation: {
      "@type": "CourseInstance",
      type: "object",
      properties: {
        courseMode: {
          oneOf: [
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        location: {
          oneOf: [
            {
              type: "object",
              "@type": "Place",
            },
            {
              type: "object",
              "@type": "PostalAddress",
            },
            {
              type: "string",
            },
            {
              type: "object",
              "@type": "VirtualLocation",
            },
          ],
        },
      },
      required: ["courseMode", "location"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyvq320bio",
    title: "CourseInstance",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "CourseInstance",
          type: "object",
          properties: {
            courseMode: {
              oneOf: [
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            location: {
              oneOf: [
                {
                  type: "object",
                  "@type": "Place",
                },
                {
                  type: "object",
                  "@type": "PostalAddress",
                },
                {
                  type: "string",
                },
                {
                  type: "object",
                  "@type": "VirtualLocation",
                },
              ],
            },
          },
          required: ["courseMode", "location"],
        },
        {
          type: "array",
          items: {
            "@type": "CourseInstance",
            type: "object",
            properties: {
              courseMode: {
                oneOf: [
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              location: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "Place",
                  },
                  {
                    type: "object",
                    "@type": "PostalAddress",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "object",
                    "@type": "VirtualLocation",
                  },
                ],
              },
            },
            required: ["courseMode", "location"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyei392bio",
    title: "Dataset",
    color: "#097969",
    validation: {
      "@type": "Dataset",
      type: "object",
      properties: {
        description: {
          type: "string",
        },
        identifier: {
          oneOf: [
            {
              type: "object",
              "@type": "PropertyValue",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        keywords: {
          oneOf: [
            {
              type: "object",
              "@type": "DefinedTerm",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        license: {
          oneOf: [
            {
              type: "object",
              "@type": "CreativeWork",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        name: {
          type: "string",
        },
        url: {
          type: "string",
          format: "uri",
        },
      },
      required: [
        "description",
        "identifier",
        "keywords",
        "license",
        "name",
        "url",
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyzn275bio",
    title: "Dataset",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Dataset",
          type: "object",
          properties: {
            description: {
              type: "string",
            },
            identifier: {
              oneOf: [
                {
                  type: "object",
                  "@type": "PropertyValue",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            keywords: {
              oneOf: [
                {
                  type: "object",
                  "@type": "DefinedTerm",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            license: {
              oneOf: [
                {
                  type: "object",
                  "@type": "CreativeWork",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            name: {
              type: "string",
            },
            url: {
              type: "string",
              format: "uri",
            },
          },
          required: [
            "description",
            "identifier",
            "keywords",
            "license",
            "name",
            "url",
          ],
        },
        {
          type: "array",
          items: {
            "@type": "Dataset",
            type: "object",
            properties: {
              description: {
                type: "string",
              },
              identifier: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "PropertyValue",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              keywords: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "DefinedTerm",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              license: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "CreativeWork",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              name: {
                type: "string",
              },
              url: {
                type: "string",
                format: "uri",
              },
            },
            required: [
              "description",
              "identifier",
              "keywords",
              "license",
              "name",
              "url",
            ],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyck995bio",
    title: "OwnershipInfo",
    color: "#097969",
    validation: {
      "@type": "OwnershipInfo",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extywn620bio",
    title: "OwnershipInfo",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "OwnershipInfo",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "OwnershipInfo",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybo253bio",
    title: "Demand",
    color: "#097969",
    validation: {
      "@type": "Demand",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extydl828bio",
    title: "Demand",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Demand",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "Demand",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyfp367bio",
    title: "EducationalOccupationalCredential",
    color: "#097969",
    validation: {
      "@type": "EducationalOccupationalCredential",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyyk828bio",
    title: "EducationalOccupationalCredential",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "EducationalOccupationalCredential",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "EducationalOccupationalCredential",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybi134bio",
    title: "EventStatusType",
    color: "#097969",
    validation: {
      "@type": "EventStatusType",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyfl477bio",
    title: "EventStatusType",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "EventStatusType",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "EventStatusType",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyxq542bio",
    title: "EventType",
    color: "#097969",
    validation: {
      "@type": "EventType",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyxq465bio",
    title: "EventType",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "EventType",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "EventType",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybi619bio",
    title: "GenderType",
    color: "#097969",
    validation: {
      "@type": "GenderType",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyzq659bio",
    title: "GenderType",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "GenderType",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "GenderType",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyej955bio",
    title: "Grant",
    color: "#097969",
    validation: {
      "@type": "Grant",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyap800bio",
    title: "Grant",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Grant",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "Grant",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extycm357bio",
    title: "HowToSection",
    color: "#097969",
    validation: {
      "@type": "HowToSection",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyfp249bio",
    title: "HowToSection",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "HowToSection",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "HowToSection",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extywo433bio",
    title: "AdministrativeArea",
    color: "#097969",
    validation: {
      "@type": "AdministrativeArea",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extycj374bio",
    title: "AdministrativeArea",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "AdministrativeArea",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "AdministrativeArea",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyvk455bio",
    title: "MedicalEntity",
    color: "#097969",
    validation: {
      "@type": "MedicalEntity",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyxo884bio",
    title: "MedicalEntity",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "MedicalEntity",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "MedicalEntity",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyco830bio",
    title: "MolecularEntity",
    color: "#097969",
    validation: {
      "@type": "MolecularEntity",
      type: "object",
      properties: {
        identifier: {
          oneOf: [
            {
              type: "object",
              "@type": "PropertyValue",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        name: {
          type: "string",
        },
        url: {
          type: "string",
          format: "uri",
        },
      },
      required: ["identifier", "name", "url"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extycn585bio",
    title: "MolecularEntity",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "MolecularEntity",
          type: "object",
          properties: {
            identifier: {
              oneOf: [
                {
                  type: "object",
                  "@type": "PropertyValue",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            name: {
              type: "string",
            },
            url: {
              type: "string",
              format: "uri",
            },
          },
          required: ["identifier", "name", "url"],
        },
        {
          type: "array",
          items: {
            "@type": "MolecularEntity",
            type: "object",
            properties: {
              identifier: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "PropertyValue",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              name: {
                type: "string",
              },
              url: {
                type: "string",
                format: "uri",
              },
            },
            required: ["identifier", "name", "url"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyfo536bio",
    title: "VirtualLocation",
    color: "#097969",
    validation: {
      "@type": "VirtualLocation",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyak592bio",
    title: "VirtualLocation",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "VirtualLocation",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "VirtualLocation",
            type: "object",
            properties: {},
            required: [],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyfj486bio",
    title: "Beacon",
    color: "#097969",
    validation: {
      "@type": "Beacon",
      type: "object",
      properties: {
        dataset: {
          type: "object",
          "@type": "DataCatalog",
        },
        name: {
          type: "string",
        },
        potentialAction: {
          type: "object",
          "@type": "Action",
        },
        provider: {
          oneOf: [
            {
              type: "object",
              "@type": "Organization",
            },
            {
              type: "object",
              "@type": "Person",
            },
          ],
        },
        "rdf:type": {
          type: "string",
          format: "uri",
        },
        supportedRefs: {
          type: "string",
        },
        url: {
          type: "string",
          format: "uri",
        },
      },
      required: [
        "dataset",
        "name",
        "potentialAction",
        "provider",
        "rdf:type",
        "supportedRefs",
        "url",
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyel373bio",
    title: "Beacon",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Beacon",
          type: "object",
          properties: {
            dataset: {
              type: "object",
              "@type": "DataCatalog",
            },
            name: {
              type: "string",
            },
            potentialAction: {
              type: "object",
              "@type": "Action",
            },
            provider: {
              oneOf: [
                {
                  type: "object",
                  "@type": "Organization",
                },
                {
                  type: "object",
                  "@type": "Person",
                },
              ],
            },
            "rdf:type": {
              type: "string",
              format: "uri",
            },
            supportedRefs: {
              type: "string",
            },
            url: {
              type: "string",
              format: "uri",
            },
          },
          required: [
            "dataset",
            "name",
            "potentialAction",
            "provider",
            "rdf:type",
            "supportedRefs",
            "url",
          ],
        },
        {
          type: "array",
          items: {
            "@type": "Beacon",
            type: "object",
            properties: {
              dataset: {
                type: "object",
                "@type": "DataCatalog",
              },
              name: {
                type: "string",
              },
              potentialAction: {
                type: "object",
                "@type": "Action",
              },
              provider: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "Organization",
                  },
                  {
                    type: "object",
                    "@type": "Person",
                  },
                ],
              },
              "rdf:type": {
                type: "string",
                format: "uri",
              },
              supportedRefs: {
                type: "string",
              },
              url: {
                type: "string",
                format: "uri",
              },
            },
            required: [
              "dataset",
              "name",
              "potentialAction",
              "provider",
              "rdf:type",
              "supportedRefs",
              "url",
            ],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyyp814bio",
    title: "ComputationalTool",
    color: "#097969",
    validation: {
      "@type": "ComputationalTool",
      type: "object",
      properties: {
        description: {
          type: "string",
        },
        name: {
          type: "string",
        },
        url: {
          type: "string",
          format: "uri",
        },
      },
      required: ["description", "name", "url"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extycj993bio",
    title: "ComputationalTool",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "ComputationalTool",
          type: "object",
          properties: {
            description: {
              type: "string",
            },
            name: {
              type: "string",
            },
            url: {
              type: "string",
              format: "uri",
            },
          },
          required: ["description", "name", "url"],
        },
        {
          type: "array",
          items: {
            "@type": "ComputationalTool",
            type: "object",
            properties: {
              description: {
                type: "string",
              },
              name: {
                type: "string",
              },
              url: {
                type: "string",
                format: "uri",
              },
            },
            required: ["description", "name", "url"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybk453bio",
    title: "ComputationalWorkflow",
    color: "#097969",
    validation: {
      "@type": "ComputationalWorkflow",
      type: "object",
      properties: {
        creator: {
          oneOf: [
            {
              type: "object",
              "@type": "Organization",
            },
            {
              type: "object",
              "@type": "Person",
            },
          ],
        },
        dateCreated: {
          oneOf: [
            {
              type: "string",
              format: "date",
            },
            {
              type: "object",
              "@type": "DateTime",
            },
          ],
        },
        input: {
          type: "object",
          "@type": "FormalParameter",
        },
        license: {
          oneOf: [
            {
              type: "object",
              "@type": "CreativeWork",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        name: {
          type: "string",
        },
        output: {
          type: "object",
          "@type": "FormalParameter",
        },
        programmingLanguage: {
          oneOf: [
            {
              type: "object",
              "@type": "ComputerLanguage",
            },
            {
              type: "string",
            },
          ],
        },
        sdPublisher: {
          oneOf: [
            {
              type: "object",
              "@type": "Organization",
            },
            {
              type: "object",
              "@type": "Person",
            },
          ],
        },
        url: {
          type: "string",
          format: "uri",
        },
        version: {
          oneOf: [
            {
              type: "number",
            },
            {
              type: "string",
            },
          ],
        },
      },
      required: [
        "creator",
        "dateCreated",
        "input",
        "license",
        "name",
        "output",
        "programmingLanguage",
        "sdPublisher",
        "url",
        "version",
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyvi914bio",
    title: "ComputationalWorkflow",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "ComputationalWorkflow",
          type: "object",
          properties: {
            creator: {
              oneOf: [
                {
                  type: "object",
                  "@type": "Organization",
                },
                {
                  type: "object",
                  "@type": "Person",
                },
              ],
            },
            dateCreated: {
              oneOf: [
                {
                  type: "string",
                  format: "date",
                },
                {
                  type: "object",
                  "@type": "DateTime",
                },
              ],
            },
            input: {
              type: "object",
              "@type": "FormalParameter",
            },
            license: {
              oneOf: [
                {
                  type: "object",
                  "@type": "CreativeWork",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            name: {
              type: "string",
            },
            output: {
              type: "object",
              "@type": "FormalParameter",
            },
            programmingLanguage: {
              oneOf: [
                {
                  type: "object",
                  "@type": "ComputerLanguage",
                },
                {
                  type: "string",
                },
              ],
            },
            sdPublisher: {
              oneOf: [
                {
                  type: "object",
                  "@type": "Organization",
                },
                {
                  type: "object",
                  "@type": "Person",
                },
              ],
            },
            url: {
              type: "string",
              format: "uri",
            },
            version: {
              oneOf: [
                {
                  type: "number",
                },
                {
                  type: "string",
                },
              ],
            },
          },
          required: [
            "creator",
            "dateCreated",
            "input",
            "license",
            "name",
            "output",
            "programmingLanguage",
            "sdPublisher",
            "url",
            "version",
          ],
        },
        {
          type: "array",
          items: {
            "@type": "ComputationalWorkflow",
            type: "object",
            properties: {
              creator: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "Organization",
                  },
                  {
                    type: "object",
                    "@type": "Person",
                  },
                ],
              },
              dateCreated: {
                oneOf: [
                  {
                    type: "string",
                    format: "date",
                  },
                  {
                    type: "object",
                    "@type": "DateTime",
                  },
                ],
              },
              input: {
                type: "object",
                "@type": "FormalParameter",
              },
              license: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "CreativeWork",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              name: {
                type: "string",
              },
              output: {
                type: "object",
                "@type": "FormalParameter",
              },
              programmingLanguage: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "ComputerLanguage",
                  },
                  {
                    type: "string",
                  },
                ],
              },
              sdPublisher: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "Organization",
                  },
                  {
                    type: "object",
                    "@type": "Person",
                  },
                ],
              },
              url: {
                type: "string",
                format: "uri",
              },
              version: {
                oneOf: [
                  {
                    type: "number",
                  },
                  {
                    type: "string",
                  },
                ],
              },
            },
            required: [
              "creator",
              "dateCreated",
              "input",
              "license",
              "name",
              "output",
              "programmingLanguage",
              "sdPublisher",
              "url",
              "version",
            ],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extydk612bio",
    title: "DataRecord",
    color: "#097969",
    validation: {
      "@type": "DataRecord",
      type: "object",
      properties: {
        identifier: {
          oneOf: [
            {
              type: "object",
              "@type": "PropertyValue",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        mainEntity: {
          type: "object",
          "@type": "Thing",
        },
      },
      required: ["identifier", "mainEntity"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extybm586bio",
    title: "DataRecord",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "DataRecord",
          type: "object",
          properties: {
            identifier: {
              oneOf: [
                {
                  type: "object",
                  "@type": "PropertyValue",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            mainEntity: {
              type: "object",
              "@type": "Thing",
            },
          },
          required: ["identifier", "mainEntity"],
        },
        {
          type: "array",
          items: {
            "@type": "DataRecord",
            type: "object",
            properties: {
              identifier: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "PropertyValue",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              mainEntity: {
                type: "object",
                "@type": "Thing",
              },
            },
            required: ["identifier", "mainEntity"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyyj958bio",
    title: "LabProtocol",
    color: "#097969",
    validation: {
      "@type": "LabProtocol",
      type: "object",
      properties: {
        bioSampleUsed: {
          oneOf: [
            {
              type: "object",
              "@type": "BioChemEntity",
            },
            {
              type: "object",
              "@type": "BioSample",
            },
            {
              type: "object",
              "@type": "DefinedTerm",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
            {
              type: "object",
              "@type": "Taxon",
            },
          ],
        },
        headline: {
          type: "string",
        },
        keywords: {
          oneOf: [
            {
              type: "object",
              "@type": "DefinedTerm",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        labEquipmentUsed: {
          oneOf: [
            {
              type: "object",
              "@type": "DefinedTerm",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        protocolPurpose: {
          oneOf: [
            {
              type: "object",
              "@type": "CreativeWork",
            },
            {
              type: "string",
            },
          ],
        },
        reagentUsed: {
          oneOf: [
            {
              type: "object",
              "@type": "BioChemEntity",
            },
            {
              type: "object",
              "@type": "MolecularEntity",
            },
            {
              type: "object",
              "@type": "ChemicalSubstance",
            },
            {
              type: "object",
              "@type": "DefinedTerm",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
      },
      required: [
        "bioSampleUsed",
        "headline",
        "keywords",
        "labEquipmentUsed",
        "protocolPurpose",
        "reagentUsed",
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyvk481bio",
    title: "LabProtocol",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "LabProtocol",
          type: "object",
          properties: {
            bioSampleUsed: {
              oneOf: [
                {
                  type: "object",
                  "@type": "BioChemEntity",
                },
                {
                  type: "object",
                  "@type": "BioSample",
                },
                {
                  type: "object",
                  "@type": "DefinedTerm",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
                {
                  type: "object",
                  "@type": "Taxon",
                },
              ],
            },
            headline: {
              type: "string",
            },
            keywords: {
              oneOf: [
                {
                  type: "object",
                  "@type": "DefinedTerm",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            labEquipmentUsed: {
              oneOf: [
                {
                  type: "object",
                  "@type": "DefinedTerm",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            protocolPurpose: {
              oneOf: [
                {
                  type: "object",
                  "@type": "CreativeWork",
                },
                {
                  type: "string",
                },
              ],
            },
            reagentUsed: {
              oneOf: [
                {
                  type: "object",
                  "@type": "BioChemEntity",
                },
                {
                  type: "object",
                  "@type": "MolecularEntity",
                },
                {
                  type: "object",
                  "@type": "ChemicalSubstance",
                },
                {
                  type: "object",
                  "@type": "DefinedTerm",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
          },
          required: [
            "bioSampleUsed",
            "headline",
            "keywords",
            "labEquipmentUsed",
            "protocolPurpose",
            "reagentUsed",
          ],
        },
        {
          type: "array",
          items: {
            "@type": "LabProtocol",
            type: "object",
            properties: {
              bioSampleUsed: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "BioChemEntity",
                  },
                  {
                    type: "object",
                    "@type": "BioSample",
                  },
                  {
                    type: "object",
                    "@type": "DefinedTerm",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                  {
                    type: "object",
                    "@type": "Taxon",
                  },
                ],
              },
              headline: {
                type: "string",
              },
              keywords: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "DefinedTerm",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              labEquipmentUsed: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "DefinedTerm",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              protocolPurpose: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "CreativeWork",
                  },
                  {
                    type: "string",
                  },
                ],
              },
              reagentUsed: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "BioChemEntity",
                  },
                  {
                    type: "object",
                    "@type": "MolecularEntity",
                  },
                  {
                    type: "object",
                    "@type": "ChemicalSubstance",
                  },
                  {
                    type: "object",
                    "@type": "DefinedTerm",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
            },
            required: [
              "bioSampleUsed",
              "headline",
              "keywords",
              "labEquipmentUsed",
              "protocolPurpose",
              "reagentUsed",
            ],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyzq261bio",
    title: "Phenotype",
    color: "#097969",
    validation: {
      "@type": "Phenotype",
      type: "object",
      properties: {
        identifier: {
          oneOf: [
            {
              type: "object",
              "@type": "PropertyValue",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        name: {
          type: "string",
        },
      },
      required: ["identifier", "name"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyzl820bio",
    title: "Phenotype",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Phenotype",
          type: "object",
          properties: {
            identifier: {
              oneOf: [
                {
                  type: "object",
                  "@type": "PropertyValue",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            name: {
              type: "string",
            },
          },
          required: ["identifier", "name"],
        },
        {
          type: "array",
          items: {
            "@type": "Phenotype",
            type: "object",
            properties: {
              identifier: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "PropertyValue",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              name: {
                type: "string",
              },
            },
            required: ["identifier", "name"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyep693bio",
    title: "Protein",
    color: "#097969",
    validation: {
      "@type": "Protein",
      type: "object",
      properties: {
        identifier: {
          oneOf: [
            {
              type: "object",
              "@type": "PropertyValue",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        name: {
          type: "string",
        },
      },
      required: ["identifier", "name"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extydq363bio",
    title: "Protein",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Protein",
          type: "object",
          properties: {
            identifier: {
              oneOf: [
                {
                  type: "object",
                  "@type": "PropertyValue",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            name: {
              type: "string",
            },
          },
          required: ["identifier", "name"],
        },
        {
          type: "array",
          items: {
            "@type": "Protein",
            type: "object",
            properties: {
              identifier: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "PropertyValue",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              name: {
                type: "string",
              },
            },
            required: ["identifier", "name"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyyp136bio",
    title: "ProteinAnnotation",
    color: "#097969",
    validation: {
      "@type": "ProteinAnnotation",
      type: "object",
      properties: {
        additionalType: {
          type: "string",
          format: "uri",
        },
        identifier: {
          oneOf: [
            {
              type: "object",
              "@type": "PropertyValue",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        "rdf:type": {
          type: "string",
          format: "uri",
        },
      },
      required: ["additionalType", "identifier", "rdf:type"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extydn428bio",
    title: "ProteinAnnotation",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "ProteinAnnotation",
          type: "object",
          properties: {
            additionalType: {
              type: "string",
              format: "uri",
            },
            identifier: {
              oneOf: [
                {
                  type: "object",
                  "@type": "PropertyValue",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            "rdf:type": {
              type: "string",
              format: "uri",
            },
          },
          required: ["additionalType", "identifier", "rdf:type"],
        },
        {
          type: "array",
          items: {
            "@type": "ProteinAnnotation",
            type: "object",
            properties: {
              additionalType: {
                type: "string",
                format: "uri",
              },
              identifier: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "PropertyValue",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              "rdf:type": {
                type: "string",
                format: "uri",
              },
            },
            required: ["additionalType", "identifier", "rdf:type"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyvj431bio",
    title: "ProteinStructure",
    color: "#097969",
    validation: {
      "@type": "ProteinStructure",
      type: "object",
      properties: {
        identifier: {
          oneOf: [
            {
              type: "object",
              "@type": "PropertyValue",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
      },
      required: ["identifier"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyxj852bio",
    title: "ProteinStructure",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "ProteinStructure",
          type: "object",
          properties: {
            identifier: {
              oneOf: [
                {
                  type: "object",
                  "@type": "PropertyValue",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
          },
          required: ["identifier"],
        },
        {
          type: "array",
          items: {
            "@type": "ProteinStructure",
            type: "object",
            properties: {
              identifier: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "PropertyValue",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
            },
            required: ["identifier"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyam935bio",
    title: "SemanticTextAnnotation",
    color: "#097969",
    validation: {
      "@type": "SemanticTextAnnotation",
      type: "object",
      properties: {
        mainEntity: {
          type: "object",
          "@type": "DefinedTerm",
        },
        text: {
          type: "string",
        },
      },
      required: ["mainEntity", "text"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyzp495bio",
    title: "SemanticTextAnnotation",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "SemanticTextAnnotation",
          type: "object",
          properties: {
            mainEntity: {
              type: "object",
              "@type": "DefinedTerm",
            },
            text: {
              type: "string",
            },
          },
          required: ["mainEntity", "text"],
        },
        {
          type: "array",
          items: {
            "@type": "SemanticTextAnnotation",
            type: "object",
            properties: {
              mainEntity: {
                type: "object",
                "@type": "DefinedTerm",
              },
              text: {
                type: "string",
              },
            },
            required: ["mainEntity", "text"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyej205bio",
    title: "Tool",
    color: "#097969",
    validation: {
      "@type": "Tool",
      type: "object",
      properties: {
        description: {
          type: "string",
        },
        name: {
          type: "string",
        },
        url: {
          type: "string",
          format: "uri",
        },
      },
      required: ["description", "name", "url"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyaj970bio",
    title: "Tool",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "Tool",
          type: "object",
          properties: {
            description: {
              type: "string",
            },
            name: {
              type: "string",
            },
            url: {
              type: "string",
              format: "uri",
            },
          },
          required: ["description", "name", "url"],
        },
        {
          type: "array",
          items: {
            "@type": "Tool",
            type: "object",
            properties: {
              description: {
                type: "string",
              },
              name: {
                type: "string",
              },
              url: {
                type: "string",
                format: "uri",
              },
            },
            required: ["description", "name", "url"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyck963bio",
    title: "TrainingMaterial",
    color: "#097969",
    validation: {
      "@type": "TrainingMaterial",
      type: "object",
      properties: {
        description: {
          type: "string",
        },
        keywords: {
          oneOf: [
            {
              type: "object",
              "@type": "DefinedTerm",
            },
            {
              type: "string",
            },
            {
              type: "string",
              format: "uri",
            },
          ],
        },
        name: {
          type: "string",
        },
      },
      required: ["description", "keywords", "name"],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: "extyep114bio",
    title: "TrainingMaterial",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "TrainingMaterial",
          type: "object",
          properties: {
            description: {
              type: "string",
            },
            keywords: {
              oneOf: [
                {
                  type: "object",
                  "@type": "DefinedTerm",
                },
                {
                  type: "string",
                },
                {
                  type: "string",
                  format: "uri",
                },
              ],
            },
            name: {
              type: "string",
            },
          },
          required: ["description", "keywords", "name"],
        },
        {
          type: "array",
          items: {
            "@type": "TrainingMaterial",
            type: "object",
            properties: {
              description: {
                type: "string",
              },
              keywords: {
                oneOf: [
                  {
                    type: "object",
                    "@type": "DefinedTerm",
                  },
                  {
                    type: "string",
                  },
                  {
                    type: "string",
                    format: "uri",
                  },
                ],
              },
              name: {
                type: "string",
              },
            },
            required: ["description", "keywords", "name"],
          },
        },
      ],
    },
    belongs_to: "bioschemas",
  },
];
