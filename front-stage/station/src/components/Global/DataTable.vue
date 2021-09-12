<template>
    <v-container fluid justify-center fill-height class="pa-0">
        <v-data-table
            dark
            :headers="box.headers" 
            :items="box.desserts"
            :disable-sort="disableSort"
            class="dessert-table"
            :class="{'no-intro': noIntro}"
            :search="filter"
            :footer-props="{
                itemsPerPageOptions: [30],
                itemsPerPageText: ''
            }"
            :loading="box.loading"
            loading-text="On The Way......"
        >
            <template v-slot:top>
                <v-row
                    class="table-input ma-0"
                >
                    <v-col cols="12" class="pb-0 ">
                        <v-text-field
                            v-model="box.search"
                            flat solo hide-details
                            background-color="transparent"
                            label="Tracker"
                            maxlength="32"
                            @keydown.native.enter="init_search"
                            color="primary"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="12" class="pb-0 ">
                        <v-text-field
                            v-model="filter"
                            flat solo hide-details
                            background-color="transparent"
                            label="Filter"
                        ></v-text-field>
                    </v-col>
                </v-row>
                <v-progress-linear
                    v-show="box.loading"
                    indeterminate
                    color="secondary"
                    height="2"
                ></v-progress-linear>
            </template>
            <template
                v-for="(header, index) in custom_headers"
                v-slot:[`item.${header.value}`]="{ item }"
            >
                <slot :name="header.value" :item="item">
                </slot>
            </template>
           <template v-slot:body.append v-if="box.next_page && !box.show_retry">
                <span></span>
            </template>
            <template v-slot:footer v-if="box.next_page > 1">
                <v-btn
                    tile
                    block
                    depressed
                    color="primary"
                    :loading="box.loading"
                    :disabled="box.loading"
                    @click="load_more"
                >
                    <v-icon color="secondary">mdi-chevron-double-down</v-icon>
                </v-btn>
            </template>
            <template v-slot:no-data v-if="box.show_retry">
                 <v-btn
                     icon
                     color="primary"
                     :loading="box.loading"
                     :disabled="box.loading"
                     @click="get"
                 >
                   <v-icon color="secondary">mdi-refresh</v-icon>
                 </v-btn>
            </template>
        </v-data-table>
    </v-container>
</template>

<script>
    export default {
        props: {
            box: {
                type: Object,
                default() {
                    return {}
                }
            },
            disableSort: {
                type: Boolean,
                default() {
                    return true
                }
            },
            noIntro: {
                type: Boolean,
                default() {
                    return true
                }
            }
        },
        model: {
            prop: 'box',
            event: '_box'
        },
        data: () => ({
            filter: "",
        }),
        watch: {
            'box.search': {
                handler(val) {
                    if (val.length === 0 && this.box.search_actived) {
                        this.reset()
                        this.get()
                        this.box.search_actived = false
                    }
                },
                deep: true
            },
        },
        computed: {
            custom_headers: function() {
                return this.box.headers.filter((header) => {
                    return header.custom
                })
            }
        },
        methods: {
            get: function() {
                if (!this.box.next_page) return
                this.$emit("action", {data: this.box.next_page, type: "get"})
            },
            search: function() {
                if (this.box.search.length <= 0 || !this.box.next_page) return
                this.box.search_actived = true
                this.$emit("action", {data: {
                    'page': this.box.next_page,
                    'tracker': this.box.search
                }, type: "search"})
            },
            load_more: function() {
                if (!this.box.search_actived) this.get()
                else this.search()
            },
            init_search: function() {
                this.box.search = this.box.search.trim()
                if (this.box.search.length <= 0 || this.box.search === this.box.last_search) return
                this.box.last_search = this.box.search
                this.reset()
                this.search()
            },
            reset: function() {
                this.box.last_search = ""
                this.box.next_page = 1
                this.box.desserts.length = 0
            },
        }
    }
</script>

<style scoped lang="scss">
    .dessert-table {
        width: 50%;
        align-self: start;
        background-color: transparent !important;
        @media only screen and (max-width: 768px) {
            border-radius: 0rem;
            width: 100%!important;
            margin-top: 0rem!important;
        }
        .table-input {
            position: sticky;
            top: 0rem;
            border-bottom: thin solid rgba(255, 255, 255, 0.12);
            z-index: 100;
        }
        ::v-deep {
            a {
                color: white;
                text-decoration: none;
                &:hover {
                    transition: .3s;
                    color: #fbd300;
                    .v-icon {
                        transition: .3s;
                        color: #fbd300;
                    }
                }
            }
            .v-input__slot {
                padding: 0 !important;
            }
            .v-data-table-header-mobile {
                display: none;
            }
            .v-data-table__wrapper {
                td {
                    text-transform: capitalize;
                }
            }
            .v-data-footer {
                position: sticky;
                bottom: 0rem;
            }
        }
    }
    .no-intro {
        ::v-deep {
            .v-data-table-header {
                display: none;
            }
        }
    }
</style>
