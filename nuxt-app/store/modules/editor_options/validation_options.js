// _id is a random unique string
// color is a unique legible color against white text

export const validation_options = [
  {
    _id: "01233",
    title: "string",
    color: "#0263fd",
    validation: {
      type: "string",
    },
  },
  {
    _id: "01432",
    title: "string(s)",
    color: "#2717a1",
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
    _id: "14325",
    title: "boolean",
    color: "#d62979",
    validation: {
      type: "boolean",
    },
  },
  {
    _id: "3543",
    title: "integer",
    color: "#6e3ac5",
    validation: {
      type: "integer",
    },
  },
  {
    _id: "4654",
    title: "url",
    color: "#fc6903",
    validation: {
      type: "string",
      format: "uri",
    },
  },
  {
    _id: "5867",
    title: "keywords",
    color: "#28908c",
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
    _id: "6876",
    title: "date",
    color: "#9bbf06",
    validation: {
      format: "date",
      type: "string",
    },
  },
  {
    _id: "7645",
    title: "enumeration",
    color: "#5a71a5",
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
    _id: "8567",
    title: "constant",
    color: "#d8272a",
    validation: {
      const: "Edit const value",
    },
  },
  {
    _id: "9654",
    title: "object|Person",
    color: "#49414b",
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
    _id: "1065",
    title: "ontology",
    color: "#a37d00",
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
    _id: "1062",
    title: "(DEF) citation(s)",
    color: "#5a064d",
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
