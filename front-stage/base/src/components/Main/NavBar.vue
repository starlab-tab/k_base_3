<template>
  <nav>
   <v-navigation-drawer
      v-model="drawer"
      expand-on-hover
      permanent
      app
      :overlay-opacity="0.1"
      class="elevation-0"
      style="background-color:#f9f7f1"
    >
      <template v-slot:append>
          <v-list nav dense>
              <v-list-item v-for="(station, index) in space" :key="index" :to="station.route">
                <v-list-item-icon>
                  <v-icon :color="station.color">{{ station.icon }}</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title class="text-capitalize">{{ station.title }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
          </v-list>
      </template>
    </v-navigation-drawer>
    <Seek :space="space" ref="callSeek"/>
  </nav>
</template>
<script>
  import Seek from '@/components/Seek.vue'
  
  export default {
    data() {
      return {
        space: [
          {icon: "mdi-home-flood", title: "knowbase", color: "indigo", route: "/"},
          {icon: "mdi-blogger", title: "blog", color: "brown", route: "/blog"},
          {icon: "mdi-shield", title: "sec", color: "#367BF0", route: "/sec"},
          {icon: "mdi-movie-open", title: "show", color: "black", route: "/show"},
          {icon: "mdi-music-note", title: "music", color: "yellow lighten-1", route: "/musiclub"},
          {icon: "mdi-image-size-select-actual", title: "art", color: "teal darken-2", route: "/artlab"},
          {icon: "mdi-card-account-details-star", title: "about", color: "red", route: "/about"},
          {icon: "mdi-message-plus", title: "message", color: "purple", route: "/message"},
          // {icon: "mdi-magnify", title: "Search", color: "#1f1d2b", route: "/sec"},
          // {icon: "", title: "", color: "", route: ""},
          // {icon: "", title: "", color: "", route: ""},
          // {icon: "", title: "", color: "", route: ""}
        ],
        drawer: false,
        group: null
      }
    },
    components: {
      Seek
    },
    watch: {
      group () {
        this.drawer = false
      },
    },
    methods: {
      callSeek: function() {
        this.$refs.callSeek.callSeek()
      }
    }
  }
</script>

<style>
</style>
