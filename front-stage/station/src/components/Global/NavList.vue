<template>
    <v-list 
        nav dense dark
        :class="sub ? 'pa-0' : ''"
    >
        <div
            v-for="nav in navs"
            :key="nav.title"
            class="pt-2"
        >
            <v-list-group
                v-if="nav.sub"
                no-action
                color="#fbd300"
				
            >
                <template v-slot:activator>
                    <v-list-item-icon>
                        <v-icon>{{ nav.icon }}</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                        <v-list-item-title v-text="nav.title"></v-list-item-title>
                    </v-list-item-content>
                </template>
                <nav-list :navs="nav.sub" :sub="true"></nav-list>
            </v-list-group>
            <v-list-item 
                v-else
                :to="nav.to"
                color="#fbd300"
            >
                <v-list-item-icon>
                    <v-icon>{{ nav.icon ? nav.icon : "mdi-circle-small" }}</v-icon>
                </v-list-item-icon>
                <v-list-item-title v-text="nav.title"></v-list-item-title>
            </v-list-item>
        </div>
    </v-list>
</template>

<script>
    export default {
        name: "NavList",
        props: {
            navs: {
                type: Array,
                default: []
            },
            sub: {
                type: Boolean,
                default: false
            }
        },
    };
</script>

<style scoped lang="scss">
    .substyle {
        padding: 0rem !important;
    }
</style>
