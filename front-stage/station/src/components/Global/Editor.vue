<template>
    <v-tabs color="#fbd300" dark app centered class="align-self-start fill-height">
        <v-tab><v-icon>mdi-typewriter</v-icon></v-tab>
        <v-tab><v-icon>mdi-view-carousel-outline</v-icon></v-tab>
        
        <v-tab-item
            class="editor"
            :transition="false"
        >
            <v-container class="writer pa-0">
                <header>
                    <v-row class="white ma-0" style="min-height: 76px;">
                        <v-col
                            class="pa-0"
                            style="max-width: fit-content !important;"
                            @click="writer_expand = !writer_expand"
                        >
                            <v-btn
                                text tile
                                :color="box.primary"
                                class="text-h4 text-capitalize font-weight-bold"
                                style="height: 100%;"
                            >
                                {{ box.name }}
                            </v-btn>
                        </v-col>
                        <v-spacer></v-spacer>
                        <v-col class="d-flex justify-end">
                            <v-btn
                                color="red" 
                                large icon
                                class="text-capitalize ma-1" 
                                @click="default_action('del')"
                            >
                                <v-icon>mdi-trash-can-outline</v-icon>
                            </v-btn>
                            <slot name="action">
                                
                            </slot>
                            <v-btn
                                color="#00E676" 
                                large icon
                                class="text-capitalize ma-1" 
                                @click="default_action('done')"
                            >
                                <v-icon>mdi-check-bold</v-icon>
                            </v-btn>
                        </v-col>
                    </v-row>
                </header>
                <main class="white">
                    <slot name="title">
                        <v-textarea
                            v-model="box.dessert.title" 
                            placeholder="Title"
                            auto-grow outlined hide-details
                            rows="1"
                            :color="box.primary"
                            class="text-h5 font-weight-black pa-3 pt-1"
                            maxlength="128"
                            :rules="[box.rules.required]">
                        </v-textarea>
                    </slot>
                    <v-progress-linear
                        v-show="box.loading"
                        indeterminate
                        :color="box.primary"
                    ></v-progress-linear>
                    <v-expand-transition mode="out-in">
                        <div v-show="writer_expand">
                            <v-row
                                style="max-width: 100%; margin: auto;"
                            >
                                <slot name="attach">
            
                                </slot>
                                <v-col cols="12" md="6" class="d-flex pt-0">
                                    <v-text-field 
                                        v-model="find_text" 
                                        :prefix="found_count"
                                        outlined hide-details
                                        :color="box.primary"
                                        placeholder="Find"
                                        @keydown.native.enter="find_dessert_content"
                                    ></v-text-field>
                                </v-col>
                                <v-col cols="12" md="6" class="d-flex pt-0">
                                    <v-text-field
                                        v-model="replace_text" 
                                        outlined hide-details
                                        :color="box.primary"
                                        placeholder="Replace"
                                        @keydown.native.enter="replace_dessert_content"
                                    ></v-text-field>
                                </v-col>
                                <v-col cols="12" class="py-0">
                                    <v-text-field
                                        v-model="box.als_image_url" 
                                        outlined hide-details
                                        :color="box.primary"
                                        label="Image Url"
                                        :loading="box.als_image_loading"
                                        @keydown.native.enter="als_image"
                                    ></v-text-field>
                                </v-col>
                            </v-row>
                        </div>
                    </v-expand-transition>
                    <slot name="editor">
                        <v-md-editor
                            v-model="box.dessert.content"
                            mode="edit"
                            height="640px"
                            :disabled-menus="[]"
                            :toolbar="box.attach_bar.toolbar"
                            :left-toolbar="'undo redo clear | h bold italic strikethrough quote | ul ol table hr | link code image' + box.attach_bar.name"
                            right-toolbar="toc fullscreen"
                            style="box-shadow: unset"
                            @upload-image="handle_upload_image"
                            @save="default_action('done')"
                            ref="vmdeditor"
                        >
                        </v-md-editor>
                    </slot>
                </main>
                <footer>
                    <slot name="footer">
                        <v-row
                            class="white"
                            style="max-width: 100%; margin: auto;"
                        >
                            <v-col cols="12" md="4" class="px-0 pb-2">
                                <v-combobox
                                    v-model="box.dessert.albums"
                                    :items="box.all_albums" 
                                    :color="box.primary"
                                    label="Albums"
                                    hide-selected hide-details multiple chips flat solo deletable-chips
                                >
                                    <template v-slot:selection="{ attrs, item, parent, selected }">
                                        <v-chip v-bind="attrs" :input-value="selected">
                                            <v-icon small @click="parent.selectItem(item)">
                                                mdi-close-circle
                                            </v-icon>
                                            <span class="pl-2 text-capitalize" style="padding-top: 1.5px;">
                                                {{ item }}
                                            </span>
                                        </v-chip>
                                    </template>
                                </v-combobox>
                            </v-col>
                            <v-col cols="12" md="4" class="px-0 pb-2">
                                <v-combobox
                                    v-model="box.dessert.chips"
                                    :color="box.primary"
                                    label="Chips"
                                    hide-selected hide-details multiple chips flat solo deletable-chips
                                >
                                    <template v-slot:selection="{ attrs, item, parent, selected }">
                                        <v-chip v-bind="attrs" :input-value="selected">
                                            <v-icon small @click="parent.selectItem(item)">
                                                mdi-close-circle
                                            </v-icon>
                                            <span class="pl-2 text-capitalize" style="padding-top: 1.5px;">
                                                {{ item }}
                                            </span>
                                        </v-chip>
                                    </template>
                                </v-combobox>
                            </v-col>
                            <v-col cols="12" md="4" class="px-0 d-flex align-center pb-2">
                                <div class="d-flex pr-4" style="width: 100%;">
                                    <v-btn icon large @click="box.dessert.visible=true">
                                        <v-icon :color="box.dessert.visible ? '#06d6a0' : ''">
                                            mdi-lock-open-outline
                                        </v-icon>
                                    </v-btn>
                                    <v-btn icon large @click="box.dessert.visible=false">
                                        <v-icon :color="box.dessert.visible ? '' : box.primary">
                                            mdi-lock-outline
                                        </v-icon>
                                    </v-btn>
                                    <v-scroll-x-transition>
                                        <v-text-field v-show="!box.dessert.visible" v-model="box.dessert.protection" class="pt-0"
                                            label="Protection" maxlength="12" flat hide-details :color="box.primary">
                                        </v-text-field>
                                    </v-scroll-x-transition>
                                </div>
                            </v-col>
                        </v-row>
                    </slot>
                </footer>
                <input
                    id="from_md"
                    type="file"
                    accept=".md,.txt"
                    @change="from_md_file"
                    style="display: none;"
                >
            </v-container>
        </v-tab-item>
        <v-tab-item 
            class="editor" 
            :transition="false"
        >
            <component :is="previewer" :dessert="box.dessert"></component>
        </v-tab-item>
    </v-tabs>
