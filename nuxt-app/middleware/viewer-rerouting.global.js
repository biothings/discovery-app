export default defineNuxtRouteMiddleware((to, from) => {
  if (to.fullPath.includes("/view") && !to.fullPath.includes("/api")) {
    return navigateTo(to.fullPath.replace("/view", "/ns"));
  }
  if (to.path.includes("/dataset") && !to.fullPath.includes("/api")) {
    return navigateTo(to.path.replace("/dataset", "/resource"));
  }
});
