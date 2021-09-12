<template>
    <editor 
        v-model="box"
        ref="Editor"
        @done="done"
        @handle_upload_image="handle_upload_image"
        @als_image="als_image"
    >
        <template #attach>
            <v-col cols="12" md="2" class="pt-0">
                <v-text-field
                    v-model="box.dessert.author"
                    placeholder="author"
                    :rules="[box.rules.required]"
                    outlined hide-details
                    :color="box.primary"
                ></v-text-field>
            </v-col>
            <v-col cols="12" md="2" class="pt-0">
                <v-text-field
                    v-model="box.dessert.pf_id" 
                    placeholder="id"
                    :rules="[box.rules.required]"
                    outlined  hide-details
                    :color="box.primary"
                ></v-text-field>
            </v-col>
            <v-col cols="12" md="2" class="pt-0">
                <v-text-field
                    v-model="box.dessert.pf_name"
                    placeholder="name"
                    :rules="[box.rules.required]"
                    outlined  hide-details
                    :color="box.primary"
                ></v-text-field>
            </v-col>
            <v-col cols="12" md="2" class="pt-0">
                <v-text-field
                    v-model="box.dessert.date" 
                    placeholder="date"
                    outlined hide-details
                    :color="box.primary"
                ></v-text-field>
            </v-col>
            <v-col cols="12" md="4" class="pt-0">
                <v-text-field
                    v-model="box.dessert.pf_url"
                    placeholder="url"
                    :rules="[box.rules.required]"
                    outlined  hide-details
                    :color="box.primary"
                ></v-text-field>
            </v-col>
        </template>
    </editor>
</template>

<script>
    import { archive_editor } from "@/mixins/sec.js"
    export default {
        mixins: [archive_editor],
        created() {
            this.box.dessert.render = true
            this.box.base_dessert.render = true
        },
        methods: {
            done: function() {
                if (this.box.dessert.visible) delete this.box.dessert.protection
                this.$surf.sec.archive.paper.create(this.box.dessert).then(res => {
                    if (res.status === 201) {
                        this.$dialog.notify.success('done', {
                            position: 'top-right',
                            timeout: 2000
                        })
                        sessionStorage.setItem('is_editor_done',true)
                        this.$router.replace({name: 'SecArchivePaper'})
                    }
                }).catch(err => {
                }).finally(result => {
                    this.$shield.down()
                })
            },
        },
    }
</script>