<template>
    <div>
         <!-- v-scroll="onScroll" -->
        <v-btn
            fab fixed bottom x-small right
            :color="btn_color"
            @click="toTop"
            style="margin-bottom: 144px;"
        >
            <v-icon small :color="iconColor" >mdi-arrow-up-drop-circle-outline</v-icon>
        </v-btn>
        <v-btn
            fab fixed bottom x-small right
            :color="btn_color" 
            @click="toMiddle"
            style="margin-bottom: 96px;"
        >
            <v-icon small :color="iconColor" >mdi-format-align-middle</v-icon>
        </v-btn>
        <v-btn
            fab fixed bottom x-small right
            :color="btn_color" 
            @click="toBottom"
            style="margin-bottom: 48px;"
        >
            <v-icon small :color="iconColor" >mdi-arrow-down-drop-circle-outline</v-icon>
        </v-btn>
    </div>
</template>

<script>
    export default {
        props: ['iconColor'],
        data: () => ({
            btn_color: 'transparent'            
        }),
        methods: {
            onScroll: function() {
              
            },
            toTop: function() {
                this.$vuetify.goTo(0)
            },
            toMiddle: function() {
                this.$vuetify.goTo(document.body.scrollHeight / 2)
            },
            toBottom: function() {
                this.$vuetify.goTo(document.body.scrollHeight)
            }
        }
    };
</script>

<style>
</style>
