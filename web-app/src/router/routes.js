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
