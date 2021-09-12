<template>
    <v-container fluid justify-center fill-height class="pa-0">
        <v-data-table
            :headers="box.headers" 
            :items="box.desserts"
            :disable-sort="disableSort"
            class="dessert-table px-2 pb-2"
            :class="{'no-intro': noIntro}"
            :search="filter"
            hide-default-footer 
            :footer-props="{
                itemsPerPageOptions: [-1],
                itemsPerPageText: ''
            }"
            :loading="box.loading"
            loading-text="On The Way......"
        >
            <template v-slot:top>
                <div class="pa-2 table-input px-0">
                    <v-text-field
                        v-if="search_bar"
                        v-model="box.search" 
                        placeholder="Search" 
                        flat hide-details
                        color="SecPrimary"
                        :disabled="box.loading"
                        maxlength="32"
                        @keydown.native.enter="init_search"
                        solo-inverted
                    >
                        <template v-slot:prepend-inner>
                            <v-chip 
                                label link
                                color="SecPrimary white--text"
                            >
                                {{ box.name }}
                            </v-chip>
                        </template>
                    </v-text-field>
                    <v-text-field
                        v-model="filter" 
                        placeholder="Filter" 
                        flat solo solo-inverted hide-details
                        color="SecPrimary"
                        class="pt-2"
                    ></v-text-field>
                    <v-progress-linear
                        v-show="box.loading"
                        indeterminate
                        color="SecPrimary"
                        height="3"
                        class="mt-1"
                    ></v-progress-linear>
                </div>
            </template>
           <template
                v-for="(header, index) in custom_headers"
                v-slot:[`item.${header.value}`]="{ item }"
            >
                <slot :name="header.value" :item="item">
                </slot>
            </template>
            <template v-slot:footer v-if="box.next_page > 1">
                <v-btn
                    tile
                    block
                    depressed
                    color="SecSecondary"
                    :loading="box.loading"
                    :disabled="box.loading"
                    @click="load_more"
                    style="position: sticky;bottom: 0;background-color: transparent!important;"
                >
                    <v-icon color="SecPrimary">mdi-chevron-double-down</v-icon>
                </v-btn>
            </template>
            <template v-slot:no-data v-if="box.show_retry">
                 <v-btn
                     icon
                     color="SecPrimary"
                     :loading="box.loading"
                     :disabled="box.loading"
                     @click="get"
                     style="position: sticky;bottom: 0;background-color: transparent!important;"
                 >
                   <v-icon color="SecPrimary">mdi-refresh</v-icon>
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
            },
            search_bar: {
                type: Boolean,
                default() {
                    return true
                }
            },
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
                this.$emit("action", {data: {page: this.box.next_page, name: this.box.name}, type: "get"})
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

<style lang="scss" scoped>
    $SecPrimary: #367BF0;
    .dessert-table {
        width: inherit!important;
        @media only screen and (max-width: 768px) {
            ::v-deep {
                .v-data-footer {
                    justify-content: flex-start;
                    .v-data-footer__pagination {
                        margin-left: 0rem;
                    }
                }
            }
        }
        .table-input {
            position: sticky;
            top: 0rem;
            z-index: 20;
        }
        ::v-deep {
            .v-input__prepend-inner {
                margin-top: 0rem!important;
                align-self: center;
                padding-right: .5rem!important;
            }
            a {
                text-decoration: none;
            }
            tbody tr {
                font-weight: 700;
            }
            .v-data-table-header-mobile {
                display: none;
            }
            .v-data-table__wrapper {
                td {
                    text-transform: capitalize;
                }
            }
            .v-data-table__progress { 
                display: none;
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
