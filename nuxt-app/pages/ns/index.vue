<template>
  <div
    class="d-flex justify-content-center align-items-center min-h-100 discoveryIntroBack alert-secondary"
  >
  <div class="col-sm-10 text-center">
    <h1 class="mainTextDark">Schema Viewer</h1>
    <p>Visualize and Register Your Own Schema</p>
    <div class="jumbotron grad-dark text-light text-left shadow">
      <h2>Get started:</h2>
      <SchemaViewerForm></SchemaViewerForm>
    </div>
  </div>
     
  </div>
</template>

<script>
export default {
  name: "SchemaViewerHome",
};
</script>
