<template>
    <v-app>
        <v-main>
            <auto-scroll icon-color="SecPrimary"></auto-scroll>
            <v-fade-transition mode="out-in">
                <router-view/>
            </v-fade-transition>
        </v-main>
    </v-app>
</template>

<script>
    import AutoScroll from '@/components/AutoScroll.vue'

    export default {
        mounted() {},
        components: {
            AutoScroll
        },
        data: () => ({}),
        computed: {},
        methods: {}
    }
</script>
