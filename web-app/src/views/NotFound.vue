<template>
  <div
    id="404"
    class="container d-flex align-items-center"
    style="min-height: 100vh"
  >
    <div class="jumbotron bg-light text-center text-muted w-100">
      <h1 style="font-size: 5em">404</h1>
      <h4>Oops! Page Not Found</h4>
      <img
        class="m-2 w-50"
        src="@/assets/img/notfound.svg"
        alt="page not found"
      /><br />
      <small>Go back to our <a href="/">homepage</a></small>
    </div>
  </div>
</template>

<script>
export default {
  name: "NotFound",
};
</script>
