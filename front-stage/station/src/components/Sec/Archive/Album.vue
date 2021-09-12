<template>
    <album-table
        v-model="box"
        @action="action"
        @del="del"
        @update="update"
    ></album-table>
</template>

<script>
    import { albumtable } from "@/mixins/albumtable.js"
    export default {
        mixins: [albumtable],
        methods: {
            action: function({data, type}) {
                this.box.loading = true
                this.$surf.sec.archive.album[type](data).then(res => {
                    this.box.desserts.push(...res.data.data)
                    this.box.next_page = res.data.next_page
                    this.box.show_retry = false
                }).catch(err => {
                    this.box.show_retry = true
                }).finally(result => {
                    this.box.loading = false
                })
            },
            del: function(id) {
                this.$surf.sec.archive.album.delete(id).then(res => {
                    this.box.desserts.splice(this.box.edited_index, 1)
                    this.$dialog.notify.success('done', {
                        position: 'top-right',
                        timeout: 2000
                    })
                    this.box.show_del_dlg = false
                }).catch(err => {
                }).finally(result => {
                    this.$shield.down()
                })
            },
            update: function(data) {
                this.$surf.sec.archive.album.update(data).then(res => {
                    this.box.desserts[this.box.edited_index].name = data.album_name
                    this.$dialog.notify.success('done', {
                        position: 'top-right',
                        timeout: 2000
                    })
                    this.box.show_edit_dlg = false
                }).catch(err => {
                }).finally(result => {
                    this.$shield.down()
                })
            },
        }
    }
</script>