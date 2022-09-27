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
      <small>Go back to our <nuxt-link to="/">homepage</nuxt-link></small>
    </div>
  </div>
</template>

<script>
export default {
  name: "NotFound",
  head(){
    return {
      'title': "DDE | Not Found",
      'meta':[
      {
          'name': 'twitter:image',
          'content': 'https://i.postimg.cc/qq5MjpZv/ddefeatured.jpg'
        },
        {
          'property': 'og:image',
          'content': 'https://i.postimg.cc/qq5MjpZv/ddefeatured.jpg'
        },
        {
          'property': 'og:url',
          'content': 'http://discovery.biothings.io'
        },
        {
          'name': 'twitter:url',
          'content': 'http://discovery.biothings.io'
        },
        {
          'property': 'og:description',
          'content': 'A project to promote FAIR data-sharing best practices & maximize the research impact of CTSA hubs.'
        },
        {
          'name': 'description',
          'content': 'A project to promote FAIR data-sharing best practices & maximize the research impact of CTSA hubs.'
        },
        {
          'name': 'twitter:card',
          'content': 'A project to promote FAIR data-sharing best practices & maximize the research impact of CTSA hubs.'
        },
      ]
    }
  },
};
</script>
