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
    path: "/faq/:portal?",
    name: "FAQ",
    props: true,
    component: () => import("../views/FAQ2.vue"),
  },
  {
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
    path: "/json-schema-viewer",
    name: "JSONSchemaViewer",
    component: () => import("../views/JSONSchemaViewer.vue"),
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
    path: "/:catchAll(.*)",
    name: "NotFound",
    component: () => import("../views/NotFound.vue"),
    meta: { sitemap: { ignoreRoute: true } },
  },
];
