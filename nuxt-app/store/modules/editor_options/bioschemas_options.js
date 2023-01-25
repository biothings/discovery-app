// _id is a random unique string
// color is a unique legible color against white text

export const bioschemas_options = [
    {
      _id: "01233bio",
      title: "text",
      color: "#097969",
      validation: {
        type: "string",
      },
    },
    {
      _id: "01432bio",
      title: "text(s)",
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
    },
    {
      _id: "14325bio",
      title: "boolean",
      color: "#097969",
      validation: {
        type: "boolean",
      },
    },
    {
      _id: "3543bio",
      title: "integer",
      color: "#097969",
      validation: {
        type: "integer",
      },
    },
    {
      _id: "4654bio",
      title: "url",
      color: "#097969",
      validation: {
        type: "string",
        format: "uri",
      },
    },
    {
      _id: "5867bio",
      title: "keywords",
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
    },
    {
      _id: "6876bio",
      title: "date",
      color: "#097969",
      validation: {
        format: "date",
        type: "string",
      },
    },
    {
      _id: "7645bio",
      title: "enumeration",
      color: "#097969",
      validation: {
        oneOf: [
          {
            type: "string",
            enum: ["option1", "option2", "option3"],
          },
          {
            type: "array",
            items: {
              type: "string",
              enum: ["option1", "option2", "option3"],
            },
          },
        ],
      },
    },
    {
      _id: "8567bio",
      title: "constant",
      color: "#097969",
      validation: {
        const: "Edit const value",
      },
    },
    {
      _id: "9654bio",
      title: "object|Person",
      color: "#097969",
      validation: {
        "@type": "Person",
        type: "object",
        properties: {
          name: { type: "string" },
          url: { type: "string", format: "uri" },
        },
        required: ["name"],
      },
    },
    {
      _id: "1065bio",
      title: "ontology",
      color: "#097969",
      validation: {
        "@type": "CreativeWork",
        type: "string",
        vocabulary: {
          ontology: ["[For example:]", "ncbitaxon"],
          children_of: [
            "[For example:]",
            "http://purl.obolibrary.org/obo/NCBITaxon_10239",
          ],
        },
        strict: false,
      },
    },
    {
      _id: "1062bio",
      title: "(DEF) citation(s)",
      color: "#023020",
      validation: {
        description: "A citation to the dataset",
        oneOf: [
          {
            $ref: "#/definitions/citation",
          },
          {
            type: "array",
            items: {
              $ref: "#/definitions/citation",
            },
          },
        ],
      },
    },
  ];
  