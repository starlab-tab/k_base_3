<template>
    <div>
        <v-dialog v-model="shield" persistent max-width="0">
        </v-dialog>
        <v-dialog v-model="shield" hide-overlay persistent width="300">
            <v-card color="primary" dark class="pa-3 d-flex">
                <div style="width: inherit;" class="text-center">
                    <span>{{msg}}</span>
                    <v-progress-linear indeterminate color="secondary" class="mb-0"></v-progress-linear>
                </div>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                shield: false,
                msg: "Please stand by...",
            }
        },

        created() {
            this.$store.subscribe((mutation, state) => {
                if (mutation.type === "shield/show") {
                    this.msg = state.shield.msg
                    this.shield = state.shield.action
                }
            })
        }
    }
</script>

<style lang="scss" scoped>
    ::v-deep {
        .v-snack__wrapper {
            min-width: 18.75rem;
            .v-snack__content {
                font-size: 1rem;
                text-align: center;
                font-weight: 800;
                // padding: 1.5rem;
            }
            .v-snack__action  {
                display: none;
            }
        }
    }
</style>
