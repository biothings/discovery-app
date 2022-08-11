<template>
  <header id="header">
  <title>Data Discovery Engine</title>
  <nav class="navbar navbar-expand-md navbar-light bg-light fixed-top">
    <a class="navbar-brand" href="/">
        <img src="@/assets/img/dde-logo-o.svg" width="30" height="30" alt="DDE" class="d-none d-md-inline">
        <i class="fas fa-home d-inline d-md-none mainTextDark"></i>
    </a>
    <a id="logo" class="navbar-brand caps logoText d-none d-md-inline logoFont" href="/">Data Discovery Engine</a>
    <button class="navbar-toggler alert-secondary" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
      <ul class="navbar-nav" id="user_link">
        <li class="nav-item headTip" data-tippy-content="Create discoverable metadata"><a class="nav-link h-link mainTextLight" href="/best-practices">Discovery Guide</a></li>
        <li class="nav-item"><a class="nav-link h-link mainTextDark headTip" href="/schema-playground" data-tippy-content="Create and Visualize a Schema">Schema Playground</a></li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="/portal" id="navbarDropdown" role="button" aria-haspopup="true" aria-expanded="false">
            Data Portals
          </a>
          <div class="dropdown-menu" aria-labelledby="navbarDropdown">
            <a class="dropdown-item" href="/portal/cd2h"><img src="@/assets/img/dde-logo-o.svg" width="20" height="20" alt="CTSA" title="CTSA Portal"> CD2H <i class="fas fa-chevron-right mainTextLight"></i></a>
            <a class="dropdown-item" href="/portal/n3c"><img src="@/assets/img/N3Co.png" width="20" height="20" alt="N3C" title="N3C"> N3C <i class="fas fa-chevron-right mainTextLight"></i></a>
            <a class="dropdown-item" href="/portal/outbreak"><img src="@/assets/img/outbreak.png" width="20" height="20" alt="Outbreak.info" title="Outbreak.info"> Outbreak.info <i class="fas fa-chevron-right mainTextLight"></i></a>
            <a class="dropdown-item" href="/portal/niaid"><img src="@/assets/img/niaid/icon.svg" width="20" height="20" alt="NIAID" title="NIAID Data Portal"> NIAID <i class="fas fa-chevron-right mainTextLight"></i></a>
          </div>
        </li>
        <li class="nav-item dropdown d-inline">
          <a class="nav-link dropdown-toggle" href="/registries" id="navbarDropdown" role="button" aria-haspopup="true" aria-expanded="false">
            Registry
          </a>
          <div class="dropdown-menu p-1" aria-labelledby="navbarDropdown" style="max-width:none;">
              <a class="dropdown-item mainTextLight text-left" href="/dataset">Metadata Registry <i class="fas fa-chevron-right"></i></a>
              <a class="dropdown-item mainTextDark text-left" href="/registry">Schema Registry <i class="fas fa-chevron-right"></i></a>
          </div>
        </li>
        <template v-if="userInfo && !userInfo.login">
          <li class='nav-item'><a class='nav-link' :href='"/login?next="+window.location.pathname'>Login</a></li>
        </template>
        <template v-if="userInfo && userInfo.login">
          <li class='nav-item'>
            <a class='nav-link pulse headTip' id='navPhotoLink' href='/dashboard/' data-tippy-content="Manage your contributions">
              <small v-text='userInfo.login'></small>
              <img v-if="!userInfo.avatar_url" id='navPhoto' class='userImage' src='@/assets/img/default.png' alt='user photo'>
              <img v-else id='navPhoto' class='userImage' :src='userInfo.avatar_url' alt='user photo'>
            </a>
          </li>
          <li class='nav-item'><a class='nav-link' :href='"/logout?next="+window.location.pathname'>Logout</a></li>
        </template>
      </ul>
    </div>
  </nav>
</header>
</template>

<script>
import axios from 'axios';

export default {
    name: 'Nav',
    data: function(){
				return {
          userInfo:{},
          window: window,
				}
			},
      methods:{
        checkUser(){
          let self = this;
          axios.get('/user').then(res=>{
            self.userInfo = res.data;
          }).catch(err=>{
            throw err;
          });
        },
    },
    mounted:function(){
      var self = this;
      self.checkUser();
      tippy( '.headTip', {
        placement:'bottom',
        theme:'light',
        sticky: true,
        animation: 'fade'});
    }
}
</script>