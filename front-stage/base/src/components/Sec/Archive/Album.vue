<template>
    <album-table
        v-model="box"
        @action="action"
        ref="DataTable"
        class="align-start"
    >
        <template #title="{ item }">
            <router-link
                :to="{name: 'SecArchivePaper', params: { id: item.pf_id } }"
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
        <template #portal="{ item }">
            <a target="_blank" :href="item.pf_url | pure_content">
                <v-btn icon>
                    <v-icon
                        small
                        class="mdi-rotate-315"
                        color="SecPrimary"
                    >
                        mdi-send
                    </v-icon>
                </v-btn>
            </a>
        </template>
    </album-table>
</template>

<script>
    import { table } from "@/mixins/table.js"
    import Utils from '@/utils/utils.js'
    export default {
        mixins: [table],
        'props': ['name'],
        data: () => ({
            box: {
                headers: [
                    {
                        text: 'Title',
                        align: 'start',
                        value: 'title',
                        custom: true,
                    },
                    {
                        text: 'Author',
                        value: 'author'
                    },
                    {
                        text: 'Platform',
                        value: 'pf_name'
                    },
                    {
                        text: 'Visible',
                        value: 'visible',
                        custom: true,
                        
                    },
                    {
                        text: 'Portal',
                        value: 'portal',
                        filterable: false,
                        custom: true,
                    },
                    {
                        text: 'Date',
                        value: 'date',
                        filterable: false
                    },
                ]
            }
        }),
        created() {
            this.box.name = this.name
        },
        methods: {
            action: function({data, type}) {
                if (type === "get") this.get(data)
                else if (type === "search") this.search(data)
                else return
            },
            get: function(data) {
                this.box.loading = true
                this.$surf.sec.archive.album.papers(data).then(res => {
                    this.box.show_retry = false
                    this.box.desserts.push(...res.data.data)
                    this.box.next_page = res.data.next_page
                    Utils.scroll_to_bottom(this)
                }).catch(err => {
                    this.box.show_retry = true
                }).finally(result => {
                    this.box.loading = false
                })
            },
            search: function(data) {
                this.box.loading = true
                data.name = this.box.name
                this.$surf.sec.archive.paper.search(data).then(res => {
                    this.box.show_retry = false
                    this.box.desserts.push(...res.data.data)
                    this.box.next_page = res.data.next_page
                    Utils.scroll_to_bottom(this)
                }).catch(err => {
                    console.log(err)
                    this.box.show_retry = true
                }).finally(result => {
                    this.box.loading = false
                })
            },
        }
    }
</script>

<style lang="scss" scoped>
    ::v-deep {
        .dessert-table {
            max-width: 80%!important;
            align-self: start;
            box-shadow: 0 5px 15px rgba(0,0,0,.07);
            margin-top: 2rem!important;
            @media only screen and (max-width: 768px) {
                max-width: 100%!important;
                margin-top: 0rem!important;
            }
        }
    }
</style>