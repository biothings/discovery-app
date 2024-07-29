export default defineNuxtRouteMiddleware((to, from) => {
  if (to.fullPath.includes("/view") && !to.fullPath.includes("/api")) {
    return navigateTo(to.fullPath.replace("/view", "/ns"));
  }
  if (to.fullPath.includes("/resource") && !to.fullPath.includes("/api")) {
    return navigateTo(to.fullPath.replace("/resource", "/dataset"));
  }
});
