<template>
    <v-container justify-center align-start fluid fill-height style="background-color:#f9f7f1">
        <!-- https://codepen.io/silkine/pen/jldif -->
        <div class="head">
            <header class="text-h2">
                KNOWBASE
            </header>
            <div class="subhead text-h6 text-capitalize">To Know More, To Be Stronger And Wiser, To Explore.</div>
        </div>
    </v-container>
</template>

<script>
    export default {
        data() {
            return {

            }
        },
        components: {

        },
        methods: {

        }
    }
</script>

<style lang="scss" scoped>
    .head {
        text-align: center;
        position: relative;
        width: inherit;

        header {
            font-family: 'Playfair Display', serif;
            font-weight: 700;
            margin-bottom: 20px;
        }

        .subhead {
            text-transform: uppercase;
            border-bottom: 2px solid #2f2f2f;
            border-top: 2px solid #2f2f2f;
            padding: 12px 0 12px 0;
        }
    }
</style>