</template>

<script>
    import Utils from '@/utils/utils.js'
    import marked from "marked"
    import DOMPurify from 'dompurify'
    const beautify_html = require('js-beautify').html
    export default {
        props: {
            id: {
                default: undefined
            },
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
            writer_expand: false,
            find_text: "",
            found_count: undefined,
            replace_text: "",
            previewer: undefined
        }),
        created() {
            if (this.box.name === "blog") {
                this.previewer = 'BlogPreviewer'
            }else if (this.box.name === "paper") {
                this.previewer = 'PaperPreviewer'
            }else {
                this.$router.replace({name: 'Dashbord'})
            }
        },
        watch: {
            'box.dessert.albums': {
                handler(val) {
                    if (val.length > 5) {
                        this.$nextTick(() => this.box.dessert.albums.pop())
                    }
                },
                deep: true
            },
            'box.dessert.chips': {
                handler(val) {
                    if (val.length > 10) {
                        this.$nextTick(() => this.box.dessert.chips.pop())
                    }
                },
                deep: true
            },
        },
        methods: {
            default_action: function(name) {
                if (!this.check_dessert_filled()) return
                if (name === 'del') {
                    this.$emit('del')
                }else if (name === 'done') {
                    this.$shield.up()
                    this.$emit('done')
                }
            },
            handle_upload_image: function(event, insertImage, files) {
                var formdata = new FormData();
                formdata.append('image', files[0])
                this.$shield.up()
                this.$emit('handle_upload_image', {data: formdata, func: insertImage})
            },
            als_image: function() {
                let url = this.box.als_image_url.match(/^https?:\/\/\S*?\/[a-z0-9\/_\?=-]*(?:\.png|\.jpg|\.jpeg|\.webp|\.gif|\.jfif)/i)
                if (url) {
                    this.$shield.up()
                    this.$emit('als_image', url[0])
                }
            },
            from_md_file: function(event) {
                this.box.loading = true
                let reader = new FileReader()
                reader.readAsText(event.target.files[0], "UTF-8")
                let self = this
                reader.onload = function(e){
                    self.box.dessert.content = e.target.result
                    self.box.loading = false
                }
            },
            find_dessert_content: function() {
                if (this.find_text.length <= 0) {
                    this.found_count = ""
                    return
                }
                let reg = new RegExp(this.find_text,'ig')
                reg = this.box.dessert.content.match(reg)
                if (!reg) return
                this.found_count = "( " + reg.length + " )"
            },
            replace_dessert_content: function() {
                if (this.find_text.length <= 0) return
                let reg = new RegExp(this.find_text,'ig')
                let replaced_content = this.box.dessert.content.replace(reg, this.replace_text)
                this.box.dessert.content = replaced_content
            },
            check_dessert_filled: function() {
                for (var i  = 0; i < this.box.required_attrs.length; i++) {
                    let attr = this.box.required_attrs[i]
                    this.box.dessert[attr] = this.box.dessert[attr].trim()
                    if (this.box.dessert[attr].length <= 0) return false
                }
                return true
            },
            check_dessert_state: function() {
                return Utils.leave_check(this.box.base_dessert, this.box.dessert)
            },
        },
        components: {
            BlogPreviewer: () => import(`@/components/Blog/Previewer.vue`),
            PaperPreviewer: () => import(`@/components/Sec/Archive/Previewer.vue`)
        }
    }
</script>

<style scoped lang="scss">
    
    
    .writer {
        width: 60%;
        margin: auto;
        @media only screen and (max-width: 1024px) {
            width: 100%;
        }
        ::v-deep {
            .v-text-field__slot {
                textarea {
                    margin-top: 0px!important;
                    padding: 12px 0px 8px 0px;
                }
            }
        }
    }
    
    ::v-deep {
        .v-md-editor ul {
            padding-left: 0px;
        }
        .v-md-editor__menu--panel {
            padding-left: 10px!important;
        }
        .v-window-item {
            background-color: #1f4a40;
            height: 100%;
            padding: 3.25rem 0rem 0rem 0rem;
        }
        .v-tabs-items {
            height: 100%;
        }
        .v-tabs-bar {
            width: 100%;
            position: fixed;
            z-index: 5;
            background-color: #1f4a40 !important;
        }
        .v-slide-group__content {
            >div:nth-child(2) {
                margin-left: calc(50% - 129px) !important;
                @media only screen and (max-width: 1024px) {
                    margin-left: calc(50% - 112px) !important;
                }
            }
        }
    }
</style>
