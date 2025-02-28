// _id is a random unique string
// color is a unique legible color against white text

export const definition_options = [
  {
    _id: "def001",
    title: "citation",
    color: "#7630dd",
    validation: {
      description:
        "A citation object for a resource which is cited by the dataset (ie- is a derivative of the dataset) , related to the dataset, or from which the dataset was based on (ie- is derived from).",
      "@type": "Thing",
      type: "object",
      properties: {
        name: {
          description: "Name of or title of the citation",
          type: "string",
        },
        identifier: {
          description: "An identifier associated with the citation",
          type: "string",
        },
        pmid: {
          description: "A pubmed identifier if available",
          type: "string",
        },
        doi: {
          description: "A doi if available",
          type: "string",
        },
        url: {
          description: "The url of the resource cited",
          type: "string",
          format: "uri",
        },
        citeText: {
          description:
            "The bibliographic citation for the referenced resource as is provided",
          type: "string",
        },
      },
      required: ["name"],
    },
  },
];
