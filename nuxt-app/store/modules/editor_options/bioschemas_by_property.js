export const bioschemas_by_property = [
  {
    _id: ["idcp679bio", "blank"],
    title: "identifier",
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
          type: "string",
        },
        {
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["idfr164bio", "blank"],
    title: "identifier",
    color: "#097969",
    validation: {
      anyOf: [
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
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["habw501bio", "blank"],
    title: "hasRepresentation",
    color: "#097969",
    validation: {
      "@type": "PropertyValue orText orURL",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["habx745bio", "blank"],
    title: "hasRepresentation",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "PropertyValue orText orURL",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "PropertyValue orText orURL",
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
    _id: ["tacx825bio", "blank"],
    title: "taxonRank",
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
          type: "string",
        },
        {
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["tagx273bio", "blank"],
    title: "taxonRank",
    color: "#097969",
    validation: {
      anyOf: [
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
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["stgv418bio", "blank"],
    title: "studyProcess",
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
          type: "string",
        },
        {
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["stds249bio", "blank"],
    title: "studyProcess",
    color: "#097969",
    validation: {
      anyOf: [
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
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["stcq896bio", "blank"],
    title: "studyDomain",
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
          type: "string",
        },
        {
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["sthp499bio", "blank"],
    title: "studyDomain",
    color: "#097969",
    validation: {
      anyOf: [
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
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["uraw856bio", "blank"],
    title: "url",
    color: "#097969",
    validation: {
      type: "string",
      format: "uri",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["urbs307bio", "blank"],
    title: "url",
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
    _id: ["saes935bio", "blank"],
    title: "sameAs",
    color: "#097969",
    validation: {
      type: "string",
      format: "uri",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["saap702bio", "blank"],
    title: "sameAs",
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
    _id: ["addt491bio", "blank"],
    title: "additionalType",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["adgu638bio", "blank"],
    title: "additionalType",
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
    _id: ["thap156bio", "blank"],
    title: "thumbnailUrl",
    color: "#097969",
    validation: {
      type: "string",
      format: "uri",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["thgs788bio", "blank"],
    title: "thumbnailUrl",
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
    _id: ["dobt943bio", "blank"],
    title: "downloadUrl",
    color: "#097969",
    validation: {
      type: "string",
      format: "uri",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["docp201bio", "blank"],
    title: "downloadUrl",
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
    _id: ["socs696bio", "blank"],
    title: "socialMedia",
    color: "#097969",
    validation: {
      type: "string",
      format: "uri",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["sobu184bio", "blank"],
    title: "socialMedia",
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
    _id: ["rdgw928bio", "blank"],
    title: "rdf:type",
    color: "#097969",
    validation: {
      type: "string",
      format: "uri",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["rdbx589bio", "blank"],
    title: "rdf:type",
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
    _id: ["atfq758bio", "blank"],
    title: "attachment",
    color: "#097969",
    validation: {
      type: "string",
      format: "uri",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["atgr700bio", "blank"],
    title: "attachment",
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
    _id: ["coaw429bio", "blank"],
    title: "codeRepository",
    color: "#097969",
    validation: {
      type: "string",
      format: "uri",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["coaw543bio", "blank"],
    title: "codeRepository",
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
    _id: ["difv247bio", "blank"],
    title: "discussionUrl",
    color: "#097969",
    validation: {
      type: "string",
      format: "uri",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["dibv154bio", "blank"],
    title: "discussionUrl",
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
    _id: ["todq932bio", "blank"],
    title: "topic",
    color: "#097969",
    validation: {
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
    belongs_to: "bioschemas",
  },
  {
    _id: ["toew338bio", "blank"],
    title: "topic",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["ouet593bio", "blank"],
    title: "outputData",
    color: "#097969",
    validation: {
      type: "string",
      format: "uri",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["ouev782bio", "blank"],
    title: "outputData",
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
    _id: ["oufs744bio", "blank"],
    title: "outputFormat",
    color: "#097969",
    validation: {
      type: "string",
      format: "uri",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["oues440bio", "blank"],
    title: "outputFormat",
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
    _id: ["PPfs112bio", "blank"],
    title: "PPEO:hasGrowthChamber",
    color: "#097969",
    validation: {
      type: "string",
      format: "uri",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["PPhv910bio", "blank"],
    title: "PPEO:hasGrowthChamber",
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
    _id: ["audq308bio", "blank"],
    title: "audience",
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
    _id: ["auep559bio", "blank"],
    title: "audience",
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
    _id: ["exgu707bio", "blank"],
    title: "expertise",
    color: "#097969",
    validation: {
      type: "string",
      format: "uri",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["exes168bio", "blank"],
    title: "expertise",
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
    _id: ["infs136bio", "blank"],
    title: "inputData",
    color: "#097969",
    validation: {
      type: "string",
      format: "uri",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["infp183bio", "blank"],
    title: "inputData",
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
    _id: ["inav985bio", "blank"],
    title: "inputFormat",
    color: "#097969",
    validation: {
      type: "string",
      format: "uri",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["ineu171bio", "blank"],
    title: "inputFormat",
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
    _id: ["feax160bio", "blank"],
    title: "featureList",
    color: "#097969",
    validation: {
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
    belongs_to: "bioschemas",
  },
  {
    _id: ["fegr432bio", "blank"],
    title: "featureList",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["nahw542bio", "blank"],
    title: "name",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["nabp659bio", "blank"],
    title: "name",
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
    _id: ["deeu745bio", "blank"],
    title: "description",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["deht204bio", "blank"],
    title: "description",
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
    _id: ["alhs968bio", "blank"],
    title: "alternateName",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["aleq612bio", "blank"],
    title: "alternateName",
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
    _id: ["keex417bio", "blank"],
    title: "keywords",
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
          type: "string",
        },
        {
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["kefs295bio", "blank"],
    title: "keywords",
    color: "#097969",
    validation: {
      anyOf: [
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
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["diht811bio", "blank"],
    title: "disambiguatingDescription",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["diav318bio", "blank"],
    title: "disambiguatingDescription",
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
    _id: ["abct413bio", "blank"],
    title: "abstract",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["abbt610bio", "blank"],
    title: "abstract",
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
    _id: ["paex332bio", "blank"],
    title: "pagination",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["pahq939bio", "blank"],
    title: "pagination",
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
    _id: ["opdp750bio", "blank"],
    title: "operatingSystem",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["opds509bio", "blank"],
    title: "operatingSystem",
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
    _id: ["hebt980bio", "blank"],
    title: "headline",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["heat376bio", "blank"],
    title: "headline",
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
    _id: ["achr283bio", "blank"],
    title: "accessibilitySummary",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["acfx167bio", "blank"],
    title: "accessibilitySummary",
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
    _id: ["apau114bio", "blank"],
    title: "applicationSuite",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["apex270bio", "blank"],
    title: "applicationSuite",
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
    _id: ["sohp727bio", "blank"],
    title: "softwareVersion",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["socw103bio", "blank"],
    title: "softwareVersion",
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
    _id: ["teax207bio", "blank"],
    title: "text",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["tefs758bio", "blank"],
    title: "text",
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
    _id: ["smhq692bio", "blank"],
    title: "smiles",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["smgu979bio", "blank"],
    title: "smiles",
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
    _id: ["moap722bio", "blank"],
    title: "molecularFormula",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["mocq824bio", "blank"],
    title: "molecularFormula",
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
    _id: ["ruer601bio", "blank"],
    title: "runtimePlatform",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["rubt497bio", "blank"],
    title: "runtimePlatform",
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
    _id: ["redu620bio", "blank"],
    title: "registrationStatus",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["reau629bio", "blank"],
    title: "registrationStatus",
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
    _id: ["subx126bio", "blank"],
    title: "supportedRefs",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["sudw414bio", "blank"],
    title: "supportedRefs",
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
    _id: ["sths860bio", "blank"],
    title: "status",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["stct474bio", "blank"],
    title: "status",
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
    _id: ["prgw612bio", "blank"],
    title: "prerequisite",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["prgt447bio", "blank"],
    title: "prerequisite",
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
    _id: ["cobs632bio", "blank"],
    title: "courseCode",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["codu712bio", "blank"],
    title: "courseCode",
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
    _id: ["dwhv256bio", "blank"],
    title: "dwc:vernacularName",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["dwet883bio", "blank"],
    title: "dwc:vernacularName",
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
    _id: ["elbw112bio", "blank"],
    title: "eligibility",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["eldx388bio", "blank"],
    title: "eligibility",
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
    _id: ["cocp966bio", "blank"],
    title: "conditionsOfAccess",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["codp388bio", "blank"],
    title: "conditionsOfAccess",
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
    _id: ["apbs774bio", "blank"],
    title: "applicationCategory",
    color: "#097969",
    validation: {
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
    belongs_to: "bioschemas",
  },
  {
    _id: ["apgs609bio", "blank"],
    title: "applicationCategory",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["apgs842bio", "blank"],
    title: "applicationSubCategory",
    color: "#097969",
    validation: {
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
    belongs_to: "bioschemas",
  },
  {
    _id: ["aphr680bio", "blank"],
    title: "applicationSubCategory",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["araq955bio", "blank"],
    title: "articleBody",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["ards465bio", "blank"],
    title: "articleBody",
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
    _id: ["chfq169bio", "blank"],
    title: "chemicalComposition",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["chas168bio", "blank"],
    title: "chemicalComposition",
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
    _id: ["exes618bio", "blank"],
    title: "experience",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["exdx429bio", "blank"],
    title: "experience",
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
    _id: ["inat939bio", "blank"],
    title: "internatonalActivities",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["inbw234bio", "blank"],
    title: "internatonalActivities",
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
    _id: ["iuev996bio", "blank"],
    title: "iupacName",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["iuev904bio", "blank"],
    title: "iupacName",
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
    _id: ["lehp928bio", "blank"],
    title: "legalName",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["lefs966bio", "blank"],
    title: "legalName",
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
    _id: ["fuex488bio", "blank"],
    title: "funding",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["fuaw475bio", "blank"],
    title: "funding",
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
    _id: ["fugu732bio", "blank"],
    title: "fundingModel",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["fubx741bio", "blank"],
    title: "fundingModel",
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
    _id: ["haex239bio", "blank"],
    title: "hasBioPolymerSequence",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["hadr665bio", "blank"],
    title: "hasBioPolymerSequence",
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
    _id: ["haet961bio", "blank"],
    title: "hasSequence",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["habx721bio", "blank"],
    title: "hasSequence",
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
    _id: ["hagq177bio", "blank"],
    title: "hasStatus",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["haax810bio", "blank"],
    title: "hasStatus",
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
    _id: ["incu981bio", "blank"],
    title: "inChI",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["iner716bio", "blank"],
    title: "inChI",
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
    _id: ["indv291bio", "blank"],
    title: "inChIKey",
    color: "#097969",
    validation: {
      type: "string",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["ingq207bio", "blank"],
    title: "inChIKey",
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
    _id: ["imgu349bio", "blank"],
    title: "image",
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
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["imcv796bio", "blank"],
    title: "image",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["lofp282bio", "blank"],
    title: "logo",
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
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["lobv884bio", "blank"],
    title: "logo",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["dahp605bio", "blank"],
    title: "dateModified",
    color: "#097969",
    validation: {
      oneOf: [
        {
          type: "string",
          format: "date",
        },
        {
          "@type": "DateTime",
          type: "object",
          properties: {},
          required: [],
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["daau626bio", "blank"],
    title: "dateModified",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["daat442bio", "blank"],
    title: "dateCreated",
    color: "#097969",
    validation: {
      oneOf: [
        {
          type: "string",
          format: "date",
        },
        {
          "@type": "DateTime",
          type: "object",
          properties: {},
          required: [],
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["daau992bio", "blank"],
    title: "dateCreated",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["stet579bio", "blank"],
    title: "startDate",
    color: "#097969",
    validation: {
      oneOf: [
        {
          type: "string",
          format: "date",
        },
        {
          "@type": "DateTime",
          type: "object",
          properties: {},
          required: [],
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["stfp682bio", "blank"],
    title: "startDate",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["enep502bio", "blank"],
    title: "endDate",
    color: "#097969",
    validation: {
      oneOf: [
        {
          type: "string",
          format: "date",
        },
        {
          "@type": "DateTime",
          type: "object",
          properties: {},
          required: [],
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["enfr228bio", "blank"],
    title: "endDate",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["daaq249bio", "blank"],
    title: "datePublished",
    color: "#097969",
    validation: {
      type: "string",
      format: "date",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["dacp304bio", "blank"],
    title: "datePublished",
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
    _id: ["lihr716bio", "blank"],
    title: "license",
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
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["ligw154bio", "blank"],
    title: "license",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["macx790bio", "blank"],
    title: "mainEntityOfPage",
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
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["macx425bio", "blank"],
    title: "mainEntityOfPage",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["iset200bio", "blank"],
    title: "isPartOf",
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
    _id: ["isbt982bio", "blank"],
    title: "isPartOf",
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
    _id: ["puhv407bio", "blank"],
    title: "publishingPrinciples",
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
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["pugq402bio", "blank"],
    title: "publishingPrinciples",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["doew616bio", "blank"],
    title: "documentation",
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
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["docx104bio", "blank"],
    title: "documentation",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["isgt247bio", "blank"],
    title: "isBasedOn",
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
    _id: ["isbu670bio", "blank"],
    title: "isBasedOn",
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
    _id: ["cifx452bio", "blank"],
    title: "citation",
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
          type: "string",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["cigv836bio", "blank"],
    title: "citation",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["prhs297bio", "blank"],
    title: "protocolAdvantage",
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
          type: "string",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["prcu362bio", "blank"],
    title: "protocolAdvantage",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["prhq853bio", "blank"],
    title: "protocolApplication",
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
          type: "string",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["prhv635bio", "blank"],
    title: "protocolApplication",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["prep694bio", "blank"],
    title: "protocolLimitation",
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
          type: "string",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["prbx119bio", "blank"],
    title: "protocolLimitation",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["prdx887bio", "blank"],
    title: "protocolOutcome",
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
          type: "string",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["preu132bio", "blank"],
    title: "protocolOutcome",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["prav800bio", "blank"],
    title: "protocolPurpose",
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
          type: "string",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["prdp387bio", "blank"],
    title: "protocolPurpose",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["edgt904bio", "blank"],
    title: "educationalLevel",
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
          type: "string",
        },
        {
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["edhw231bio", "blank"],
    title: "educationalLevel",
    color: "#097969",
    validation: {
      anyOf: [
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
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["cohw771bio", "blank"],
    title: "competencyRequired",
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
          type: "string",
        },
        {
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["cogs747bio", "blank"],
    title: "competencyRequired",
    color: "#097969",
    validation: {
      anyOf: [
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
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["lafs722bio", "blank"],
    title: "labEquipmentUsed",
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
          type: "string",
        },
        {
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["ladw393bio", "blank"],
    title: "labEquipmentUsed",
    color: "#097969",
    validation: {
      anyOf: [
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
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["abbt905bio", "blank"],
    title: "about",
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
    _id: ["abat552bio", "blank"],
    title: "about",
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
    _id: ["mehq508bio", "blank"],
    title: "mentions",
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
    _id: ["medw143bio", "blank"],
    title: "mentions",
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
    _id: ["maax217bio", "blank"],
    title: "mainEntity",
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
    _id: ["maht755bio", "blank"],
    title: "mainEntity",
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
    _id: ["ishx856bio", "blank"],
    title: "isBasisFor",
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
          "@type": "Product",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["isfp198bio", "blank"],
    title: "isBasisFor",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["dies132bio", "blank"],
    title: "dissolutionDate",
    color: "#097969",
    validation: {
      type: "string",
      format: "date",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["difx179bio", "blank"],
    title: "dissolutionDate",
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
    _id: ["acct729bio", "blank"],
    title: "acceptanceNotificationDate",
    color: "#097969",
    validation: {
      type: "string",
      format: "date",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["accr512bio", "blank"],
    title: "acceptanceNotificationDate",
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
    _id: ["fobr188bio", "blank"],
    title: "foundingDate",
    color: "#097969",
    validation: {
      type: "string",
      format: "date",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["fobr249bio", "blank"],
    title: "foundingDate",
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
    _id: ["aucs882bio", "blank"],
    title: "author",
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
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["auer947bio", "blank"],
    title: "author",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["coht838bio", "blank"],
    title: "contributor",
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
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["cobx549bio", "blank"],
    title: "contributor",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["crft524bio", "blank"],
    title: "creator",
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
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["crgt495bio", "blank"],
    title: "creator",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["fufq764bio", "blank"],
    title: "funder",
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
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["fucq690bio", "blank"],
    title: "funder",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["prcp419bio", "blank"],
    title: "provider",
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
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["prcw592bio", "blank"],
    title: "provider",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["pufx326bio", "blank"],
    title: "publisher",
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
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["pueu818bio", "blank"],
    title: "publisher",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["magv247bio", "blank"],
    title: "maintainer",
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
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["macs212bio", "blank"],
    title: "maintainer",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["ordx238bio", "blank"],
    title: "organizer",
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
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["orcr844bio", "blank"],
    title: "organizer",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["mebu941bio", "blank"],
    title: "member",
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
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["mebp608bio", "blank"],
    title: "member",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["sdfs930bio", "blank"],
    title: "sdPublisher",
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
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["sdeu393bio", "blank"],
    title: "sdPublisher",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["prep264bio", "blank"],
    title: "producer",
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
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["prhp219bio", "blank"],
    title: "producer",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["spcv341bio", "blank"],
    title: "sponsor",
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
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["spfw989bio", "blank"],
    title: "sponsor",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["suhu878bio", "blank"],
    title: "submitter",
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
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["sufu370bio", "blank"],
    title: "submitter",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["pedu362bio", "blank"],
    title: "performer",
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
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["pehs910bio", "blank"],
    title: "performer",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["cuev369bio", "blank"],
    title: "custodian",
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
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["cuhr706bio", "blank"],
    title: "custodian",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["cofr979bio", "blank"],
    title: "contact",
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
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["cobv182bio", "blank"],
    title: "contact",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["cogu680bio", "blank"],
    title: "collector",
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
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["cogt444bio", "blank"],
    title: "collector",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["foes941bio", "blank"],
    title: "founderMember",
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
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["foex873bio", "blank"],
    title: "founderMember",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["ingp566bio", "blank"],
    title: "inLanguage",
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
          type: "string",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["inct850bio", "blank"],
    title: "inLanguage",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["aseq582bio", "blank"],
    title: "associatedDisease",
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
          "@type": "PropertyValue",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["asbp161bio", "blank"],
    title: "associatedDisease",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["ishp398bio", "blank"],
    title: "isInvolvedInBiologicalProcess",
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
          "@type": "PropertyValue",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["isgt499bio", "blank"],
    title: "isInvolvedInBiologicalProcess",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["hahw582bio", "blank"],
    title: "hasMolecularFunction",
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
          "@type": "PropertyValue",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["haas186bio", "blank"],
    title: "hasMolecularFunction",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["iscx143bio", "blank"],
    title: "isLocatedInSubcellularLocation",
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
          "@type": "PropertyValue",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["iscq913bio", "blank"],
    title: "isLocatedInSubcellularLocation",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["adhx546bio", "blank"],
    title: "additionalProperty",
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
    _id: ["adhp367bio", "blank"],
    title: "additionalProperty",
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
    _id: ["cras502bio", "blank"],
    title: "creationMethod",
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
    _id: ["crfu400bio", "blank"],
    title: "creationMethod",
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
    _id: ["hafv991bio", "blank"],
    title: "hasBioChemEntityPart",
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
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["hahp417bio", "blank"],
    title: "hasBioChemEntityPart",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["iseu529bio", "blank"],
    title: "isPartOfBioChemEntity",
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
    _id: ["isbu152bio", "blank"],
    title: "isPartOfBioChemEntity",
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
    _id: ["biev141bio", "blank"],
    title: "bioChemInteraction",
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
    _id: ["biep863bio", "blank"],
    title: "bioChemInteraction",
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
    _id: ["bigp826bio", "blank"],
    title: "bioChemSimilarity",
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
    _id: ["biew371bio", "blank"],
    title: "bioChemSimilarity",
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
    _id: ["enct236bio", "blank"],
    title: "encodesBioChemEntity",
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
    _id: ["enfw321bio", "blank"],
    title: "encodesBioChemEntity",
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
    _id: ["biet619bio", "blank"],
    title: "bioChemAssociation",
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
    _id: ["bicw377bio", "blank"],
    title: "bioChemAssociation",
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
    _id: ["hagp680bio", "blank"],
    title: "hasPart",
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
    _id: ["habs936bio", "blank"],
    title: "hasPart",
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
    _id: ["soer720bio", "blank"],
    title: "softwareHelp",
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
    _id: ["soat509bio", "blank"],
    title: "softwareHelp",
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
    _id: ["wocu390bio", "blank"],
    title: "works",
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
    _id: ["wodv980bio", "blank"],
    title: "works",
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
    _id: ["wocw317bio", "blank"],
    title: "workTranslation",
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
    _id: ["wocw440bio", "blank"],
    title: "workTranslation",
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
    _id: ["wodq606bio", "blank"],
    title: "workFeatured",
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
    _id: ["wocs117bio", "blank"],
    title: "workFeatured",
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
    _id: ["jocp981bio", "blank"],
    title: "journalReferee",
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
    _id: ["joap365bio", "blank"],
    title: "journalReferee",
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
    _id: ["isdt712bio", "blank"],
    title: "isAccessibleForFree",
    color: "#097969",
    validation: {
      type: "boolean",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["iset630bio", "blank"],
    title: "isAccessibleForFree",
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
    _id: ["vahu385bio", "blank"],
    title: "valueRequired",
    color: "#097969",
    validation: {
      type: "boolean",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["vaex219bio", "blank"],
    title: "valueRequired",
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
    _id: ["aghv554bio", "blank"],
    title: "aggregator",
    color: "#097969",
    validation: {
      type: "boolean",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["agcr961bio", "blank"],
    title: "aggregator",
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
    _id: ["isfu441bio", "blank"],
    title: "isCodingRNA",
    color: "#097969",
    validation: {
      type: "boolean",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["iscq542bio", "blank"],
    title: "isCodingRNA",
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
    _id: ["isds416bio", "blank"],
    title: "isControl",
    color: "#097969",
    validation: {
      type: "boolean",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["isap938bio", "blank"],
    title: "isControl",
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
    _id: ["edaw758bio", "blank"],
    title: "editor",
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
    _id: ["edcw691bio", "blank"],
    title: "editor",
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
    _id: ["addv322bio", "blank"],
    title: "advisor",
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
    _id: ["adct625bio", "blank"],
    title: "advisor",
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
    _id: ["infv797bio", "blank"],
    title: "instructor",
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
    _id: ["inhq584bio", "blank"],
    title: "instructor",
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
    _id: ["taeq154bio", "blank"],
    title: "taxonomicRange",
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
          type: "string",
        },
        {
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["tafw150bio", "blank"],
    title: "taxonomicRange",
    color: "#097969",
    validation: {
      anyOf: [
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
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["vegv986bio", "blank"],
    title: "version",
    color: "#097969",
    validation: {
      oneOf: [
        {
          type: "number",
        },
        {
          type: "string",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["vebq501bio", "blank"],
    title: "version",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "number",
        },
        {
          type: "array",
          items: {
            type: "number",
          },
        },
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
    _id: ["enau869bio", "blank"],
    title: "encodingFormat",
    color: "#097969",
    validation: {
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
    belongs_to: "bioschemas",
  },
  {
    _id: ["enfu684bio", "blank"],
    title: "encodingFormat",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["orhx545bio", "blank"],
    title: "orcid",
    color: "#097969",
    validation: {
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
    belongs_to: "bioschemas",
  },
  {
    _id: ["oret502bio", "blank"],
    title: "orcid",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["megv546bio", "blank"],
    title: "measurementTechnique",
    color: "#097969",
    validation: {
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
    belongs_to: "bioschemas",
  },
  {
    _id: ["meft139bio", "blank"],
    title: "measurementTechnique",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["sofr788bio", "blank"],
    title: "softwareRequirements",
    color: "#097969",
    validation: {
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
    belongs_to: "bioschemas",
  },
  {
    _id: ["sofs727bio", "blank"],
    title: "softwareRequirements",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["tybr947bio", "blank"],
    title: "type",
    color: "#097969",
    validation: {
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
    belongs_to: "bioschemas",
  },
  {
    _id: ["tyfr891bio", "blank"],
    title: "type",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["sthq317bio", "blank"],
    title: "structureDeterminationMethod",
    color: "#097969",
    validation: {
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
    belongs_to: "bioschemas",
  },
  {
    _id: ["sthr380bio", "blank"],
    title: "structureDeterminationMethod",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["prhq141bio", "blank"],
    title: "programme",
    color: "#097969",
    validation: {
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
    belongs_to: "bioschemas",
  },
  {
    _id: ["prep184bio", "blank"],
    title: "programme",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["deaw366bio", "blank"],
    title: "deadline",
    color: "#097969",
    validation: {
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
    belongs_to: "bioschemas",
  },
  {
    _id: ["deau118bio", "blank"],
    title: "deadline",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["coew984bio", "blank"],
    title: "courseMode",
    color: "#097969",
    validation: {
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
    belongs_to: "bioschemas",
  },
  {
    _id: ["coer753bio", "blank"],
    title: "courseMode",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["cubw775bio", "blank"],
    title: "curriculumVitae",
    color: "#097969",
    validation: {
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
    belongs_to: "bioschemas",
  },
  {
    _id: ["cuds700bio", "blank"],
    title: "curriculumVitae",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["boeq341bio", "blank"],
    title: "boundMolecule",
    color: "#097969",
    validation: {
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
    belongs_to: "bioschemas",
  },
  {
    _id: ["bobu695bio", "blank"],
    title: "boundMolecule",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["incw939bio", "blank"],
    title: "interest",
    color: "#097969",
    validation: {
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
    belongs_to: "bioschemas",
  },
  {
    _id: ["inbt863bio", "blank"],
    title: "interest",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "string",
        },
        {
          type: "array",
          items: {
            type: "string",
          },
        },
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
    _id: ["preu863bio", "blank"],
    title: "programmingLanguage",
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
          type: "string",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["prbs563bio", "blank"],
    title: "programmingLanguage",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["pafv689bio", "blank"],
    title: "pageEnd",
    color: "#097969",
    validation: {
      oneOf: [
        {
          type: "integer",
        },
        {
          type: "string",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["paar921bio", "blank"],
    title: "pageEnd",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "integer",
        },
        {
          type: "array",
          items: {
            type: "integer",
          },
        },
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
    _id: ["paar183bio", "blank"],
    title: "pageStart",
    color: "#097969",
    validation: {
      oneOf: [
        {
          type: "integer",
        },
        {
          type: "string",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["pacv402bio", "blank"],
    title: "pageStart",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "integer",
        },
        {
          type: "array",
          items: {
            type: "integer",
          },
        },
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
    _id: ["voap511bio", "blank"],
    title: "volumeNumber",
    color: "#097969",
    validation: {
      oneOf: [
        {
          type: "integer",
        },
        {
          type: "string",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["voap417bio", "blank"],
    title: "volumeNumber",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "integer",
        },
        {
          type: "array",
          items: {
            type: "integer",
          },
        },
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
    _id: ["poct537bio", "blank"],
    title: "position",
    color: "#097969",
    validation: {
      oneOf: [
        {
          type: "integer",
        },
        {
          type: "string",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["poav664bio", "blank"],
    title: "position",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "integer",
        },
        {
          type: "array",
          items: {
            type: "integer",
          },
        },
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
    _id: ["isgq376bio", "blank"],
    title: "issueNumber",
    color: "#097969",
    validation: {
      oneOf: [
        {
          type: "integer",
        },
        {
          type: "string",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["isbw468bio", "blank"],
    title: "issueNumber",
    color: "#097969",
    validation: {
      anyOf: [
        {
          type: "integer",
        },
        {
          type: "array",
          items: {
            type: "integer",
          },
        },
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
    _id: ["bihu106bio", "blank"],
    title: "biologicalRole",
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
    _id: ["bihx111bio", "blank"],
    title: "biologicalRole",
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
    _id: ["poew934bio", "blank"],
    title: "potentialUse",
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
    _id: ["poex427bio", "blank"],
    title: "potentialUse",
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
    _id: ["chcu245bio", "blank"],
    title: "chemicalRole",
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
    _id: ["chaw375bio", "blank"],
    title: "chemicalRole",
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
    _id: ["vaaq474bio", "blank"],
    title: "valueReference",
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
    _id: ["vaeu450bio", "blank"],
    title: "valueReference",
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
    _id: ["anft915bio", "blank"],
    title: "anatomicalLocation",
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
    _id: ["anhw400bio", "blank"],
    title: "anatomicalLocation",
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
    _id: ["bihq320bio", "blank"],
    title: "biogicalRole",
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
    _id: ["bibv268bio", "blank"],
    title: "biogicalRole",
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
    _id: ["madp956bio", "blank"],
    title: "maximumAttendeeCapacity",
    color: "#097969",
    validation: {
      type: "integer",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["mabq581bio", "blank"],
    title: "maximumAttendeeCapacity",
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
    _id: ["cogq889bio", "blank"],
    title: "commentCount",
    color: "#097969",
    validation: {
      type: "integer",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["coeq533bio", "blank"],
    title: "commentCount",
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
    _id: ["sacp752bio", "blank"],
    title: "samplingAge",
    color: "#097969",
    validation: {
      type: "integer",
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["saaw812bio", "blank"],
    title: "samplingAge",
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
    _id: ["mefx996bio", "blank"],
    title: "memberOf",
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
          "@type": "ProgramMembership",
          type: "object",
          properties: {},
          required: [],
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["medv888bio", "blank"],
    title: "memberOf",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["isew395bio", "blank"],
    title: "isEncodedByBioChemEntity",
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
          "@type": "RNA",
          type: "object",
          properties: {},
          required: [],
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["isgs740bio", "blank"],
    title: "isEncodedByBioChemEntity",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["albt204bio", "blank"],
    title: "alternativeOf",
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
    _id: ["alax631bio", "blank"],
    title: "alternativeOf",
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
    _id: ["digp985bio", "blank"],
    title: "distribution",
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
    _id: ["difw668bio", "blank"],
    title: "distribution",
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
    _id: ["sobu364bio", "blank"],
    title: "softwareAddOn",
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
    _id: ["soas542bio", "blank"],
    title: "softwareAddOn",
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
    _id: ["tagu190bio", "blank"],
    title: "targetProduct",
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
    _id: ["taar900bio", "blank"],
    title: "targetProduct",
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
    _id: ["isaq446bio", "blank"],
    title: "isContainedIn",
    color: "#097969",
    validation: {
      "@type": "BioChemEntity orURL",
      type: "object",
      properties: {},
      required: [],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["isfs667bio", "blank"],
    title: "isContainedIn",
    color: "#097969",
    validation: {
      oneOf: [
        {
          "@type": "BioChemEntity orURL",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "array",
          items: {
            "@type": "BioChemEntity orURL",
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
    _id: ["crcu226bio", "blank"],
    title: "creativeWorkStatus",
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
          type: "string",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["crbw426bio", "blank"],
    title: "creativeWorkStatus",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["tebx507bio", "blank"],
    title: "teaches",
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
          type: "string",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["tecv532bio", "blank"],
    title: "teaches",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["legs673bio", "blank"],
    title: "learningResourceType",
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
          type: "string",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["lehr965bio", "blank"],
    title: "learningResourceType",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["tigr135bio", "blank"],
    title: "timeRequired",
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
    _id: ["tidq878bio", "blank"],
    title: "timeRequired",
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
    _id: ["tocp784bio", "blank"],
    title: "totalTime",
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
    _id: ["toav935bio", "blank"],
    title: "totalTime",
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
    _id: ["pecv812bio", "blank"],
    title: "performTime",
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
    _id: ["pebr524bio", "blank"],
    title: "performTime",
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
    _id: ["prdw663bio", "blank"],
    title: "prepTime",
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
    _id: ["prfx642bio", "blank"],
    title: "prepTime",
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
    _id: ["duhw715bio", "blank"],
    title: "duration",
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
    _id: ["duhr412bio", "blank"],
    title: "duration",
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
    _id: ["sueq726bio", "blank"],
    title: "superEvent",
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
    _id: ["sudx303bio", "blank"],
    title: "superEvent",
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
    _id: ["sugr863bio", "blank"],
    title: "subEvent",
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
    _id: ["subu677bio", "blank"],
    title: "subEvent",
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
    _id: ["rees893bio", "blank"],
    title: "recordedAt",
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
    _id: ["redx126bio", "blank"],
    title: "recordedAt",
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
    _id: ["coex962bio", "blank"],
    title: "contains",
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
          type: "string",
          format: "uri",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["cofs185bio", "blank"],
    title: "contains",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["lohx419bio", "blank"],
    title: "location",
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
          "@type": "PostalAddress",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "string",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["lofw986bio", "blank"],
    title: "location",
    color: "#097969",
    validation: {
      anyOf: [
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
    _id: ["itau860bio", "blank"],
    title: "itemLocation",
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
          "@type": "PostalAddress",
          type: "object",
          properties: {},
          required: [],
        },
        {
          type: "string",
        },
      ],
    },
    belongs_to: "bioschemas",
  },
  {
    _id: ["itaq599bio", "blank"],
    title: "itemLocation",
    color: "#097969",
    validation: {
      anyOf: [
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
];
