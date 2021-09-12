<template>
    <v-container justify-center fluid fill-height class="pa-0">
        <nav-bar></nav-bar>
        <v-scroll-x-transition  mode="out-in">
            <router-view :key="$route.fullPath"></router-view>
        </v-scroll-x-transition>
    </v-container>
</template>

<script>
    import NavBar from '@/components/Sec/Archive/NavBar.vue'

    export default {
        components: {
            NavBar
        },
        data: () => ({}),
    }
</script>

<style>
</style>
