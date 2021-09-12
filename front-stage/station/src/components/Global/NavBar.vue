<template>
    <nav>
        <v-navigation-drawer 
            app
            permanent
            color="primary"
            expand-on-hover
        >   
            <v-list-item link class="py-6">
                <v-list-item-content>
                    <v-list-item-title class="title text-h5 font-weight-bold text-center text-uppercase"
                        style="color: #fbd300;">
                        MotherBase
                    </v-list-item-title>
                </v-list-item-content>
            </v-list-item>
            <nav-list :navs="navs" :sub="false"></nav-list>
            <template v-slot:append v-if="is_login">
                <v-list nav dense>
                    <v-list-item dark link @click="logout_dialog=true">
                        <v-list-item-icon>
                            <v-icon>mdi-logout mdi-rotate-180</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>
                            Logout
                        </v-list-item-title>
                    </v-list-item>
                </v-list>
            </template>
        </v-navigation-drawer>
        <v-dialog v-model="logout_dialog" max-width="300px">
            <v-card color="primary" dark>
                <v-card-title class="headline justify-center">Logout ? </v-card-title>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="grey" text @click="logout_dialog=false">Cancel</v-btn>
                    <v-btn color="secondary" text @click="logout">OK</v-btn>
                    <v-spacer></v-spacer>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </nav>
</template>

<script>
    import NavList from "./NavList";
    import Utils from "@/utils/utils.js";
    export default {
        data: () => ({
            mini: true,
            selectedItem: 0,
            is_mobile: false,
            is_login: false,
            logout_dialog: false,
            navs: [{
                    icon: 'mdi-view-dashboard-outline',
                    title: 'Dashbord',
                    to: {
                        name: "Dashbord"
                    }
                },
                {
                    title: 'Blog',
                    icon: 'mdi-blogger',
                    sub: [{
                            title: 'Post',
                            to: {
                                name: "BlogPost"
                            }
                        },
                        {
                            title: 'Album',
                            to: {
                                name: "BlogAlbum"
                            }
                        },
                    ],
                },
                {
                    icon: 'mdi-artstation',
                    title: 'Art',
                    to: {
                        name: "Art"
                    }
                },
                {
                    icon: 'mdi-television-classic',
                    title: 'Show',
                    to: {
                        name: "Show"
                    }
                },
                {
                    icon: 'mdi-security',
                    sub: [{
                            title: 'Archive',
                            icon: 'mdi-ticket',
                            sub: [{
                                    title: 'Paper',
                                    to: {
                                        name: "SecArchivePaper"
                                    }
                                },
                                {
                                    title: 'Album',
                                    to: {
                                        name: "SecArchiveAlbum"
                                    }
                                },
                                {
                                    title: 'Crawler',
                                    to: {
                                        name: "SecArchiveCrawler"
                                    }
                                },
                                {
                                    title: 'Manual',
                                    to: {
                                        name: "SecArchiveManual"
                                    }
                                },
                            ]
                        },
                        {
                            title: 'Vuln',
                            icon: 'mdi-shield-bug-outline',
                            to: {
                                name: "SecVuln"
                            }
                        },
                    ],
                    title: 'Sec',
                },
                {
                    icon: 'mdi-email-variant',
                    sub: [
                        {
                            title: 'Main',
                            to: {
                                name: "MessageMain"
                            }
                        },
                        {
                            title: 'Chat',
                            to: {
                                name: "Chat"
                            }
                        },
                        {
                            title: 'Email',
                            to: {
                                name: "Email"
                            }
                        },
                    ],
                    title: 'Message',
                },
            ],
        }),
        created() {
            this.is_login = localStorage.getItem('language') ? true : false
        },
        // watch: {
        //     '$vuetify.breakpoint.name': {
        //         handler(val) {
        //             this.is_mobile = Utils.is_mobile()
        //         },
        //         deep: true
        //     },
        // },
        computed: {

        },
        methods: {
            logout: function() {
                this.$surf.bridge.de_auth().then(res => {
                    let key = localStorage.getItem("language")
                    localStorage.removeItem('language')
                    localStorage.removeItem(key)
                    sessionStorage.setItem('is_editor_done', true)
                    this.$dialog.notify.success('Logout', {
                        position: 'top-right',
                        timeout: 2000
                    })
                    this.$router.replace({
                        name: 'Bridge'
                    })
                }).catch(err => {

                })
            },
        },
        components: {
            NavList
        }
    }
</script>

<style lang="scss" scoped>
</style>
