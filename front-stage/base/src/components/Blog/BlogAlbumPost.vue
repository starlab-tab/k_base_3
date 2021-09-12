<template>
    <v-container white fill-height class="pt-6" justify-center align-start>
        <v-row class="justify-center">
            <v-col cols="12" class="pb-0 pt-3">
                <div class="intro">
                    <span
                        style="width: 100%" 
                        class="text-center"
                    >{{name}}</span>
                </div>
            </v-col>
            <v-col cols="12" class="pa-0"></v-col>
            <v-col cols="12" class="pa-0">
                <album-table
                    v-model="box"
                    @action="action"
                    ref="DataTable"
                    :noIntro="false"
                    :disableSort="false"
                    :search_bar="false"
                >
                    <template #title="{ item }">
                        <router-link
                            :to="{name: 'BlogPost', params: { id: item.id } }"
                            style="color: #367bf0;"
                        >
                            {{item.title | pure_content}}
                        </router-link>
                    </template>
                    <template #visible="{ item }">
                        <v-btn icon>
                            <v-icon
                                style="font-size: 20px;"
                                small
                                :color="item.visible ? '#06d6a0' : 'red'"
                            >
                                {{item.visible ? 'mdi-lock-open-variant-outline' : 'mdi-lock-outline'}}
                            </v-icon>
                        </v-btn>
                    </template>
                    <template #date="{ item }">
                        {{ item.created_at | format_time}}
                    </template>
                </album-table>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
    import { table } from "@/mixins/table.js"
    import Utils from '@/utils/utils.js'
    export default {
        mixins: [table],
        props: ['name'],
        data: () => ({
            box: {
                headers: [
                    {
                        text: 'Title',
                        align: 'start',
                        value: 'title',
                        sortable: false,
                        custom: true,
                    },
                    {
                        text: 'views',
                        value: 'views',
                        align: 'end',
                        
                    },
                    {
                        text: 'Visible',
                        value: 'visible',
                        align: 'end',
                        sortable: false,
                        custom: true,
                        
                    },
                    {
                        text: 'Date',
                        value: 'date',
                        align: 'end',
                        filterable: false,
                        sortable: false,
                        custom: true,
                    },
                ]
            }
        }),
        created() {
            this.box.name = this.name
        },
        filters: {
            format_time(val) {
                if (val) {
                    return val.replace(/T/g, ' ')
                }else {
                    return '无限期搁置'
                }
            }
        },
        methods: {
            action: function({data, type}) {
                if (type === "get") this.get(data)
                else if (type === "search") this.search(data)
                else return
            },
            get: function(data) {
                this.box.loading = true
                this.$surf.blog.album.posts(data).then(res => {
                    this.box.show_retry = false
                    this.box.desserts.push(...res.data.data)
                    this.box.next_page = res.data.next_page
                    Utils.scroll_to_bottom(this)
                }).catch(res => {
                    this.box.show_retry = true
                }).finally(result => {
                    this.box.loading = false
                })
            },
            search: function() {
                
            }
        }
    }
</script>

<style lang="scss" scoped>
    $primary: #367bf0;
    
    .row {
        max-width: 56% !important;
        
            
        @media only screen and (max-width: 768px) {
            max-width: 100% !important;
        }
        
        @media only screen and (max-width: 1024px) {
            max-width: 100% !important;
        }
        
        
        .intro {
            display: flex;
            align-items: center;
            font-weight: 800;
            font-size: 1.5rem;
            width: 100%;
            height: 50px;
            background: #fff;
            border-radius: 2px;
            // box-shadow: 0 0 3px rgb(0 0 0 / 15%);
            color: $primary;
            border-top: 2px solid #2f2f2f;
            border-bottom: 2px solid #2f2f2f;
        }
        
        .subhead {
            margin: 0 auto;
            text-transform: uppercase;
            border-bottom: 2px solid #2f2f2f;
            border-top: 2px solid #2f2f2f;
            font-weight: bold;
            font-size: 1.5rem;
            color: $primary;
        }
    }

</style>