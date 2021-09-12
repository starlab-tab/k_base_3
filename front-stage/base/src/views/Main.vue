<template>
    <v-app>
        <nav-bar></nav-bar>
        <auto-scroll></auto-scroll>
        <v-main class="ma-0">
            <v-fade-transition mode="out-in">
                <router-view />
            </v-fade-transition>
        </v-main>
    </v-app>
</template>

<script>
    import NavBar from '@/components/Main/NavBar.vue'
    import AutoScroll from '@/components/AutoScroll.vue'

    export default {
        components: {
            NavBar,
            AutoScroll
        },
        data: () => ({

        }),
        methods: {

        }
    }
</script>

<style>
</style>
