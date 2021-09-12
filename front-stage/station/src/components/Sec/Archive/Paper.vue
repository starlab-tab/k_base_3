<template>
    <data-table
        v-model="box"
        @action="action"
        ref="DataTable"
    >
        <template #title="{ item }">
            <router-link
                :to="{name: 'SecArchiveEdit', params: { id: item.id } }"
            >
                {{item.title}}
            </router-link>
        </template>
        <template #visible="{ item }">
            <div class="font-weight-bold">
                <v-icon small :color="item.visible ? '#06d6a0' : '#367BF0'">mdi-circle-medium
                </v-icon>
                <span
                    :style="{color: item.visible ? '#06d6a0' : '#367BF0'}">{{item.visible ? 'Open' : 'Protected'}}</span>
            </div>
        </template>
        <template #portal="{ item }">
            <a target="_blank" class="table-link" :href="item.pf_url">
              <v-icon
                small
                class="mr-2 mdi-rotate-315"
              >
                mdi-send
              </v-icon>
            </a>
        </template>
    </data-table>
</template>

<script>
    import { table } from "@/mixins/table.js"
    export default {
        mixins: [table],
        data: () => ({
            box: {
                headers: [
                    {
                        text: 'Title',
                        value: 'title',
                        custom: true,
                    },
                    {
                        text: 'Platform',
                        value: 'pf_name',
                    },
                    {
                        text: 'Visible',
                        value: 'visible',
                        custom: true,
                        filterable: false,
                    },
                    {
                        text: 'Date',
                        value: 'date',
                        filterable: false,
                    },
                    {
                        text: 'Portal',
                        value: 'portal',
                        custom: true,
                        filterable: false,
                    },
                ],
            }
        }),
        methods: {
            action: function({data, type}) {
                this.box.loading = true
                this.$surf.sec.archive.paper[type](data).then(res => {
                    this.box.desserts.push(...res.data.data)
                    this.box.next_page = res.data.next_page
                    this.box.show_retry = false
                }).catch(err => {
                    this.box.show_retry = true
                }).finally(result => {
                    this.box.loading = false
                })
            }
        }
    }
</script>
