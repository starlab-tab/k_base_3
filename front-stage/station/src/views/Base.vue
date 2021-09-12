<template>
    <v-container fill-height fluid class="pa-0">
        <nav-bar></nav-bar>
        <v-fade-transition mode="out-in">
            <router-view></router-view>
        </v-fade-transition>
    </v-container>
</template>

<script>
    export default {
        mounted() {},
        components: {
            NavBar: () => import(`@/components/Global/NavBar.vue`)
        },
        data: () => ({}),
        computed: {},
        methods: {}
    }
</script>