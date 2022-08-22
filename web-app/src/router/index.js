import { createRouter, createWebHistory } from "vue-router";
import { routes } from "./routes.js";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  linkActiveClass: "route-active",
  scrollBehavior() {
    return { x: 0, y: 0 };
  },
  routes,
});

export default router;
