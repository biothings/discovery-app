export default defineNuxtRouteMiddleware((to, from) => {
  if (to.fullPath.includes("/view") && !to.fullPath.includes("/api")) {
    return navigateTo(to.fullPath.replace("/view", "/ns"));
  }
  if (to.fullPath.includes("/dataset") && !to.fullPath.includes("/api")) {
    return navigateTo(to.fullPath.replace("/dataset", "/resource"));
  }
});
