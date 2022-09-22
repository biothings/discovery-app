export default defineNuxtRouteMiddleware((to, from) => {
    if (to.fullPath.includes('/view')) {
        return navigateTo(to.fullPath.replace('/view', '/ns'))
    }
})