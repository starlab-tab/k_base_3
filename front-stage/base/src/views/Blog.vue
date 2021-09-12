<template>
    <v-app>
        <side-bar></side-bar>
        <v-main>
            <auto-scroll icon-color="BlogPrimary"></auto-scroll>
            <v-scroll-x-reverse-transition mode="out-in">
                <router-view />
            </v-scroll-x-reverse-transition>
        </v-main>
    </v-app>
</template>

<script>
    import SideBar from '@/components/Blog/SideBar.vue'
    import AutoScroll from '@/components/AutoScroll.vue'
    export default {
        mounted() {},
        components: {

        },
        data: () => ({
        }),
        components: {
            SideBar,
            AutoScroll
        }
    }
</script>