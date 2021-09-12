<template>
    <v-container fluid align-self-start class="pa-0">
        <v-row class="justify-center ma-0">
            <v-col cols="12"
                style="background:#fbd300; height:160px;" 
                class="d-flex justify-center align-center px-0"
            >
                <h1 style="color: #1f4a40" class="text-center">
                    BlogPost
                    <v-btn icon x-large color="primary" :to="{name: 'BlogCreate'}">
                        <v-icon x-large>mdi-plus-circle</v-icon>
                    </v-btn>
                </h1>
            </v-col>
            <v-col cols="12" class="px-0">
                <data-table
                    v-model="box"
                    @action="action"
                    ref="DataTable"
                >
                    <template #title="{ item }">
                        <router-link
                            :to="{name: 'BlogEdit', params: { id: item.id } }"
                        >
                            {{item.title}}
                        </router-link>
                    </template>
                    <template #visible="{ item }">
                        <div class="font-weight-bold">
                            <v-icon small :color="item.visible ? '#06d6a0' : '#367BF0'">
                                mdi-circle-medium
                            </v-icon>
                            <span
                                :style="{color: item.visible ? '#06d6a0' : '#367BF0'}"
                            >
                                {{item.visible ? 'Open' : 'Protected'}}
                            </span>
                        </div>
                    </template>
                </data-table>
            </v-col>
        </v-row>
    </v-container>
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
                        custom: true,
                        value: 'title',
                    },
                    {
                        text: 'Views',
                        value: 'views',
                        align: 'end',
                        filterable: false,
                    },
                    {
                        text: 'Visible',
                        value: 'visible',
                        align: 'end',
                        custom: true,
                        filterable: false,
                    },
                ],
            }
        }),
        methods: {
            action: function({data, type}) {
                this.box.loading = true
                this.$surf.blog.post[type](data).then(res => {
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