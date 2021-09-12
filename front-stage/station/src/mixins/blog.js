import { eld } from "@/mixins/eld.js"
export const blog_editor={
    mixins: [eld],
    props: {
        id: {
            default: undefined
        }
    },
    data: () => ({
        box: {
            name: "blog",
            primary: "#367bf0",
            attach_bar: {
                toolbar: {
                    More: {
                        title: 'More',
                        icon: 'v-md-icon-tip',
                        menus: {
                            mode: 'panel',
                            itemWidth: '56px',
                            rowNum: 5,
                            items: [
                                {
                                    text: 'From md',
                                    action() {
                                        document.getElementById('from_md').click()
                                    }
                                }
                            ],
                        },
                    }
                },
                name: "| More"
            },
            dessert: {
                cover: "",
                title: "",
                content: "",
                chips: [],
                images: [],
                albums: [],
                visible: true,
                protection: ''
            },
            base_dessert: {
                cover: "",
                title: "",
                content: "",
                chips: [],
                images: [],
                albums: [],
                visible: true,
                protection: ''
            },
            loading: true,
            all_albums: [],
            als_image_url: "",
            als_image_loading: false,
            rules: {
                required: value => !!value || '',
            },
            required_attrs: ['title'],
        },
    }),
    created() {
        this.get_detail()
        this.get_albums()
    },
    components: {
        Editor: () => import(`@/components/Global/Editor.vue`)
    },
    methods: {
        get_detail: function() {
            if (!this.id) return
            var numReg = /^[0-9]*$/
            var numReg = new RegExp(numReg)
            if (numReg.test(this.id)) {
                this.box.loading = true
                this.$surf.blog.post.detail(this.id).then(res => {
                    this.box.dessert = {...res.data.data}
                    this.box.base_dessert = {...res.data.data}
                }).catch(err => {
                    this.$router.replace({name: 'BlogPost'})
                }).finally(result => {
                    this.box.loading = false
                })
            }else {
                this.$router.replace({name: 'BlogPost'})
            }
        },
        get_albums: function() {
            this.box.loading = true
           this.$surf.blog.album.get(0).then(res => {
                this.box.all_albums = res.data.data.map(x => { return x[0] })
            }).finally(result => {
                this.box.loading = false
            })
        },
        handle_upload_image: function({data, func}) {
            this.box.als_image_loading = true
            this.$surf.blog.image.upload(data).then(res => {
                func({
                    url: res.data.data,
                    // url: 'http://127.0.0.1:5000' + res.data.data,
                    desc: 'Chappie',
                });
            }).catch(err => {
            }).finally(result => {
                this.box.als_image_loading = false
                this.$shield.down()
            })
        },
        als_image: function(url) {
            this.box.als_image_loading = true
            this.$surf.blog.image.als({url: url}).then(res => {
                this.box.als_image_url = ""
                this.$refs.Editor.$refs.vmdeditor.insert(function (selected){
                    return {
                        text: `![Chappie](${res.data.data})`,
                        selected: res.data.data
                    }
                })
            }).catch(err => {
            }).finally(result => {
                this.box.als_image_loading = false
                this.$shield.down()
            })
        }
    }
}