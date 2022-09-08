//Mapping to load any guide on /guide/ns?/cls?

export const presets = [
  {
    namespace: "biomedical",
    prefix: "bts",
    name: "BioMedicalDataset",
    guide: "/guide",
    description: "A schema describing a BioMedical Dataset",
  },
  {
    namespace: "n3c",
    prefix: "n3c",
    name: "Dataset",
    guide: "/guide/n3c/dataset",
    description:
      "This is the schema for describing the Dataset schema used for N3C.",
  },
  {
    namespace: "niaid",
    prefix: "niaid",
    name: "Dataset",
    guide: "/guide/niaid",
    description:
      "A schema describing a minimal Dataset for the National Institute of Allergy and Infectious Disease (NIAID). A dataset is a collection of data of a particular experimental type. Additional schema.org and/or custom properties could be added.",
  },
  {
    namespace: "niaid",
    prefix: "niaid",
    name: "ComputationalTool",
    guide: "/guide/niaid/ComputationalTool",
    description:
      "A schema describing a minimal ComputationalTool for the National Institute of Allergy and Infectious Disease (NIAID). A ComputationalTool is a software used for the collection, processing, distribution, analysis, visualization, interpretation, etc. of data. Additional schema.org and/or custom properties could be added.",
  },
  {
    namespace: "outbreak",
    prefix: "outbreak",
    name: "Dataset",
    guide: "/guide/outbreak/dataset",
    description:
      "This is the schema for describing the Dataset schema used for outbreak.info.",
  },
];
