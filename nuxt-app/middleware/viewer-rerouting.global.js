import axios from "axios";

export default defineNuxtRouteMiddleware(async (to, from) => {
  const runtimeConfig = useRuntimeConfig();

  if (to.fullPath.includes("/view") && !to.fullPath.includes("/api")) {
    return navigateTo(to.fullPath.replace("/view", "/ns"));
  }
  if (to.path.includes("/dataset") && !to.fullPath.includes("/api")) {
    return navigateTo(to.path.replace("/dataset", "/resource"));
  }
  // Client-only storage logic
  if (!to.path.includes("/ns") && process.client) {
    localStorage.removeItem("user-schema-classes");
    localStorage.removeItem("user-schema-url");
    sessionStorage.clear();
    return;
  }
  // Check if user belongs to organization
  if (to.path.startsWith("/guide/nde")) {
    try {
      const response = await axios.post(
        runtimeConfig.public.apiUrl + "/org-check",
        {
          organization_name: "NIAID-Data-Ecosystem",
        }
      );

      if (response.data.success) {
        return; // Proceed normally
      } else {
        return navigateTo("/portal/nde", { replace: true });
      }
    } catch (error) {
      console.error("Error checking organization membership:", error);
      return navigateTo("/portal/nde", { replace: true });
    }
  }
});
