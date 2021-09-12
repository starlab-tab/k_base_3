<template>
    <nav>
       <v-btn
            fab fixed bottom x-small right
            color="transparent"
            @click.stop="toggle_navbar"
            style="margin-bottom: 192px;"
        >
            <v-icon small color="SecPrimary">mdi-menu</v-icon>
        </v-btn>
        <v-navigation-drawer 
            v-model="drawer" 
            app :overlay-opacity="0.1" 
            class="elevation-0"
            style="background-color: #1e1e1e;"
        >
            <v-list nav dense dark>
              <div
                    class="text-center text-h5 pa-6" 
                    style="box-shadow: 0 5px 15px rgba(0,0,0,.07);"
                >
                    <router-link to="/" style="text-decoration: none;color: #367bf0;;">Sec</router-link>
                </div>
                <v-list-item-group color="SecPrimary" class="mt-4">
                    <v-text-field
                        v-model="search"
                        color="SecPrimary"
                        placeholder="Filter"
                        solo flat solo-inverted hide-details
                        class="pb-2"
                    >
                        
                    </v-text-field>
                    <v-list-item v-for="(dessert, i) in filteredItems" :key="i"
                        :to="{ name: 'SecArchiveAlbum', params: { name: dessert.name } }"
                    >
                        <v-list-item-icon>
                            <v-icon style="opacity: .3;" color="SecPrimary" x-small>mdi-circle</v-icon>
                        </v-list-item-icon>

                        <v-list-item-content>
                            <v-list-item-title v-text="dessert.name" class="font-weight-bold text-capitalize">
                            </v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list-item-group>
            </v-list>
        </v-navigation-drawer>
    </nav>
</template>

<script>
    export default {
        data: () => ({
            drawer: null,
            desserts: [{id: 0, name: "all"}],
            search: '',
        }),
        created() {
            this.$surf.sec.archive.album.get().then(res => {
                this.desserts.push(...res.data.data)
            }).catch(err => {
        
            })
        },
        computed: {
            toggle_navbar_icon: function() {
                return this.drawer ? 'mdi-chevron-double-left' : 'mdi-chevron-double-right';
            },
            filteredItems() {
                return this.desserts.filter((item) => {
                    return item.name.toLowerCase().match(this.search)
                })
            }
        },
        methods: {
            toggle_navbar() {
                this.drawer = !this.drawer
            },
        },
        components: {},
    }
</script>
