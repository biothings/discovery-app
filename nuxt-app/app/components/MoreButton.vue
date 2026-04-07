<template>
  <svg
    version="1.1"
    id="more_svg"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    x="0px"
    y="0px"
    viewBox="0 0 1220.9 768"
    style="enable-background: new 0 0 1220.9 768"
    xml:space="preserve"
  >
    <path
      id="yellow"
      class="st0"
      d="M663,425.2H557.9c-5.2,0-9.4-4.2-9.4-9.4v-63.5c0-5.2,4.2-9.4,9.4-9.4H663c5.2,0,9.4,4.2,9.4,9.4
  v63.5C672.4,420.9,668.2,425.2,663,425.2z"
    />
    <path
      id="purple"
      class="st1"
      d="M663,425.2H557.9c-5.2,0-9.4-4.2-9.4-9.4v-63.5c0-5.2,4.2-9.4,9.4-9.4H663c5.2,0,9.4,4.2,9.4,9.4
  v63.5C672.4,420.9,668.2,425.2,663,425.2z"
    />
    <path
      id="red"
      class="st2"
      d="M657.8,425.2h-94.8c-8,0-14.5-6.5-14.5-14.5v-53.2c0-8,6.5-14.5,14.5-14.5h94.8
  c8,0,14.5,6.5,14.5,14.5v53.2C672.4,418.6,665.9,425.2,657.8,425.2z"
    />
    <path
      id="pink"
      class="st3"
      d="M653.6,425.2h-86.3c-10.4,0-18.8-8.4-18.8-18.8v-44.8c0-10.4,8.4-18.8,18.8-18.8h86.3
  c10.4,0,18.8,8.4,18.8,18.8v44.8C672.5,416.7,664.1,425.2,653.6,425.2z"
    />
    <path
      id="green"
      class="st4"
      d="M660.4,425.2h-99.9c-6.6,0-12-5.4-12-12v-58.3c0-6.6,5.4-12,12-12h99.9c6.6,0,12,5.4,12,12v58.3
  C672.4,419.8,667.1,425.2,660.4,425.2z"
    />
    <path
      id="blue"
      class="st5"
      d="M655.6,425.2h-90.3c-9.3,0-16.8-7.5-16.8-16.8v-48.7c0-9.3,7.5-16.8,16.8-16.8h90.3
  c9.3,0,16.8,7.5,16.8,16.8v48.7C672.4,417.6,664.9,425.2,655.6,425.2z"
    />
    <polygon
      id="plus"
      class="st6"
      points="734.8,336.2 660.9,336.2 660.9,259.7 565.3,259.7 565.3,336.2 486.1,336.2 486.1,431.8 
  565.3,431.8 565.3,508.3 660.9,508.3 660.9,431.8 734.8,431.8 "
    />
  </svg>
</template>

<script>
export default {
  name: "MoreButton",
};
</script>

<style scoped>
.st0 {
  fill: #6d58c0;
}
.st1 {
  fill: #c084fc;
}
.st2 {
  fill: #d83f87;
}
.st3 {
  fill: #8265a7;
}
.st4 {
  fill: #a4b3b7;
}
.st5 {
  fill: #5e43cb;
}
.st6 {
  fill: #ffffff;
}
#more_svg:hover > #blue {
  transition: all 0.8s;
  transform: scale(1.4) translate(300px, 200px);
  transform-origin: center;
}
#more_svg:hover > #green {
  transition: all 0.8s;
  transform-origin: center;
  transform: translate(-350px, 100px);
}
#more_svg:hover > #red {
  transition: all 0.5s;
  transform-origin: center;
  transform: scale(3.4) translate(-100px, -40px);
}
#more_svg:hover > #yellow {
  transition: all 0.6s;
  transform-origin: center;
  transform: scale(2.5) translate(120px, -80px);
}
#more_svg:hover > #purple {
  transition: all 1s;
  transform-origin: center;
  transform: scale(1.5) translate(10px, 180px);
}
#more_svg:hover > #pink {
  transition: all 0.7s;
  transform-origin: center;
  transform: scale(1.7) translate(-150px, 130px);
}
</style>
