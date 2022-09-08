import HomeView from "../views/HomeView.vue";

export const routes = [
  {
    path: "/",
    name: "Home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (About.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import("../views/About.vue"),
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: () => import("../views/Dashboard.vue"),
  },
  {
    path: "/faq/:portal?",
    name: "FAQ",
    props: true,
    component: () => import("../views/FAQ.vue"),
  },
  {
    path: "/contributor/:username?",
    name: "Contributor",
    props: true,
    component: () => import("../views/Contributor.vue"),
  },
  {
    // NIAID specific, schema.org compatibility portals
    path: "/compatibility",
    name: "Compatibility",
    component: () => import("../views/Compatibility.vue"),
  },
  {
    path: "/best-practices",
    name: "BestPractices",
    component: () => import("../views/BestPractices.vue"),
  },
  {
    path: "/schema-playground",
    name: "SchemaPlayground",
    component: () => import("../views/SchemaPlayground.vue"),
  },
  {
    // internal testing tool for JSON Schema Validation
    path: "/json-schema-viewer",
    name: "JSONSchemaViewer",
    component: () => import("../views/JSONSchemaViewer.vue"),
  },
  {
    path: "/registries",
    name: "Registries",
    component: () => import("../views/Registries.vue"),
  },
  {
    path: "/portal",
    name: "Portals",
    component: () => import("../views/Portals.vue"),
  },
  {
    path: "/portal/:portal_name",
    name: "Portal",
    props: true,
    component: () => import("../views/Portal.vue"),
  },
  {
    path: "/resource",
    name: "ResourceRegistry",
    component: () => import("../views/ResourceRegistry.vue"),
  },
  {
    path: "/resource/:id",
    name: "Resource",
    props: true,
    component: () => import("../views/Resource.vue"),
  },
  {
    path: "/dataset",
    name: "DatasetRegistry",
    redirect: (to) => {
      return { name: "ResourceRegistry" };
    },
  },
  {
    path: "/dataset/:id",
    name: "Dataset",
    redirect: (to) => {
      // the function receives the target route as the argument
      // we return a redirect path/location here.
      return { path: "/resource/" + to.params.id };
    },
  },
  {
    path: "/guide/niaid/:guide_query?",
    name: "GuideNIAID",
    props: true,
    meta: {
      presets: [
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
      ],
    },
    component: () => import("../views/Guide.vue"),
  },
  {
    path: "/guide/outbreak/:guide_query?",
    name: "GuideOutbreak",
    props: true,
    meta: {
      presets: [
        {
          namespace: "outbreak",
          prefix: "outbreak",
          name: "Dataset",
          guide: "/guide/outbreak/dataset",
          description:
            "This is the schema for describing the Dataset schema used for outbreak.info.",
        },
      ],
    },
    component: () => import("../views/Guide.vue"),
  },
  {
    path: "/guide/n3c/:guide_query?",
    name: "GuideN3C",
    props: true,
    meta: {
      presets: [
        {
          namespace: "n3c",
          prefix: "n3c",
          name: "Dataset",
          guide: "/guide/n3c/dataset",
          description:
            "This is the schema for describing the Dataset schema used for N3C.",
        },
      ],
    },
    component: () => import("../views/Guide.vue"),
  },
  {
    path: "/guide/:guide_query?",
    name: "GuideHome",
    props: true,
    meta: {
      presets: [
        {
          namespace: "biomedical",
          prefix: "bts",
          name: "BioMedicalDataset",
          guide: "/guide",
          description: "A schema describing a BioMedical Dataset",
        },
      ],
    },
    component: () => import("../views/Guide.vue"),
  },
  {
    path: "/editor",
    name: "SchemaEditor",
    component: () => import("../views/Editor.vue"),
  },
  {
    path: "/registry",
    name: "SchemaRegistry",
    component: () => import("../views/SchemaRegistry.vue"),
  },
  {
    path: "/view/:namespace?/:query?",
    name: "SchemaViewer",
    props: true,
    component: () => import("../views/SchemaViewer.vue"),
  },
  {
    path: "/:catchAll(.*)",
    name: "NotFound",
    component: () => import("../views/NotFound.vue"),
    meta: { sitemap: { ignoreRoute: true } },
  },
];
