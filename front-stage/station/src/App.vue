<template>
    <v-app>
        <shield></shield>
        <v-main>
            <v-fade-transition mode="out-in">
                <router-view></router-view>
            </v-fade-transition>
        </v-main>
    </v-app>

</template>

<script>
    export default {
        components: {
            Shield: () => import("@/components/Global/Shield.vue")
        },
    }
</script>

<style>
    .v-application {
        background-color: #1f4a40 !important;
    }
    .v-application code {
        background-color: unset !important;
        padding: 0rem !important;
    }
</style>
