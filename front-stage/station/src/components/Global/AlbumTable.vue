<template>
    <v-container fluid fill-height justify-center class="pa-0">
        <data-table
            v-model="box"
            :disableSort="false"
            :noIntro="false"
            @action="action"
            class="albums-table"
        >
            <template #actions="{ item }">
                <v-icon small class="mr-2" @click="edit_item(item)">
                    mdi-pencil
                </v-icon>
                <v-icon small @click="delete_item(item)">
                    mdi-delete
                </v-icon>
            </template>
        </data-table>
        <v-dialog v-model="box.show_edit_dlg" max-width="360px">
            <v-card dark color="primary">
                <v-card-title>
                    <span class="headline" style="color:#fbd300">Edit</span>
                </v-card-title>
                <v-card-text class="py-0">
                        <v-row>
                            <v-col cols="12" class="py-0">
                                <v-text-field 
                                    v-model="box.edited_item.name"
                                    @keydown.native.enter="update"
                                    autofocus
                                ></v-text-field>
                            </v-col>
                        </v-row>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="grey" class="text-capitalize" text @click="box.show_edit_dlg = false" :disabled="box.loading">
                        Cancel
                    </v-btn>
                    <v-btn color="secondary" class="text-capitalize" text @click="update" :loading="box.loading">
                        Update
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog v-model="box.show_del_dlg" max-width="360px">
            <v-card color="primary" dark>
                <v-card-title class="headline justify-center text-capitalize">Confirm Delete {{box.edited_item.name}}?</v-card-title>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="grey" text @click="box.show_del_dlg=false">Cancel</v-btn>
                    <v-btn color="secondary" text @click="del">OK</v-btn>
                    <v-spacer></v-spacer>
                </v-card-actions>
            </v-card>
        </v-dialog>
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
        },
        model: {
            prop: 'box',
            event: '_box'
        },
        data: () => ({

        }),
        created() {
            this.action({data: this.box.next_page, type: "get"})
        },
        components: {
            DataTable: () => import(`@/components/Global/DataTable.vue`),
        },
        methods: {
            action: function(pkage) {
                this.box.loading = true
                this.$emit("action", pkage)
            },
            del: function() {
                if (!this.box.desserts[this.box.edited_index]) {
                    this.box.show_del_dlg = false
                }else {
                    this.$shield.up()
                    this.$emit("del", this.box.desserts[this.box.edited_index].id)
                }
            },
            update: function() {
                let item = this.box.desserts[this.box.edited_index]
                let new_name = this.box.edited_item.name
                if (!(item.name === new_name)) {
                    this.$shield.up()
                    this.$emit("update", {id: item.id, album_name: new_name})
                }
            },
            edit_item: function(item) {
                this.box.edited_index = this.box.desserts.indexOf(item)
                this.box.edited_item = Object.assign({}, item)
                this.box.show_edit_dlg = true
            },
            delete_item: function(item) {
                this.box.edited_index = this.box.desserts.indexOf(item)
                this.box.edited_item = Object.assign({}, item)
                this.box.show_del_dlg = true
            },
        }
    }
</script>