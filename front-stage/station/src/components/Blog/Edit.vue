<template>
    <editor 
        v-model="box"
        ref="Editor"
        @del="del"
        @done="done"
        @handle_upload_image="handle_upload_image"
        @als_image="als_image"
    >
    </editor>
</template>

<script>
    import { blog_editor } from "@/mixins/blog.js"
    import Utils from '@/utils/utils.js'
    export default {
        mixins: [blog_editor],
        methods: {
            del: async function() {
                if (
                    await this.$dialog.warning({
                        text: `Delete Blog ${this.box.dessert.title} ?`,
                        title: '',
                    })
                ) {
                    this.$shield.up()
                    this.$surf.blog.post.delete(this.id).then(res => {
                        if (res.status === 204) {
                            this.$dialog.notify.success('done', {
                                position: 'top-right',
                                timeout: 2000
                            })
                            this.$router.replace({name: 'BlogPost'})
                        }
                    }).catch(err => {
                    }).finally(result => {
                        this.$shield.down()
                    })
                }
            },
            done: function() {
                let data = Utils.get_update_map(this.box.base_dessert, this.box.dessert)
                if (!data) return
                data.id = this.box.base_dessert.id
                if (this.box.dessert.visible) {
                    delete data.protection
                }else {
                    data.protection = this.box.dessert.protection
                }
                this.box.loading = true
                this.$surf.blog.post.update(data).then(res => {
                    this.box.base_dessert = {...this.box.dessert}
                    this.$dialog.notify.success('done', {
                        position: 'top-right',
                        timeout: 2000
                    })
                }).catch(err => {
                }).finally(result => {
                    this.box.loading = false
                    this.$shield.down()
                })
            },
        },
    }
</script>