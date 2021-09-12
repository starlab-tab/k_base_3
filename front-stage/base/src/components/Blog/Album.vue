<template>
    <v-container fluid fill-height class="d-flex flex-column justify-space-between align-center">
        <div class="album-main d-flex justify-center pt-3">
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
                        >Album</span>
                        <v-text-field
                            v-else
                            v-model="search_text"
                            color="BlogPrimary"
                            @blur="search_bar_blur"
                            prepend-inner-icon="mdi-magnify"
                            @keydown.native.enter="initialize_search"
                            autofocus flat solo hide-details
                        ></v-text-field>
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
                <v-col cols="6" md="3"
                    v-for="item in desserts"
                    :key="item.album_name"
                >
                    <v-card
                        flat
                        rounded="lg"
                        class="album-card text-center"
                        color="367bf0"
                    >
                        <v-card-text
                            class="pb-3"
                        >
                            <router-link class="title" :to="{ name: 'BlogAlbumPost', params: { name: item.album_name } }"
                            >
                              {{ item.album_name | pure_content}}
                            </router-link>
                        </v-card-text>
                        <v-card-text
                            class="py-0 pb-1"
                        >
                            <router-link class="blog" :to="{ name: 'BlogPost', params: { id: item.post_id } }">
                              {{item.post_title | pure_content}}
                            </router-link>
                        </v-card-text>
                        <v-card-actions class="detail">
                            <ul class="d-flex justify-space-between pl-0">
                                <li class="text-start">
                                    <label>Latest</label>
                                    <p>{{item.latest | format_time}}</p>
                                </li>
                                <li>
                                    <label>Blogs</label>
                                    <p>{{item.post_num}}</p>
                                </li>
                            </ul>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
        </div>
        <div
            style="max-width: 100%; background: transparent; position: sticky; bottom: 8px;"
        >
            <v-pagination
                v-if="total_pages"
                v-model="current_page"
                class="mt-4 mb-1"
                :length="total_pages"
                color="BlogPrimary"
                @input="get_albums"
                :disabled="loading"
             ></v-pagination>
        </div>
    </v-container>
</template>

<script>
    export default {
        data: () => ({
            desserts: [],
            current_page: 1,
            total_pages: 0,
            show_intro: true,
            search_text: "",
            last_search: "",
            search_actived: false,
            no_data: false,
            loading: false
        }),
        created() {
            this.get_albums()
        },
        watch: {
            search_text(val) {
                if (val.length === 0 && this.search_actived) {
                    this.reset_search()
                    this.search_actived = false
                }
            }
        },
        filters: {
            format_time(val) {
                if (val) {
                    return val.substr(0,10)
                }else {
                    return '无限期搁置'
                }
            }
        },
        methods: {
            get_albums: function() {
                this.loading = true
                if (this.search_actived) {
                    this.search_album()
                }else {
                    this.$surf.blog.album.get().then(res => {
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
                    this.search_album()
                }
            },
            search_album: function() {
                this.loading = true
                this.$surf.blog.album.search({tracker: this.search_text, page: this.current_page}).then(res => {
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
                this.get_albums()
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
    
    .album-main {
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
                background: #fff;
                border-radius: 6px;
                box-shadow: 0 0 3px rgb(0 0 0 / 15%);
                color: $primary;
            }
            
            .album-card {
                // min-width: 10.625rem;
                border: 1px solid #c5d0d1;
                
                .title {
                    font-size: 1.2rem !important;
                    color: $primary !important;
                    word-break: break-word;
                    font-family: Quicksand,sans-serif;
                    text-decoration: none;
                    &:hover {
                      text-decoration: underline;
                    }
                }
                
                .blog {
                    min-height: 4.375rem;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    display: -webkit-box;
                    -webkit-line-clamp: 3;
                    -webkit-box-orient: vertical;
                    word-break: break-word;
                    font-family: Quicksand,sans-serif;
                    text-decoration: none;
                    color: unset;
                    &:hover {
                      text-decoration: underline;
                    }
                }
                
                .detail {
                    border-top: 1px solid #c5d0d1;
                    background-color: rgba(#c5d0d1, 0.1);
                    ul {
                        color: #3d5358;
                        width: 100%;
                        height: fit-content;
                        list-style: none;
                        label {
                            font-size: 0.8rem;
                        }
                        p {
                            font-size: 0.9rem;
                            margin: 0;
                        }
                    }
                }
            }
        }
    }
    
</style>
