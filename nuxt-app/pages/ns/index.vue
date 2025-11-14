<template>
  <div class="min-100 bg-light">
    <PageTitle
      title="Schema Viewer"
      subtitle="Visualize and Register Your Own Schema"
    ></PageTitle>
    <div class="d-flex justify-content-center align-items-center mt-5">
      <div class="col-sm-10 text-center">
        <div class="jumbotron grad-dark text-light text-left shadow">
          <h2>Get started:</h2>
          <SchemaViewerForm></SchemaViewerForm>
        </div>
      </div>
       
    </div>
  </div>
</template>

<script>
export default {
  name: "SchemaViewerHome",
};
</script>
