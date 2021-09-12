<template>
    <v-container fluid fill-height class="d-flex flex-column justify-space-between align-center">
        <div class="post-main d-flex justify-center pt-3">
            <v-row>
                <v-col
                    cols="12"
                    style="position: sticky; top: 0; background: transparent;z-index: 5;"
                >
                    <div class="intro">
                        <span
                            v-if="show_intro"
                            style="width: 100%" 
                            class="text-center"
                            @click="show_intro=!show_intro"
                        >Latest</span>
                        <v-text-field
                            v-else
                            v-model="search_text"
                            color="BlogPrimary"
                            @blur="search_bar_blur"
                            prepend-inner-icon="mdi-magnify"
                            @keydown.native.enter="initialize_search"
                            autofocus flat solo hide-details
                        ></v-text-field>
                        <!--  -->
                    </div>
                </v-col>
                <v-progress-linear
                    v-show="loading"
                    indeterminate
                    color="SecPrimary"
                    height="3"
                    class="mx-3"
                ></v-progress-linear>
                <v-col cols="12" class="text-center" v-if="no_data">
                    <span style="color:#BDBDBD;">no data...</span>
                </v-col>
                <v-col cols="12" class="py-0">
                    <v-card
                        flat
                        v-for="item in desserts"
                        :key="item.id"
                        class="mt-4 post-card"
                        :style="{borderLeft: item.visible ? '' : '4px solid #fb7373'}"
                    >
                        <div class="px-4">
                             <v-chip
                                 label
                                 v-for="(album, index) in item.albums"
                                 :key="index"
                                 class="mr-2 mt-2"
                                 text-color="BlogPrimary"
                                 :to="{name: 'BlogAlbumPost', params: {name: album.name}}"
                                 style="background-color: #f0f8ff !important; text-transform: capitalize;"
                             >
                                 {{album.name | pure_content}}
                             </v-chip>
                         </div>
                        <v-card-text class="pb-0">
                            <span>{{item.created_at | format_time}}</span>
                            <span class="d-flex align-center" style="position: absolute; right: 12px;top:14px">
                                <span style="font-size: 12px;">{{item.views}}</span>
                                <v-icon small class="pl-2">mdi-glasses</v-icon>
                            </span>
                        </v-card-text>
                        <v-card-title class="py-1">
                            <router-link :to="{ name: 'BlogPost', params: { id: item.id } }">
                                {{item.title | pure_content}}
                            </router-link>
                        </v-card-title>
                        <v-card-text class="post-card__desc py-0">
                            {{item.desc | pure_content}}
                        </v-card-text>
                        <div class="px-4">
                            <v-chip
                                v-for="(chip, index) in item.chips"
                                :key="index"
                                class="mr-2 mb-2 post-card__chip"
                            >
                                {{chip | pure_content}}
                            </v-chip>
                        </div>
                    </v-card>
                </v-col>
            </v-row>
        </div>
        <div style="max-width: 100%; background: transparent; position: sticky; bottom: 8px;">
            <v-pagination
                v-if="total_pages"
                v-model="current_page"
                class="mt-4 mb-1"
                :length="total_pages"
                color="BlogPrimary"
                @input="get_blogs"
                :disabled="loading"
             ></v-pagination>
        </div>
    </v-container>
</template>

<script>
    import DOMPurify from 'dompurify'
    export default {
        created() {
            this.get_blogs()
        },
        data() {
            return {
                desserts: [],
                current_page: 1,
                total_pages: 0,
                show_intro: true,
                search_text: "",
                last_search: "",
                search_actived: false,
                loading: false,
                no_data: false
            }
        },
        watch: {
            search_text(val) {
                if (val.length === 0 && this.search_actived) {
                    this.reset_search()
                    this.search_actived = false
                }
            }
        },
        methods: {
            get_blogs: function() {
                this.loading = true
                if (this.search_actived) {
                    this.search_post()
                }else {
                    this.$surf.blog.post.get(this.current_page).then(res => {
                        this.desserts = res.data.data
                        this.total_pages = res.data.total_pages
                        if (res.data.data.length > 0) this.no_data = false
                        else this.no_data = true
                    }).catch(err => {
                        
                    }).finally(result => {
                        this.loading = false
                    })
                }

            },
            initialize_search: function() {
                this.search_text = this.search_text.trim()
                if (this.search_text.length > 0 && this.last_search !== this.search_text) {
                    this.total_pages = 0
                    this.current_page = 1
                    this.search_post()
                }
            },
            search_post: function() {
                this.loading = true
                this.$surf.blog.post.search({tracker: this.search_text, page: this.current_page}).then(res => {
                    this.last_search = this.search_text
                    this.search_actived = true
                    this.desserts = res.data.data
                    this.total_pages = res.data.total_pages
                    if (res.data.data.length > 0) this.no_data = false
                    else this.no_data = true
                }).catch(err => {
                    
                }).finally(result => {
                    this.loading = false
                })
            },
            reset_search: function() {
                if (!this.search_actived) return
                this.total_pages = 0
                this.current_page = 1
                this.search_actived = false
                this.search_text = ''
                this.get_blogs()
            },
            search_bar_blur: function(e) {
                if (this.search_actived) return
                this.show_intro = true
            }
        }
    }
</script>

<style lang="scss" scoped>
    
    $primary: #367bf0;
    
    .post-main {
        width: 56% !important;
        
            
        @media only screen and (max-width: 768px) {
            width: 100% !important;
        }
        
        @media only screen and (max-width: 1024px) {
            width: 100% !important;
        }
        
        .row {
            .intro {
                display: flex;
                align-items: center;
                font-weight: 800;
                font-size: 1.5rem;
                width: 100%;
                height: 50px;
                border-radius: 6px;
                box-shadow: 0 0 3px rgb(0 0 0 / 15%);
                color: $primary;
            }
            .post-card {
                padding-bottom: 0.8rem;
                box-shadow: 0 5px 30px rgba(0,0,0,7%)!important;
                .v-card__title {
                    a {
                        text-decoration: none;
                        font-weight: 600;
                        color: $primary;
                    }
                }
                
                &__desc {
                    overflow: hidden;
                    text-overflow: ellipsis;
                    display: -webkit-box;
                    -webkit-line-clamp: 3;
                    -webkit-box-orient: vertical;
                    word-break: break-word;
                    font-family: Quicksand,sans-serif;
                }
                
                &__chip {
                    background-color: #f1f1f1;
                    color: #5a5757;
                }
            }
        }
    }
</style>
